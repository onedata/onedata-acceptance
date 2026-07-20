"""This module contains gherkin steps to run acceptance tests featuring
tokens management in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz, Natalia Organek"
__copyright__ = "Copyright (C) 2017-2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time

from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.common.common import wait_for_sliding_panel_to_stop_moving
from tests.gui.steps.oneprovider.common import wait_for_item_to_disappear
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils import Modals, OZLoggedIn, Popups
from tests.gui.utils.common.privilege_tree_in_tokens import PrivilegeTree
from tests.gui.utils.generic import transform
from tests.gui.utils.onezone.discovery_page import DiscoveryPage
from tests.gui.utils.onezone.token_caveats import CaveatField
from tests.gui.utils.onezone.tokens_page import TokenRow, TokensPage
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_FRONTEND)
def get_token_by_name(driver: WebDriver, token_name: str) -> TokenRow:
    oz_page = OZLoggedIn(driver)
    oz_page.open_panel(TokensPage)
    return oz_page.tokens.sidebar.tokens[token_name]


def _open_menu_for_token(driver: WebDriver, token_name: str) -> None:
    get_token_by_name(driver, token_name).menu_button.click()


def click_option_for_token_row_menu(driver: WebDriver, option: str) -> None:
    Popups(driver).menu_popup_with_text.menu[option.capitalize()]()


def _click_on_btn_for_token(driver: WebDriver, token_name: str, btn: str) -> None:
    _open_menu_for_token(driver, token_name)
    click_option_for_token_row_menu(driver, btn)


@wt(parsers.parse('user of {browser_id} clicks on "{token_name}" on token list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_token_on_tokens_list(
    selenium: SeleniumDrivers, browser_id: str, token_name: str
) -> None:
    driver = selenium[browser_id]
    get_token_by_name(driver, token_name).click()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) clicks on (?P<btn>rename|remove) "
        r'button for token named "(?P<token_name>.*?)" on tokens list'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def wt_click_on_btn_for_oz_token(
    selenium: SeleniumDrivers, browser_id: str, btn: str, token_name: str
) -> None:
    driver = selenium[browser_id]
    _click_on_btn_for_token(driver, token_name, btn)


@wt(
    parsers.parse(
        "user of {browser_id} sees exactly {expected_num:d} item(s) "
        "on tokens list in tokens sidebar"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_oz_tokens_list_has_num_tokens(
    selenium: SeleniumDrivers, browser_id: str, expected_num: int
) -> None:
    driver = selenium[browser_id]
    displayed_tokens_num = len(OZLoggedIn(driver).tokens.sidebar.tokens)
    assert displayed_tokens_num == expected_num, (
        f"Displayed number of tokens on tokens page: {displayed_tokens_num}"
        f" instead of excepted: {expected_num}"
    )


@wt(parsers.parse('user of {browser_id} clicks on "{button}" button in tokens sidebar'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_button_in_tokens_sidebar(
    selenium: SeleniumDrivers, browser_id: str, button: str
) -> None:
    driver = selenium[browser_id]

    if button == "Create new token":
        oz_page = OZLoggedIn(driver)
        oz_page.open_panel(TokensPage)
        oz_page.tokens.sidebar.click_create_new_token(driver)
    elif button == "Clean up obsolete tokens":
        sidebar = OZLoggedIn(driver).tokens.sidebar
        button_clean = getattr(sidebar, transform(button))
        for _ in range(50):
            if "clickable" in button_clean.web_elem.get_attribute("class"):
                button_clean.click()
                return
            time.sleep(0.1)
        raise RuntimeError(f"Did not manage to click {button} button")
    else:
        sidebar = OZLoggedIn(driver).tokens.sidebar
        getattr(sidebar, transform(button))()


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "Create custom token" '
        'option in "Create new token" view'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_custom_token(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    OZLoggedIn(driver).tokens.create_token_page.create_custom_token()
    wait_for_sliding_panel_to_stop_moving(
        driver, WAIT_FRONTEND, '[data-one-carousel-slide-id="form"]'
    )


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "{link}" link in "Create new token" view'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_link_in_create_token_view(
    selenium: SeleniumDrivers, browser_id: str, link: str
) -> None:
    driver = selenium[browser_id]
    link = f"{link} link" if "documentation" in link else link
    element = getattr(OZLoggedIn(driver).tokens.create_token_page, transform(link))
    try:
        element.click()
    except ElementNotInteractableException:
        driver.execute_script("arguments[0].click();", element)


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "Show inactive caveats" '
        'label in "Create new token" view'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def show_inactive_caveats(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    OZLoggedIn(driver).tokens.create_token_page.expand_caveats()
    assert OZLoggedIn(driver).tokens.create_token_page.caveats_expanded()


@wt(
    parsers.parse("user of {browser_id} clicks on Confirm button on consume token page")
)
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_confirm_button_on_tokens_page(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    oz_page = OZLoggedIn(selenium[browser_id])
    oz_page.tokens.confirm_button()
    oz_page.set_current_page(DiscoveryPage)


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{member_name}" {type} '
        "from dropdown on tokens page"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def select_member_from_dropdown(
    selenium: SeleniumDrivers, browser_id: str, member_name: str
) -> None:
    driver = selenium[browser_id]

    OZLoggedIn(driver).tokens.expand_dropdown()
    Popups(driver).dropdown.options[member_name].click()


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "Create token" button '
        'in "Create new token" view'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND * 2)
def click_create_token_button_in_create_token_page(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    # prevent clicking when there is ongoing animation
    time.sleep(0.2)
    create_token_button = OZLoggedIn(driver).tokens.create_token_page.create_token
    create_token_button.click()
    # ensure clicking at create token succeeded
    wait_for_item_to_disappear(create_token_button)


@wt(
    parsers.parse(
        "user of {browser_id} chooses {token_type} token type in "
        '"Create new token" view'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_token_type_to_create(
    selenium: SeleniumDrivers, browser_id: str, token_type: str
) -> None:
    driver = selenium[browser_id]
    option = f"{token_type}_option"
    getattr(OZLoggedIn(driver).tokens.create_token_page, option).click()
    # ensure correct option is selected
    option_input = f"{token_type}_input"
    error_message = f"did not manage to select {option}"
    assert getattr(
        OZLoggedIn(driver).tokens.create_token_page, option_input
    ).is_selected(), error_message


@wt(parsers.parse("user of {browser_id} clicks on copy button in token view"))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_copy_button_in_token_view(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    OZLoggedIn(driver).tokens.copy_token()


@wt(parsers.parse('user of {browser_id} chooses "{invite_type}" invite type'))
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_invite_type_in_oz_token_page(
    selenium: SeleniumDrivers, browser_id: str, invite_type: str
) -> None:
    driver = selenium[browser_id]
    new_token_page = OZLoggedIn(driver).tokens.create_token_page
    new_token_page.expand_invite_type_dropdown()
    Popups(driver).power_select.choose_item(invite_type)


@repeat_failed(timeout=WAIT_FRONTEND)
def choose_invite_select(
    selenium: SeleniumDrivers, browser_id: str, target: str, hosts: Hosts
) -> None:
    if "oneprovider" in target:
        target = hosts[target]["name"]

    driver = selenium[browser_id]
    new_token_page = OZLoggedIn(driver).tokens.create_token_page
    new_token_page.expand_invite_target_dropdown()
    Popups(driver).power_select.choose_item(target)


@repeat_failed(timeout=WAIT_FRONTEND)
def select_token_usage_limit(
    selenium: SeleniumDrivers, browser_id: str, limit: str
) -> None:
    driver = selenium[browser_id]
    limits = OZLoggedIn(driver).tokens.create_token_page.usage_limit
    if limit == "infinity":
        limits.infinity_option.click()
    else:
        limits.number_option.click()
        limits.number_input = limit


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{token_name}" token\'s type is {token_type}'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_token_is_type(
    selenium: SeleniumDrivers, browser_id: str, token_type: str, token_name: str
) -> None:
    driver = selenium[browser_id]
    token = get_token_by_name(driver, token_name)
    assert token.is_type_of(
        token_type
    ), f"Token should be type of {token_type} but is not"


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{token_filter}" filter in tokens sidebar'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_token_filter(
    selenium: SeleniumDrivers, browser_id: str, token_filter: str
) -> None:
    filters = OZLoggedIn(selenium[browser_id]).tokens.sidebar.filter
    getattr(filters, token_filter.lower())()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) chooses "(?P<token_filter>.*)" '
        r"(?P<filter_type>name Invite|Invite) filter in tokens sidebar"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_invite_token_filter(
    selenium: SeleniumDrivers,
    browser_id: str,
    token_filter: str,
    filter_type: str,
    hosts: Hosts,
) -> None:
    driver = selenium[browser_id]
    invite_filter = OZLoggedIn(driver).tokens.sidebar.invite_filter
    if filter_type == "name Invite":
        if "oneprovider" in token_filter:
            token_filter = hosts[token_filter]["name"]
        invite_filter.dropdown_menus[1].click()
    else:
        invite_filter.dropdown_menus[0].click()
    Popups(driver).dropdown.options[token_filter].click()


@wt(
    parsers.parse(
        "user of {browser_id} sees that all tokens in tokens sidebar "
        "are type of {token_type}"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_all_tokens_are_type(
    selenium: SeleniumDrivers, browser_id: str, token_type: str
) -> None:
    tokens = OZLoggedIn(selenium[browser_id]).tokens.sidebar.tokens
    assert all(
        token.is_type_of(token_type) for token in tokens
    ), f"Not all visible tokens are type of {token_type}"


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) sees that "
        r'token named "(?P<token_name>.*?)" is marked as '
        r"(?P<status>active|revoked)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_token_is_marked(
    selenium: SeleniumDrivers, browser_id: str, status: str, token_name: str
) -> None:
    driver = selenium[browser_id]
    token = get_token_by_name(driver, token_name)
    if status == "active":
        assert not token.is_revoked(), "Token is revoked and should not be"
    elif status == "revoked":
        assert token.is_revoked(), "Token is active and should be revoked"


@wt(parsers.parse("user of {browser_id} clicks on tokens view menu button"))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_menu_button_of_tokens_page(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    OZLoggedIn(driver).tokens.menu()


@wt(parsers.parse('user of {browser_id} clicks "{option}" option in tokens view menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_token_page_menu(
    selenium: SeleniumDrivers, browser_id: str, option: str
) -> None:
    driver = selenium[browser_id]
    Popups(driver).menu_popup_with_text.menu[option]()


@wt(parsers.parse('user of {browser_id} clicks "Revoke" toggle to {action} token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def switch_toggle_to_change_token(
    selenium: SeleniumDrivers, browser_id: str, action: str
) -> None:
    driver = selenium[browser_id]
    if action == "revoke":
        OZLoggedIn(driver).tokens.revoke_toggle.check()
    elif action == "activate":
        OZLoggedIn(driver).tokens.revoke_toggle.uncheck()


@wt(parsers.parse('user of {browser_id} clicks "Save" button on tokens view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_save_button_on_tokens_page(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    OZLoggedIn(driver).tokens.save_button()


@wt(
    parsers.parse(
        'user of {browser_id} appends "{text}" to name of token named "{token_name}'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def append_token_name_in_sidebar(
    selenium: SeleniumDrivers, browser_id: str, text: str
) -> None:
    driver = selenium[browser_id]
    input_box = OZLoggedIn(driver).tokens.sidebar.name_input
    OZLoggedIn(driver).tokens.sidebar.name_input = input_box + text


@wt(parsers.parse("user of {browser_id} confirms changes in token named {token_name}"))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_token_changes_in_sidebar(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    OZLoggedIn(driver).tokens.sidebar.confirm()


@wt(
    parsers.parse(
        "user of {browser_id} sees that there is token named "
        '"{token_name}" on tokens list'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_token_on_tokens_list(
    selenium: SeleniumDrivers, browser_id: str, token_name: str
) -> None:
    driver = selenium[browser_id]
    token_list = OZLoggedIn(driver).tokens.sidebar.tokens
    assert token_name in token_list, f"There is no {token_name} on tokens list"


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) succeeds to type "(?P<token_name>.*?)" to token'
        r' name input box in "Create new token" view'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def type_new_token_name(
    selenium: SeleniumDrivers, browser_id: str, token_name: str
) -> None:
    driver = selenium[browser_id]
    input_box = OZLoggedIn(driver).tokens.create_token_page.token_name_input
    input_box.value = token_name
    assert (
        input_box.value == token_name
    ), f"Failed to type new token name, expected {token_name}, got: {input_box.value}"


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_token_name(
    selenium: SeleniumDrivers, browser_id: str, token_name: str
) -> None:
    driver = selenium[browser_id]
    given_name = OZLoggedIn(driver).tokens.token_name
    assert (
        given_name == token_name
    ), f"Given name {given_name} is not like expected {token_name}"


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_token_revoked(
    selenium: SeleniumDrivers, browser_id: str, revoke_expectation: bool
) -> None:
    driver = selenium[browser_id]
    if revoke_expectation:
        msg = "Token is not revoked while should be"
    else:
        msg = "Token is revoked while should not be"
    assert OZLoggedIn(driver).tokens.is_token_revoked() == revoke_expectation, msg


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_token_type(
    selenium: SeleniumDrivers, browser_id: str, expected_type: str
) -> None:
    driver = selenium[browser_id]
    actual_type = OZLoggedIn(driver).tokens.token_type
    assert (
        actual_type == expected_type.capitalize()
    ), f"Expected type {expected_type} does not match actual {actual_type}"


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_invite_type(
    selenium: SeleniumDrivers, browser_id: str, expected_type: str
) -> None:
    driver = selenium[browser_id]
    actual_type = OZLoggedIn(driver).tokens.invite_type
    assert (
        actual_type == expected_type
    ), f"Expected invite type {expected_type} does not match actual {actual_type}"


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_invite_target(
    selenium: SeleniumDrivers,
    browser_id: str,
    expected_target: str,
    hosts: Hosts,
    spaces: dict[str, str],
) -> None:
    if "oneprovider" in expected_target:
        expected_target = hosts[expected_target]["name"]

    driver = selenium[browser_id]
    actual_type = OZLoggedIn(driver).tokens.invite_target
    if expected_target.startswith("$(resolve_id"):
        space_name = expected_target.split(" ")[1].replace(")", "")
        expected_target = "ID: " + spaces[space_name]
    assert (
        actual_type == expected_target
    ), f"Expected invite target {expected_target} does not match actual {actual_type}"


@wt(parsers.parse('user of {browser_id} sees that token usage count is "{count}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_token_usage_count_value(
    selenium: SeleniumDrivers, browser_id: str, count: str
) -> None:
    driver = selenium[browser_id]
    text = OZLoggedIn(driver).tokens.usage_count
    parse_and_compare_usage_count(text, count)


def parse_and_compare_usage_count(text_given: str, text_expected: str) -> None:
    no1, no2 = text_given.split("/")
    exp1, exp2 = text_expected.split("/")
    assert str(no1).strip() == str(exp1).strip(), f"First number should be {exp1}"
    assert str(no2).strip() == str(exp2).strip(), f"Second number should be {exp2}"


@repeat_failed(timeout=WAIT_FRONTEND)
def get_caveat_by_name(
    selenium: SeleniumDrivers, browser_id: str, caveat_name: str
) -> CaveatField:
    driver = selenium[browser_id]
    new_token_page = OZLoggedIn(driver).tokens.create_token_page
    return new_token_page.get_caveat(caveat_name)


@wt(parsers.parse("user of {browser_id} sets read only token caveat"))
@repeat_failed(timeout=WAIT_FRONTEND)
def set_caveat_by_name(selenium: SeleniumDrivers, browser_id: str) -> None:
    caveat = get_caveat_by_name(selenium, browser_id, "readonly")
    caveat.set_readonly_caveat()


@repeat_failed(timeout=WAIT_FRONTEND)
def get_privileges_tree(selenium: SeleniumDrivers, browser_id: str) -> PrivilegeTree:
    driver = selenium[browser_id]
    return OZLoggedIn(driver).tokens.privilege_tree


@wt(
    parsers.parse(
        'user of {browser_id} deselects "{token_name}" '
        'in modal "Clean up obsolete tokens"'
    )
)
def deselect_tokens_on_modal(
    browser_id: str, token_name: str, selenium: SeleniumDrivers
) -> None:
    driver = selenium[browser_id]
    clean_modal = Modals(driver).clean_up_obsolete_tokens

    # expand token types to make tokens visible
    for token_type in clean_modal.token_types:
        token_type.click()

    clean_modal.tokens[token_name].checkbox.click()


@wt(
    parsers.parse(
        'user of {browser_id} deselects "{token_type}" type '
        'in modal "Clean up obsolete tokens"'
    )
)
def deselect_token_type_on_modal(
    browser_id: str, token_type: str, selenium: SeleniumDrivers
) -> None:
    driver = selenium[browser_id]
    clean_modal = Modals(driver).clean_up_obsolete_tokens

    clean_modal.token_types[token_type].checkbox.click()


@wt(
    parsers.parse(
        'user of {browser_id} {ability_to_see} "{token_name}" '
        "in token list on tokens page sidebar"
    )
)
def assert_token_on_token_page_sidebar(
    browser_id: str,
    ability_to_see: str,
    token_name: str,
    selenium: SeleniumDrivers,
) -> None:
    driver = selenium[browser_id]
    tokens_page = OZLoggedIn(driver).tokens.sidebar

    if ability_to_see == "sees":
        error_message = f"token list on sidebar should contain {token_name}"
        assert token_name in {token.name for token in tokens_page.tokens}, error_message
    if ability_to_see == "does not see":
        error_message = f"token list on sidebar should not contain {token_name}"
        assert token_name not in {
            token.name for token in tokens_page.tokens
        }, error_message


def choose_token_template(
    selenium: SeleniumDrivers, browser_id: str, template: str
) -> None:
    driver = selenium[browser_id]
    tokens_page = OZLoggedIn(driver).tokens
    getattr(tokens_page, f"{transform(template)}_template").click()


@wt(parsers.parse('user of {browser_id} sees alert with text: "{text}" on tokens page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_alert_on_tokens_page(
    browser_id: str, text: str, selenium: SeleniumDrivers
) -> None:
    alert = OZLoggedIn(selenium[browser_id]).tokens.alert
    assert text in alert, f"{text} does not match alert: {alert}"


@given(parsers.parse("{sender} sends {item_type} to {receiver}"))
def given_send_copied_item_to_other_user(
    sender: str, receiver: str, item_type: str, tmp_memory: TmpMemory
) -> None:
    tmp_memory[receiver]["mailbox"][item_type.lower()] = tmp_memory[sender][item_type]


@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_token_containing_name(
    selenium: SeleniumDrivers, browser_id: str, token_name: str
) -> None:
    driver = selenium[browser_id]
    tokens = OZLoggedIn(driver).tokens.sidebar.tokens
    for token in tokens:
        if token_name in token.name:
            token.click()
            return
    raise ValueError(f"token {token_name} not found")
