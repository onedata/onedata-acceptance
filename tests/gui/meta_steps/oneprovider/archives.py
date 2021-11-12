"""This module contains meta steps for operations on archives in Onezone
using web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import yaml

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.meta_steps.oneprovider.data import go_to_path_without_last_elem
from tests.gui.meta_steps.oneprovider.dataset import go_to_and_assert_browser
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed
from tests.gui.steps.onezone.spaces import (
    click_on_option_of_space_on_left_sidebar_menu)
from tests.gui.steps.oneprovider.data_tab import assert_browser_in_tab_in_op
from tests.gui.steps.oneprovider.browser import (
    click_option_in_data_row_menu_in_browser,
    click_menu_for_elem_in_browser, assert_items_presence_in_browser,
    assert_not_click_option_in_data_row_menu)
from tests.gui.steps.oneprovider.archives import (
    check_toggle_in_create_archive_modal,
    write_description_in_create_archive_modal, click_on_number_in_archives,
    double_click_on_archive, click_menu_for_archive,
    write_in_confirmation_input,
    assert_number_of_archives_for_item_in_dataset_browser,
    assert_tag_for_archive_in_archive_browser,
    assert_not_archive_with_description, get_archive_from_description)
from tests.gui.steps.modal import click_modal_button


@wt(parsers.parse('user of {browser_id} {option} archive for item '
                  '"{item_name}" in "{space_name}" with following '
                  'configuration:\n{config}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_archive(browser_id, selenium, config, item_name, space_name,
                   oz_page, op_container, tmp_memory, modals, clipboard,
                   displays, option):
    """Create archive according to given config.

    Config format given in yaml is as follow:

            description: archive_description        ---> optional
            layout: plain/BagIt
            create nested archives: True/False      ---> optional,
            incremental:                            ---> optional
                enabled: True/False
            include DIP: True/False                 ---> optional


    Example configuration:

          layout: plain
          incremental:
            enabled: True
    """
    _create_archive(browser_id, selenium, config, item_name, space_name,
                    oz_page, op_container, tmp_memory, modals, clipboard,
                    displays, option)


def _create_archive(browser_id, selenium, config, item_name, space_name,
                    oz_page, op_container, tmp_memory, modals,
                    clipboard, displays, option):
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

    if '/' in item_name:
        click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                      space_name,
                                                      option_in_space, oz_page)
        assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                    tmp_memory, item_browser)
        go_to_path_without_last_elem(selenium, browser_id, tmp_memory,
                                     item_name, op_container, item_browser)
        item_name = item_name.split('/')[-1]

    click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory,
                                   item_browser)
    if option == 'creates':
        click_option_in_data_row_menu_in_browser(selenium, browser_id,
                                                 option_in_data_row_menu,
                                                 modals)
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
            if incremental['enabled']:
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
    elif option == 'fails to create':
        assert_not_click_option_in_data_row_menu(selenium, browser_id,
                                                 option_in_data_row_menu,
                                                 modals)


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
    option_in_space = 'Datasets'
    dataset_browser = 'dataset browser'
    archive_browser = 'archive browser'
    archive_file_browser = 'archive file browser'
    go_to_and_assert_browser(selenium, browser_id, oz_page, space_name,
                             option_in_space, op_container, tmp_memory,
                             item_browser=dataset_browser)
    if '/' in item_name:
        click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                      space_name,
                                                      option_in_space, oz_page)
        assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                    tmp_memory, item_browser=dataset_browser)
        go_to_path_without_last_elem(selenium, browser_id, tmp_memory,
                                     item_name, op_container,
                                     item_browser=dataset_browser)
        item_name = item_name.split('/')[-1]

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
                             description, option):
    option_in_space = 'Datasets'
    dataset_browser = 'dataset browser'
    archive_browser = 'archive browser'
    option_in_menu = 'Purge archive'
    text = 'I understand that data of the archive will be lost'
    button_name = 'Purge archive'
    go_to_and_assert_browser(selenium, browser_id, oz_page, space_name,
                             option_in_space, op_container, tmp_memory,
                             item_browser=dataset_browser)
    click_on_number_in_archives(browser_id, tmp_memory, item_name)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory, item_browser=archive_browser)
    click_menu_for_archive(browser_id, tmp_memory, description)

    if option == 'removes':
        click_option_in_data_row_menu_in_browser(selenium, browser_id,
                                                 option_in_menu, modals)
        write_in_confirmation_input(browser_id, modals, text, selenium)
        click_modal_button(selenium, browser_id, button_name,
                           option_in_menu, modals)
    elif option == 'fails to remove':
        assert_not_click_option_in_data_row_menu(selenium, browser_id,
                                                 button_name,
                                                 modals)


def assert_archive_with_option_in_op_gui(browser_id, selenium, oz_page,
                                         space_name, op_container, tmp_memory,
                                         item_name, option, description):
    option_in_space = 'Datasets'
    dataset_browser = 'dataset browser'
    archive_browser = 'archive browser'
    tag_type = transform(option)
    go_to_and_assert_browser(selenium, browser_id, oz_page, space_name,
                             option_in_space, op_container, tmp_memory,
                             item_browser=dataset_browser)
    click_on_number_in_archives(browser_id, tmp_memory, item_name)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory, item_browser=archive_browser)
    assert_tag_for_archive_in_archive_browser(browser_id, tag_type, tmp_memory,
                                              description)


def assert_number_of_archive_in_op_gui(browser_id, selenium, item_name,
                                       space_name, oz_page, op_container,
                                       tmp_memory, number):
    option_in_space = 'Datasets'
    dataset_browser = 'dataset browser'
    go_to_and_assert_browser(selenium, browser_id, oz_page, space_name,
                             option_in_space, op_container, tmp_memory,
                             item_browser=dataset_browser)
    if '/' in item_name:
        click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                      space_name,
                                                      option_in_space, oz_page)
        assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                    tmp_memory, item_browser=dataset_browser)
        go_to_path_without_last_elem(selenium, browser_id, tmp_memory,
                                     item_name, op_container,
                                     item_browser=dataset_browser)
        item_name = item_name.split('/')[-1]
    assert_number_of_archives_for_item_in_dataset_browser(browser_id, item_name,
                                                          number, tmp_memory)


def assert_base_archive_for_archive_in_op_gui(browser_id, selenium, item_name,
                                              space_name, oz_page, op_container,
                                              tmp_memory, description,
                                              base_description):
    option_in_space = 'Datasets'
    dataset_browser = 'dataset browser'

    archive_browser = 'archive browser'
    go_to_and_assert_browser(selenium, browser_id, oz_page, space_name,
                             option_in_space, op_container, tmp_memory,
                             item_browser=dataset_browser)
    click_on_number_in_archives(browser_id, tmp_memory, item_name)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory, item_browser=archive_browser)
    browser = tmp_memory[browser_id]['archive_browser']
    archive = get_archive_from_description(browser, description)
    err_msg = (f'Base archive: {archive.base_archive} does not match expected '
               f'archive with description {base_description}')
    assert base_description in archive.base_archive, err_msg
