"""This module contains gherkin steps to run acceptance tests featuring
joining spaces in onezone web GUI.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import parsers

from tests.utils.acceptance_utils import wt
from tests.utils.utils import repeat_failed
from tests.gui.utils.generic import parse_seq
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import press_enter_on_active_element


@wt(parsers.parse('user of {browser_id} sends invitation {item_type} '
                  'to "{browser_list}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def send_invitation_token_to_browser(selenium, browser_id, item_type, oz_page,
                                     displays, clipboard, browser_list,
                                     tmp_memory):
    item = clipboard.paste(display=displays[browser_id])
    for browser in parse_seq(browser_list):
        tmp_memory[browser]['mailbox'][item_type.lower()] = item


@wt(parsers.parse('user of {browser_id} clicks "{group_name}" '
                  'on the groups list in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_group_on_groups_on_left_sidebar_menu(selenium, browser_id,
                                               group_name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['groups'].elements_list[group_name].click()

