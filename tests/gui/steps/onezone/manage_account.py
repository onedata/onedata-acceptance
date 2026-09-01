"""This module contains gherkin steps to run acceptance tests featuring
account management in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz, Piotr Duleba"
__copyright__ = "Copyright (C) 2017-2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from selenium.webdriver.common.action_chains import ActionChains

from tests.gui.utils import Modals, OZLoggedIn, Popups
from tests.gui.utils.common.constants import WAIT_FRONTEND
from tests.gui.utils.onezone.manage_account_page import ManageAccountPage
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_FRONTEND)
def open_manage_account_page(selenium: SeleniumDrivers, browser_id: str) -> None:
    oz_page = OZLoggedIn(selenium[browser_id])
    oz_page.open_panel(ManageAccountPage)
    oz_page.expand_panel_if_needed()


@wt(
    parsers.parse(
        "user of {browser_id} expands account settings dropdown in the sidebar"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def expand_account_settings_in_oz(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    oz_page = OZLoggedIn(driver)
    oz_page.expand_panel_if_needed()
    button = oz_page.profile.profile.web_elem
    ActionChains(driver).move_to_element(button).click(button).perform()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) clicks on "
        r"(?P<option>Logout|Manage account) item in expanded "
        r"settings dropdown in the sidebar"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_in_account_settings_in_oz(
    selenium: SeleniumDrivers, browser_id: str, option: str
) -> None:
    driver = selenium[browser_id]
    oz_page = OZLoggedIn(driver)
    if option == "Manage account":
        oz_page.open_panel(ManageAccountPage)
    Popups(driver).user_account_menu.options[option].click()


@repeat_failed(timeout=WAIT_FRONTEND)
def click_emergency_panel_logout(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    button = OZLoggedIn(driver).profile.logout.web_elem
    ActionChains(driver).move_to_element(button).click(button).perform()


@repeat_failed(timeout=WAIT_FRONTEND)
def start_username_change(selenium: SeleniumDrivers, browser_id: str) -> None:
    OZLoggedIn(selenium[browser_id]).profile.rename_username()


@repeat_failed(timeout=WAIT_FRONTEND)
def enter_new_username(
    selenium: SeleniumDrivers, browser_id: str, new_username: str
) -> None:
    OZLoggedIn(selenium[browser_id]).profile.edit_user_name_box.value = new_username


@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_username_change(selenium: SeleniumDrivers, browser_id: str) -> None:
    OZLoggedIn(selenium[browser_id]).profile.edit_user_name_box.confirm.click()


@repeat_failed(timeout=WAIT_FRONTEND)
def click_edit_password_form(selenium: SeleniumDrivers, browser_id: str) -> None:
    OZLoggedIn(selenium[browser_id]).profile.rename_password()


@repeat_failed(timeout=WAIT_FRONTEND)
def enter_password_change_values(
    selenium: SeleniumDrivers,
    browser_id: str,
    current_password: str,
    new_password: str,
) -> None:
    profile = OZLoggedIn(selenium[browser_id]).profile
    profile.current_password_box = current_password
    profile.type_new_password_box = new_password
    profile.retype_new_password_box = new_password


@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_password_change(selenium: SeleniumDrivers, browser_id: str) -> None:
    OZLoggedIn(selenium[browser_id]).profile.change_password.click()


@wt(parsers.parse("user of {browser_id} clicks on menu button on Profile page"))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_user_menu_button_in_oz(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    OZLoggedIn(driver).profile.show_user_account_menu_toolbar.click()


@wt(
    parsers.parse(
        "user of {browser_id} clicks on remove user button in menu on Profile page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_remove_user_button_in_oz(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    Popups(driver).user_delete_account_popover_menu.click()


@wt(
    parsers.parse(
        "user of {browser_id} checks understand consequences "
        "of removing user account checkbox in modal"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_understand_consequences_checkbox_in_oz(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    Modals(driver).delete_user_account.understand_consequences.click()


@wt(parsers.parse("user of {browser_id} clicks on delete account button in modal"))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_delete_account_button_in_oz(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    Modals(driver).delete_user_account.delete_account.click()


@wt(
    parsers.parse(
        "user of {browser_id} sees that the user's name displayed "
        'in Profile page is "{expected_user_name}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_correct_user_name_in_oz(
    selenium: SeleniumDrivers, browser_id: str, expected_user_name: str
) -> None:
    driver = selenium[browser_id]
    displayed_user_name = OZLoggedIn(driver).profile.user_name
    error_message = (
        f"expected {expected_user_name} as user name, but instead "
        f"displayed is {displayed_user_name} in USER NAME oz panel"
    )
    assert displayed_user_name == expected_user_name, error_message


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) sees "(?P<username>.*?)" '
        r"alias in the sidebar panel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_user_alias_in_sidebar(
    selenium: SeleniumDrivers, browser_id: str, username: str
) -> None:
    driver = selenium[browser_id]
    error_message = "User alias: {} not found in the sidebar, visible alias: {}"

    try:
        name = OZLoggedIn(driver).profile_username
        assert name == username, error_message.format(username, name)
    except AssertionError:
        OZLoggedIn(driver).profile.profile()
        name = OZLoggedIn(driver).profile_username
        assert name == username, error_message.format(username, name)
