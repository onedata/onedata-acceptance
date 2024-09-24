"""This module contains meta steps for operations on archives in Onezone
using web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import yaml
import time
import re

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.meta_steps.oneprovider.data import (
    go_to_path_without_last_elem, go_to_and_assert_browser)
from tests.gui.meta_steps.oneprovider.dataset import (
    get_item_name_from_path)
from tests.gui.steps.oneprovider.archives_recall import (
    assert_recall_duration_in_archive_recall_information_modal)
from tests.gui.steps.oneprovider.dataset import click_on_dataset
from tests.gui.steps.oneprovider.file_browser import (
    click_on_status_tag_for_file_in_file_browser)
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed
from tests.gui.steps.onezone.spaces import (
    click_on_option_of_space_on_left_sidebar_menu)
from tests.gui.steps.oneprovider.data_tab import (
    assert_browser_in_tab_in_op,  check_size_statistic_in_dir_details,
    check_size_stats_for_provider)
from tests.gui.steps.oneprovider.browser import (
    click_option_in_data_row_menu_in_browser,
    click_menu_for_elem_in_browser, assert_items_presence_in_browser,
    assert_option_state_in_data_row_menu)
from tests.gui.steps.oneprovider.archives import (
    check_toggle_in_create_archive_modal,
    write_description_in_create_archive_modal,
    click_and_press_enter_on_archive, click_menu_for_archive,
    write_in_confirmation_input,
    assert_number_of_archives_for_item_in_dataset_browser,
    assert_tag_for_archive_in_archive_browser,
    assert_not_archive_with_description, get_archive_with_description,
    assert_archive_info_in_properties_modal)
from tests.gui.steps.modals.modal import (
    click_modal_button, write_name_into_text_field_in_modal)


OPTION_IN_SPACE = 'Datasets, Archives'
DATASET_BROWSER = 'dataset browser'
ARCHIVE_BROWSER = 'archive browser'
ARCHIVE_FILE_BROWSER = 'archive file browser'


@wt(parsers.parse('user of {browser_id} {option} to create archive for item '
                  '"{item_name}" in "{space_name}" with following '
                  'configuration:\n{config}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_archive(browser_id, selenium, config, item_name, space_name,
                   oz_page, op_container, tmp_memory, modals, clipboard,
                   displays, option, popups):
    """Create archive according to given config.

    Config format given in yaml is as follows:

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
                    displays, option, popups)


@wt(parsers.parse('user of {browser_id} {option} to create archive for item '
                  '"{item_name}" in "{space_name}" with following '
                  'configuration and follow symbolic links set as'
                  ' {follow_symbolic_links}:\n{config}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_archive_with_follow_symbolic_link(browser_id, selenium, config,
                                             item_name, space_name, oz_page,
                                             op_container, tmp_memory, modals,
                                             clipboard, displays, option,
                                             popups, follow_symbolic_links):
    follow_symbolic_links = follow_symbolic_links == 'true'

    _create_archive(browser_id, selenium, config, item_name, space_name,
                    oz_page, op_container, tmp_memory, modals, clipboard,
                    displays, option, popups, follow_symbolic_links)


def _create_archive(browser_id, selenium, config, item_name, space_name,
                    oz_page, op_container, tmp_memory, modals, clipboard,
                    displays, option, popups, follow_symbolic_links=True):
    option_in_data_row_menu = 'Create archive'
    button_name = 'Create'
    option_state = 'disabled'
    try:
        op_container(selenium[browser_id]).dataset_browser.breadcrumbs
    except RuntimeError:
        click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                      space_name,
                                                      OPTION_IN_SPACE, oz_page)
        assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                    tmp_memory, DATASET_BROWSER)

    if '/' in item_name:
        go_to_path_without_last_elem(selenium, browser_id, tmp_memory,
                                     item_name, op_container, DATASET_BROWSER)
        item_name = item_name.split('/')[-1]
    click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory,
                                   DATASET_BROWSER)
    if option == 'succeeds' or option == 'tries':
        click_option_in_data_row_menu_in_browser(selenium, browser_id,
                                                 option_in_data_row_menu,
                                                 popups, DATASET_BROWSER)
        data = yaml.load(config, yaml.Loader)

        description = data.get('description', False)
        layout = data['layout']
        create_nested_archives = data.get('create nested archives', False)
        incremental = data.get('incremental', False)
        include_dip = data.get('include DIP', False)
        if follow_symbolic_links:
            follow_symbolic_links = data.get('follow symbolic links', True)

        if description:
            write_description_in_create_archive_modal(selenium, browser_id,
                                                      modals, description)
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
                check_toggle_in_create_archive_modal(browser_id, selenium,
                                                     modals, option)
        if include_dip:
            option = 'include_dip'
            check_toggle_in_create_archive_modal(browser_id, selenium, modals,
                                                 option)
        if not follow_symbolic_links:
            option = 'follow_symbolic_links'
            check_toggle_in_create_archive_modal(browser_id, selenium, modals,
                                                 option)
        click_modal_button(selenium, browser_id, button_name,
                           option_in_data_row_menu, modals)
        client = 'web GUI'
        if description:
            copy_archive_id_to_tmp_memory(selenium, browser_id, op_container,
                                          client, tmp_memory, popups, clipboard,
                                          displays, description)
            # wait for "archive id copied to clipboard" message to disappear
            time.sleep(5)
    elif option == 'fails':
        assert_option_state_in_data_row_menu(selenium, browser_id,
                                             option_in_data_row_menu, popups,
                                             option_state, DATASET_BROWSER)


@repeat_failed(timeout=WAIT_BACKEND)
def copy_archive_id_to_tmp_memory(selenium, browser_id, op_container, client,
                                  tmp_memory, popups, clipboard, displays,
                                  description):
    if client.lower() == 'web gui':
        option_in_menu = 'Copy archive ID'
        assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                    tmp_memory, ARCHIVE_BROWSER)
        click_menu_for_archive(browser_id, tmp_memory, description, popups,
                               selenium)
        click_option_in_data_row_menu_in_browser(selenium, browser_id,
                                                 option_in_menu, popups,
                                                 ARCHIVE_BROWSER)
        tmp_memory[description] = clipboard.paste(
            display=displays[browser_id])


def assert_archive_in_op_gui(browser_id, selenium, item_name, space_name,
                             oz_page, op_container, tmp_memory, option,
                             description):
    go_to_and_assert_browser(selenium, browser_id, oz_page, space_name,
                             OPTION_IN_SPACE, op_container, tmp_memory,
                             item_browser=DATASET_BROWSER)
    if '/' in item_name:
        item_name = get_item_name_from_path(selenium, browser_id, space_name,
                                            oz_page, op_container, tmp_memory,
                                            item_name, OPTION_IN_SPACE,
                                            DATASET_BROWSER)

    if option == 'sees':
        click_on_dataset(browser_id, tmp_memory, item_name)
        assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                    tmp_memory, item_browser=ARCHIVE_BROWSER)
        click_and_press_enter_on_archive(browser_id, tmp_memory, description)
        assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                    tmp_memory,
                                    item_browser=ARCHIVE_FILE_BROWSER)
        assert_items_presence_in_browser(selenium, browser_id, item_name,
                                         tmp_memory,
                                         which_browser=ARCHIVE_FILE_BROWSER)
    else:
        try:
            number = '0'
            assert_number_of_archives_for_item_in_dataset_browser(browser_id,
                                                                  item_name,
                                                                  number,
                                                                  tmp_memory)
        except AssertionError:
            click_on_dataset(browser_id, tmp_memory, item_name)
            assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                        tmp_memory,
                                        item_browser=ARCHIVE_BROWSER)
            assert_not_archive_with_description(tmp_memory, browser_id,
                                                description)


def remove_archive_in_op_gui(browser_id, selenium, item_name, space_name,
                             oz_page, op_container, tmp_memory, modals,
                             description, option, popups):
    option_in_menu = 'Delete archive'
    text = 'I understand that data of the archive will be lost'
    button_name = 'Delete archive'
    option_state = 'disabled'
    go_to_and_assert_browser(selenium, browser_id, oz_page, space_name,
                             OPTION_IN_SPACE, op_container, tmp_memory,
                             item_browser=DATASET_BROWSER)
    click_on_dataset(browser_id, tmp_memory, item_name)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory, item_browser=ARCHIVE_BROWSER)
    click_menu_for_archive(browser_id, tmp_memory, description, popups,
                           selenium)

    if option == 'succeeds':
        click_option_in_data_row_menu_in_browser(selenium, browser_id,
                                                 option_in_menu, popups,
                                                 which_browser=ARCHIVE_BROWSER)
        write_in_confirmation_input(browser_id, modals, text, selenium)
        click_modal_button(selenium, browser_id, button_name,
                           option_in_menu, modals)
    elif option == 'fails':
        assert_option_state_in_data_row_menu(selenium, browser_id,
                                             button_name, popups,
                                             option_state, ARCHIVE_BROWSER)


def assert_archive_with_option_in_op_gui(browser_id, selenium, oz_page,
                                         space_name, op_container, tmp_memory,
                                         item_name, option, description):
    tag_type = transform(option)
    go_to_and_assert_browser(selenium, browser_id, oz_page, space_name,
                             OPTION_IN_SPACE, op_container, tmp_memory,
                             item_browser=DATASET_BROWSER)
    click_on_dataset(browser_id, tmp_memory, item_name)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory, item_browser=ARCHIVE_BROWSER)
    assert_tag_for_archive_in_archive_browser(browser_id, tag_type, tmp_memory,
                                              description)


def assert_number_of_archive_in_op_gui(browser_id, selenium, item_name,
                                       space_name, oz_page, op_container,
                                       tmp_memory, number):
    go_to_and_assert_browser(selenium, browser_id, oz_page, space_name,
                             OPTION_IN_SPACE, op_container, tmp_memory,
                             item_browser=DATASET_BROWSER)
    if '/' in item_name:
        item_name = get_item_name_from_path(selenium, browser_id, space_name,
                                            oz_page, op_container, tmp_memory,
                                            item_name, OPTION_IN_SPACE,
                                            DATASET_BROWSER)
    assert_number_of_archives_for_item_in_dataset_browser(browser_id, item_name,
                                                          number, tmp_memory)


def assert_base_archive_for_archive_in_op_gui(browser_id, selenium, item_name,
                                              space_name, oz_page, op_container,
                                              tmp_memory, description,
                                              base_description):
    go_to_and_assert_browser(selenium, browser_id, oz_page, space_name,
                             OPTION_IN_SPACE, op_container, tmp_memory,
                             item_browser=DATASET_BROWSER)
    click_on_dataset(browser_id, tmp_memory, item_name)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory, item_browser=ARCHIVE_BROWSER)
    browser = tmp_memory[browser_id]['archive_browser']
    archive = get_archive_with_description(browser, description)
    err_msg = (f'Base archive: {archive.base_archive} does not match expected '
               f'archive with description {base_description}')
    assert base_description in archive.base_archive_description, err_msg


def assert_archive_callback_in_op_gui(browser_id, tmp_memory, description,
                                      selenium, popups, modals, expected,
                                      option):
    modal = 'Archive Details'
    option_in_menu = 'Properties'
    info = f'{option} callback URL'
    button_name = 'X'
    click_menu_for_archive(browser_id, tmp_memory, description, popups,
                           selenium)
    click_option_in_data_row_menu_in_browser(selenium, browser_id,
                                             option_in_menu, popups,
                                             ARCHIVE_BROWSER)
    assert_archive_info_in_properties_modal(selenium, browser_id, modals,
                                            expected, info)
    click_modal_button(selenium, browser_id, button_name, modal, modals)


def recall_archive_for_archive_in_op_gui(browser_id, description, tmp_memory,
                                         popups, selenium, modals, name):
    option_in_menu = 'Recall to...'
    modal_name = 'Recall archive'
    name_textfield = 'target name input'
    button_name = 'Recall'
    click_menu_for_archive(browser_id, tmp_memory, description, popups,
                           selenium)
    click_option_in_data_row_menu_in_browser(selenium, browser_id,
                                             option_in_menu, popups,
                                             ARCHIVE_BROWSER)
    write_name_into_text_field_in_modal(selenium, browser_id, name, modal_name,
                                        modals, name_textfield)
    click_modal_button(selenium, browser_id, button_name, modal_name, modals)


@repeat_failed(timeout=WAIT_FRONTEND)
def recalled_archive_details_in_op_gui(browser_id, item_name, tmp_memory,
                                       data, modals, selenium):
    status_type = 'recalled'
    click_on_status_tag_for_file_in_file_browser(browser_id, status_type,
                                                 item_name, tmp_memory)
    recall_modal = modals(selenium[browser_id]).archive_recall_information

    for key, expected_value in data.items():
        if key == 'time':
            expected_value = expected_value.split(' >= ')
            start = expected_value[-1]
            stop = expected_value[0]
            if 'cancelled' in expected_value:
                cancelled = expected_value[1]
                assert_recall_duration_in_archive_recall_information_modal(
                    selenium, browser_id, modals, start, cancelled)
                assert_recall_duration_in_archive_recall_information_modal(
                    selenium, browser_id, modals, cancelled, stop)
            assert_recall_duration_in_archive_recall_information_modal(
                selenium, browser_id, modals, start, stop)
        else:
            value = re.sub(r'\s*', '', getattr(recall_modal, key))
            expected_value = re.sub(r'\s*', '', expected_value)
            err_msg = (f'{key} for archive recall "{item_name}" is {value} '
                       f'but expected value is {expected_value} ')
            if expected_value == 'Cancelled':
                assert expected_value in value, err_msg
            elif '<=' in expected_value:
                characters = "[\nMBGi ]"
                err_msg = (f'{key} for archive recall "{item_name}" is {value} '
                           f'and is not lower or equal to expected value: '
                           f'{expected_value} ')
                value = int(re.sub(characters, "", value).split('/')[0])
                expected_value = int(re.sub(characters, "",
                                            expected_value).split('<=')[-1])
                assert value <= expected_value, err_msg
            else:
                assert value == expected_value, err_msg


@wt(parsers.parse('user of {browser_id} sees that current size statistics are '
                  'as follow:\n{config}'))
def check_size_stats_for_archive(selenium, modals, browser_id, config):
    """ Check size stats in directory details according to given config.

            Config format given in yaml is as follows:

                logical size: storage_type
                total physical size: total_physical_size
                contain counter: contain_counter
        """

    size_statistics = yaml.load(config, yaml.Loader)
    for stat_type, expected_value in size_statistics.items():
        check_size_statistic_in_dir_details(selenium, modals, browser_id,
                                            stat_type, expected_value)


@wt(parsers.parse('user of {browser_id} sees that size statistics for '
                  '{provider} are as follow:\n{config}'))
def check_size_stats_for_archive_per_provider(selenium, modals, browser_id,
                                              hosts, config, provider):
    """ Check size stats in directory details for specified provider according
        to given config.

            Config format given in yaml is as follows:

                logical size: storage_type
                physical size: physical_size
                content: content
        """

    size_statistics = yaml.load(config, yaml.Loader)
    for stat_type, expected_value in size_statistics.items():
        check_size_stats_for_provider(selenium, hosts, modals, browser_id,
                                      stat_type, provider, expected_value)
