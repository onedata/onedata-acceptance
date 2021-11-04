"""This module contains meta steps for operations on archives in Onezone
using web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import yaml

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed
from tests.gui.steps.onezone.spaces import (
    click_on_option_of_space_on_left_sidebar_menu,
    click_on_option_in_the_sidebar, click_element_on_lists_on_left_sidebar_menu)
from tests.gui.steps.oneprovider.data_tab import assert_browser_in_tab_in_op
from tests.gui.steps.oneprovider.browser import (
    click_option_in_data_row_menu_in_browser,
    click_menu_for_elem_in_browser, assert_items_presence_in_browser)
from tests.gui.steps.oneprovider.archives import (
    check_toggle_in_create_archive_modal,
    write_description_in_create_archive_modal, click_on_number_in_archives,
    double_click_on_archive, click_menu_for_archive,
    write_in_confirmation_input,
    assert_number_of_archives_for_item_in_dataset_browser,
    assert_tag_for_archive_in_archive_browser,
    assert_not_archive_with_description)
from tests.gui.steps.modal import click_modal_button


@wt(parsers.parse('user of {browser_id} creates archive for item '
                  '"{item_name}" in "{space_name}" with following '
                  'configuration:\n{config}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_archive(browser_id, selenium, config, item_name, space_name,
                   oz_page, op_container, tmp_memory, modals, clipboard,
                   displays):
    """Create archive according to given config.

    Config format given in yaml is as follow:

            description: archive_description        ---> optional
            layout: plain/BagIt
            create nested archives: True/False      ---> optional,
            incremental: True/False                 ---> optional
            include DIP: True/False                 ---> optional


    Example configuration:

          layout: plain
          incremental: True
    """
    _create_archive(browser_id, selenium, config, item_name, space_name,
                    oz_page, op_container, tmp_memory, modals, clipboard,
                    displays)


@repeat_failed(timeout=WAIT_FRONTEND)
def _create_archive(browser_id, selenium, config, item_name, space_name,
                    oz_page, op_container, tmp_memory, modals,
                    clipboard, displays):
    option_in_space = 'Datasets'
    item_browser = 'dataset browser'
    option_in_data_row_menu = 'Create archive'
    button_name = 'Create'
    try:
        op_container(selenium[browser_id]).dataset_browser.breadcrumbs
    except RuntimeError:
        click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                      space_name,
                                                      option_in_space, oz_page)
        assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                    tmp_memory, item_browser)
    click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory,
                                   item_browser)
    click_option_in_data_row_menu_in_browser(selenium, browser_id,
                                             option_in_data_row_menu, modals)
    data = yaml.load(config)

    description = data.get('description', False)
    layout = data['layout']
    create_nested_archives = data.get('create nested archives', False)
    incremental = data.get('incremental', False)
    include_dip = data.get('include DIP', False)
    if description:
        write_description_in_create_archive_modal(selenium, browser_id, modals,
                                                  description)
    if layout == 'BagIt':
        click_modal_button(selenium, browser_id, layout,
                           option_in_data_row_menu, modals)
    if create_nested_archives:
        option = 'create_nested_archives'
        check_toggle_in_create_archive_modal(browser_id, selenium, modals,
                                             option)
    if incremental:
        option = 'incremental'
        check_toggle_in_create_archive_modal(browser_id, selenium, modals,
                                             option)
    if include_dip:
        option = 'include_dip'
        check_toggle_in_create_archive_modal(browser_id, selenium, modals,
                                             option)
    click_modal_button(selenium, browser_id, button_name,
                       option_in_data_row_menu, modals)
    client = 'web GUI'
    if description:
        copy_archive_id_to_tmp_memory(selenium, browser_id, op_container,
                                      client, tmp_memory, modals, clipboard,
                                      displays, description)


def copy_archive_id_to_tmp_memory(selenium, browser_id, op_container, client,
                                  tmp_memory, modals, clipboard, displays,
                                  description):
    if client.lower() == 'web gui':
        archive_browser = 'archive browser'
        option_in_menu = 'Copy archive ID'
        assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                    tmp_memory, archive_browser)
        click_menu_for_archive(browser_id, tmp_memory, description)
        click_option_in_data_row_menu_in_browser(selenium, browser_id,
                                                 option_in_menu, modals)
        tmp_memory[description] = clipboard.paste(
            display=displays[browser_id])


def assert_archive_in_op_gui(browser_id, selenium, item_name, space_name,
                             oz_page, op_container, tmp_memory, option,
                             description):
    option2 = 'Data'
    element = 'spaces'
    option_in_space = 'Datasets'
    dataset_browser = 'dataset browser'
    archive_browser = 'archive browser'
    archive_file_browser = 'archive file browser'
    click_on_option_in_the_sidebar(selenium, browser_id, option2, oz_page)
    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id,
                                                element, space_name,
                                                oz_page)
    click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                  space_name,
                                                  option_in_space, oz_page)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory, item_browser=dataset_browser)
    if option == 'sees':
        click_on_number_in_archives(browser_id, tmp_memory, item_name)
        assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                    tmp_memory, item_browser=archive_browser)
        double_click_on_archive(browser_id, tmp_memory, description)
        assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                    tmp_memory,
                                    item_browser=archive_file_browser)
        assert_items_presence_in_browser(browser_id, item_name, tmp_memory,
                                         which_browser=archive_file_browser)
    else:
        try:
            number = '0'
            assert_number_of_archives_for_item_in_dataset_browser(browser_id,
                                                                  item_name,
                                                                  number,
                                                                  tmp_memory)
        except AssertionError:
            click_on_number_in_archives(browser_id, tmp_memory, item_name)
            assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                        tmp_memory,
                                        item_browser=archive_browser)
            assert_not_archive_with_description(tmp_memory, browser_id,
                                                description)


def remove_archive_in_op_gui(browser_id, selenium, item_name, space_name,
                             oz_page, op_container, tmp_memory, modals,
                             description):
    option = 'Data'
    element = 'spaces'
    option_in_space = 'Datasets'
    dataset_browser = 'dataset browser'
    archive_browser = 'archive browser'
    option_in_menu = 'Purge archive'
    text = 'I understand that data of the archive will be lost'
    button_name = 'Purge archive'
    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id,
                                                element, space_name,
                                                oz_page)
    click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                  space_name,
                                                  option_in_space, oz_page)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory, item_browser=dataset_browser)
    click_on_number_in_archives(browser_id, tmp_memory, item_name)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory, item_browser=archive_browser)
    click_menu_for_archive(browser_id, tmp_memory, description)
    click_option_in_data_row_menu_in_browser(selenium, browser_id,
                                             option_in_menu, modals)
    write_in_confirmation_input(browser_id, modals, text, selenium)
    click_modal_button(selenium, browser_id, button_name,
                       option_in_menu, modals)


def assert_bagit_archive_in_op_gui(browser_id, selenium, oz_page, space_name,
                                   op_container, tmp_memory, item_name, option,
                                   description):
    option2 = 'Data'
    element = 'spaces'
    option_in_space = 'Datasets'
    dataset_browser = 'dataset browser'
    archive_browser = 'archive browser'
    tag_type = transform(option)
    click_on_option_in_the_sidebar(selenium, browser_id, option2, oz_page)
    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id,
                                                element, space_name,
                                                oz_page)
    click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                  space_name,
                                                  option_in_space, oz_page)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory, item_browser=dataset_browser)
    click_on_number_in_archives(browser_id, tmp_memory, item_name)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory, item_browser=archive_browser)
    assert_tag_for_archive_in_archive_browser(browser_id, tag_type, tmp_memory,
                                              description)

