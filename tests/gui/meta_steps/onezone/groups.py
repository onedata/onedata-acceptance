"""This module contains meta steps for operations on groups in Onezone
using web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.steps.common.miscellaneous import *
from tests.gui.steps.common.copy_paste import send_copied_item_to_other_users
from tests.gui.steps.onezone.groups import *
from tests.gui.steps.onezone.members import *
from tests.gui.utils.generic import parse_seq
from tests.utils.utils import repeat_failed


@wt(parsers.re('user of (?P<browser_id>.*) renames group "(?P<group>.*)" '
               'to "(?P<new_group>.*)" using '
               '(?P<confirm_type>.*) to confirm'))
@repeat_failed(timeout=WAIT_FRONTEND)
def rename_group(selenium, browser_id, group, new_group, confirm_type, oz_page):
    option = 'Rename'
    text = new_group

    click_on_group_menu_button(selenium, browser_id, option, group, oz_page)
    input_new_group_name_into_rename_group_inpux_box(selenium, browser_id, text,
                                                     oz_page)
    if confirm_type == 'button':
        click_on_confirmation_button_to_rename_group(selenium, browser_id,
                                                     oz_page)
    else:
        press_enter_on_active_element(selenium, browser_id)
        selenium[browser_id].switch_to.active_element.send_keys(Keys.RETURN)


@wt(parsers.parse('user of {browser_id} leaves group "{group}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def leave_group(selenium, browser_id, group, oz_page):
    option = 'Leave'
    modal = "LEAVE GROUP"

    click_on_group_menu_button(selenium, browser_id, option, group, oz_page)
    click_modal_button(selenium, browser_id, option, modal, oz_page)


@wt(parsers.parse('user of {browser_id} removes group "{group}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_group(selenium, browser_id, group, oz_page):
    option = 'Remove'
    modal = "REMOVE GROUP"

    click_on_group_menu_button(selenium, browser_id, option, group, oz_page)
    click_modal_button(selenium, browser_id, option, modal, oz_page)


@wt(parsers.parse('user of {browser_id} creates group "{group_list}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_groups_using_op_gui(selenium, browser_id, group_list, oz_page):
    operation = 'Create'
    for group in parse_seq(group_list):
        click_create_or_join_group_button_in_panel(selenium, browser_id,
                                                   operation, oz_page)
        input_name_or_token_into_input_box_on_main_groups_page(selenium,
                                                               browser_id,
                                                               group, oz_page)
        confirm_name_or_token_input_on_main_groups_page(selenium, browser_id,
                                                        oz_page)


def see_groups_using_op_gui(selenium, user, oz_page, group_list):
    option = 'sees'
    for group in parse_seq(group_list):
        assert_group_exists(selenium, user, option, group, oz_page)


def rename_groups_using_op_gui(selenium, user, oz_page, group_list, new_names,
                               tmp_memory):
    confirm_type = 'enter'
    for group, new_name in zip(parse_seq(group_list), parse_seq(new_names)):
        rename_group(selenium, user, group, new_name, confirm_type,
                     oz_page)


@repeat_failed(timeout=WAIT_FRONTEND)
def fail_to_see_groups_using_op_gui(selenium, user, oz_page, group_list):
    option = 'does not see'
    for group in parse_seq(group_list):
        assert_group_exists(selenium, user, option, group, oz_page)


def leave_groups_using_op_gui(selenium, user, oz_page, group_list, tmp_memory):
    for group in parse_seq(group_list):
        leave_group(selenium, user, group, oz_page)


def assert_subgroups_using_op_gui(selenium, user, oz_page, group_list, parent):
    where = 'group'
    direct_selector = 'effective'
    mode_selector = 'memberships'
    list_type = 'users'
    subpage = 'members'

    go_to_group_subpage(selenium, user, parent, subpage, oz_page)
    click_show_view_option(selenium, user, oz_page, where)
    click_mode_view_in_members_subpage(selenium, user, direct_selector,
                                       oz_page, where)
    click_mode_view_in_members_subpage(selenium, user, mode_selector,
                                       oz_page, where)
    click_element_in_members_list(selenium, user, user,
                                  oz_page, where, list_type)
    for group in parse_seq(group_list):
        assert_element_is_member_of_parent_in_memberships(selenium, user,
                                                          group,
                                                          parent,
                                                          where,
                                                          where,
                                                          oz_page, where)


def fail_to_see_subgroups_using_op_gui(selenium, user, oz_page,
                                       group_list, parent):
    where = 'group'
    direct_selector = 'effective'
    mode_selector = 'memberships'
    list_type = 'users'
    subpage = 'members'

    go_to_group_subpage(selenium, user, parent, subpage, oz_page)
    click_show_view_option(selenium, user, oz_page, where)
    click_mode_view_in_members_subpage(selenium, user, direct_selector,
                                       oz_page, where)
    click_mode_view_in_members_subpage(selenium, user, mode_selector,
                                       oz_page, where)
    click_element_in_members_list(selenium, user, user,
                                  oz_page, where, list_type)
    for group in parse_seq(group_list):
        assert_element_is_not_member_of_parent_in_memberships(selenium, user,
                                                              group, where,
                                                              parent, oz_page,
                                                              where, where)


def _create_group_token(selenium, user, user2, oz_page, name,
                        tmp_memory, displays, clipboard, member):
    item_type = 'token'
    where = 'group'
    button = 'Invite {} using token'.format(member)
    member += 's'
    modal = 'Invite using token'

    click_on_option_in_members_list_menu(selenium, user, button,
                                         name, where, member, oz_page)
    copy_token_from_modal(selenium, user)
    close_modal(selenium, user, modal)
    send_copied_item_to_other_users(user, item_type, user2,
                                    tmp_memory, displays, clipboard)


@when(parsers.re('(?P<user>\w+) invites (?P<user2>\w+) to group '
                 '"(?P<group_name>.*)" using Oneprovider web GUI'))
@then(parsers.re('(?P<user>\w+) invites (?P<user2>\w+) to group '
                 '"(?P<name>.*)" using Oneprovider web GUI'))
def create_group_token_to_invite_user_using_op_gui(selenium, user, user2,
                                                   oz_page, name, tmp_memory,
                                                   displays, clipboard):
    member = 'user'
    _create_group_token(selenium, user, user2, oz_page, name,
                        tmp_memory, displays, clipboard, member)


def create_group_token_to_invite_group_using_op_gui(selenium, user, user2,
                                                    oz_page, name, tmp_memory,
                                                    displays, clipboard):
    member = 'group'
    _create_group_token(selenium, user, user2, oz_page, name,
                        tmp_memory, displays, clipboard, member)


@when(parsers.re('(?P<user>\w+) joins group he was invited to using '
                 'Oneprovider web GUI'))
@then(parsers.re('(?P<user>\w+) joins group he was invited to using '
                 'Oneprovider web GUI'))
def join_group_using_op_gui(selenium, user, oz_page, tmp_memory):

    confirm_type = 'enter'
    join_group(selenium, user, confirm_type, oz_page, tmp_memory)


def add_subgroups_using_op_gui(selenium, user, oz_page, parent, group_list,
                               tmp_memory, displays, clipboard):
    for child in parse_seq(group_list):
        create_group_token_to_invite_group_using_op_gui(selenium, user, user,
                                                        oz_page, parent,
                                                        tmp_memory, displays,
                                                        clipboard)
        add_group_as_subgroup(selenium, user, child, oz_page, tmp_memory)


def remove_subgroups_using_op_gui(selenium, user, oz_page, group_list,
                                  tmp_memory, parent):
    member_type = 'group'
    for child in parse_seq(group_list):
        remove_member_from_group(selenium, user, child, member_type, parent,
                                 oz_page, tmp_memory)


def fail_to_rename_groups_using_op_gui(selenium, user, oz_page, group_list,
                                       new_names, tmp_memory):
    text = 'failed'

    for group, new_name in zip(parse_seq(group_list), parse_seq(new_names)):
        rename_groups_using_op_gui(selenium, user, oz_page, group, new_name,
                                   tmp_memory)
        assert_error_modal_with_text_appeared(selenium, user, text, oz_page)


def fail_to_add_subgroups_using_op_gui(selenium, user, oz_page, parent,
                                       group_list, tmp_memory, displays,
                                       clipboard):
    create_group_token_to_invite_group_using_op_gui(selenium, user, user,
                                                    oz_page, parent, tmp_memory,
                                                    displays, clipboard)
    for child in parse_seq(group_list):
        error = 'joining group as subgroup failed'
        modal = 'error'
        add_group_as_subgroup(selenium, user, child, oz_page, tmp_memory)
        assert_error_modal_with_text_appeared(selenium, user, error,
                                              oz_page)
        close_modal(selenium, user, modal)

