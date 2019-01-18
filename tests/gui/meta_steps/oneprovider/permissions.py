"""Steps implementation for permissions GUI tests."""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.steps.oneprovider.permissions import *
from tests.gui.meta_steps.oneprovider.data import _select_item
from tests.gui.steps.common.notifies import notify_visible_with_text
from tests.gui.steps.oneprovider.data_tab import (
    click_tooltip_from_toolbar_in_data_tab_in_op)
from tests.gui.steps.oneprovider.file_browser import (
    select_files_from_file_list_using_ctrl)
from tests.gui.steps.modal import (wt_wait_for_modal_to_appear,
                                   wt_click_on_confirmation_btn_in_modal,
                                   wt_wait_for_modal_to_disappear)
from tests.gui.steps.common.url import refresh_site


def open_permission_modal(selenium, browser_id, path, space, op_page,
                          tmp_memory):
    modal_name = 'Edit permissions'
    tooltip = 'Change element permissions'
    _select_item(selenium, browser_id, space, op_page, tmp_memory, path)
    click_tooltip_from_toolbar_in_data_tab_in_op(selenium, browser_id, tooltip,
                                                 op_page)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)


def open_acl_modal(selenium, browser_id, path, space, op_page, tmp_memory,
                   modals):
    open_permission_modal(selenium, browser_id, path, space, op_page,
                          tmp_memory)
    select_permission_type(selenium, browser_id, 'ACL', modals)


def open_posix_modal(selenium, browser_id, path, space, op_page, tmp_memory,
                     modals):
    open_permission_modal(selenium, browser_id, path, space, op_page,
                          tmp_memory)
    select_permission_type(selenium, browser_id, 'POSIX', modals)


def assert_posix_permissions_in_op_gui(selenium, browser_id, space, path, perm,
                                       op_page, tmp_memory, modals):
    refresh_site(selenium, browser_id)
    open_posix_modal(selenium, browser_id, path, space, op_page,
                     tmp_memory, modals)
    check_permission(selenium, browser_id, perm, modals)


def set_posix_permissions_in_op_gui(selenium, browser_id, space, path, perm,
                                    result, op_page, tmp_memory, modals):
    open_posix_modal(selenium, browser_id, path, space, op_page,
                     tmp_memory, modals)
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
def set_acl_entry_in_op_gui(selenium, browser_id, priv, type, name, modals,
                            numerals):
    add_acl(selenium, browser_id, modals)
    select_acl_subject_type(selenium, browser_id, type, 'last', numerals,
                            modals)
    select_acl_subject(selenium, browser_id, name, 'last', numerals,  modals)
    select_acl_options(selenium, browser_id, priv, modals, 'last', numerals)


@when(parsers.re('user of (?P<browser_id>\w+) sets (?P<path>.*) ACL '
                 '(?P<priv>.*) privileges for (?P<type>.*) (?P<name>.*)'
                 ' in "(?P<space>.*)"'))
def grant_acl_privileges_in_op_gui(selenium, browser_id, path, priv, type, name,
                                 op_page, tmp_memory, modals, space, numerals):
    open_acl_modal(selenium, browser_id, path, space, op_page, tmp_memory,
                   modals)
    set_acl_entry_in_op_gui(selenium, browser_id, priv, type, name, modals,
                            numerals)
    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, 'Ok',
                                          tmp_memory)
    wt_wait_for_modal_to_disappear(selenium, browser_id, tmp_memory)


@then(parsers.re('user of (?P<browser_id>\w+) (?P<res>.*) to read "(?P<path>.*)"'
                 ' ACL in "(?P<space>.*)"'))
def read_items_acl(selenium, browser_id, path, tmp_memory, op_page, res,
                   space, modals):
    open_acl_modal(selenium, browser_id, path, space, op_page, tmp_memory,
                   modals)
    if res == "fails":
        assert_amount_of_acls(selenium, browser_id, modals, 0)
    else:
        assert_amount_of_acls(selenium, browser_id, modals, 1)
    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, "Cancel",
                                          tmp_memory)
    wt_wait_for_modal_to_disappear(selenium, browser_id, tmp_memory)


@then(parsers.re('user of (?P<browser_id>\w+) sees that (?P<path>.*?) in space '
                 '"(?P<space>\w+)" (has|have) (?P<priv>.*) privileges? set for '
                 '(?P<type>.*?) (?P<name>.*) in (?P<num>.*) ACL record'))
def assert_ace_in_op_gui(selenium, browser_id, priv, type, name, num, space,
                         path, op_page, tmp_memory, modals, numerals):
    selenium[browser_id].refresh()
    open_acl_modal(selenium, browser_id, path, space, op_page, tmp_memory,
                   modals)
    assert_acl_subject(selenium, browser_id, modals, num, numerals, type, name)
    assert_set_acl_privileges(selenium, browser_id, modals, num, numerals, priv)
    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, "Cancel",
                                          tmp_memory)


@then(parsers.re('user of (?P<browser_id>\w+) (?P<res>.*) to change "(?P<path>.*)"'
                 ' ACL in "(?P<space>.*)"'))
def change_acl_privileges(selenium, browser_id, path, tmp_memory, op_page, res,
                          space, modals):
    open_acl_modal(selenium, browser_id, path, space, op_page, tmp_memory,
                   modals)
    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, "Ok", tmp_memory)
    if res == 'fails':
        notify_visible_with_text(selenium, browser_id, 'error', '.*failed.*')
        wt_click_on_confirmation_btn_in_modal(selenium, browser_id, "Cancel",
                                              tmp_memory)
    else:
        notify_visible_with_text(selenium, browser_id, 'info',
                                 '.*permissions.*set.*')
    wt_wait_for_modal_to_disappear(selenium, browser_id, tmp_memory)
