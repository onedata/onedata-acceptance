"""This module contains gherkin steps to run acceptance tests featuring
tokens management in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz, Natalia Organek"
__copyright__ = "Copyright (C) 2017-2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_FRONTEND)
def get_token_by_name(oz_page, token_name, driver):
    return oz_page(driver).get_page_and_click("tokens").sidebar.tokens[token_name]


def _open_menu_for_token(driver, oz_page, token_name):
    get_token_by_name(oz_page, token_name, driver).menu_button.click()


def click_option_for_token_row_menu(driver, option, popups):
    popups(driver).menu_popup_with_text.menu[option.capitalize()]()


def _click_on_btn_for_token(driver, oz_page, token_name, btn, popups):
    _open_menu_for_token(driver, oz_page, token_name)
    click_option_for_token_row_menu(driver, btn, popups)


@wt(parsers.parse('user of {browser_id} clicks on "{token_name}" on token list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_token_on_tokens_list(selenium, browser_id, token_name, oz_page):
    driver = selenium[browser_id]
    get_token_by_name(oz_page, token_name, driver).click()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) clicks on (?P<btn>rename|remove) "
        r'button for token named "(?P<token_name>.*?)" on tokens list'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def wt_click_on_btn_for_oz_token(
    selenium, browser_id, btn, token_name, oz_page, popups
):
    driver = selenium[browser_id]
    _click_on_btn_for_token(driver, oz_page, token_name, btn, popups)


@wt(
    parsers.parse(
        "user of {browser_id} sees exactly {expected_num:d} item(s) "
        "on tokens list in tokens sidebar"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_oz_tokens_list_has_num_tokens(selenium, browser_id, expected_num, oz_page):
    driver = selenium[browser_id]
    displayed_tokens_num = len(oz_page(driver)["tokens"].sidebar.tokens)
    assert displayed_tokens_num == expected_num, (
        f"Displayed number of tokens on tokens page: {displayed_tokens_num}"
        f" instead of excepted: {expected_num}"
    )


@wt(parsers.parse('user of {browser_id} clicks on "{button}" button in tokens sidebar'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_button_in_tokens_sidebar(selenium, browser_id, oz_page, button):
    driver = selenium[browser_id]

    if button == "Create new token":
        oz_page(driver).get_page_and_click("tokens").sidebar.click_create_new_token(
            driver
        )
    elif button == "Clean up obsolete tokens":
        sidebar = oz_page(driver)["tokens"].sidebar
        button_clean = getattr(sidebar, transform(button))
        for _ in range(50):
            if "clickable" in button_clean.web_elem.get_attribute("class"):
                button_clean.click()
                return
            time.sleep(0.1)
        raise RuntimeError(f"did not menage to click {button} button")
    else:
        sidebar = oz_page(driver)["tokens"].sidebar
        getattr(sidebar, transform(button))()


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "Create custom token" '
        'option in "Create new token" view'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_custom_token(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)["tokens"].create_token_page.create_custom_token()


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "Show inactive caveats" '
        'label in "Create new token" view'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def show_inactive_caveats(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)["tokens"].create_token_page.expand_caveats()


@wt(
    parsers.parse("user of {browser_id} clicks on Confirm button on consume token page")
)
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_confirm_button_on_tokens_page(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])["tokens"].confirm_button()


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{member_name}" {type} '
        "from dropdown on tokens page"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def select_member_from_dropdown(selenium, browser_id, member_name, popups, oz_page):
    driver = selenium[browser_id]

    oz_page(driver)["tokens"].expand_dropdown()
    popups(driver).dropdown.options[member_name].click()


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "Create token" button '
        'in "Create new token" view'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_token_button_in_create_token_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)["tokens"].create_token_page.create_token()


@wt(
    parsers.parse(
        "user of {browser_id} chooses {token_type} token type in "
        '"Create new token" view'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_token_type_to_create(selenium, browser_id, oz_page, token_type):
    driver = selenium[browser_id]
    option = f"{token_type}_option"
    getattr(oz_page(driver)["tokens"].create_token_page, option).click()


@wt(parsers.parse("user of {browser_id} clicks on copy button in token view"))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_copy_button_in_token_view(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)["tokens"].copy_token()


@wt(parsers.parse('user of {browser_id} chooses "{invite_type}" invite type'))
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_invite_type_in_oz_token_page(
    selenium, browser_id, oz_page, invite_type, popups
):
    driver = selenium[browser_id]
    new_token_page = oz_page(driver)["tokens"].create_token_page
    new_token_page.expand_invite_type_dropdown()
    popups(driver).power_select.choose_item(invite_type)


@repeat_failed(timeout=WAIT_FRONTEND)
def choose_invite_select(selenium, browser_id, oz_page, target, hosts, popups):
    if "oneprovider" in target:
        target = hosts[target]["name"]

    driver = selenium[browser_id]
    new_token_page = oz_page(driver)["tokens"].create_token_page
    new_token_page.expand_invite_target_dropdown()
    popups(driver).power_select.choose_item(target)


@repeat_failed(timeout=WAIT_FRONTEND)
def select_token_usage_limit(selenium, browser_id, limit, oz_page):
    driver = selenium[browser_id]
    limits = oz_page(driver)["tokens"].create_token_page.usage_limit
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
def assert_token_is_type(selenium, browser_id, token_type, oz_page, token_name):
    driver = selenium[browser_id]
    token = get_token_by_name(oz_page, token_name, driver)
    assert token.is_type_of(
        token_type
    ), f"Token should be type of {token_type} but is not"


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{token_filter}" filter in tokens sidebar'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_token_filter(selenium, browser_id, token_filter, oz_page):
    filters = oz_page(selenium[browser_id])["tokens"].sidebar.filter
    getattr(filters, token_filter.lower())()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) chooses "(?P<token_filter>.*)" '
        r"(?P<filter_type>name Invite|Invite) filter in tokens sidebar"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_invite_token_filter(
    selenium, browser_id, token_filter, filter_type, oz_page, hosts
):
    invite_filter = oz_page(selenium[browser_id])["tokens"].sidebar.invite_filter
    if filter_type == "name Invite":
        if "oneprovider" in token_filter:
            token_filter = hosts[token_filter]["name"]
        invite_filter.dropdown_menus[1].click()
        invite_filter.name_options[token_filter].click()
    else:
        invite_filter.dropdown_menus[0].click()
        invite_filter.options[token_filter].click()


@wt(
    parsers.parse(
        "user of {browser_id} sees that all tokens in tokens sidebar "
        "are type of {token_type}"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_all_tokens_are_type(selenium, browser_id, token_type, oz_page):
    tokens = oz_page(selenium[browser_id])["tokens"].sidebar.tokens
    assert all(
        token.is_type_of(token_type) for token in tokens
    ), f"Not all visible tokens are type of {token_type}"


@wt(
    parsers.re(
        "user of (?P<browser_id>.*?) sees that "
        'token named "(?P<token_name>.*?)" is marked as '
        "(?P<status>active|revoked)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_token_is_marked(selenium, browser_id, status, oz_page, token_name):
    driver = selenium[browser_id]
    token = get_token_by_name(oz_page, token_name, driver)
    if status == "active":
        assert not token.is_revoked(), "Token is revoked and should not be"
    elif status == "revoked":
        assert token.is_revoked(), "Token is active and should be revoked"


@wt(parsers.parse("user of {browser_id} clicks on tokens view menu button"))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_menu_button_of_tokens_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)["tokens"].menu()


@wt(parsers.parse('user of {browser_id} clicks "{option}" option in tokens view menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_token_page_menu(selenium, browser_id, option, popups):
    driver = selenium[browser_id]
    popups(driver).menu_popup_with_text.menu[option]()


@wt(parsers.parse('user of {browser_id} clicks "Revoke" toggle to {action} token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def switch_toggle_to_change_token(selenium, browser_id, action, oz_page):
    driver = selenium[browser_id]
    if action == "revoke":
        oz_page(driver)["tokens"].revoke_toggle.check()
    elif action == "activate":
        oz_page(driver)["tokens"].revoke_toggle.uncheck()


@wt(parsers.parse('user of {browser_id} clicks "Save" button on tokens view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_save_button_on_tokens_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)["tokens"].save_button()


@wt(
    parsers.parse(
        'user of {browser_id} appends "{text}" to name of token named "{token_name}'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def append_token_name_in_sidebar(selenium, browser_id, text, oz_page):
    driver = selenium[browser_id]
    input_box = oz_page(driver)["tokens"].sidebar.name_input
    oz_page(driver)["tokens"].sidebar.name_input = input_box + text


@wt(parsers.parse("user of {browser_id} confirms changes in token named {token_name}"))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_token_changes_in_sidebar(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)["tokens"].sidebar.confirm()


@wt(
    parsers.parse(
        "user of {browser_id} sees that there is token named "
        '"{token_name}" on tokens list'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_token_on_tokens_list(selenium, browser_id, oz_page, token_name):
    driver = selenium[browser_id]
    token_list = oz_page(driver)["tokens"].sidebar.tokens
    assert token_name in token_list, f"There is no {token_name} on tokens list"


@wt(
    parsers.parse(
        'user of {browser_id} types "{token_name}" to token name '
        'input box in "Create new token" view'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def type_new_token_name(selenium, browser_id, oz_page, token_name):
    driver = selenium[browser_id]
    input_box = oz_page(driver)["tokens"].create_token_page.token_name_input
    input_box.value = token_name


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_token_name(selenium, browser_id, oz_page, token_name):
    driver = selenium[browser_id]
    given_name = oz_page(driver)["tokens"].token_name
    assert (
        given_name == token_name
    ), f"Given name {given_name} is not like expected {token_name}"


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_token_revoked(selenium, browser_id, oz_page, revoke_expectation):
    driver = selenium[browser_id]
    if revoke_expectation:
        msg = "Token is not revoked while should be"
    else:
        msg = "Token is revoked while should not be"
    assert oz_page(driver)["tokens"].is_token_revoked() == revoke_expectation, msg


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_token_type(selenium, browser_id, oz_page, expected_type):
    driver = selenium[browser_id]
    actual_type = oz_page(driver)["tokens"].token_type
    assert (
        actual_type == expected_type.capitalize()
    ), f"Expected type {expected_type} does not match actual {actual_type}"


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_invite_type(selenium, browser_id, oz_page, expected_type):
    driver = selenium[browser_id]
    actual_type = oz_page(driver)["tokens"].invite_type
    assert (
        actual_type == expected_type
    ), f"Expected invite type {expected_type} does not match actual {actual_type}"


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_invite_target(selenium, browser_id, oz_page, expected_target, hosts, spaces):
    if "oneprovider" in expected_target:
        expected_target = hosts[expected_target]["name"]

    driver = selenium[browser_id]
    actual_type = oz_page(driver)["tokens"].invite_target
    if expected_target.startswith("$(resolve_id"):
        space_name = expected_target.split(" ")[1].replace(")", "")
        expected_target = "ID: " + spaces[space_name]
    assert (
        actual_type == expected_target
    ), f"Expected invite target {expected_target} does not match actual {actual_type}"


@wt(parsers.parse('user of {browser_id} sees that token usage count is "{count}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_token_usage_count_value(selenium, browser_id, count, oz_page):
    driver = selenium[browser_id]
    text = oz_page(driver)["tokens"].usage_count
    parse_and_compare_usage_count(text, count)


def parse_and_compare_usage_count(text_given, text_expected):
    no1, no2 = text_given.split("/")
    exp1, exp2 = text_expected.split("/")
    assert str(no1).strip() == str(exp1).strip(), f"First number should be {exp1}"
    assert str(no2).strip() == str(exp2).strip(), f"Second number should be {exp2}"


@repeat_failed(timeout=WAIT_FRONTEND)
def get_caveat_by_name(selenium, browser_id, oz_page, caveat_name):
    driver = selenium[browser_id]
    new_token_page = oz_page(driver)["tokens"].create_token_page
    return new_token_page.get_caveat(caveat_name)


@repeat_failed(timeout=WAIT_FRONTEND)
def get_privileges_tree(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    return oz_page(driver)["tokens"].privilege_tree


@wt(
    parsers.parse(
        'user of {browser_id} deselects "{token_name}" '
        'in modal "Clean up obsolete tokens"'
    )
)
def deselect_tokens_on_modal(browser_id, token_name, selenium, modals):
    driver = selenium[browser_id]
    clean_modal = modals(driver).clean_up_obsolete_tokens

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
def deselect_token_type_on_modal(browser_id, token_type, selenium, modals):
    driver = selenium[browser_id]
    clean_modal = modals(driver).clean_up_obsolete_tokens

    clean_modal.token_types[token_type].checkbox.click()


@wt(
    parsers.parse(
        'user of {browser_id} {ability_to_see} "{token_name}" '
        "in token list on tokens page sidebar"
    )
)
def assert_token_on_token_page_sidebar(
    browser_id, ability_to_see, token_name, selenium, oz_page
):
    driver = selenium[browser_id]
    tokens_page = oz_page(driver)["tokens"].sidebar

    if ability_to_see == "sees":
        err_msg = f"token list on sidebar should contain {token_name}"
        assert token_name in {token.name for token in tokens_page.tokens}, err_msg
    if ability_to_see == "does not see":
        err_msg = f"token list on sidebar should not contain {token_name}"
        assert token_name not in {token.name for token in tokens_page.tokens}, err_msg


def choose_token_template(selenium, browser_id, template, oz_page):
    driver = selenium[browser_id]
    tokens_page = oz_page(driver)["tokens"]
    getattr(tokens_page, f"{transform(template)}_template").click()


@wt(parsers.parse('user of {browser_id} sees alert with text: "{text}" on tokens page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_alert_on_tokens_page(browser_id, text, oz_page, selenium):
    alert = oz_page(selenium[browser_id])["tokens"].alert
    assert text in alert, f"{text} does not match alert: {alert}"


@given(parsers.parse("{sender} sends {item_type} to {receiver}"))
def given_send_copied_item_to_other_user(sender, receiver, item_type, tmp_memory):
    tmp_memory[receiver]["mailbox"][item_type.lower()] = tmp_memory[sender][item_type]
