"""Steps implementation for permissions GUI tests."""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.steps.oneprovider.permissions import *
from tests.gui.meta_steps.oneprovider.data import (
    assert_file_browser_in_data_tab_in_op, go_to_filebrowser)
from tests.gui.steps.common.notifies import notify_visible_with_text
from tests.gui.steps.oneprovider.file_browser import (
    click_menu_for_elem_in_file_browser,
    click_option_in_data_row_menu_in_file_browser)
from tests.gui.steps.modal import (wt_wait_for_modal_to_appear,
                                   wt_click_on_confirmation_btn_in_modal,
                                   wt_wait_for_modal_to_disappear)
from tests.gui.steps.common.url import refresh_site
from tests.gui.steps.onezone.groups import assert_error_modal_with_text_appeared
from tests.gui.steps.onezone.spaces import (
    click_element_on_lists_on_left_sidebar_menu,
    click_on_option_of_space_on_left_sidebar_menu)


def open_permission_modal(selenium, browser_id, path, tmp_memory, modals):
    option = 'Permissions'
    modal_name = 'Edit Permissions'

    click_menu_for_elem_in_file_browser(selenium, browser_id, path,
                                        tmp_memory)
    click_option_in_data_row_menu_in_file_browser(selenium, browser_id,
                                                  option, modals)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)


def open_acl_modal(selenium, browser_id, path, tmp_memory, modals, oz_page,
                   op_page, space):
    try:
        open_permission_modal(selenium, browser_id, path, tmp_memory, modals)
    except KeyError:
        go_to_filebrowser(selenium, browser_id, oz_page, op_page,
                          tmp_memory, space)
        open_permission_modal(selenium, browser_id, path, tmp_memory, modals)

    select_permission_type(selenium, browser_id, 'acl', modals)


def open_posix_modal(selenium, browser_id, path, tmp_memory, modals):
    open_permission_modal(selenium, browser_id, path, tmp_memory, modals)
    select_permission_type(selenium, browser_id, '[posix]', modals)


def assert_posix_permissions_in_op_gui(selenium, browser_id, space, path, perm,
                                       op_page, tmp_memory, modals):
    refresh_site(selenium, browser_id)
    open_posix_modal(selenium, browser_id, path, tmp_memory, modals)
    check_permission(selenium, browser_id, perm, modals)


def set_posix_permissions_in_op_gui(selenium, browser_id, space, path, perm,
                                    result, op_page, tmp_memory, modals):
    open_posix_modal(selenium, browser_id, path, tmp_memory, modals)
    set_permission(selenium, browser_id, perm, modals)
    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, 'Ok',
                                          tmp_memory)
    if result == 'fails':
        notify_visible_with_text(selenium, browser_id, 'error', '.*failed.*')
        wt_click_on_confirmation_btn_in_modal(selenium, browser_id, 'Cancel',
                                              tmp_memory)
    wt_wait_for_modal_to_disappear(selenium, browser_id, tmp_memory)


@when(parsers.re('user of (?P<browser_id>\w+) adds ACE with (?P<priv>.*)'
                 ' privileges? set for (?P<type>.*?) (?P<name>.*)'))
def set_acl_entry_in_op_gui(selenium, browser_id, priv, name, modals):
    permission_typ = 'acl'

    select_permission_type(selenium, browser_id, permission_typ, modals)
    select_acl_subject(selenium, browser_id, name, modals)
    expand_subject_record_in_edit_permissions_modal(selenium, browser_id,
                                                    modals, name)
    select_acl_options(selenium, browser_id, priv, modals, name)


@when(parsers.re('user of (?P<browser_id>\w+) sets "(?P<path>.*)" ACL '
                 '(?P<priv>.*) privileges for (?P<type>.*) (?P<name>.*) '
                 'in "(?P<space>.*)"'))
def grant_acl_privileges_in_op_gui(selenium, browser_id, path, priv, name,
                                   op_page, tmp_memory, modals, space, oz_page):
    option = 'spaces'
    option_in_submenu = 'Data'
    option_for_dir = 'Permissions'
    modal_name = 'Edit Permissions'

    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id, option,
                                                space, oz_page)
    click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                  space, option_in_submenu,
                                                  oz_page)
    assert_file_browser_in_data_tab_in_op(selenium, browser_id,
                                          op_page, tmp_memory)
    click_menu_for_elem_in_file_browser(selenium, browser_id, path,
                                        tmp_memory)
    click_option_in_data_row_menu_in_file_browser(selenium, browser_id,
                                                  option_for_dir, modals)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)

    set_acl_entry_in_op_gui(selenium, browser_id, priv, name, modals)
    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, 'Save',
                                          tmp_memory)


@then(parsers.re('user of (?P<browser_id>\w+) (?P<res>.*) to read "(?P<path>.*)"'
                 ' ACL in "(?P<space>.*)"'))
def read_items_acl(selenium, browser_id, path, tmp_memory, res,
                   space, modals, oz_page, op_page):
    open_acl_modal(selenium, browser_id, path, tmp_memory, modals,
                   oz_page, op_page, space)

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
                         path, tmp_memory, modals, numerals):
    selenium[browser_id].refresh()
    open_acl_modal(selenium, browser_id, path, tmp_memory, modals)
    assert_acl_subject(selenium, browser_id, modals, num, numerals, type, name)
    assert_set_acl_privileges(selenium, browser_id, modals, num, numerals, priv)
    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, "Cancel",
                                          tmp_memory)


@then(parsers.re('user of (?P<browser_id>\w+) (?P<res>.*) to change "(?P<path>.*)"'
                 ' ACL for (?P<name>.*) in "(?P<space>.*)"'))
def change_acl_privileges(selenium, browser_id, path, tmp_memory, res,
                          space, modals, op_page, oz_page, name):
    priv = '[attributes]' if res == 'succeeds' else '[acl:change acl]'
    text = 'Modifying permissions failed'

    open_acl_modal(selenium, browser_id, path, tmp_memory, modals,
                   oz_page, op_page, space)
    expand_subject_record_in_edit_permissions_modal(selenium, browser_id,
                                                    modals, name)
    select_acl_options(selenium, browser_id, priv, modals, name)
    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, 'Save',
                                          tmp_memory)

    if res == 'fails':
        assert_error_modal_with_text_appeared(selenium, browser_id, text)

    else:
        open_acl_modal(selenium, browser_id, path, tmp_memory, modals,
                       oz_page, op_page, space)
        check_permissions_list_in_edit_permissions_modal(selenium, browser_id,
                                                         modals)


