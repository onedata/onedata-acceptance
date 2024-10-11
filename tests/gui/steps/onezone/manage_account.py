"""This module contains gherkin steps to run acceptance tests featuring
account management in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz, Piotr Duleba"
__copyright__ = "Copyright (C) 2017-2020 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        "user of {browser_id} expands account settings dropdown in the sidebar"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def expand_account_settings_in_oz(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)["profile"].profile()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) clicks on "
        r"(?P<option>Logout|Manage account) item in expanded "
        r"settings dropdown in the sidebar"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_in_account_settings_in_oz(
    selenium, browser_id, option, popups
):
    driver = selenium[browser_id]
    popups(driver).user_account_menu.options[option].click()


@wt(parsers.parse("user of {browser_id} clicks on menu button on Profile page"))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_user_menu_button_in_oz(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)["profile"].show_user_account_menu_toolbar.click()


@wt(
    parsers.parse(
        "user of {browser_id} clicks on remove user button in menu "
        "on Profile page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_remove_user_button_in_oz(selenium, browser_id, popups):
    driver = selenium[browser_id]
    popups(driver).user_delete_account_popover_menu.click()


@wt(
    parsers.parse(
        "user of {browser_id} checks understand consequences "
        "of removing user account checkbox in modal"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_understand_consequences_checkbox_in_oz(selenium, browser_id, modals):
    driver = selenium[browser_id]
    modals(driver).delete_user_account.understand_consequences.click()


@wt(
    parsers.parse(
        "user of {browser_id} clicks on delete account button in modal"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_delete_account_button_in_oz(selenium, browser_id, modals):
    driver = selenium[browser_id]
    modals(driver).delete_user_account.delete_account.click()


@wt(
    parsers.parse(
        "user of {browser_id} sees that the user's name displayed "
        'in Profile page is "{expected_user_name}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_correct_user_name_in_oz(
    selenium, browser_id, expected_user_name, oz_page
):
    driver = selenium[browser_id]
    displayed_user_name = oz_page(driver)["profile"].user_name
    err_msg = (
        f"expected {expected_user_name} as user name, but instead "
        f"displayed is {displayed_user_name} in USER NAME oz panel"
    )
    assert displayed_user_name == expected_user_name, err_msg


@wt(
    parsers.re(
        'user of (?P<browser_id>.*) sees "(?P<username>.*?)" alias in '
        "the sidebar panel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_user_alias_in_sidebar(selenium, browser_id, oz_page, username):
    driver = selenium[browser_id]
    err_msg = "User alias: {} not found in the sidebar, visible alias: {}"

    try:
        name = oz_page(driver).profile_username
        assert name == username, err_msg.format(username, name)
    except AssertionError:
        oz_page(driver)["profile"].profile()
        name = oz_page(driver).profile_username
        assert name == username, err_msg.format(username, name)
