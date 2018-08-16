"""Steps for test suite for space.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import parsers
from tests.utils.acceptance_utils import wt
from tests.gui.utils.generic import parse_seq, repeat_failed
from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND


@wt(parsers.parse('user of {browser_id} clicks Invite user on Menu of Members'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_invite_user_on_menu_of_members(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    elem = oz_page(driver)['spaces']
    elem.members_page.menu_button()
    elem.invite_user()


@wt(parsers.parse('user of {browser_id} sends invitation {item_type} to "{browser_list}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def send_invitation_token_to_browser(selenium, browser_id, item_type, oz_page, displays,
                                     clipboard, browser_list, tmp_memory):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].members_page.input_box.confirm()

    item = clipboard.paste(display=displays[browser_id])
    for browser in parse_seq(browser_list):
        tmp_memory[browser]['mailbox'][item_type.lower()] = item


@wt(parsers.parse('user of {browser_id} clicks Join some space using a space invitation token button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_join_some_space_using_space_invitation_token_button(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].join_space_button()


@wt(parsers.parse('user of {browser_id} pastes Space invitation {item_type} to input '
                  'on Join to a space page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def paste_space_invitation_token_to_input_on_join_to_space_page(selenium, browser_id, tmp_memory,
                                                                item_type, oz_page):
    driver = selenium[browser_id]
    token = tmp_memory[browser_id]['mailbox'][item_type]
    oz_page(driver)['spaces'].input_box.value = token


@wt(parsers.parse('user of {browser_id} clicks Join the space button on Join to a space page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_join_the_space_button_on_join_to_space_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].input_box.confirm()


@wt(parsers.parse('user of {browser_id} clicks Invite group on Menu of Members'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_invite_group_on_menu_of_members(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    elem = oz_page(driver)['spaces']
    elem.members_page.menu_button()
    elem.invite_group()


@wt(parsers.parse('user of {browser_id} clicks Join space on groups menu on left sidebar menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_join_space_on_groups_menu_on_left_sidebar_menu(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    elem = oz_page(driver)['groups']
    elem.menu_button()
    elem.join_space()


@wt(parsers.parse('user of {browser_id} clicks "{group_name}" on groups on left sidebar menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_group_on_groups_on_left_sidebar_menu(selenium, browser_id, group_name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['groups'].elements_list[group_name].click()


@wt(parsers.parse('user of {browser_id} clicks join an existing space on Welcome page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_join_existing_space_on_welcome_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].welcome_page.join_existing_space()