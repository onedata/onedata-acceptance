"""Steps implementation for permissions GUI tests."""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.steps.oneprovider.permissions import *
from tests.gui.meta_steps.oneprovider.data import (
    assert_file_browser_in_data_tab_in_op, choose_option_from_selection_menu,
    _click_menu_for_elem_somewhere_in_file_browser,
    open_modal_for_file_browser_item)
from tests.gui.steps.oneprovider.file_browser import (
    click_option_in_data_row_menu_in_file_browser,
    select_files_from_file_list_using_ctrl)
from tests.gui.steps.modal import (
    wt_wait_for_modal_to_appear, wt_click_on_confirmation_btn_in_modal,
    assert_error_modal_with_text_appeared)
from tests.gui.steps.common.url import refresh_site
from tests.gui.steps.onezone.spaces import (
    click_element_on_lists_on_left_sidebar_menu,
    click_on_option_of_space_on_left_sidebar_menu)


def open_permission_modal(selenium, browser_id, path, space, tmp_memory, modals,
                          oz_page, op_container, permission_type):
    option = 'Permissions'
    modal_name = 'Edit Permissions'

    open_modal_for_file_browser_item(selenium, browser_id, modals, modal_name,
                                     path, tmp_memory, option, space,
                                     oz_page, op_container)

    select_permission_type(selenium, browser_id, permission_type, modals)


def assert_posix_permissions_in_op_gui(selenium, browser_id, space, path, perm,
                                       oz_page, op_container, tmp_memory,
                                       modals):
    refresh_site(selenium, browser_id)
    open_permission_modal(selenium, browser_id, path, space, tmp_memory, modals,
                          oz_page, op_container, 'posix')
    check_permission(selenium, browser_id, perm, modals)


@wt(parsers.re(r'user of (?P<browser_id>\w+) sets (?P<path>.*) POSIX '
               '(?P<perm>.*) privileges in "(?P<space>.*)"'))
def set_posix_permissions_in_op_gui(selenium, browser_id, space, path, perm,
                                    op_container, tmp_memory, modals, oz_page):
    open_permission_modal(selenium, browser_id, path, space, tmp_memory, modals,
                          oz_page, op_container, 'posix')
    set_posix_permission(selenium, browser_id, perm, modals)
    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, 'Save',
                                          tmp_memory)


@when(parsers.re('user of (?P<browser_id>\w+) adds ACE with (?P<priv>.*) '
                 'privileges? set for (?P<type>.*?) (?P<name>.*)'))
def set_acl_entry_in_op_gui(selenium, browser_id, priv, name, modals):
    permission_type = 'acl'

    select_permission_type(selenium, browser_id, permission_type, modals)
    select_acl_subject(selenium, browser_id, name, modals)
    expand_subject_record_in_edit_permissions_modal(selenium, browser_id,
                                                    modals, name)
    select_acl_options(selenium, browser_id, priv, modals, name)


def _set_acl_privilages_for_selected(browser_id, selenium, popups, tmp_memory,
                                     priv, name, modals):
    option = 'Permissions'
    modal_name = 'Edit permissions'

    choose_option_from_selection_menu(browser_id, selenium, option, popups,
                                      tmp_memory)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)

    set_acl_entry_in_op_gui(selenium, browser_id, priv, name, modals)
    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, 'Save',
                                          tmp_memory)


@when(parsers.re('user of (?P<browser_id>\w+) sets selected items ACL '
                 '(?P<priv>.*) privileges for (?P<type>.*) (?P<name>.*)'))
def grant_acl_privileges_to_selected_in_filebrowser(selenium, browser_id, priv,
                                                    name, op_container,
                                                    tmp_memory, popups, oz_page,
                                                    modals):
    assert_file_browser_in_data_tab_in_op(selenium, browser_id, op_container,
                                          tmp_memory)
    _set_acl_privilages_for_selected(browser_id, selenium, popups, tmp_memory,
                                     priv, name, modals)


@when(parsers.re('user of (?P<browser_id>\w+) sets (?P<item_list>.*) ACL '
                 '(?P<priv>.*) privileges for (?P<type>.*) (?P<name>.*) '
                 'in "(?P<space>.*)"'))
def grant_acl_privileges_in_op_gui(selenium, browser_id, item_list, priv, name,
                                   op_container, tmp_memory, popups, space,
                                   oz_page, modals):
    option = 'spaces'
    option_in_submenu = 'Data'
    path = item_list.replace('"', '')

    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id, option,
                                                space, oz_page)
    click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id, space,
                                                  option_in_submenu, oz_page)
    assert_file_browser_in_data_tab_in_op(selenium, browser_id, op_container,
                                          tmp_memory)
    select_files_from_file_list_using_ctrl(browser_id, path, tmp_memory)
    _set_acl_privilages_for_selected(browser_id, selenium, popups, tmp_memory,
                                     priv, name, modals)


@then(
    parsers.re('user of (?P<browser_id>\w+) (?P<res>.*) to read "(?P<path>.*)"'
               ' ACL in "(?P<space>.*)"'))
def read_items_acl(selenium, browser_id, path, tmp_memory, res, space, modals,
                   oz_page, op_container):
    open_permission_modal(selenium, browser_id, path, space, tmp_memory, modals,
                          oz_page, op_container, 'acl')

    if res == "fails":
        check_permission_denied_alert_in_edit_permissions_modal(selenium,
                                                                browser_id,
                                                                modals)
    else:
        check_permissions_list_in_edit_permissions_modal(selenium, browser_id,
                                                         modals)
    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, 'Cancel',
                                          tmp_memory)


@then(parsers.re('user of (?P<browser_id>\w+) sees that (?P<path>.*?) in space '
                 '"(?P<space>\w+)" (has|have) (?P<priv>.*) privileges? set for '
                 '(?P<type>.*?) (?P<name>.*) in (?P<num>.*) ACL record'))
def assert_ace_in_op_gui(selenium, browser_id, priv, type, name, num, space,
                         path, tmp_memory, modals, numerals, oz_page,
                         op_container):
    selenium[browser_id].refresh()
    open_permission_modal(selenium, browser_id, path, space, tmp_memory, modals,
                          oz_page, op_container, 'acl')
    assert_acl_subject(selenium, browser_id, modals, num, numerals, type, name)
    assert_set_acl_privileges(selenium, browser_id, modals, num, numerals, priv)
    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, "Cancel",
                                          tmp_memory)


@then(parsers.re(
    'user of (?P<browser_id>\w+) (?P<res>.*) to change "(?P<path>.*)"'
    ' ACL for (?P<name>.*) in "(?P<space>.*)"'))
def change_acl_privileges(selenium, browser_id, path, tmp_memory, res, space,
                          modals, op_container, oz_page, name):
    privileges_option_list = (
        '[attributes]' if res == 'succeeds' else '[acl:change acl]')
    text = 'Modifying permissions failed'

    open_permission_modal(selenium, browser_id, path, space, tmp_memory, modals,
                          oz_page, op_container, 'acl')
    expand_subject_record_in_edit_permissions_modal(selenium, browser_id,
                                                    modals, name)
    select_acl_options(selenium, browser_id, privileges_option_list, modals,
                       name)
    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, 'Save',
                                          tmp_memory)

    if res == 'fails':
        assert_error_modal_with_text_appeared(selenium, browser_id, text)

    else:
        open_permission_modal(selenium, browser_id, path, space, tmp_memory,
                              modals, oz_page, op_container, 'acl')
        check_permissions_list_in_edit_permissions_modal(selenium, browser_id,
                                                         modals)
