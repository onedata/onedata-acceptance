"""This module contains meta steps for operations on datasets in Onezone
using web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import re
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.meta_steps.oneprovider.data import (
    go_to_path_without_last_elem, check_file_structure_in_browser)
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
    assert_items_absence_in_browser, assert_status_tag_for_file_in_browser,
    click_on_state_view_mode_tab)
from tests.gui.steps.oneprovider.dataset import (
    click_mark_file_as_dataset_toggle, click_protection_toggle,
    assert_general_toggle_checked_for_ancestors,
    fail_to_mark_file_as_dataset_toggle)
from tests.gui.steps.modal import click_modal_button

DATA_PROTECTION = 'data_protection'
METADATA_PROTECTION = 'metadata_protection'


def get_flags(option):
    flags = []
    if re.search("(?!meta)data", option):
        flags.append(DATA_PROTECTION)
    if 'metadata' in option:
        flags.append(METADATA_PROTECTION)
    return flags


def go_to_and_assert_browser(selenium, browser_id, oz_page, space_name,
                             option_in_space, op_container, tmp_memory,
                             item_browser='file browser'):
    option = 'Data'
    element = 'spaces'
    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id,
                                                element, space_name,
                                                oz_page)
    click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                  space_name,
                                                  option_in_space, oz_page)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory, item_browser=item_browser)


def get_item_name_from_path(selenium, browser_id, space_name, oz_page,
                            op_container, tmp_memory, path, option_in_space,
                            item_browser):
    click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                  space_name,
                                                  option_in_space, oz_page)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory, item_browser)
    go_to_path_without_last_elem(selenium, browser_id, tmp_memory,
                                 path, op_container, item_browser)
    return path.split('/')[-1]


@wt(parsers.parse('user of {browser_id} creates dataset{option}for item '
                  '"{item_name}" in "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_dataset(browser_id, tmp_memory, item_name, space_name,
                   selenium, oz_page, op_container, modals, option='no flags'):
    option_in_space = 'Files'
    option_in_data_row_menu = 'Datasets'
    button_name = 'X'

    try:
        op_container(selenium[browser_id]).file_browser.breadcrumbs
    except RuntimeError:
        go_to_and_assert_browser(selenium, browser_id, oz_page, space_name,
                                 option_in_space, op_container, tmp_memory)

    if '/' in item_name:
        item_browser = 'file browser'
        item_name = get_item_name_from_path(selenium, browser_id, space_name,
                                            oz_page, op_container, tmp_memory,
                                            item_name, option_in_space,
                                            item_browser)

    click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id,
                                             option_in_data_row_menu, modals)
    click_mark_file_as_dataset_toggle(browser_id, selenium, modals)
    flags = [item.replace('_protection', '') for item in get_flags(option)]
    for flag in flags:
        click_protection_toggle(browser_id, selenium, modals, flag,
                                option_in_data_row_menu)
    click_modal_button(selenium, browser_id, button_name,
                       option_in_data_row_menu, modals)


def fail_to_create_dataset_in_op_gui(browser_id, tmp_memory, item_name,
                                     space_name, selenium, oz_page,
                                     op_container, modals):
    option_in_space = 'Files'
    option_in_data_row_menu = 'Datasets'
    go_to_and_assert_browser(selenium, browser_id, oz_page, space_name,
                             option_in_space, op_container, tmp_memory)
    click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id,
                                             option_in_data_row_menu, modals)
    fail_to_mark_file_as_dataset_toggle(browser_id, selenium, modals)


def assert_top_level_dataset_in_space_in_op_gui(selenium, browser_id, oz_page,
                                                space_name, op_container,
                                                tmp_memory, item_name, option):
    option_in_space = 'Datasets'
    item_browser = 'dataset browser'
    go_to_and_assert_browser(selenium, browser_id, oz_page, space_name,
                             option_in_space, op_container, tmp_memory,
                             item_browser=item_browser)
    if option == 'sees':
        assert_items_presence_in_browser(browser_id, item_name, tmp_memory,
                                         which_browser=item_browser)
    else:
        assert_items_absence_in_browser(browser_id, item_name, tmp_memory,
                                        which_browser=item_browser)


def remove_dataset_in_op_gui(selenium, browser_id, oz_page, space_name,
                             op_container, tmp_memory, item_name, modals):
    option_in_space = 'Datasets'
    item_browser = 'dataset browser'
    option_in_data_row_menu = 'Remove dataset'
    button_name = 'Remove'
    modal = 'Remove selected dataset'
    go_to_and_assert_browser(selenium, browser_id, oz_page, space_name,
                             option_in_space, op_container, tmp_memory,
                             item_browser=item_browser)
    click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory,
                                   which_browser=item_browser)
    click_option_in_data_row_menu_in_browser(selenium, browser_id,
                                             option_in_data_row_menu, modals)
    click_modal_button(selenium, browser_id, button_name,
                       modal, modals)


def check_dataset_structure_in_op_gui(selenium, browser_id, oz_page, space_name,
                                      config, op_container, tmpdir, tmp_memory):
    # function checks only if what is in config exists, does not
    # fail if there are more datasets
    option_in_space = 'Datasets'
    item_browser = 'dataset browser'
    go_to_and_assert_browser(selenium, browser_id, oz_page, space_name,
                             option_in_space, op_container, tmp_memory,
                             item_browser=item_browser)
    check_file_structure_in_browser(browser_id, config, selenium, tmp_memory,
                                    op_container, tmpdir,
                                    which_browser=item_browser)


def check_effective_protection_flags_for_file_in_op_gui(
        selenium, browser_id, oz_page, space_name, op_container, tmp_memory,
        item_name, modals, option):
    option_in_space = 'Files'
    option_in_data_row_menu = 'Datasets'
    go_to_and_assert_browser(selenium, browser_id, oz_page, space_name,
                             option_in_space, op_container, tmp_memory)
    go_to_path_without_last_elem(selenium, browser_id, tmp_memory,
                                 item_name, op_container)
    item_name = item_name.split('/')[-1]
    click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id,
                                             option_in_data_row_menu, modals)
    flags = [item.replace('_protection', '') for item in get_flags(option)]
    for flag in flags:
        check_effective_protection_flag(browser_id, selenium, modals, flag,
                                        item_name, tmp_memory)


def check_effective_protection_flag(browser_id, selenium, modals, kind,
                                    item_name, tmp_memory):
    try:
        assert_general_toggle_checked_for_ancestors(browser_id, selenium,
                                                    modals, kind)
    except AssertionError:
        status_type = kind + ' protected'
        assert_status_tag_for_file_in_browser(browser_id, status_type,
                                              item_name, tmp_memory)


def set_protection_flags_for_dataset_in_op_gui(browser_id, selenium, oz_page,
                                               space_name, op_container,
                                               tmp_memory, item_name, modals,
                                               option):
    option_in_space = 'Datasets'
    item_browser = 'dataset browser'
    option_in_data_row_menu = 'Write protection'
    go_to_and_assert_browser(selenium, browser_id, oz_page, space_name,
                             option_in_space, op_container, tmp_memory,
                             item_browser=item_browser)
    go_to_path_without_last_elem(selenium, browser_id, tmp_memory,
                                 item_name, op_container,
                                 item_browser=item_browser)
    item_name = item_name.split('/')[-1]

    click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory,
                                   which_browser=item_browser)
    click_option_in_data_row_menu_in_browser(selenium, browser_id,
                                             option_in_data_row_menu, modals)
    button_name = 'Close'
    flags = [item.replace('_protection', '') for item in get_flags(option)]
    for flag in flags:
        click_protection_toggle(browser_id, selenium, modals, flag,
                                option_in_data_row_menu)
    click_modal_button(selenium, browser_id, button_name,
                       option_in_data_row_menu, modals)


def detach_dataset_in_op_gui(selenium, browser_id, oz_page, space_name,
                             op_container, tmp_memory, item_name, modals):
    option_in_space = 'Datasets'
    item_browser = 'dataset browser'
    option_in_data_row_menu = 'Detach'
    modal = 'Detach Dataset'
    button_name = 'Proceed'
    go_to_and_assert_browser(selenium, browser_id, oz_page, space_name,
                             option_in_space, op_container, tmp_memory,
                             item_browser=item_browser)
    click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory,
                                   which_browser=item_browser)
    click_option_in_data_row_menu_in_browser(selenium, browser_id,
                                             option_in_data_row_menu, modals)
    click_modal_button(selenium, browser_id, button_name,
                       modal, modals)


def assert_dataset_detached_in_op_gui(selenium, browser_id, oz_page, item_name,
                                      space_name, op_container, tmp_memory):
    option_in_space = 'Datasets'
    which = 'dataset'
    state = 'detached'
    item_browser = 'dataset browser'
    go_to_and_assert_browser(selenium, browser_id, oz_page, space_name,
                             option_in_space, op_container, tmp_memory,
                             item_browser=item_browser)
    click_on_state_view_mode_tab(browser_id, oz_page, selenium, state, which)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory, item_browser=item_browser)
    assert_items_presence_in_browser(browser_id, item_name, tmp_memory,
                                     which_browser=item_browser)


def reattach_dataset_in_op_gui(selenium, browser_id, oz_page, space_name,
                               op_container, tmp_memory, item_name, modals):
    option_in_space = 'Datasets'
    item_browser = 'dataset browser'
    which = 'dataset'
    state = 'detached'
    option_in_data_row_menu = 'Reattach'
    modal = 'Detach Dataset'
    button_name = 'Proceed'
    go_to_and_assert_browser(selenium, browser_id, oz_page, space_name,
                             option_in_space, op_container, tmp_memory,
                             item_browser=item_browser)
    click_on_state_view_mode_tab(browser_id, oz_page, selenium, state, which)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory, item_browser=item_browser)
    click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory,
                                   which_browser=item_browser)
    click_option_in_data_row_menu_in_browser(selenium, browser_id,
                                             option_in_data_row_menu, modals)
    click_modal_button(selenium, browser_id, button_name,
                       modal, modals)

