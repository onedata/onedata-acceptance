"""This module contains meta steps for operations on datasets in Onezone
using web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed
from tests.gui.steps.onezone.spaces import (
    click_element_on_lists_on_left_sidebar_menu,
    click_on_option_of_space_on_left_sidebar_menu,
    click_on_option_in_the_sidebar)
from tests.gui.steps.oneprovider.data_tab import assert_browser_in_tab_in_op
from tests.gui.steps.oneprovider.browser import (
    click_option_in_data_row_menu_in_browser,
    click_menu_for_elem_in_browser, assert_items_presence_in_browser,
    assert_items_absence_in_browser)
from tests.gui.steps.oneprovider.dataset import (
    click_mark_file_as_dataset_toggle, click_protection_toggle)
from tests.gui.steps.modal import click_modal_button


@wt(parsers.parse('user of {browser_id} creates dataset for item '
                  '"{item_name}" in "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_dataset(browser_id, tmp_memory, item_name, space_name,
                   selenium, oz_page, op_container, modals, option):
    option2 = 'Data'
    element = 'spaces'
    option_in_space = 'Files'
    option_in_data_row_menu = 'Datasets'
    button_name = 'X'

    try:
        op_container(selenium[browser_id]).file_browser.breadcrumbs
    except RuntimeError:
        click_on_option_in_the_sidebar(selenium, browser_id, option2, oz_page)
        click_element_on_lists_on_left_sidebar_menu(selenium, browser_id,
                                                    element, space_name,
                                                    oz_page)
        click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                      space_name,
                                                      option_in_space, oz_page)
        assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                    tmp_memory)
    click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id,
                                             option_in_data_row_menu, modals)
    click_mark_file_as_dataset_toggle(browser_id, selenium, modals)
    if ' data' in option:
        toggle_type = 'data'
        click_protection_toggle(browser_id, selenium, modals, toggle_type,
                                option_in_data_row_menu)
    if 'metadata' in option:
        toggle_type = 'metadata'
        click_protection_toggle(browser_id, selenium, modals, toggle_type,
                                option_in_data_row_menu)
    click_modal_button(selenium, browser_id, button_name,
                       option_in_data_row_menu, modals)


def assert_dataset_for_item_in_op_gui(selenium, browser_id, oz_page,
                                      space_name, op_container, tmp_memory,
                                      item_name, option):
    option2 = 'Data'
    element = 'spaces'
    option_in_space = 'Datasets'
    item_browser = 'dataset browser'
    click_on_option_in_the_sidebar(selenium, browser_id, option2, oz_page)
    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id,
                                                element, space_name,
                                                oz_page)
    click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                  space_name,
                                                  option_in_space, oz_page)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory, item_browser=item_browser)
    if option == 'sees':
        assert_items_presence_in_browser(browser_id, item_name, tmp_memory,
                                         which_browser=item_browser)
    else:
        assert_items_absence_in_browser(browser_id, item_name, tmp_memory,
                                        which_browser=item_browser)


def remove_dataset_in_op_gui(selenium, browser_id, oz_page, space_name,
                             op_container, tmp_memory, item_name, modals):
    option = 'Data'
    element = 'spaces'
    option_in_space = 'Datasets'
    item_browser = 'dataset browser'
    option_in_data_row_menu = 'Remove dataset'
    button_name = 'Remove'
    modal = 'Remove selected dataset'
    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id,
                                                element, space_name,
                                                oz_page)
    click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                  space_name,
                                                  option_in_space, oz_page)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory, item_browser=item_browser)
    click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory,
                                   which_browser=item_browser)
    click_option_in_data_row_menu_in_browser(selenium, browser_id,
                                             option_in_data_row_menu, modals)
    click_modal_button(selenium, browser_id, button_name,
                       modal, modals)


