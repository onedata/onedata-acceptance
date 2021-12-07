"""Meta steps for operations in data tab in Oneprovider
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import yaml

from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException)

from tests.gui.steps.oneprovider.file_browser import *
from tests.gui.steps.oneprovider.data_tab import *
from tests.gui.steps.oneprovider.metadata import *
from tests.gui.steps.oneprovider.browser import *
from tests.gui.steps.oneprovider.archives import \
    click_and_press_enter_on_archive
from tests.gui.steps.common.notifies import notify_visible_with_text
from tests.gui.steps.common.url import refresh_site
from tests.gui.meta_steps.oneprovider.common import (
    navigate_to_tab_in_op_using_gui)
from tests.gui.steps.modal import (
    assert_error_modal_with_text_appeared, wt_wait_for_modal_to_appear,
    write_name_into_text_field_in_modal, close_modal)
from tests.gui.steps.onezone.spaces import (
    click_on_option_of_space_on_left_sidebar_menu,
    click_element_on_lists_on_left_sidebar_menu, click_on_option_in_the_sidebar)
from tests.gui.steps.rest.env_up.spaces import init_storage


def _click_menu_for_elem_somewhere_in_file_browser(selenium, browser_id, path,
                                                   space, tmp_memory, oz_page,
                                                   op_container):
    item_name, _ = get_item_name_and_containing_dir_path(path)

    try:
        go_to_path_without_last_elem(selenium, browser_id, tmp_memory,
                                     path, op_container)
        click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory)
    except (KeyError, StaleElementReferenceException):
        go_to_filebrowser(selenium, browser_id, oz_page, op_container,
                          tmp_memory, space)
        go_to_path_without_last_elem(selenium, browser_id, tmp_memory,
                                     path, op_container)
        click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory)


@wt(parsers.re(r'user of (?P<browser_id>\w+) (?P<res>.*) to rename '
               '"(?P<path>.*)" to "(?P<new_path>.*)" in "(?P<space>.*)"'))
def rename_item(selenium, browser_id, path, new_path, tmp_memory, res, space,
                modals, oz_page, op_container):
    option = 'Rename'
    modal_header = 'Rename'
    modal_name = 'Rename modal'
    confirmation_option = 'button'
    text = 'Renaming the file failed'
    new_name = new_path.split('/')[-1]

    open_modal_for_file_browser_item(selenium, browser_id, modals, modal_header,
                                     path, tmp_memory, option, space, oz_page,
                                     op_container)
    write_name_into_text_field_in_modal(selenium, browser_id, new_name,
                                        modal_name, modals)
    confirm_rename_directory(selenium, browser_id, confirmation_option, modals)
    if res == 'fails':
        assert_error_modal_with_text_appeared(selenium, browser_id, text)
    else:
        assert_items_presence_in_browser(browser_id, new_name, tmp_memory)


@wt(parsers.re(r'user of (?P<browser_id>\w+) (?P<res>.*) to remove '
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
        assert_items_absence_in_browser(browser_id, path, tmp_memory)


def remove_dir_and_parents_in_op_gui(selenium, browser_id, path, tmp_memory,
                                     op_container, res, space, modals, oz_page):
    item_name = _select_item(selenium, browser_id, tmp_memory, path,
                             op_container)
    remove_item_in_op_gui(selenium, browser_id, item_name, tmp_memory,
                          op_container, res, space, modals, oz_page)


@wt(parsers.re(r'using web gui, (?P<browser_id>\w+) (?P<res>.*) to see item '
               'named "(?P<subfiles>.*)" in "(?P<path>.*)" in space'
               '"(?P<space>.*)" in oneprovider-1'))
@wt(parsers.re(r'user of (?P<browser_id>\w+) (?P<res>.*) to see '
               '(?P<subfiles>.*) in "(?P<path>.*)" in "(?P<space>.*)"'))
def see_items_in_op_gui(selenium, browser_id, path, subfiles, tmp_memory,
                        op_container, res, space, oz_page):
    selenium[browser_id].refresh()

    try:
        assert_browser_in_tab_in_op(selenium, browser_id,
                                    op_container, tmp_memory)
    except NoSuchElementException:
        go_to_filebrowser(selenium, browser_id, oz_page, op_container,
                          tmp_memory, space)

    if path:
        for item in path.split('/'):
            click_and_press_enter_on_item_in_browser(selenium, browser_id, item,
                                                     tmp_memory, op_container)

    if res == 'fails':
        assert_items_absence_in_browser(browser_id, subfiles, tmp_memory)
    else:
        assert_items_presence_in_browser(browser_id, subfiles, tmp_memory)


@wt(parsers.re(r'user of (?P<browser_id>\w+) (?P<res>.*) to create '
               r'(?P<item_type>directory) "(?P<name>[\w._-]+)" '
               '(in "(?P<path>.*)" )?in "(?P<space>.*)"'))
def create_item_in_op_gui(selenium, browser_id, path, item_type, name,
                          tmp_memory, op_container, res, space,
                          modals, oz_page):
    # change None to empty string if path not given
    path = path.lstrip('/') if path else ''
    button = f'New {item_type}'
    modal_header = f'Create new {item_type}:'
    modal_name = 'Create dir'
    text = 'Creating directory failed'
    option = 'enter'

    def _open_menu_for_item_in_file_browser():
        if path:
            go_to_path(selenium, browser_id, tmp_memory, path, op_container)
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
        assert_items_presence_in_browser(browser_id, name, tmp_memory)


@wt(parsers.re(r'user of (?P<browser_id>\w+) sees that the file structure '
               'for archive with description: "(?P<description>.*)" in '
               '(?P<which_browser>.*) is as follow:\n'
               r'(?P<config>(.|\s)*)'))
def check_file_structure_for_archive(browser_id, config, selenium, tmp_memory,
                                     op_container, tmpdir, description,
                                     which_browser='file browser'):
    subtree = yaml.load(config)
    _check_files_tree(subtree, browser_id, tmp_memory, '', selenium,
                      op_container, tmpdir, which_browser, description)


@wt(parsers.re(r'user of (?P<browser_id>\w+) sees that the file structure in '
               '(?P<which_browser>.*) is as follow:\n'
               r'(?P<config>(.|\s)*)'))
def check_file_structure_in_browser(browser_id, config, selenium, tmp_memory,
                                    op_container, tmpdir,
                                    which_browser='file browser'):
    subtree = yaml.load(config)
    _check_files_tree(subtree, browser_id, tmp_memory, '', selenium,
                      op_container, tmpdir, which_browser)


def _check_files_tree(subtree, user, tmp_memory, cwd, selenium, op_container,
                      tmpdir, which_browser='file browser', description=''):
    for item in subtree:
        try:
            [(item_name, item_subtree)] = item.items()
        except AttributeError:
            assert_items_presence_in_browser(user, item, tmp_memory,
                                             which_browser)
            if item.startswith('dir'):
                click_and_press_enter_on_item_in_browser(selenium, user, item,
                                                         tmp_memory,
                                                         op_container,
                                                         which_browser)
                assert_empty_browser_in_files_tab_in_op(selenium, user,
                                                        op_container,
                                                        tmp_memory,
                                                        which_browser)
                change_cwd_using_breadcrumbs_in_data_tab_in_op(selenium,
                                                               user, cwd,
                                                               op_container,
                                                               which_browser)
        else:
            assert_items_presence_in_browser(user, item_name, tmp_memory,
                                             which_browser)
            click_and_press_enter_on_item_in_browser(selenium, user, item_name,
                                                     tmp_memory, op_container,
                                                     which_browser)
            # if item is directory go deeper
            if (item_name.startswith('dir') or
                    (which_browser == 'archive file browser'
                     and item_name == 'data')):
                if isinstance(item_subtree, int):
                    assert_num_of_files_are_displayed_in_browser(user,
                                                                 item_subtree,
                                                                 tmp_memory,
                                                                 which_browser)
                else:
                    path_tmp = f'{cwd}/{item_name}'
                    _check_files_tree(item_subtree, user, tmp_memory, path_tmp,
                                      selenium, op_container, tmpdir,
                                      which_browser)
                change_cwd_using_breadcrumbs_in_data_tab_in_op(selenium,
                                                               user, cwd,
                                                               op_container,
                                                               which_browser)
                if which_browser == 'archive file browser':
                    click_and_press_enter_on_archive(user, tmp_memory,
                                                     description)
            else:
                has_downloaded_file_content(user, item_name, str(item_subtree),
                                            tmpdir)
    change_cwd_using_breadcrumbs_in_data_tab_in_op(selenium, user, cwd,
                                                   op_container, which_browser)


def assert_space_content_in_op_gui(config, selenium, user, op_container,
                                   tmp_memory, tmpdir, space_name, oz_page,
                                   provider, hosts):
    try:
        assert_browser_in_tab_in_op(selenium, user, op_container,
                                    tmp_memory)
    except (KeyError, NoSuchElementException):
        go_to_filebrowser(selenium, user, oz_page, op_container,
                          tmp_memory, space_name)
    _check_files_tree(yaml.load(config), user, tmp_memory, '', selenium,
                      op_container, tmpdir)


def see_num_of_items_in_path_in_op_gui(selenium, user, tmp_memory, op_container,
                                       path, space, num, oz_page, provider,
                                       hosts, modals):
    tab_name = 'data'

    try:
        assert_browser_in_tab_in_op(selenium, user, op_container,
                                    tmp_memory)
    except KeyError:
        navigate_to_tab_in_op_using_gui(selenium, user, oz_page, provider,
                                        tab_name, hosts, modals)
        _select_item(selenium, user, tmp_memory, path, op_container)
        refresh_site(selenium, user)
        assert_browser_in_tab_in_op(selenium, user, op_container,
                                    tmp_memory)
    assert_num_of_files_are_displayed_in_browser(user, num, tmp_memory)


def assert_file_content_in_op_gui(text, path, space, selenium, user, users,
                                  provider, hosts, oz_page, op_container,
                                  tmp_memory, tmpdir, modals):
    try:
        assert_browser_in_tab_in_op(selenium, user,
                                    op_container, tmp_memory)
        go_to_path_without_last_elem(selenium, user, tmp_memory, path,
                                     op_container)
    except (KeyError, NoSuchElementException):
        go_to_filebrowser(selenium, user, oz_page, op_container,
                          tmp_memory, space)
        go_to_path_without_last_elem(selenium, user, tmp_memory, path,
                                     op_container)
    item_name = _select_item(selenium, user, tmp_memory, path, op_container)
    click_and_press_enter_on_item_in_browser(selenium, user, item_name,
                                             tmp_memory,
                                             op_container)
    has_downloaded_file_content(user, item_name, text, tmpdir)
    change_cwd_using_breadcrumbs_in_data_tab_in_op(selenium, user,
                                                   'home', op_container)


@given(parsers.re('directory structure created by (?P<user>\w+) '
                  'in "(?P<space>.*)" space on (?P<host>.*) as follows:\n'
                  '(?P<config>(.|\s)*)'))
def g_create_directory_structure(user, config, space, host, users, hosts):
    owner = users[user]
    items = yaml.load(config)
    provider_hostname = hosts[host]['hostname']

    init_storage(owner, space, hosts, provider_hostname, users, items)


def create_directory_structure_in_op_gui(selenium, user, op_container, config,
                                         space, tmp_memory, modals, oz_page,
                                         popups):
    items = yaml.load(config)
    cwd = ''

    _create_content(selenium, user, items, cwd, space, tmp_memory,
                    op_container, modals, oz_page, popups)


def _create_item(selenium, browser_id, name, content, cwd, space, tmp_memory,
                 op_container, modals, oz_page, popups):
    item_type = 'directory' if name.startswith('dir') else 'file'
    if item_type == 'directory':
        create_item_in_op_gui(selenium, browser_id, cwd, item_type, name,
                              tmp_memory, op_container, "succeeds", space,
                              modals, oz_page)
    else:
        upload_file_to_op_gui(cwd, selenium, browser_id, space, "succeeds",
                              name, op_container, tmp_memory, oz_page, popups)
    change_cwd_using_breadcrumbs_in_data_tab_in_op(selenium, browser_id,
                                                   'home', op_container)
    if not content:
        return
    cwd += '/' + name
    _create_content(selenium, browser_id, content, cwd, space, tmp_memory,
                    op_container, modals, oz_page, popups)


def _create_content(selenium, browser_id, content, cwd, space, tmp_memory,
                    op_container, modals, oz_page, popups):
    for item in content:
        try:
            [(name, content)] = item.items()
        except AttributeError:
            name = item
            content = None
        _create_item(selenium, browser_id, name, content, cwd, space,
                     tmp_memory, op_container, modals, oz_page, popups)


@wt(parsers.re('user of (?P<browser_id>.*) uploads "(?P<path>.*)" to the '
               'root directory of "(?P<space>.*)"'))
def successfully_upload_file_to_op_gui(path, selenium, browser_id, space,
                                       op_container, tmp_memory, oz_page,
                                       popups):
    go_to_filebrowser(selenium, browser_id, oz_page, op_container, tmp_memory,
                      space)
    upload_file_to_cwd_in_file_browser(selenium, browser_id, path, op_container,
                                       popups)
    assert_items_presence_in_browser(browser_id, path, tmp_memory)


@wt(parsers.re('user of (?P<browser_id>.*) (?P<res>.*) to upload '
               '"(?P<filename>.*)" to "(?P<path>.*)" in "(?P<space>.*)"'))
def upload_file_to_op_gui(path, selenium, browser_id, space, res, filename,
                          op_container, tmp_memory, oz_page, popups):
    try:
        assert_browser_in_tab_in_op(selenium, browser_id,
                                    op_container, tmp_memory)
        go_to_path(selenium, browser_id, tmp_memory, path, op_container)
    except (KeyError, NoSuchElementException):
        go_to_filebrowser(selenium, browser_id, oz_page, op_container,
                          tmp_memory, space)
        go_to_path(selenium, browser_id, tmp_memory, path, op_container)
    if res == 'succeeds':
        upload_file_to_cwd_in_file_browser(selenium, browser_id, filename,
                                           op_container, popups)
        assert_items_presence_in_browser(browser_id, filename, tmp_memory)
    else:
        upload_file_to_cwd_in_file_browser_no_waiting(selenium, browser_id,
                                                      filename, op_container)
        check_error_in_upload_presenter(selenium, browser_id, popups)


@repeat_failed(timeout=WAIT_BACKEND)
def assert_mtime_not_earlier_than_op_gui(path, time, browser_id, tmp_memory,
                                         selenium, op_container):
    assert_nonempty_file_browser_in_files_tab_in_op(selenium, browser_id,
                                                    op_container, tmp_memory,
                                                    item_browser='file browser')
    item_name = _select_item(selenium, browser_id, tmp_memory, path,
                             op_container)
    assert_item_in_file_browser_is_of_mdate(browser_id, item_name, time,
                                            tmp_memory)


def _select_item(selenium, browser_id, tmp_memory, path, op_container):
    item_name, path = get_item_name_and_containing_dir_path(path)
    go_to_path_without_last_elem(selenium, browser_id, tmp_memory, path,
                                 op_container)
    select_files_from_file_list_using_ctrl(browser_id, item_name, tmp_memory)
    return item_name


@wt(parsers.parse('user of {browser_id} goes to "{path}" in {which_browser}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def go_to_path(selenium, browser_id, tmp_memory, path, op_container,
               which_browser='file browser'):
    if '/' in path:
        item_name, path_list = get_item_name_and_containing_dir_path(path)
        path_list.append(item_name)
    else:
        path_list = [path]
    for directory in path_list:
        if directory != '':
            click_and_press_enter_on_item_in_browser(selenium, browser_id,
                                                     directory,
                                                     tmp_memory, op_container,
                                                     which_browser)


def go_to_path_without_last_elem(selenium, browser_id, tmp_memory, path,
                                 op_container, item_browser='file browser'):
    if '/' in path:
        _, path_list = get_item_name_and_containing_dir_path(path)

        for directory in path_list:
            click_and_press_enter_on_item_in_browser(selenium, browser_id,
                                                     directory,
                                                     tmp_memory, op_container,
                                                     item_browser)


def get_item_name_and_containing_dir_path(path):
    path_list = path.strip('\"').split('/')
    item_name = path_list.pop()
    return item_name, path_list


@wt(parsers.parse('user of {browser_id} opens file browser for "{space}" '
                  'space'))
def go_to_filebrowser(selenium, browser_id, oz_page, op_container,
                      tmp_memory, space):
    space_option = 'spaces'
    option_in_menu = 'Data'
    option_in_space_submenu = 'Files'

    click_on_option_in_the_sidebar(selenium, browser_id, option_in_menu,
                                   oz_page)
    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id,
                                                space_option, space, oz_page)
    click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id, space,
                                                  option_in_space_submenu,
                                                  oz_page)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory)


def open_modal_for_file_browser_item(selenium, browser_id, modals, modal_name,
                                     path, tmp_memory, option, space,
                                     oz_page, op_container):
    _click_menu_for_elem_somewhere_in_file_browser(selenium, browser_id, path,
                                                   space, tmp_memory, oz_page,
                                                   op_container)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option,
                                             modals)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)


def check_file_owner(selenium, browser_id, owner, file_name, tmp_memory,
                     modals):
    option = 'Information'
    modal_name = 'File details'

    click_menu_for_elem_in_browser(browser_id, file_name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option,
                                             modals)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    check_file_owner_in_file_details_modal(selenium, browser_id, modals, owner)
    close_modal(selenium, browser_id, modal_name, modals)


@wt(parsers.parse('user of {browser_id} creates hardlink of "{file_name}" '
                  'file in space "{space}" in file browser'))
def create_hardlinks_of_file(selenium, browser_id, file_name, space,
                             tmp_memory, oz_page, op_container, modals):
    option = 'Create hard link'
    button = 'place hard link'

    _create_link_in_file_browser(selenium, browser_id, file_name, space,
                                 tmp_memory, oz_page, op_container, modals,
                                 option, button)


@wt(parsers.parse('user of {browser_id} creates symlink of "{file_name}" '
                  'file in space "{space}" in file browser'))
def create_symlinks_of_file(selenium, browser_id, file_name, space,
                            tmp_memory, oz_page, op_container, modals):
    option = 'Create symbolic link'
    button = 'place symbolic link'

    _create_link_in_file_browser(selenium, browser_id, file_name, space,
                                 tmp_memory, oz_page, op_container, modals,
                                 option, button)


def _create_link_in_file_browser(selenium, browser_id, file_name, space,
                                 tmp_memory, oz_page, op_container, modals,
                                 option, button):
    go_to_filebrowser(selenium, browser_id, oz_page, op_container, tmp_memory,
                      space)
    _click_menu_for_elem_somewhere_in_file_browser(selenium, browser_id,
                                                   file_name, space, tmp_memory,
                                                   oz_page, op_container)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option,
                                             modals)
    click_file_browser_button(browser_id, button, tmp_memory)


@wt(parsers.re(r'using web GUI, (?P<user>\w+) copies "(?P<name>.*)" ID to'
               r' clipboard from "(?P<modal>.*)" modal in space '
               r'"(?P<space>\w+)" in (?P<host>.*)'))
def copy_object_id_to_tmp_memory(tmp_memory, selenium, user, name, space,
                                 oz_page, op_container, modals, modal):
    option = 'Information'
    button = 'File ID'
    if modal == 'Directory Details':
        modal = 'File details'
    _click_menu_for_elem_somewhere_in_file_browser(selenium, user, name,
                                                   space, tmp_memory, oz_page,
                                                   op_container)
    click_option_in_data_row_menu_in_browser(selenium, user, option,
                                             modals)
    click_modal_button(selenium, user, button, modal, modals)
    close_modal(selenium, user, modal, modals)


# TODO: Function just for the needs of scenario "User downloads files from
#  shared directory on single share view in full Onezone interface" working
#  properly (VFS-6383)
@wt(parsers.parse('user of {browser_id} downloads item "{item_name}" by '
                  'clicking and pressing enter and then sees that '
                  'content of downloaded file is equal to: "{content}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_and_press_enter_with_content_check(browser_id, item_name, content,
                                             tmpdir, tmp_memory,
                                             which_browser='file browser'):
    which_browser = transform(which_browser)
    browser = tmp_memory[browser_id][which_browser]
    browser.data[item_name].click_and_enter()

    has_downloaded_file_content(browser_id, item_name, content, tmpdir)
