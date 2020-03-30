"""Meta steps implementation for shares GUI tests."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.steps.oneprovider.data_tab import \
    assert_file_browser_in_data_tab_in_op
from tests.gui.steps.onezone.clusters import \
    click_option_of_record_in_the_sidebar
from tests.gui.steps.onezone.spaces import \
    click_on_option_of_space_on_left_sidebar_menu
from tests.utils.bdd_utils import wt, when, then, parsers
from tests.gui.steps.modal import (
    wt_wait_for_modal_to_appear, write_name_into_text_field_in_modal,
    click_modal_button, click_share_info_icon_in_share_directory_modal)
from tests.gui.steps.oneprovider.file_browser import (
    click_menu_for_elem_in_file_browser,
    click_option_in_data_row_menu_in_file_browser)
from tests.gui.steps.oneprovider.shares import *


@wt(parsers.parse('user of {browser_id} creates "{share_name}" share of'
                  ' "{item_name}" file'))
@wt(parsers.parse('user of {browser_id} creates "{share_name}" share of'
                  ' "{item_name}" directory'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_share(selenium, browser_id, share_name, item_name, tmp_memory,
                 modals):
    option = 'Share'
    modal_name = 'Share directory'
    text_field = 'share name'
    button = 'Create'

    click_menu_for_elem_in_file_browser(browser_id, item_name, tmp_memory)
    click_option_in_data_row_menu_in_file_browser(selenium, browser_id, option,
                                                  modals)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    write_name_into_text_field_in_modal(selenium, browser_id, share_name,
                                        modal_name, modals, text_field)
    click_modal_button(selenium, browser_id, button, modal_name, modals)


@wt(parsers.parse('user of {browser_id} moves to "{share_name}" single share '
                  'view using modal icon'))
@repeat_failed(timeout=WAIT_FRONTEND)
def move_to_single_share_view_by_modal(selenium, browser_id, share_name, modals,
                                       op_page, tmp_memory):
    modal_name = 'Share directory'
    items_browser = 'file_browser'

    click_share_info_icon_in_share_directory_modal(selenium, browser_id, modals,
                                                   share_name)
    assert_file_browser_in_data_tab_in_op(selenium, browser_id, op_page,
                                          tmp_memory, items_browser)
    is_selected_share_named(selenium, browser_id, share_name, op_page)
    change_shares_browser_to_file_browser(selenium, browser_id, op_page,
                                          tmp_memory)


@wt(parsers.parse('user of {browser_id} creates another '
                  'share named "{share_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_another_share(selenium, browser_id, share_name, modals):
    button = 'Create another share'
    modal_name = 'Share directory'
    text_field = 'share name'
    create_button = 'Create'

    click_modal_button(selenium, browser_id, button, modal_name, modals)
    write_name_into_text_field_in_modal(selenium, browser_id, share_name,
                                        modal_name, modals, text_field)
    click_modal_button(selenium, browser_id, create_button, modal_name, modals)


@wt(parsers.parse('user of {browser_id} removes current share'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_current_share(selenium, browser_id, op_page, modals, tmp_memory):
    option = 'Remove'
    modal_name = 'Remove share'
    button = 'Remove'

    click_menu_button_on_shares_page(selenium, browser_id, op_page)
    click_option_in_share_row_menu(selenium, browser_id, option, modals)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    click_modal_button(selenium, browser_id, button, modal_name, modals)


@wt(parsers.parse('user of {browser_id} moves to shares view'
                  ' of "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def move_to_shares_view_of_given_space(selenium, browser_id, oz_page,
                                       space_name, op_page, tmp_memory):
    option = 'Shares'
    items_browser = 'shares_browser'

    click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                  space_name, option, oz_page)
    assert_file_browser_in_data_tab_in_op(selenium, browser_id, op_page,
                                          tmp_memory, items_browser)


@wt(parsers.parse('user of {browser_id} moves to "{share_name}" single share '
                  'view using sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def move_to_single_share_view_by_sidebar(selenium, browser_id, share_name,
                                         op_page, tmp_memory, oz_page,
                                         space_name):
    move_to_shares_view_of_given_space(selenium, browser_id, oz_page,
                                       space_name, op_page, tmp_memory)
    click_share_in_shares_browser(selenium, browser_id, share_name, op_page)
    change_shares_browser_to_file_browser(selenium, browser_id, op_page,
                                          tmp_memory)

