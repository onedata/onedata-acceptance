"""This module contains gherkin steps to run acceptance tests featuring
account management in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz, Piotr Duleba"
__copyright__ = "Copyright (C) 2017-2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from pytest_bdd import parsers, when, then
from tests.utils.acceptance_utils import wt
from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.utils import repeat_failed
from tests.gui.utils.common.popups import Popups as popups


@when(parsers.parse('user of {browser_id} expands account settings '
                    'dropdown in the sidebar'))
@then(parsers.parse('user of {browser_id} expands account settings '
                    'dropdown in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def expand_account_settings_in_oz(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['profile'].profile()


@when(parsers.re(r'user of (?P<browser_id>.+?) clicks on '
                 r'(?P<option>Logout|Manage account) item in expanded '
                 r'settings dropdown in the sidebar'))
@then(parsers.re(r'user of (?P<browser_id>.+?) clicks on '
                 r'(?P<option>Logout|Manage account) item in expanded '
                 r'settings dropdown in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_in_account_settings_in_oz(selenium, browser_id, option):
    driver = selenium[browser_id]
    popups(driver).user_account_menu.options[option].click()


@wt(parsers.parse('user of {browser_id} clicks on remove user toolbar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_remove_user_toolbar_in_oz(selenium, browser_id, oz_page,):
    oz_page(selenium[browser_id])['profile'].show_user_account_menu_toolbar.click()


@wt(parsers.parse('user of {browser_id} clicks on remove user button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_remove_user_button_in_oz(selenium, browser_id, popups):
    popups(selenium[browser_id]).user_delete_account_popover_menu.click()


@wt(parsers.parse('user of {browser_id} clicks on understand consequences checkbox'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_understand_consequences_checkbox_in_oz(selenium, browser_id, modals):
    modals(selenium[browser_id]).delete_user_account.understand_consequences.click()


@wt(parsers.parse('user of {browser_id} clicks on delete account button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_delete_account_button_in_oz(selenium, browser_id, modals, users):
    modals(selenium[browser_id]).delete_user_account.delete_account.click()
    users.pop('user1', None)


