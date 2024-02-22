"""Steps implementation for permissions GUI tests."""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from selenium.common.exceptions import StaleElementReferenceException

from tests.gui.conftest import WAIT_BACKEND
from tests.gui.steps.modals.details_modal import (assert_tab_in_modal,
                                                  assert_posix_tab_in_panel)
from tests.gui.steps.oneprovider.browser import (
    click_option_in_data_row_menu_in_browser)
from tests.gui.steps.oneprovider.data_tab import \
    choose_option_for_file_from_selection_menu
from tests.gui.steps.oneprovider.permissions import *
from tests.gui.meta_steps.oneprovider.data import (
    assert_browser_in_tab_in_op, choose_option_from_selection_menu,
    _click_menu_for_elem_somewhere_in_file_browser)
from tests.gui.steps.oneprovider.file_browser import (
    select_files_from_file_list_using_ctrl)
from tests.gui.steps.modals.modal import (
    click_modal_button, click_panel_button, assert_there_is_no_button_in_panel,
    check_warning_modal)
from tests.gui.steps.onezone.spaces import (
    click_element_on_lists_on_left_sidebar_menu,
    click_on_option_of_space_on_left_sidebar_menu,
    click_on_option_in_the_sidebar)


def open_permission_modal(selenium, browser_id, path, space, tmp_memory, modals,
                          oz_page, op_container, permission_type, popups):
    option = 'Permissions'
    modal_name = 'Details modal'

    _click_menu_for_elem_somewhere_in_file_browser(selenium, browser_id, path,
                                                   space, tmp_memory, oz_page,
                                                   op_container)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option,
                                             popups)
    assert_tab_in_modal(selenium, browser_id, option, modals, modal_name)

    try:
        select_permission_type(selenium, browser_id, permission_type, modals)
    except RuntimeError as err:
        if permission_type == 'posix':
            assert_posix_tab_in_panel(selenium, browser_id, modals, modal_name)
        else:
            raise err


def _assert_posix_permissions(selenium, browser_id, space, path, perm,
                              oz_page, op_container, tmp_memory,
                              modals, popups):
    modal_name = 'Details modal'
    close_button = 'X'
    open_permission_modal(selenium, browser_id, path, space, tmp_memory, modals,
                          oz_page, op_container, 'posix', popups)
    check_permission(selenium, browser_id, perm, modals)
    click_modal_button(selenium, browser_id, close_button, modal_name, modals)


@repeat_failed(timeout=WAIT_BACKEND)
def assert_posix_permissions_in_op_gui(selenium, browser_id, space, path, perm,
                                       oz_page, op_container, tmp_memory,
                                       modals, popups):
    modal_name = 'Details modal'
    close_button = 'X'
    try:
        click_modal_button(selenium, browser_id, close_button, modal_name,
                           modals)
        _assert_posix_permissions(selenium, browser_id, space, path, perm,
                                  oz_page, op_container, tmp_memory,
                                  modals, popups)
    except (AttributeError, StaleElementReferenceException, RuntimeError):
        _assert_posix_permissions(selenium, browser_id, space, path, perm,
                                  oz_page, op_container, tmp_memory,
                                  modals, popups)


@wt(parsers.re(r'user of (?P<browser_id>\w+) sets (?P<path>.*) POSIX '
               '(?P<perm>.*) privileges in "(?P<space>.*)"'))
def set_posix_permissions_in_op_gui(selenium, browser_id, space, path, perm,
                                    op_container, tmp_memory, modals, oz_page,
                                    popups):
    modal_name = 'Details modal'
    button = 'Save'
    close_button = 'X'
    panel = 'Edit permissions'

    open_permission_modal(selenium, browser_id, path, space, tmp_memory, modals,
                          oz_page, op_container, 'posix', popups)
    set_posix_permission(selenium, browser_id, perm, modals)

    click_panel_button(selenium, browser_id, button, panel, modals)
    click_modal_button(selenium, browser_id, close_button, modal_name, modals)


def fail_to_set_posix_permissions_in_op_gui(selenium, browser_id, space, path,
                                            perm, op_container, tmp_memory,
                                            modals, oz_page, popups):
    button = 'Save'
    panel = 'Edit permissions'
    text = 'Modifying permissions failed'
    details_modal = 'Details modal'
    x_button = 'X'

    open_permission_modal(selenium, browser_id, path, space, tmp_memory, modals,
                          oz_page, op_container, 'posix', popups)
    fail_to_set_posix_permission(selenium, browser_id, perm, modals)
    assert_there_is_no_button_in_panel(selenium, browser_id, button, panel,
                                       modals)
    click_modal_button(selenium, browser_id, x_button, details_modal,
                       modals)


@wt(parsers.re(r'user of (?P<browser_id>\w+) adds ACE with (?P<priv>.*) '
               r'privileges? set for (?P<type>.*?) (?P<name>.*)'))
def set_acl_entry_in_op_gui(selenium, browser_id, priv, name, modals, popups):
    permission_type = 'acl'

    select_permission_type(selenium, browser_id, permission_type, modals)
    select_acl_subject(selenium, browser_id, name, modals, popups)
    expand_subject_record_in_edit_permissions_modal(selenium, browser_id,
                                                    modals, name)
    select_acl_options(selenium, browser_id, priv, modals, name)
    click_on_record_header_in_edit_permissions_modal(selenium, browser_id,
                                                     modals, name)


def _set_acl_privilages_for_selected(browser_id, selenium, popups, tmp_memory,
                                     priv, name, modals, path=None):
    option = 'Permissions'
    modal_name = 'Details modal'
    button = 'Save'
    close_button = 'X'
    panel = 'Edit permissions'
    warning_modal = 'warning'
    proceed_button = 'proceed'
    path = parse_seq(path)

    if path and len(path) == 1:
        choose_option_for_file_from_selection_menu(browser_id, selenium, option,
                                                   popups, tmp_memory,
                                                   path[0])
    else:
        choose_option_from_selection_menu(browser_id, selenium, option, popups,
                                          tmp_memory)
    assert_tab_in_modal(selenium, browser_id, option, modals, modal_name)

    set_acl_entry_in_op_gui(selenium, browser_id, priv, name, modals, popups)
    click_panel_button(selenium, browser_id, button, panel, modals)
    if check_warning_modal(selenium, browser_id):
        click_modal_button(selenium, browser_id, proceed_button, warning_modal
                           , modals)
    click_modal_button(selenium, browser_id, close_button, modal_name, modals)


@wt(parsers.re(r'user of (?P<browser_id>\w+) sets "(?P<item_name>.*)" '
               '(directory|file) ACL (?P<priv>.*) privileges for'
               ' (?P<type>.*) (?P<name>.*)'))
def grant_acl_privileges_to_selected_in_filebrowser(
        selenium, browser_id, priv, name, op_container, tmp_memory, popups,
        oz_page, modals, item_name):
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory)
    _set_acl_privilages_for_selected(browser_id, selenium, popups, tmp_memory,
                                     priv, name, modals, item_name)


@wt(parsers.re(r'user of (?P<browser_id>\w+) sets (?P<item_list>.*) ACL '
               '(?P<priv>.*) privileges for (?P<type>.*) (?P<name>.*) '
               'in "(?P<space>.*)"'))
def grant_acl_privileges_in_op_gui(selenium, browser_id, item_list, priv, name,
                                   op_container, tmp_memory, popups, space,
                                   oz_page, modals):
    option_in_menu = 'Data'
    option = 'spaces'
    option_in_submenu = 'Files'
    path = item_list.replace('"', '')

    click_on_option_in_the_sidebar(selenium, browser_id, option_in_menu,
                                   oz_page)
    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id, option,
                                                space, oz_page)
    click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id, space,
                                                  option_in_submenu, oz_page)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory)
    select_files_from_file_list_using_ctrl(browser_id, path, tmp_memory)
    _set_acl_privilages_for_selected(browser_id, selenium, popups, tmp_memory,
                                     priv, name, modals, path)


@wt(parsers.re(r'user of (?P<browser_id>\w+) (?P<res>.*) to read "(?P<path>.*)"'
               ' ACL in "(?P<space>.*)"'))
def read_items_acl(selenium, browser_id, path, tmp_memory, res, space, modals,
                   oz_page, op_container, popups):
    modal_name = 'Details modal'
    close_button = 'X'
    open_permission_modal(selenium, browser_id, path, space, tmp_memory, modals,
                          oz_page, op_container, 'acl', popups)

    if res == "fails":
        check_permission_denied_alert_in_edit_permissions_modal(selenium,
                                                                browser_id,
                                                                modals)
    else:
        check_permissions_list_in_edit_permissions_modal(selenium, browser_id,
                                                         modals)

    click_modal_button(selenium, browser_id, close_button, modal_name, modals)


@wt(parsers.re(r'user of (?P<browser_id>\w+) sees that (?P<path>.*?) in space '
               r'"(?P<space>\w+)" (has|have) (?P<priv>.*) privileges? set for '
               '(?P<type>.*?) (?P<name>.*) in (?P<num>.*) ACL record'))
def assert_ace_in_op_gui(selenium, browser_id, priv, type, name, num, space,
                         path, tmp_memory, modals, numerals, oz_page,
                         op_container, popups):
    modal_name = 'Details modal'
    close_button = 'X'
    open_permission_modal(selenium, browser_id, path, space, tmp_memory, modals,
                          oz_page, op_container, 'acl', popups)
    if type != 'unknown':
        assert_acl_subject(selenium, browser_id, modals, num, numerals,
                           type, name)
    assert_set_acl_privileges(selenium, browser_id, modals, num, numerals, priv)
    click_modal_button(selenium, browser_id, close_button, modal_name, modals)


@wt(parsers.re(r'user of (?P<browser_id>\w+) sees that (?P<path>.*?) in space '
               r'"(?P<space>\w+)" contains id of user "(?P<name>.*)" in '
               r'(?P<num>.*) ACL record'))
def assert_user_id_in_ace_in_op_gui(
        selenium, browser_id, name, num, space, path, tmp_memory, modals,
        numerals, oz_page, op_container, popups, users):
    modal_name = 'Details modal'
    close_button = 'X'
    open_permission_modal(selenium, browser_id, path, space, tmp_memory, modals,
                          oz_page, op_container, 'acl', popups)
    visible_id = get_unknown_user_id_from_acl_entry(selenium, browser_id,
                                                    modals, num, numerals)
    user_id = users[name]._user_id
    err_msg = (f'id in acl entry: {visible_id} differs from actual '
               f'user id: {user_id}')
    assert visible_id == user_id, err_msg
    click_modal_button(selenium, browser_id, close_button, modal_name, modals)


@wt(parsers.re(r'user of (?P<browser_id>\w+) (?P<res>.*) to change '
               '"(?P<path>.*)" ACL for (?P<name>.*) in "(?P<space>.*)"'))
def change_acl_privileges(selenium, browser_id, path, tmp_memory, res, space,
                          modals, op_container, oz_page, name, popups):
    privileges_option_list = (
        '[attributes]' if res == 'succeeds' else '[acl:change acl]')
    button = 'Save'
    panel = 'Edit permissions'

    open_permission_modal(selenium, browser_id, path, space, tmp_memory, modals,
                          oz_page, op_container, 'acl', popups)
    expand_subject_record_in_edit_permissions_modal(selenium, browser_id,
                                                    modals, name)

    if res == 'fails':
        assert_fail_to_select_acl_option(selenium, browser_id,
                                         privileges_option_list, modals, name)

    else:
        select_acl_options(selenium, browser_id, privileges_option_list, modals,
                           name)
        click_panel_button(selenium, browser_id, button, panel, modals)
        open_permission_modal(selenium, browser_id, path, space, tmp_memory,
                              modals, oz_page, op_container, 'acl', popups)
        check_permissions_list_in_edit_permissions_modal(selenium, browser_id,
                                                         modals)
