"""This module contains gherkin steps to run acceptance tests featuring
common operations in onepanel web GUI.
"""

__author__ = "Michal Dronka"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_BACKEND
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} clicks on "Invite user using token" '
                  'button on cluster members page'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_invite_user_using_token_btn_on_members_panel(selenium, browser_id,
                                                       onepanel):
    driver = selenium[browser_id]
    onepanel(driver).content.members_emergency_interface.invite_using_token\
        .click()


@wt(parsers.parse('user of {browser_id} clicks on "Copy" button on cluster '
                  'members page'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_copy_btn_on_members_panel(selenium, browser_id, onepanel):
    driver = selenium[browser_id]
    onepanel(driver).content.members_emergency_interface.copy_token.click()


@wt(parsers.parse('user of {browser_id} sees number of direct users is equal '
                  '{number} on cluster members page'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_equal_direct_user_number(selenium, browser_id, number, onepanel):
    driver = selenium[browser_id]
    assert onepanel(driver).content.members_emergency_interface\
               .direct_users_number == number
