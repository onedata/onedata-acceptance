"""Meta steps for basic operations on groups in Oneprovider web GUI
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


import pytest
from pytest_bdd import when, then, given, parsers
from tests.gui.utils.generic import parse_seq, repeat_failed
from tests.gui.steps.common.miscellaneous import *
from tests.gui.steps.oneprovider.groups import *
from tests.gui.steps.oneprovider_common import *
from tests.gui.steps.common.copy_paste import *
from tests.gui.steps.modal import *
from tests.gui.steps.common.notifies import notify_visible_with_text
from tests.gui.conftest import WAIT_FRONTEND


def see_groups_using_op_gui(selenium, user, op_page, group_list):
    wt_click_on_the_given_main_menu_tab(selenium, user, 'groups')
    for group in parse_seq(group_list):
        is_present_on_groups_list(selenium, user, group, op_page)


def create_groups_using_op_gui(selenium, user, op_page, group_list, tmp_memory):
    wt_click_on_the_given_main_menu_tab(selenium, user, 'groups')
    modal_name = "Create a new group"
    for group in parse_seq(group_list):
        click_on_btn_in_groups_sidebar_header(selenium, user, 'Create', op_page)
        wt_wait_for_modal_to_appear(selenium, user, modal_name, tmp_memory)
        activate_input_box_in_modal(user, '', tmp_memory)
        type_string_into_active_element(selenium, user, group)
        press_enter_on_active_element(selenium, user)
        wt_wait_for_modal_to_disappear(selenium, user, tmp_memory)
        is_present_on_groups_list(selenium, user, group, op_page)


def rename_groups_using_op_gui(selenium, user, op_page, group_list, new_names, 
                               tmp_memory):
    wt_click_on_the_given_main_menu_tab(selenium, user, 'groups')
    modal_name = "Rename a group"
    for group, new_name in zip(parse_seq(group_list), parse_seq(new_names)):
        regexp = '.*{}.*renamed.*{}'.format(group, new_name)
        click_settings_icon_for_group(selenium, user, group, op_page)
        click_on_item_in_group_settings_dropdown(selenium, user, 'RENAME', 
                                                 group, op_page)
        wt_wait_for_modal_to_appear(selenium, user, modal_name, tmp_memory)
        activate_input_box_in_modal(user, '', tmp_memory)
        type_string_into_active_element(selenium, user, new_name)
        press_enter_on_active_element(selenium, user)
        notify_visible_with_text(selenium, user, 'info', regexp)
        wt_wait_for_modal_to_disappear(selenium, user, tmp_memory)


@repeat_failed(timeout = WAIT_FRONTEND)
def fail_to_see_groups_using_op_gui(selenium, user, op_page, group_list):
    wt_click_on_the_given_main_menu_tab(selenium, user, 'groups')
    selenium[user].refresh()
    for group in parse_seq(group_list):
        is_not_present_in_group_list(selenium, user, group, op_page)


def leave_groups_using_op_gui(selenium, user, op_page, group_list, tmp_memory):
    wt_click_on_the_given_main_menu_tab(selenium, user, 'groups')
    modal_name = "Leave the group"
    for group in parse_seq(group_list):
        regexp = '.*{}.*left successfully.*'.format(group)
        click_settings_icon_for_group(selenium, user, group, op_page)
        click_on_item_in_group_settings_dropdown(selenium, user, 'LEAVE THIS GROUP',
                                                 group, op_page)
        wt_wait_for_modal_to_appear(selenium, user, modal_name, tmp_memory)
        wt_click_on_confirmation_btn_in_modal(selenium, user, 'YES', tmp_memory)
        notify_visible_with_text(selenium, user, 'info', regexp)
        wt_wait_for_modal_to_disappear(selenium, user, tmp_memory)
   

def assert_subgroups_using_op_gui(selenium, user, op_page, group_list, parent):
    wt_click_on_the_given_main_menu_tab(selenium, user, 'groups')
    select_group_from_sidebar_list(selenium, user, parent, op_page)
    for group in parse_seq(group_list):
        assert_item_appeared_in_groups_perm_table(selenium, user, group, 
                                                  'GROUPS', op_page)


def fail_to_see_subgroups_using_op_gui(selenium, user, op_page, 
                                       group_list, parent):
    wt_click_on_the_given_main_menu_tab(selenium, user, 'groups')
    select_group_from_sidebar_list(selenium, user, parent, op_page)
    for group in parse_seq(group_list):
        assert_item_disappeared_from_groups_perm_table(selenium, user, group, 
                                                       'GROUPS', op_page)


@when(parsers.re('(?P<user>\w+) invites (?P<user2>\w+) to group '
                 '"(?P<group_name>.*)" using Oneprovider web GUI'))
@then(parsers.re('(?P<user>\w+) invites (?P<user2>\w+) to group '
                 '"(?P<group_name>.*)" using Oneprovider web GUI'))
def create_group_token_using_op_gui(selenium, user, user2, op_page, group_name, 
                                    tmp_memory, displays, clipboard):
    modal_name = "Invite user to the group"
    click_settings_icon_for_group(selenium, user, group_name, op_page)
    click_on_item_in_group_settings_dropdown(selenium, user, 'INVITE USER', 
                                             group_name, op_page)
    wt_wait_for_modal_to_appear(selenium, user, modal_name, tmp_memory)
    get_token_from_modal(selenium, user, tmp_memory)
    click_on_copy_btn_in_modal(selenium, user, tmp_memory)
    send_copied_item_to_other_users(user, 'token', user2, tmp_memory, displays, 
                                    clipboard)
    wt_click_on_confirmation_btn_in_modal(selenium, user, 'OK', tmp_memory)
    wt_wait_for_modal_to_disappear(selenium, user, tmp_memory)


@when(parsers.re('(?P<user>\w+) joins group he was invited to using '
                 'Oneprovider web GUI'))
@then(parsers.re('(?P<user>\w+) joins group he was invited to using '
                 'Oneprovider web GUI'))
def join_group_using_op_gui(selenium, user, op_page, tmp_memory):
    wt_click_on_the_given_main_menu_tab(selenium, user, 'groups')
    modal_name = "Join a group"
    regexp = '.*joined.*'
    click_on_btn_in_groups_sidebar_header(selenium, user, 'Join', op_page)
    wt_wait_for_modal_to_appear(selenium, user, modal_name, tmp_memory)
    activate_input_box_in_modal(user, '', tmp_memory)
    type_item_into_active_element(selenium, user, 'token', tmp_memory)
    press_enter_on_active_element(selenium, user)
    notify_visible_with_text(selenium, user, 'info', regexp)
    wt_wait_for_modal_to_disappear(selenium, user, tmp_memory)


def _create_invite_group_token(selenium, user, op_page, parent, tmp_memory, 
                               displays, clipboard):
    wt_click_on_the_given_main_menu_tab(selenium, user, 'groups')
    modal_name = "Invite group to the group"
    click_settings_icon_for_group(selenium, user, parent, op_page)
    click_on_item_in_group_settings_dropdown(selenium, user, 'INVITE '
                                             'GROUP', parent, op_page)
    wt_wait_for_modal_to_appear(selenium, user, modal_name, tmp_memory)
    get_token_from_modal(selenium, user, tmp_memory)
    click_on_copy_btn_in_modal(selenium, user, tmp_memory)
    send_copied_item_to_other_users(user, 'token', user, tmp_memory, 
                                    displays, clipboard)


@repeat_failed(timeout=WAIT_FRONTEND)    
def _try_to_join_group_to_group(selenium, user, child, op_page, tmp_memory, 
                                regexp, notify_type):
    modal_name = "Join a group to group"
    click_settings_icon_for_group(selenium, user, child, op_page)
    click_on_item_in_group_settings_dropdown(selenium, user, 'JOIN AS SUBGROUP',
                                             child, op_page)
    wt_wait_for_modal_to_appear(selenium, user, modal_name, tmp_memory)
    activate_input_box_in_modal(user, '', tmp_memory)
    type_item_into_active_element(selenium, user, 'token', tmp_memory)
    press_enter_on_active_element(selenium, user)
    notify_visible_with_text(selenium, user, notify_type, regexp)
    wt_wait_for_modal_to_disappear(selenium, user, tmp_memory)


def add_subgroups_using_op_gui(selenium, user, op_page, parent, group_list, 
                               tmp_memory, displays, clipboard):
    _create_invite_group_token(selenium, user, op_page, parent, tmp_memory, 
                               displays, clipboard)
    for child in parse_seq(group_list):
        regexp = '.*joined group.*{}.*to group.*{}.*'.format(child, parent)
        _try_to_join_group_to_group(selenium, user, child, op_page, tmp_memory,
                                    regexp, 'info')


def fail_to_add_subgroups_using_op_gui(selenium, user, op_page, parent, group_list, 
                                       tmp_memory, displays, clipboard):
    _create_invite_group_token(selenium, user, op_page, parent, tmp_memory, 
                               displays, clipboard)
    for child in parse_seq(group_list):
        regexp = 'Failed to join.*{}.*'.format(child)
        _try_to_join_group_to_group(selenium, user, child, op_page, tmp_memory,
                                    regexp, 'error')


def remove_subgroups_using_op_gui(selenium, user, op_page, group_list,
                                  tmp_memory, parent):
    wt_click_on_the_given_main_menu_tab(selenium, user, 'groups')
    modal_name = "Leave a parent group..."
    # Sleep to ensure that 'Leave parent' button has appeared in dropdown 
    time.sleep(10)
    for child in parse_seq(group_list):
        regexp = 'Group.*{}.*left.*{}.*'.format(parent, child)
        selenium[user].refresh()
        click_settings_icon_for_group(selenium, user, child, op_page)
        click_on_item_in_group_settings_dropdown(selenium, user, 'LEAVE PARENT'
                                                 ' GROUP...', child, op_page)
        wt_wait_for_modal_to_appear(selenium, user, modal_name, tmp_memory)
        wt_click_on_confirmation_btn_in_modal(selenium, user, 'OK', tmp_memory)
        notify_visible_with_text(selenium, user, 'info', regexp)
        wt_wait_for_modal_to_disappear(selenium, user, tmp_memory)


def fail_to_rename_groups_using_op_gui(selenium, user, op_page, group_list, 
                                       new_names, tmp_memory):
    wt_click_on_the_given_main_menu_tab(selenium, user, 'groups')
    modal_name = "Rename a group"
    for group, new_name in zip(parse_seq(group_list), parse_seq(new_names)):
        regexp = '.*{}.*{}.*failed.*'.format(group, new_name)
        click_settings_icon_for_group(selenium, user, group, op_page)
        click_on_item_in_group_settings_dropdown(selenium, user, 'RENAME', 
                                                 group, op_page)
        wt_wait_for_modal_to_appear(selenium, user, modal_name, tmp_memory)
        activate_input_box_in_modal(user, '', tmp_memory)
        type_string_into_active_element(selenium, user, new_name)
        press_enter_on_active_element(selenium, user)
        notify_visible_with_text(selenium, user, 'error', regexp)
        wt_wait_for_modal_to_disappear(selenium, user, tmp_memory)
