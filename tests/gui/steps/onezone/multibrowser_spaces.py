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


@wt(parsers.parse('user of {browser_id} clicks Invite user on Menu of Members'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_invite_user_on_menu_of_members(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    elem = oz_page(driver)['spaces']
    elem.menu_button()
    elem.menu['Invite user'].click()


@wt(parsers.parse('user of {browser_id} sends invitation {item_type} '
                  'to "{browser_list}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def send_invitation_token_to_browser(selenium, browser_id, item_type, oz_page,
                                     displays, clipboard, browser_list,
                                     tmp_memory):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].members_page.token.copy()

    item = clipboard.paste(display=displays[browser_id])
    for browser in parse_seq(browser_list):
        tmp_memory[browser]['mailbox'][item_type.lower()] = item


@wt(parsers.parse('user of {browser_id} clicks Join some space '
                  'using a space invitation token button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_join_some_space_using_space_invitation_token_button(selenium,
                                                              browser_id,
                                                              oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].join_space_button()


@wt(parsers.parse('user of {browser_id} pastes Space invitation {item_type} '
                  'into space token text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def paste_space_invitation_token_to_input_on_join_to_space_page(selenium,
                                                                browser_id,
                                                                tmp_memory,
                                                                item_type,
                                                                oz_page):
    driver = selenium[browser_id]
    token = tmp_memory[browser_id]['mailbox'][item_type]
    oz_page(driver)['spaces'].input_box.value = token


@wt(parsers.parse('user of {browser_id} clicks Join the space button '
                  'on Join to a space page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_join_the_space_button_on_join_to_space_page(selenium, browser_id,
                                                      oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].input_box.confirm()


@wt(parsers.parse('user of {browser_id} clicks Join space '
                  'on the groups list in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_join_space_on_groups_menu_on_left_sidebar_menu(selenium, browser_id,
                                                         oz_page):
    driver = selenium[browser_id]
    elem = oz_page(driver)['groups']
    elem.groups_menu_button()
    elem.join_space.click()


@wt(parsers.parse('user of {browser_id} clicks "{group_name}" '
                  'on the groups list in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_group_on_groups_on_left_sidebar_menu(selenium, browser_id,
                                               group_name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['groups'].elements_list[group_name].click()


@wt(parsers.re('user of (?P<browser_id>.*) confirms join the space '
               'using (?P<option>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_join_the_space(selenium, browser_id, option, oz_page):
    if option == 'enter':
        press_enter_on_active_element(selenium, browser_id)
    else:
        click_join_the_space_button_on_join_to_space_page(selenium, browser_id,
                                                          oz_page)
