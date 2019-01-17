"""This module contains gherkin steps to run acceptance tests featuring
account management in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from pytest_bdd import parsers, when, then

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
