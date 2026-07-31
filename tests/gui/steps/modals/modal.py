"""Steps used for modal handling in various GUI testing scenarios"""

__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2016 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import re
from typing import cast

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.ui import WebDriverWait

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils import Modals, Popups
from tests.gui.utils.core.web_objects import PageObjectsSequence
from tests.gui.utils.generic import click_on_web_elem, transform
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.utils import repeat_failed

in_type_to_id = {
    "username": "login-form-username-input",
    "password": "login-form-password-input",
}


def check_modal_name(modal_name: str) -> str:
    modal_name = transform(modal_name)
    # dict mapping part of the modal name into the used modal name in tests
    s = {
        "remove": "remove_modal",
        "leave": "leave_modal",
        "add_one": "add_one_of_elements",
        "rename": "rename_modal",
        "invite": "invite_using_token",
        "file_details": "details_modal",
        "directory_details": "details_modal",
        "share": "share",
    }
    for k, v in s.items():
        if k in modal_name:
            return v
    return modal_name


@wt(parsers.parse('user of {browser_id} sees that modal "Add storage" has appeared'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wait_for_add_storage_modal_to_appear(
    selenium: SeleniumDrivers, browser_id: str, tmp_memory: TmpMemory
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).add_storage
    tmp_memory[browser_id]["window"]["modal"] = modal


@wt(parsers.parse('user of {browser_id} copies token from "Add storage" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def cp_token_from_add_storage_modal(browser_id: str, tmp_memory: TmpMemory) -> None:
    modal = tmp_memory[browser_id]["window"]["modal"]
    modal.copy()


@wt(parsers.parse('user of {browser_id} generate another token in "Add storage" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def gen_another_token_in_add_storage_modal(
    browser_id: str, tmp_memory: TmpMemory
) -> None:
    modal = tmp_memory[browser_id]["window"]["modal"]
    modal.generate_token()


@wt(parsers.parse('user of {browser_id} sees non-empty token in "Add storage" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_non_empty_token_in_add_storage_modal(
    browser_id: str, tmp_memory: TmpMemory
) -> None:
    token = tmp_memory[browser_id]["window"]["modal"].token
    assert (
        len(token) > 0
    ), "expected token in Add storage modal, but token field is empty"
    tmp_memory[browser_id]["token"] = token


def _find_modal(driver: WebDriver, modal_name: str) -> WebElement:

    # TODO: VFS-13648 Refactor find modal function

    def _find() -> WebElement:
        elements_list = [
            "group",
            "token",
            "cluster",
            "harvester",
            "spaces",
            "rename",
            "permissions",
            "directory",
            "data",
            "share",
            "metadata",
            "delete",
            "remove",
            "quality",
            "file details",
            "symbolic link",
            "inventory",
            "workflow",
            "unsaved",
            "cease",
            "modify",
            "create",
            "unlink",
            "download",
        ]
        if any(name for name in elements_list if name in modal_name.lower()):
            modals = driver.find_elements(
                By.CSS_SELECTOR, ".modal, .modal .modal-header h1"
            )
        elif "leave this space" in modal_name:
            modals = driver.find_elements(By.CSS_SELECTOR, ".modal.in, .modal.in h1")
        else:
            modals = driver.find_elements(
                By.CSS_SELECTOR, ".modal.in, .modal.in .modal-title"
            )

        for name, modal in zip(modals[1::2], modals[::2]):
            if name.text.lower() == modal_name.lower():
                return modal
        raise NoSuchElementException(f"modal {modal_name} not found")

    modal_name = modal_name.lower()
    return WebDriverWait(driver, WAIT_BACKEND).until(
        lambda _: _find(),
        message=f"waiting for {modal_name:s} modal to appear",
    )


def _wait_for_modal_to_appear(
    driver: WebDriver, browser_id: str, modal_name: str, tmp_memory: TmpMemory
) -> None:
    modal = _find_modal(driver, modal_name)
    tmp_memory[browser_id]["window"]["modal"] = modal


def check_warning_modal(selenium: SeleniumDrivers, browser_id: str) -> bool:
    driver = selenium[browser_id]
    if not driver.find_elements(By.CSS_SELECTOR, ".question-modal"):
        return False
    return True


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{modal_name}" modal has not appeared'
    )
)
def assert_modal_does_not_appear(
    selenium: SeleniumDrivers, browser_id: str, modal_name: str, tmp_memory: TmpMemory
) -> None:
    driver = selenium[browser_id]
    try:
        _wait_for_modal_to_appear(driver, browser_id, modal_name, tmp_memory)
        raise AssertionError(f"Modal {modal_name} has appeared")
    except TimeoutException:
        pass


@given(
    parsers.parse('user of {browser_id} seen that "{modal_name}" modal has appeared')
)
@wt(
    parsers.re(
        r"(using web GUI, )?user of (?P<browser_id>.*) sees that "
        r'"(?P<modal_name>.*)" modal has appeared'
    )
)
def wt_wait_for_modal_to_appear(
    selenium: SeleniumDrivers, browser_id: str, modal_name: str, tmp_memory: TmpMemory
) -> None:
    driver = selenium[browser_id]
    _wait_for_modal_to_appear(driver, browser_id, modal_name, tmp_memory)


@given(
    parsers.parse('user of {browser_id} seen that "{modal_name}" modal has appeared')
)
def g_wait_for_modal_to_appear(
    selenium: SeleniumDrivers, browser_id: str, modal_name: str, tmp_memory: TmpMemory
) -> None:
    driver = selenium[browser_id]
    _wait_for_modal_to_appear(driver, browser_id, modal_name, tmp_memory)


def _wait_for_modal_to_disappear(
    driver: WebDriver, browser_id: str, tmp_memory: TmpMemory
) -> None:
    modal = tmp_memory[browser_id]["window"]["modal"]
    WebDriverWait(driver, WAIT_BACKEND).until_not(
        lambda _: not staleness_of(modal) or modal.is_displayed(),
        message="waiting for modal to disappear",
    )
    tmp_memory[browser_id]["window"]["modal"] = None


def wait_for_named_modal_to_disappear(
    selenium: SeleniumDrivers,
    browser_id: str,
    modal_name: str,
    wait_time: int = WAIT_FRONTEND,
) -> None:
    driver = selenium[browser_id]
    modal_name = check_modal_name(modal_name)
    try:
        modal = getattr(Modals(driver), transform(modal_name))
    except NoSuchElementException:
        return
    WebDriverWait(
        driver,
        wait_time,
        ignored_exceptions=[
            StaleElementReferenceException,
            NoSuchElementException,
        ],
    ).until_not(
        lambda _: not staleness_of(modal) or modal.is_displayed(),
        message="waiting for modal to disappear",
    )


@wt(parsers.parse("user of {browser_id} sees that the modal has disappeared"))
def wt_wait_for_modal_to_disappear(
    selenium: SeleniumDrivers, browser_id: str, tmp_memory: TmpMemory
) -> None:
    driver = selenium[browser_id]
    _wait_for_modal_to_disappear(driver, browser_id, tmp_memory)


@given(parsers.parse("user of {browser_id} seen that the modal has disappeared"))
def g_wait_for_modal_to_disappear(
    selenium: SeleniumDrivers, browser_id: str, tmp_memory: TmpMemory
) -> None:
    driver = selenium[browser_id]
    _wait_for_modal_to_disappear(driver, browser_id, tmp_memory)


def _click_on_confirmation_btn_in_modal(
    driver: WebDriver, browser_id: str, button_name: str, tmp_memory: TmpMemory
) -> None:
    @repeat_failed(attempts=WAIT_BACKEND, timeout=True)
    def click_on_btn(d: WebDriver, elem: WebElement, msg: str) -> None:
        click_on_web_elem(d, elem, msg)

    button_name = button_name.lower()
    modal = tmp_memory[browser_id]["window"]["modal"]
    buttons = modal.find_elements(By.CSS_SELECTOR, "button")
    error_message = f"clicking on {button_name} in displayed modal disabled"
    for btn in buttons:
        if btn.text.lower() == button_name:
            click_on_btn(driver, btn, error_message)
            break
    else:
        raise AssertionError(f"no button named {button_name} found")


@wt(
    parsers.re(
        r'user of (?P<browser_id>\w+) clicks "(?P<button_name>.*)" '
        r"(confirmation )?button in displayed modal"
    )
)
def wt_click_on_confirmation_btn_in_modal(
    selenium: SeleniumDrivers, browser_id: str, button_name: str, tmp_memory: TmpMemory
) -> None:
    driver = selenium[browser_id]
    _click_on_confirmation_btn_in_modal(driver, browser_id, button_name, tmp_memory)


@given(
    parsers.parse(
        'user of {browser_id} clicked "{button_name}" '
        "confirmation button in displayed modal"
    )
)
def g_click_on_confirmation_btn_in_modal(
    selenium: SeleniumDrivers, browser_id: str, button_name: str, tmp_memory: TmpMemory
) -> None:
    driver = selenium[browser_id]
    _click_on_confirmation_btn_in_modal(driver, browser_id, button_name, tmp_memory)


@wt(
    parsers.parse(
        "user of {browser_id} sees that message displayed in modal matches: {regexp}"
    )
)
def is_modal_msg_matching(browser_id: str, regexp: str, tmp_memory: TmpMemory) -> None:
    modal = tmp_memory[browser_id]["window"]["modal"]
    msg = modal.find_element(By.CSS_SELECTOR, ".modal-body .message-text").text
    assert re.match(
        regexp, msg
    ), f"mag displayed in modal: {msg} does not match {regexp}"


@wt(parsers.parse("user of {browser_id} sees non-empty token in active modal"))
def get_token_from_modal(
    selenium: SeleniumDrivers, browser_id: str, tmp_memory: TmpMemory
) -> None:
    driver = selenium[browser_id]
    modal = tmp_memory[browser_id]["window"]["modal"]
    token_box = modal.find_element(By.CSS_SELECTOR, "input[readonly]")
    token = WebDriverWait(driver, WAIT_BACKEND).until(
        lambda _: token_box.get_attribute("value"),
        message="waiting for token to appear",
    )
    tmp_memory[browser_id]["token"] = token


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) clicks on "
        r"((?P<in_type>.*?) )?input box in active modal"
    )
)
def activate_input_box_in_modal(
    browser_id: str, in_type: str, tmp_memory: TmpMemory
) -> None:
    modal = tmp_memory[browser_id]["window"]["modal"]
    css_path = f"input#{in_type_to_id[in_type]}" if in_type else "input"
    in_box = modal.find_element(By.CSS_SELECTOR, css_path)
    # send NULL to activates input box
    in_box.send_keys(Keys.NULL)


@wt(parsers.parse("user of {browser_id} clicks on {option} button in active modal"))
def click_on_button_in_active_modal(
    selenium: SeleniumDrivers, browser_id: str, tmp_memory: TmpMemory, option: str
) -> None:
    driver = selenium[browser_id]
    modal = tmp_memory[browser_id]["window"]["modal"]
    if option == "copy":
        button = modal.find_element(By.CSS_SELECTOR, "button.copy-btn")
    else:
        button = modal.find_element(By.CSS_SELECTOR, ".modal-footer button.btn-default")

    @repeat_failed(attempts=WAIT_FRONTEND, timeout=True)
    def click_on_btn(d: WebDriver, btn: WebElement, error_message: str) -> None:
        click_on_web_elem(d, btn, error_message)

    click_on_btn(driver, button, f"{option} btn for displayed modal disabled")


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{text}" option in modal is not selected'
    )
)
def assert_modal_option_is_not_selected(
    browser_id: str, text: str, tmp_memory: TmpMemory
) -> None:
    modal = tmp_memory[browser_id]["window"]["modal"]
    options = modal.find_elements(
        By.CSS_SELECTOR, ".one-option-button, .one-option-button .oneicon"
    )
    error_message = f'option "{text}" is selected while it should not be'
    for option, checkbox in zip(options[::2], options[1::2]):
        if option.text == text:
            checkbox_css = checkbox.get_attribute("class")
            assert "oneicon-checkbox-empty" in checkbox_css, error_message


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{btn_name}" item '
        "displayed in modal is disabled"
    )
)
def assert_btn_in_modal_is_disabled(
    browser_id: str, btn_name: str, tmp_memory: TmpMemory
) -> None:
    button_name = btn_name.lower()
    modal = tmp_memory[browser_id]["window"]["modal"]
    buttons = modal.find_elements(By.CSS_SELECTOR, "button")
    for btn in buttons:
        if btn.text.lower() == button_name:
            assert not btn.is_enabled(), f"{btn_name} is not disabled"
            break
    else:
        raise AssertionError(f"no button named {button_name} found")


@wt(parsers.parse('user of {browser_id} selects "{text}" option in displayed modal'))
def select_option_with_text_in_modal(
    browser_id: str, text: str, tmp_memory: TmpMemory
) -> None:
    modal = tmp_memory[browser_id]["window"]["modal"]
    options = modal.find_elements(
        By.CSS_SELECTOR, ".one-option-button, .one-option-button .oneicon"
    )
    for option, checkbox in zip(options[::2], options[1::2]):
        if option.text == text:
            checkbox_css = checkbox.get_attribute("class")
            if "oneicon-checkbox-empty" in checkbox_css:
                checkbox.click()


@wt(
    parsers.parse(
        'user of browser sees that "{btn_name}" item displayed in modal is enabled'
    )
)
def assert_btn_in_modal_is_enabled(
    browser_id: str, btn_name: str, tmp_memory: TmpMemory
) -> None:
    button_name = btn_name.lower()
    modal = tmp_memory[browser_id]["window"]["modal"]
    buttons = modal.find_elements_by(By.CSS_SELECTOR, "button")
    for btn in buttons:
        if btn.text.lower() == button_name:
            assert btn.is_enabled(), f"{btn_name} is disabled"
            break
    else:
        raise AssertionError(f"no button named {button_name} found")


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) sees "(?P<text>.*)" '
        r'(?P<element>info|alert) in "(?P<modal>.*)" modal'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_element_text_in_modal(
    selenium: SeleniumDrivers,
    browser_id: str,
    modal: str,
    text: str,
    element: str,
) -> None:
    driver = selenium[browser_id]
    modal = check_modal_name(modal)
    element_sel = "forbidden_alert" if element == "alert" else "info"
    assert_element_text(getattr(Modals(driver), modal), element_sel, text)


def assert_element_text(elem: object, selector: str, elem_text: str) -> None:
    text = cast(WebElement, getattr(elem, selector)).text
    assert elem_text in text, f"found {elem_text} text instead of {text}"


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) clicks on "(?P<button>.*?)" '
        r"button in (?P<panel_name>.*?) panel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_panel_button(
    selenium: SeleniumDrivers, browser_id: str, button: str, panel_name: str
) -> None:
    tab = getattr(Modals(selenium[browser_id]).details_modal, transform(panel_name))
    getattr(tab, transform(button))()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) clicks on clicks on question mark beside the "
        r"(?P<panel_name>.*?) type selector"
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) clicks on clicks on question mark beside the "
        r"(?P<panel_name>Quality of Service) requirements label"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_panel_question_icon(
    selenium: SeleniumDrivers, browser_id: str, panel_name: str
) -> None:
    panel_name = "qos" if panel_name == "Quality of Service" else panel_name
    tab = getattr(Modals(selenium[browser_id]).details_modal, transform(panel_name))
    getattr(tab, "question_icon").click()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) clicks on "(?P<link>.*?)" link in info popup'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_popup_link(selenium: SeleniumDrivers, browser_id: str, link: str) -> None:
    link = "documentation_link" if "documentation" in link else link
    tab = getattr(Popups(selenium[browser_id]), transform("info"))
    getattr(tab, transform(link)).click()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) sees that there is no "
        r'"(?P<button>.*?)" button in (?P<panel_name>.*?) panel'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_there_is_no_button_in_panel(
    selenium: SeleniumDrivers, browser_id: str, button: str, panel_name: str
) -> None:
    modal = getattr(
        Modals(selenium[browser_id]).details_modal, check_modal_name(panel_name)
    )

    try:
        getattr(modal, transform(button))
        raise AssertionError(
            f'There is a "{button}" button visible in {panel_name}'
            " panel when it shouldn't be"
        )
    except RuntimeError:
        pass


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) clicks on "(?P<button>.*?)" '
        r'button in modal "(?P<modal_name>.*?)"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_modal_button(
    selenium: SeleniumDrivers, browser_id: str, button: str, modal_name: str
) -> None:
    modal = getattr(Modals(selenium[browser_id]), check_modal_name(modal_name))
    button = button.replace(".", "")
    getattr(modal, transform(button)).click()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) clicks on "(?P<link>.*?)" '
        r'link in modal "(?P<modal_name>.*?)"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_modal_link(
    selenium: SeleniumDrivers, browser_id: str, link: str, modal_name: str
) -> None:
    modal = getattr(Modals(selenium[browser_id]), check_modal_name(modal_name))
    getattr(modal, transform(link)).click()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) writes "(?P<item_name>.*?)" '
        r"into(?P<name_textfield>.*?) text field "
        r"in (?P<panel_name>.*?) panel"
    )
)
def wt_write_name_into_text_field_in_panel(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_name: str,
    panel_name: str,
    name_textfield: str,
) -> None:
    write_name_into_text_field_in_panel(
        selenium,
        browser_id,
        item_name,
        panel_name,
        name_textfield=name_textfield,
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def write_name_into_text_field_in_panel(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_name: str,
    panel_name: str,
    name_textfield: str = "input name",
) -> None:
    if name_textfield == "":
        name_textfield = "input name"
    driver = selenium[browser_id]
    modal = getattr(Modals(driver).details_modal, check_modal_name(panel_name))
    setattr(modal, transform(name_textfield), item_name)


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) writes "(?P<item_name>.*?)" '
        r"into(?P<name_textfield>.*?) text field "
        r'in modal "(?P<modal_name>.*?)"'
    )
)
def wt_write_name_into_text_field_in_modal(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_name: str,
    modal_name: str,
    name_textfield: str,
) -> None:
    write_name_into_text_field_in_modal(
        selenium,
        browser_id,
        item_name,
        modal_name,
        name_textfield=name_textfield,
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def write_name_into_text_field_in_modal(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_name: str,
    modal_name: str,
    name_textfield: str = "input name",
) -> None:
    if name_textfield == "":
        name_textfield = "input name"
    driver = selenium[browser_id]
    modal = getattr(Modals(driver), check_modal_name(modal_name))
    setattr(modal, transform(name_textfield), item_name)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) sees that item named"
        r' "(?P<item_name>.*?)" '
        r"is shared (?P<number>.*?) times? in modal"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_number_of_shares_in_modal(
    selenium: SeleniumDrivers, browser_id: str, item_name: str, number: str
) -> None:
    name = "Shares"
    driver = selenium[browser_id]
    shares_tab = Modals(driver).details_modal.shares
    navigation = Modals(driver).details_modal.navigation
    links = shares_tab.share_options
    info = look_for_tab_name(navigation, name)
    error_message = f"Item {item_name} is not shared {number} times"
    assert _assert_number_of_shares_in_modal(int(number), links, info), error_message


def look_for_tab_name(navigation: PageObjectsSequence, name: str) -> str:
    for elem in navigation:
        if name in elem.name:
            return elem.name
    raise ValueError(f"tab {name} not found")


def _assert_number_of_shares_in_modal(
    number: int, links: PageObjectsSequence, info: str
) -> bool:
    return str(number) in info and len(links) == number


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "Show details" link for '
        '"{share_name}" share in shares panel'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_share_details_link_in_shares_panel(
    selenium: SeleniumDrivers, browser_id: str, share_name: str
) -> None:
    modal = Modals(selenium[browser_id]).details_modal.shares

    icon = modal.share_options[share_name].share_details_link
    icon.click()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) clicks on "
        r'("(?P<owner_name>.*?)" )?(?P<icon_name>copy) icon'
        r' in modal "(?P<modal_name>.*?)"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_icon_in_share_directory_modal(
    selenium: SeleniumDrivers,
    browser_id: str,
    owner_name: str,
    icon_name: str,
) -> None:
    elem_groups = Modals(selenium[browser_id]).details_modal.shares.share_options
    icon_name = transform(icon_name) + "_icon"
    if owner_name:
        icon = getattr(elem_groups[owner_name], icon_name)
    else:
        icon = getattr(elem_groups[0], icon_name)
    icon.click()


@wt(
    parsers.parse(
        'user of {browser_id} sees that error modal with text "{text}" appeared'
    )
)
@repeat_failed(timeout=WAIT_BACKEND * 6)
def assert_error_modal_with_text_appeared(
    selenium: SeleniumDrivers, browser_id: str, text: str
) -> None:
    modal_text = Modals(selenium[browser_id]).error.content.lower()
    message = f'Modal does not contain text "{text}".\nVisible message: "{modal_text}"'
    assert text.lower().replace("\\", "") in modal_text, message


@wt(parsers.parse('user of {browser_id} sees that "{title}" error modal appeared'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_titled_error_modal_appeared(
    selenium: SeleniumDrivers, browser_id: str, title: str
) -> None:
    message = f'Modal is not titled "{title}"'
    modal_text = Modals(selenium[browser_id]).error.title.lower()
    assert title.lower() in modal_text, message


@repeat_failed(timeout=WAIT_FRONTEND)
def get_error_modal_text(selenium: SeleniumDrivers, browser_id: str) -> str:
    return Modals(selenium[browser_id]).error.content.lower()


@wt(parsers.re(r'user of (?P<browser_id>.*) closes "(?P<modal>.*)" (modal|panel)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def close_modal(selenium: SeleniumDrivers, browser_id: str, modal: str) -> None:
    modal = check_modal_name(modal)
    try:
        getattr(Modals(selenium[browser_id]), modal).close()
    except AttributeError:
        try:
            getattr(Modals(selenium[browser_id]), modal).cancel()
        except AttributeError:
            getattr(Modals(selenium[browser_id]), modal).x()
    except RuntimeError:
        return

    wait_for_named_modal_to_disappear(selenium, browser_id, modal)


@wt(parsers.parse("user of {browser_id} clicks copy command icon in REST API modal"))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_copy_icon_in_rest_api_modal(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    Modals(selenium[browser_id]).rest_api_modal.copy_command_button()


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{option}" in {dropdown_name} '
        'in modal "{modal_name}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_option_in_dropdown_menu_in_modal(
    selenium: SeleniumDrivers,
    browser_id: str,
    dropdown_name: str,
    option: str,
    modal_name: str,
) -> None:
    driver = selenium[browser_id]
    modal = getattr(Modals(driver), transform(modal_name))
    dropdown_menu = getattr(modal, transform(dropdown_name))
    dropdown_menu.click()

    Popups(driver).power_select.choose_item(option)


@wt(
    parsers.re(
        r"(using web GUI, )?user of (?P<browser_id>.*) sees that path where symbolic"
        r' link points is "(?P<expected_path>.*)" in (?P<modal>.*) modal'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_path_where_symbolic_link_points(
    selenium: SeleniumDrivers,
    browser_id: str,
    expected_path: str,
    modal: str,
) -> None:
    driver = selenium[browser_id]
    modal = transform(modal)
    modal_page = getattr(Modals(driver), modal)
    path = modal_page.path.replace("\n", "")

    assert (
        expected_path == path
    ), f"Expected path: {expected_path} does not match path: {path}"


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) (?P<option>checks|unchecks) "
        r'"(?P<toggle_name>.*)" toggle in modal "(?P<modal_name>.*)"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def switch_toggle_in_modal(
    selenium: SeleniumDrivers,
    browser_id: str,
    toggle_name: str,
    option: str,
    modal_name: str,
) -> None:
    driver = selenium[browser_id]
    modal = getattr(Modals(driver), check_modal_name(modal_name))
    toggle = getattr(modal, transform(toggle_name))
    getattr(toggle, option[:-1])()


@wt(
    parsers.parse(
        "user of {browser_id} accepts terms of privacy in Space "
        'Marketplace using checkbox in modal "Advertise space in the marketplace"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def check_checkbox_in_advertise_space_modal(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).advertise_space_in_the_marketplace
    modal.checkbox.click()


@wt(
    parsers.parse(
        'user of {browser_id} closes by pressing "{button}" "{warning_label}" warning'
    )
)
@wt(
    parsers.parse('user of {browser_id} clicks "{button}" on "{warning_label}" warning')
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_on_warning(
    selenium: SeleniumDrivers, browser_id: str, button: str
) -> None:
    driver = selenium[browser_id]
    getattr(Modals(driver).warning_info, transform(button))()
