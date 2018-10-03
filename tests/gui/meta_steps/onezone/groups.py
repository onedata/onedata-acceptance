"""This module contains meta steps for operations on groups in Onezone
using web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import parsers
from tests.gui.utils.generic import repeat_failed
from tests.utils.acceptance_utils import wt
from tests.gui.conftest import WAIT_FRONTEND
from selenium.webdriver.common.keys import Keys
from tests.gui.steps.onezone.groups import *
from tests.gui.steps.common.miscellaneous import *


@wt(parsers.re('user of (?P<browser_id>.*) renames group "(?P<group>.*)" '
               'to "(?P<new_group>.*)" using '
               '(?P<confirm_type>.*) to confirm'))
@repeat_failed(timeout=WAIT_FRONTEND)
def rename_group(selenium, browser_id, group, new_group, confirm_type, oz_page):
    option = 'Rename'
    text = new_group

    click_on_group_menu_button(selenium, browser_id, option, group, oz_page)
    input_new_group_name_into_rename_group_inpux_box(selenium, browser_id, text,
                                                     oz_page)
    if confirm_type == 'button':
        click_on_confirmation_button_to_rename_group(selenium, browser_id,
                                                     oz_page)
    else:
        press_enter_on_active_element(selenium, browser_id)
        selenium[browser_id].switch_to.active_element.send_keys(Keys.RETURN)


@wt(parsers.parse('user of {browser_id} leaves group "{group}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def leave_group(selenium, browser_id, group, oz_page):
    option = 'Leave'
    modal = "LEAVE GROUP"

    click_on_group_menu_button(selenium, browser_id, option, group, oz_page)
    click_modal_button(selenium, browser_id, option, modal, oz_page)


@wt(parsers.parse('user of {browser_id} removes group "{group}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_group(selenium, browser_id, group, oz_page):
    option = 'Remove'
    modal = "REMOVE GROUP"

    click_on_group_menu_button(selenium, browser_id, option, group, oz_page)
    click_modal_button(selenium, browser_id, option, modal, oz_page)


@wt(parsers.parse('user of {browser_id} creates group "{group}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_group(selenium, browser_id, group, oz_page):
    operation = 'Create'
    name = group

    click_create_or_join_group_button_in_panel(selenium, browser_id, operation,
                                               oz_page)
    input_name_or_token_into_input_box_on_main_groups_page(selenium, browser_id,
                                                           name, oz_page)
    confirm_name_or_token_input_on_main_groups_page(selenium, browser_id,
                                                    oz_page)
