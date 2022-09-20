"""Steps implementation for permissions GUI tests."""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from selenium.common.exceptions import StaleElementReferenceException

from tests.gui.conftest import WAIT_BACKEND
from tests.gui.steps.modals.details_modal import (assert_tab_in_modal,
                                                  click_button_in_panel)
from tests.gui.steps.oneprovider.browser import (
    click_option_in_data_row_menu_in_browser)
from tests.gui.steps.oneprovider.permissions import *
from tests.gui.meta_steps.oneprovider.data import (
    assert_browser_in_tab_in_op, choose_option_from_selection_menu,
    _click_menu_for_elem_somewhere_in_file_browser)
from tests.gui.steps.oneprovider.file_browser import (
    select_files_from_file_list_using_ctrl)
from tests.gui.steps.modals.modal import assert_error_modal_with_text_appeared
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

    select_permission_type(selenium, browser_id, permission_type, modals)


def _assert_posix_permissions(selenium, browser_id, space, path, perm,
                              oz_page, op_container, tmp_memory,
                              modals, popups):
    modal_name = 'Details modal'
    close_button = 'Close'
    open_permission_modal(selenium, browser_id, path, space, tmp_memory, modals,
                          oz_page, op_container, 'posix', popups)
    check_permission(selenium, browser_id, perm, modals)
    click_modal_button(selenium, browser_id, close_button, modal_name, modals)


@repeat_failed(timeout=WAIT_BACKEND)
def assert_posix_permissions_in_op_gui(selenium, browser_id, space, path, perm,
                                       oz_page, op_container, tmp_memory,
                                       modals, popups):
    modal_name = 'Details modal'
    close_button = 'Close'
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
    close_button = 'Close'
    tab = 'Edit permissions'

    open_permission_modal(selenium, browser_id, path, space, tmp_memory, modals,
                          oz_page, op_container, 'posix', popups)
    set_posix_permission(selenium, browser_id, perm, modals)
    click_button_in_panel(selenium, browser_id, button, modals, tab)
    click_modal_button(selenium, browser_id, close_button, modal_name, modals)


def fail_to_set_posix_permissions_in_op_gui(selenium, browser_id, space, path,
                                            perm, op_container, tmp_memory,
                                            modals, oz_page, popups):
    button = 'Save'
    tab = 'Edit permissions'
    text = 'Modifying permissions failed'
    details_modal = 'Details modal'
    close_button = 'Close'
    error_modal = 'Error'
    discard_changes = 'Discard changes'

    open_permission_modal(selenium, browser_id, path, space, tmp_memory, modals,
                          oz_page, op_container, 'posix', popups)
    set_posix_permission(selenium, browser_id, perm, modals)
    click_button_in_panel(selenium, browser_id, button, modals, tab)
    assert_error_modal_with_text_appeared(selenium, browser_id, text)
    click_modal_button(selenium, browser_id, close_button, error_modal, modals)
    click_button_in_panel(selenium, browser_id, discard_changes, modals, tab)
    click_modal_button(selenium, browser_id, close_button, details_modal,
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
                                     priv, name, modals):
    option = 'Permissions'
    modal_name = 'Details modal'
    button = 'Save'
    close_button = 'Close'
    tab = 'Edit permissions'

    choose_option_from_selection_menu(browser_id, selenium, option, popups,
                                      tmp_memory)
    assert_tab_in_modal(selenium, browser_id, option, modals, modal_name)

    set_acl_entry_in_op_gui(selenium, browser_id, priv, name, modals, popups)
    click_button_in_panel(selenium, browser_id, button, modals, tab)
    click_modal_button(selenium, browser_id, close_button, modal_name, modals)


@wt(parsers.re('user of (?P<browser_id>\w+) sets selected items ACL '
               '(?P<priv>.*) privileges for (?P<type>.*) (?P<name>.*)'))
def grant_acl_privileges_to_selected_in_filebrowser(selenium, browser_id, priv,
                                                    name, op_container,
                                                    tmp_memory, popups, oz_page,
                                                    modals):
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory)
    _set_acl_privilages_for_selected(browser_id, selenium, popups, tmp_memory,
                                     priv, name, modals)


@wt(parsers.re('user of (?P<browser_id>\w+) sets (?P<item_list>.*) ACL '
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
                                     priv, name, modals)


@wt(parsers.re(r'user of (?P<browser_id>\w+) (?P<res>.*) to read "(?P<path>.*)"'
               ' ACL in "(?P<space>.*)"'))
def read_items_acl(selenium, browser_id, path, tmp_memory, res, space, modals,
                   oz_page, op_container, popups):
    modal_name = 'Details modal'
    close_button = 'Close'
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
    close_button = 'Close'
    open_permission_modal(selenium, browser_id, path, space, tmp_memory, modals,
                          oz_page, op_container, 'acl', popups)
    assert_acl_subject(selenium, browser_id, modals, num, numerals, type, name)
    assert_set_acl_privileges(selenium, browser_id, modals, num, numerals, priv)
    click_modal_button(selenium, browser_id, close_button, modal_name, modals)


@wt(parsers.re(r'user of (?P<browser_id>\w+) (?P<res>.*) to change '
               '"(?P<path>.*)" ACL for (?P<name>.*) in "(?P<space>.*)"'))
def change_acl_privileges(selenium, browser_id, path, tmp_memory, res, space,
                          modals, op_container, oz_page, name, popups):
    privileges_option_list = (
        '[attributes]' if res == 'succeeds' else '[acl:change acl]')
    text = 'Modifying permissions failed'
    button = 'Save'
    panel = 'Edit permissions'

    open_permission_modal(selenium, browser_id, path, space, tmp_memory, modals,
                          oz_page, op_container, 'acl', popups)
    expand_subject_record_in_edit_permissions_modal(selenium, browser_id,
                                                    modals, name)
    select_acl_options(selenium, browser_id, privileges_option_list, modals,
                       name)
    click_modal_button(selenium, browser_id, button, panel, modals)

    if res == 'fails':
        assert_error_modal_with_text_appeared(selenium, browser_id, text)

    else:
        open_permission_modal(selenium, browser_id, path, space, tmp_memory,
                              modals, oz_page, op_container, 'acl', popups)
        check_permissions_list_in_edit_permissions_modal(selenium, browser_id,
                                                         modals)
