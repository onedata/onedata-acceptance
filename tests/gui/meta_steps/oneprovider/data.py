"""Meta steps for operations in data tab in Oneprovider
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import yaml

from selenium.common.exceptions import NoSuchElementException

from tests.gui.steps.oneprovider.file_browser import *
from tests.gui.steps.oneprovider.data_tab import *
from tests.gui.steps.oneprovider.metadata import *
from tests.gui.steps.common.notifies import notify_visible_with_text
from tests.gui.steps.common.url import refresh_site
from tests.gui.meta_steps.oneprovider.common import (
    navigate_to_tab_in_op_using_gui)
from tests.gui.steps.modal import (
    assert_error_modal_with_text_appeared, wt_wait_for_modal_to_appear,
    write_name_into_text_field_in_modal)
from tests.gui.steps.onezone.spaces import (
    click_on_option_of_space_on_left_sidebar_menu,
    click_element_on_lists_on_left_sidebar_menu)


def _click_menu_for_elem_somewhere_in_file_browser(selenium, browser_id, path,
                                                   space, tmp_memory, oz_page,
                                                   op_container):
    item_name, _ = get_item_name_and_containing_dir_path(path)

    try:
        go_to_path_without_last_elem(browser_id, tmp_memory, path)
        click_menu_for_elem_in_file_browser(browser_id, item_name, tmp_memory)
    except KeyError:
        go_to_filebrowser(selenium, browser_id, oz_page, op_container,
                          tmp_memory, space)
        go_to_path_without_last_elem(browser_id, tmp_memory, path)
        click_menu_for_elem_in_file_browser(browser_id, item_name, tmp_memory)


@then(parsers.re('user of (?P<browser_id>\w+) (?P<res>.*) to rename '
                 '"(?P<path>.*)" to "(?P<new_name>.*)" in "(?P<space>.*)"'))
def rename_item(selenium, browser_id, path, new_name, tmp_memory, res, space,
                modals, oz_page, op_container):
    option = 'Rename'
    modal_header = 'Rename'
    modal_name = 'Rename modal'
    confirmation_option = 'button'
    text = 'Renaming the file failed'

    open_modal_for_file_browser_item(selenium, browser_id, modals, modal_header,
                                     path, tmp_memory, option, space, oz_page,
                                     op_container)
    write_name_into_text_field_in_modal(selenium, browser_id, new_name,
                                        modal_name, modals)
    confirm_rename_directory(selenium, browser_id, confirmation_option, modals)
    if res == 'fails':
        assert_error_modal_with_text_appeared(selenium, browser_id, text)
    else:
        assert_items_presence_in_file_browser(browser_id, new_name, tmp_memory)


@wt(parsers.re('user of (?P<browser_id>\w+) (?P<res>.*) to remove '
               '"(?P<path>.*)" in "(?P<space>.*)"'))
def remove_item_in_op_gui(selenium, browser_id, path, tmp_memory, op_container,
                          res, space, modals, oz_page):
    option = 'Delete'
    button = 'Yes'
    modal = 'Delete modal'
    modal_header = 'Delete'
    text = 'Deleting file(s) failed'

    open_modal_for_file_browser_item(selenium, browser_id, modals, modal_header,
                                     path, tmp_memory, option, space, oz_page,
                                     op_container)
    click_modal_button(selenium, browser_id, button, modal, modals)

    if res == 'fails':
        assert_error_modal_with_text_appeared(selenium, browser_id, text)
    else:
        assert_items_absence_in_file_browser(browser_id, path, tmp_memory)


def remove_dir_and_parents_in_op_gui(selenium, browser_id, path, tmp_memory,
                                     op_container, res, space):
    item_name = _select_item(browser_id, tmp_memory, path)
    remove_item_in_op_gui(selenium, browser_id, item_name, tmp_memory,
                          op_container, res, space)


@then(parsers.re('user of (?P<browser_id>\w+) (?P<res>.*) to see '
                 '(?P<subfiles>.*) in "(?P<path>.*)" in "(?P<space>.*)"'))
def see_items_in_op_gui(selenium, browser_id, path, subfiles, tmp_memory, 
                        op_container, res, space, oz_page):
    selenium[browser_id].refresh()

    try:
        assert_file_browser_in_data_tab_in_op(selenium, browser_id,
                                              op_container, tmp_memory)
    except NoSuchElementException:
        go_to_filebrowser(selenium, browser_id, oz_page, op_container,
                          tmp_memory, space)

    if path:
        double_click_on_item_in_file_browser(browser_id, path, tmp_memory)
    if res == 'fails':
        assert_items_absence_in_file_browser(browser_id, subfiles, tmp_memory)
    else:
        assert_items_presence_in_file_browser(browser_id, subfiles, tmp_memory)


@wt(parsers.re('user of (?P<browser_id>\w+) (?P<res>.*) to create '
               '(?P<item_type>directory) "(?P<name>[\w._-]+)" '
               '(in "(?P<path>.*)" )?in "(?P<space>.*)"'))
def create_item_in_op_gui(selenium, browser_id, path, item_type, name,
                          tmp_memory, op_container, res, space, modals, oz_page):
    # change None to empty string if path not given
    path = path if path else ''

    button = f'New {item_type}'
    modal_header = f'Create new {item_type}:'
    modal_name = 'Create dir'
    text = 'Creating directory failed'
    option = 'enter'

    def _open_menu_for_item_in_file_browser():
        if path:
            double_click_on_item_in_file_browser(browser_id, path, tmp_memory)
        click_button_from_file_browser_menu_bar(selenium, browser_id,
                                                button, op_container)

    try:
        _open_menu_for_item_in_file_browser()
    except (RuntimeError, KeyError) as e:
        go_to_filebrowser(selenium, browser_id, oz_page, op_container,
                          tmp_memory, space)
        _open_menu_for_item_in_file_browser()

    wt_wait_for_modal_to_appear(selenium, browser_id, modal_header, tmp_memory)
    write_name_into_text_field_in_modal(selenium, browser_id, name,
                                        modal_name, modals)
    confirm_create_new_directory(selenium, browser_id, option, modals)
    if res == 'fails':
        assert_error_modal_with_text_appeared(selenium, browser_id, text)
    else:
        assert_items_presence_in_file_browser(browser_id, name, tmp_memory)


def _check_files_tree(subtree, user, tmp_memory, cwd, selenium, op_container,
                      tmpdir):
    for item in subtree:
        try:
            [(item_name, item_subtree)] = item.items()
        except AttributeError:
            assert_items_presence_in_file_browser(user, item, tmp_memory)
            if item.startswith('dir'):
                double_click_on_item_in_file_browser(user, item, tmp_memory)
                assert_empty_file_browser_in_data_tab_in_op(selenium, user,
                                                            op_container,
                                                            tmp_memory)
                change_cwd_using_dir_tree_in_data_tab_in_op(selenium, user,
                                                            cwd, op_container)
        else:
            assert_items_presence_in_file_browser(user, item_name, tmp_memory)
            double_click_on_item_in_file_browser(user, item_name,
                                                 tmp_memory)

            # if item is directory go deeper
            if item_name.startswith('dir'):
                if isinstance(item_subtree, int):
                    assert_num_of_files_are_displayed_in_file_browser(
                        user, item_subtree, tmp_memory)
                else:
                    path = '{}{}/'.format(cwd, item_name)
                    _check_files_tree(item_subtree, user,
                                      tmp_memory, path,
                                      selenium, op_container, tmpdir)
                change_cwd_using_dir_tree_in_data_tab_in_op(selenium, user, cwd,
                                                            op_container)
            else:
                has_downloaded_file_content(user, item_name, str(item_subtree),
                                            tmpdir)
    change_cwd_using_dir_tree_in_data_tab_in_op(selenium, user, cwd,
                                                op_container)


def assert_space_content_in_op_gui(config, selenium, user, op_container,
                                   tmp_memory, tmpdir, space_name, oz_page,
                                   provider, hosts, modals):
    tab_name = 'data'

    navigate_to_tab_in_op_using_gui(selenium, user, oz_page, provider, tab_name,
                                    hosts, modals)
    refresh_site(selenium, user)
    change_space_view_in_data_tab_in_op(selenium, user, space_name,
                                        oz_page)
    assert_file_browser_in_data_tab_in_op(selenium, user, op_container,
                                          tmp_memory)
    _check_files_tree(yaml.load(config), user, tmp_memory, '/', selenium,
                      op_container, tmpdir)


def see_num_of_items_in_path_in_op_gui(selenium, user, tmp_memory, op_container,
                                       path, space, num, oz_page, provider,
                                       hosts, modals):
    tab_name = 'data'

    navigate_to_tab_in_op_using_gui(selenium, user, oz_page, provider, tab_name,
                                    hosts, modals)
    _select_item(user, tmp_memory, path)
    refresh_site(selenium, user)
    assert_file_browser_in_data_tab_in_op(selenium, user, op_container,
                                          tmp_memory)
    assert_num_of_files_are_displayed_in_file_browser(user, num, tmp_memory)


def assert_file_content_in_op_gui(text, path, space, selenium, user, users,
                                  provider, hosts, oz_page, op_container,
                                  tmp_memory, tmpdir, modals):
    tab_name = 'data'

    navigate_to_tab_in_op_using_gui(selenium, user, oz_page, provider, tab_name,
                                    hosts, modals)
    item_name = _select_item(user, tmp_memory, path)
    double_click_on_item_in_file_browser(user, item_name, tmp_memory)
    has_downloaded_file_content(user, item_name, text, tmpdir)


@given(parsers.re('directory structure created by user of (?P<browser_id>\w+) '
                  'in "(?P<space>.*)" space on (?P<host>.*) as follows:\n'
                  '(?P<config>(.|\s)*)'))
def g_create_directory_structure_in_op_gui(selenium, user, op_container, config,
                                           space, tmp_memory):
    create_directory_structure_in_op_gui(selenium, user, op_container, config,
                                         space, tmp_memory)


def create_directory_structure_in_op_gui(selenium, user, op_container, config,
                                         space, tmp_memory):
    items = yaml.load(config)
    cwd = ''
    _create_content(selenium, user, items, cwd, space, tmp_memory, op_container)
    

def _create_item(selenium, browser_id, name, content, cwd, space, tmp_memory,
                 op_container):
    item_type = 'directory' if name.startswith('dir') else 'file'
    create_item_in_op_gui(selenium, browser_id, cwd, item_type, name, 
                          tmp_memory, op_container, "succeeds", space)
    if not content:
        return 
    cwd += '/' + name
    _create_content(selenium, browser_id, content, cwd, space, tmp_memory, 
                    op_container)


def _create_content(selenium, browser_id, content, cwd, space, tmp_memory, 
                    op_container):
    for item in content:
        try:
            [(name, content)] = item.items()
        except AttributeError:
            name = item
            content = None
        _create_item(selenium, browser_id, name, content, cwd, space, 
                     tmp_memory, op_container)


@wt(parsers.re('user of (?P<browser_id>.*) uploads "(?P<path>.*)" to the '
               'root directory of "(?P<space>.*)"'))
def successfully_upload_file_to_op_gui(path, selenium, browser_id, space,
                                       op_container, tmp_memory, oz_page):
    go_to_filebrowser(selenium, browser_id, oz_page, op_container, tmp_memory,
                      space)
    upload_file_to_cwd_in_file_browser(selenium, browser_id, path, op_container)
    assert_items_presence_in_file_browser(browser_id, path, tmp_memory)


@wt(parsers.re('user of (?P<browser_id>.*) (?P<res>.*) to upload '
               '"(?P<filename>.*)" to "(?P<path>.*)" in "(?P<space>.*)"'))
def upload_file_to_op_gui(path, selenium, browser_id, space, res, filename,
                          op_container, tmp_memory, oz_page, popups):
    try:
        go_to_path(browser_id, tmp_memory, path)
    except KeyError:
        go_to_filebrowser(selenium, browser_id, oz_page, op_container,
                          tmp_memory, space)
        go_to_path(browser_id, tmp_memory, path)
    upload_file_to_cwd_in_file_browser(selenium, browser_id, filename,
                                       op_container)
    if res == 'succeeds':
        assert_items_presence_in_file_browser(browser_id, filename, tmp_memory)
    else:
        check_error_in_upload_presenter(selenium, browser_id, popups)


def assert_mtime_not_earlier_than_op_gui(path, time, browser_id, tmp_memory):
    item_name = _select_item(browser_id, tmp_memory, path)
    assert_item_in_file_browser_is_of_mdate(browser_id, item_name, time,
                                            tmp_memory)


def _select_item(browser_id, tmp_memory, path):
    item_name, path = get_item_name_and_containing_dir_path(path)
    go_to_path_without_last_elem(browser_id, tmp_memory, path)
    select_files_from_file_list_using_ctrl(browser_id, item_name, tmp_memory)
    return item_name


def go_to_path(browser_id, tmp_memory, path):
    if '/' in path:
        item_name, path_list = get_item_name_and_containing_dir_path(path)
        path_list.append(item_name)
    else:
        path_list = [path]
    for directory in path_list:
        double_click_on_item_in_file_browser(browser_id, directory, tmp_memory)


def go_to_path_without_last_elem(browser_id, tmp_memory, path):
    if '/' in path:
        _, path_list = get_item_name_and_containing_dir_path(path)
        for directory in path_list:
            double_click_on_item_in_file_browser(browser_id, directory,
                                                 tmp_memory)


def get_item_name_and_containing_dir_path(path):
    path_list = path.strip('\"').split('/')
    item_name = path_list.pop()
    return item_name, path_list


def go_to_filebrowser(selenium, browser_id, oz_page, op_container,
                      tmp_memory, space):
    option_in_menu = 'spaces'
    option_in_submenu = 'Data'

    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id,
                                                option_in_menu, space, oz_page)
    click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id, space,
                                                  option_in_submenu, oz_page)
    assert_file_browser_in_data_tab_in_op(selenium, browser_id, op_container,
                                          tmp_memory)


def open_modal_for_file_browser_item(selenium, browser_id, modals, modal_name,
                                     path, tmp_memory, option, space,
                                     oz_page, op_container):
    _click_menu_for_elem_somewhere_in_file_browser(selenium, browser_id, path,
                                                   space, tmp_memory, oz_page,
                                                   op_container)
    click_option_in_data_row_menu_in_file_browser(selenium, browser_id, option,
                                                  modals)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
