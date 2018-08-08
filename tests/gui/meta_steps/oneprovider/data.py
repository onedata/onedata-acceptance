"""Meta steps for operations in data tab in Oneprovider
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import yaml
from tests.utils.acceptance_utils import wt
from pytest_bdd import when, then, given, parsers
from tests.gui.utils.generic import parse_seq
from tests.gui.steps.oneprovider.permissions import *
from tests.gui.steps.oneprovider.file_browser import *
from tests.gui.steps.oneprovider.data_tab import *
from tests.gui.steps.common.miscellaneous import *
from tests.gui.steps.oneprovider.metadata import *
from tests.gui.steps.modal import *
from tests.gui.steps.common.notifies import notify_visible_with_text
from tests.gui.steps.common.url import refresh_site
from tests.gui.meta_steps.oneprovider.common import (
    navigate_to_tab_in_op_using_gui)


@when(parsers.re('user of (?P<browser_id>\w+) adds ACE with (?P<priv>.*)'
                 ' privileges? set for (?P<type>.*?) (?P<name>.*)'))
def set_acl_entry_in_op_gui(selenium, browser_id, priv, type, name, modals, 
                            numerals):
    add_acl(selenium, browser_id, modals)
    select_acl_subject_type(selenium, browser_id, type, 'last', numerals, modals)
    select_acl_subject(selenium, browser_id, name, 'last', numerals,  modals)
    select_acl_options(selenium, browser_id, priv, modals, 'last', numerals)


def open_acl_modal(selenium, browser_id, path, space, op_page, tmp_memory, 
                   modals):
    modal_name = "Edit permissions"
    tooltip = "Change element permissions"
    _select_item(selenium, browser_id, space, op_page, tmp_memory, path) 
    click_tooltip_from_toolbar_in_data_tab_in_op(selenium, browser_id, tooltip, 
                                                 op_page)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    select_permission_type(selenium, browser_id, "ACL", modals)


@when(parsers.re('user of (?P<browser_id>\w+) sets (?P<path>.*) ACL '
                 '(?P<priv>.*) privileges for (?P<type>.*) (?P<name>.*)'
                 ' in "(?P<space>.*)"'))
def grant_acl_privileges_in_op_gui(selenium, browser_id, path, priv, type, name,
                                 op_page, tmp_memory, modals, space, numerals):
    open_acl_modal(selenium, browser_id, path, space, op_page, tmp_memory, 
                   modals)
    set_acl_entry_in_op_gui(selenium, browser_id, priv, type, name, modals, 
                            numerals)
    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, "Ok", tmp_memory)
    wt_wait_for_modal_to_disappear(selenium, browser_id, tmp_memory)


@then(parsers.re('user of (?P<browser_id>\w+) (?P<res>.*) to rename "(?P<path>.*)"'
                 ' to "(?P<new_name>.*)" in "(?P<space>.*)"'))
def rename_item(selenium, browser_id, path, new_name, tmp_memory, op_page, 
                res, space):
    modal_name = "Rename file or directory"
    tooltip = "Rename element"
    try:
        _select_item(selenium, browser_id, space, op_page, tmp_memory, path)
    except RuntimeError as e:
        if res == 'fails':
            return
        raise e
    click_tooltip_from_toolbar_in_data_tab_in_op(selenium, browser_id, tooltip, 
                                                 op_page)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    activate_input_box_in_modal(browser_id, '', tmp_memory)
    type_string_into_active_element(selenium, browser_id, new_name)
    press_enter_on_active_element(selenium, browser_id)
    if res == 'fails':
        notify_visible_with_text(selenium, browser_id, 'error', 
                                 '.*[Aa]ccess denied.*')
    else:
        notify_visible_with_text(selenium, browser_id, 'info', '.*renamed.*')
    wt_wait_for_modal_to_disappear(selenium, browser_id, tmp_memory)


@then(parsers.re('user of (?P<browser_id>\w+) (?P<res>.*) to remove "(?P<path>.*)"'
                 ' in "(?P<space>.*)"'))
def remove_item_in_op_gui(selenium, browser_id, path, tmp_memory, op_page, 
                          res, space):
    modal_name = "Remove files"
    tooltip = "Remove element"
    try:
        _select_item(selenium, browser_id, space, op_page, tmp_memory, path)
    except RuntimeError as e:
        if res == 'fails':
            return
        raise e
    click_tooltip_from_toolbar_in_data_tab_in_op(selenium, browser_id, tooltip, 
                                                 op_page)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, 'YES', tmp_memory)

    if res == 'fails':
        notify_visible_with_text(selenium, browser_id, 'error', '.*not.*removed.*')
    else:
        notify_visible_with_text(selenium, browser_id, 'info', '.*removed.*')
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


@when(parsers.re('user of (?P<browser_id>\w+) (?P<res>.*) to write '
                 '"(?P<path>.*)" (?P<tab_name>basic|JSON|RDF) metadata:'
                 ' "(?P<val>.*)" in "(?P<space>.*)"'))
@then(parsers.re('user of (?P<browser_id>\w+) (?P<res>.*) to write '
                 '"(?P<path>.*)" (?P<tab_name>basic|JSON|RDF) metadata:'
                 ' "(?P<val>.*)" in "(?P<space>.*)"'))
def set_metadata_in_op_gui(selenium, browser_id, path, tmp_memory, op_page, 
                           res, space, tab_name, val):
    tooltip = "Edit metadata"
    button_name = "Save all changes"
    item_name = _select_item(selenium, browser_id, space, op_page, tmp_memory, 
                             path)
    click_tooltip_from_toolbar_in_data_tab_in_op(selenium, browser_id, tooltip, 
                                                 op_page)
    assert_files_metadata_panel_displayed(browser_id, item_name, tmp_memory)
    if tab_name == "basic":
        attr, val = val.split('=')
        type_text_to_attr_input_in_new_basic_entry(browser_id, attr, item_name, 
                                                   tmp_memory)
        type_text_to_val_input_in_new_basic_entry(browser_id, val, item_name, 
                                                  tmp_memory)
        click_on_add_meta_rec_btn_in_metadata_panel(browser_id, item_name, 
                                                    tmp_memory)
    else:
        click_on_navigation_tab_in_metadata_panel(browser_id, tab_name, 
                                                  item_name, tmp_memory)
        type_text_to_metadata_textarea(browser_id, item_name, val, tab_name, 
                                       tmp_memory)
    click_on_button_in_metadata_panel(browser_id, button_name, item_name, 
                                      tmp_memory)
    if res == 'fails':
        notify_visible_with_text(selenium, browser_id, 'error', '.*Cannot.*'
                                 'save.*metadata.*')
    else:
        notify_visible_with_text(selenium, browser_id, 'info', '.*successfully.*')
    click_tooltip_from_toolbar_in_data_tab_in_op(selenium, browser_id, tooltip, 
                                                 op_page)


@then(parsers.re('user of (?P<browser_id>\w+) (?P<res>.*) to read '
                 '"(?P<path>.*)" (?P<tab_name>basic|JSON|RDF) metadata '
                 '"(?P<val>.*)" in "(?P<space>.*)"'))
def assert_metadata_in_op_gui(selenium, browser_id, path, tmp_memory, op_page, 
                              res, space, tab_name, val):
    selenium[browser_id].refresh()
    tooltip = 'Edit metadata'
    item_name = _select_item(selenium, browser_id, space, op_page, tmp_memory, 
                             path)
    click_tooltip_from_toolbar_in_data_tab_in_op(selenium, browser_id, tooltip, 
                                                 op_page)
    assert_files_metadata_panel_displayed(browser_id, item_name, tmp_memory)
    if tab_name == 'basic':
        (attr, val) = val.split('=')
        if res == 'fails':
            file_browser = tmp_memory[browser_id]['file_browser']
            metadata_row = file_browser.get_metadata_for(item_name)
            if not metadata_row.is_resource_load_error():
                assert_there_is_no_such_meta_record(browser_id, attr, item_name, 
                                                    tmp_memory)
        else:
            assert_there_is_such_meta_record(browser_id, attr, val, item_name, 
                                             tmp_memory)
    else:
        click_on_navigation_tab_in_metadata_panel(browser_id, tab_name, 
                                                  item_name, tmp_memory)
        if res == 'fails':
            assert_textarea_content_is_eq_to(browser_id, item_name,
                                             '{}' if tab_name == 'json' else '',
                                             tab_name, tmp_memory)
        else:
            assert_textarea_contains_record(browser_id, val, tab_name, 
                                            item_name, tmp_memory)


def remove_all_metadata_in_op_gui(selenium, browser_id, space, op_page, 
                                  tmp_memory, path):
    selenium[browser_id].refresh()
    tooltip = "Edit metadata"
    item_name = _select_item(selenium, browser_id, space, op_page, tmp_memory, 
                             path)
    click_tooltip_from_toolbar_in_data_tab_in_op(selenium, browser_id, tooltip, 
                                                 op_page)
    assert_files_metadata_panel_displayed(browser_id, item_name, tmp_memory)
    click_on_button_in_metadata_panel(browser_id, 'Remove metadata', item_name, 
                                      tmp_memory)
    notify_visible_with_text(selenium, browser_id, 'info', '.*[Dd]eleted.*')


@then(parsers.re('user of (?P<browser_id>\w+) (?P<res>.*) to see '
                 '(?P<subfiles>.*) in "(?P<path>.*)" in "(?P<space>.*)"'))
def see_items_in_op_gui(selenium, browser_id, path, subfiles, tmp_memory, 
                        op_page, res, space):
    selenium[browser_id].refresh()
    item_name = _select_item(selenium, browser_id, space, op_page, tmp_memory, 
                             path)
    if path:
        double_click_on_item_in_file_browser(browser_id, item_name, tmp_memory)
    if res == 'fails':
        assert_items_absence_in_file_browser(browser_id, subfiles, tmp_memory)
    else:
        assert_items_presence_in_file_browser(browser_id, subfiles, tmp_memory)


@wt(parsers.re('user of (?P<browser_id>\w+) (?P<res>.*) to create '
               '(?P<item_type>directory|file) "(?P<name>[\w._-]+)" '
               '(in "(?P<path>.*)" )?in "(?P<space>.*)"'))
def create_item_in_op_gui(selenium, browser_id, path, item_type, name,
                          tmp_memory, op_page, res, space):

    # change None to empty string if path not given
    path = path if path else ''
    item_name = _select_item(selenium, browser_id, space, op_page, tmp_memory, 
                             path)
    if path:
        double_click_on_item_in_file_browser(browser_id, item_name, tmp_memory)
    tooltip = "Create {}".format(item_type)
    modal_name = "New {}".format(item_type)
    click_tooltip_from_toolbar_in_data_tab_in_op(selenium, browser_id, tooltip, 
                                                 op_page)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    type_string_into_active_element(selenium, browser_id, name)
    press_enter_on_active_element(selenium, browser_id)
    if res == 'fails':
        notify_visible_with_text(selenium, browser_id, 'error', 
                                 '.*[Ff]ailed.*')
    else:
        assert_items_presence_in_file_browser(browser_id, name, tmp_memory)


def _check_files_tree(subtree, user, tmp_memory, cwd, selenium, op_page,
                      tmpdir):
    for item in subtree:
        try:
            [(item_name, item_subtree)] = item.items()
        except AttributeError:
            assert_items_presence_in_file_browser(user, item, tmp_memory)
            if item.startswith('dir'):
                double_click_on_item_in_file_browser(user, item, tmp_memory)
                assert_empty_file_browser_in_data_tab_in_op(selenium, user,
                                                            op_page, tmp_memory)
                change_cwd_using_dir_tree_in_data_tab_in_op(selenium, user,
                                                            cwd, op_page)
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
                                      selenium, op_page, tmpdir)
                change_cwd_using_dir_tree_in_data_tab_in_op(selenium, user,
                                                            cwd, op_page)
            else:
                has_downloaded_file_content(user, item_name, str(item_subtree),
                                            tmpdir)
    change_cwd_using_dir_tree_in_data_tab_in_op(selenium, user, cwd, op_page)


def assert_space_content_in_op_gui(config, selenium, user, op_page, tmp_memory,
                                   tmpdir, space_name, oz_page, provider, hosts):
    tab_name = 'data'

    navigate_to_tab_in_op_using_gui(selenium, user, oz_page, provider, tab_name,
                                    hosts)
    refresh_site(selenium, user)
    change_space_view_in_data_tab_in_op(selenium, user, space_name, op_page)
    assert_file_browser_in_data_tab_in_op(selenium, user, op_page, tmp_memory)
    _check_files_tree(yaml.load(config), user, tmp_memory, '/', selenium,
                      op_page, tmpdir)


def create_directory_structure_in_op_gui(selenium, user, op_page, config, space,
                                         tmp_memory):
    items = yaml.load(config)
    cwd = ''
    _create_content(selenium, user, items, cwd, space, tmp_memory, op_page)
    

def _create_item(selenium, browser_id, name, content, cwd, space, tmp_memory,
                 op_page):
    item_type = 'directory' if name.startswith('dir') else 'file'
    create_item_in_op_gui(selenium, browser_id, cwd, item_type, name, 
                          tmp_memory, op_page, "succeeds", space)
    if not content:
        return 
    cwd += '/' + name
    _create_content(selenium, browser_id, content, cwd, space, tmp_memory, 
                    op_page)



def _create_content(selenium, browser_id, content, cwd, space, tmp_memory, 
                    op_page):
    for item in content:
        try: 
            [(name, content)] = item.items()
        except AttributeError:
            name = item
            content = None
        _create_item(selenium, browser_id, name, content, cwd, space, 
                     tmp_memory, op_page)


def _select_item(selenium, browser_id, space, op_page, tmp_memory, path):
    change_space_view_in_data_tab_in_op(selenium, browser_id, space, op_page)
    assert_file_browser_in_data_tab_in_op(selenium, browser_id, op_page, 
                                          tmp_memory)
    path_list = path.strip('\"').split('/')
    item_name = path_list.pop()
    path = '/'.join(path_list)
    change_cwd_using_dir_tree_in_data_tab_in_op(selenium, browser_id, path,
                                                op_page)
    select_files_from_file_list_using_ctrl(browser_id, item_name, tmp_memory)
    return item_name
