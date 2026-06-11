"""This module contains meta steps for operations on groups in Onezone
using web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Any

from selenium.webdriver.common.keys import Keys

from tests.conftest import Hosts, SeleniumDrivers, Users
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.meta_steps.onezone.tokens import (
    add_element_with_copied_token,
    consume_received_token,
)
from tests.gui.steps.common.copy_paste import send_copied_item_to_other_users
from tests.gui.steps.modals.modal import (
    assert_error_modal_with_text_appeared,
    click_modal_button,
    close_modal,
)
from tests.gui.steps.onezone.groups import (
    assert_group_exists,
    click_create_group_button_in_panel,
    click_on_confirmation_button_to_rename_group,
    click_on_group_menu_button,
    confirm_name_input_on_main_groups_page,
    go_to_group_subpage,
    input_name_into_input_box_on_main_groups_page,
    input_new_group_name_into_rename_group_inpux_box,
    press_enter_on_active_element,
)
from tests.gui.steps.onezone.members import (
    assert_element_is_member_of_parent_in_memberships,
    assert_element_is_not_member_of_parent_in_memberships,
    click_element_in_members_list,
    click_on_option_in_members_list_menu,
    copy_token_from_modal,
    remove_member_from_parent,
)
from tests.gui.steps.rest.groups import get_user_groups, leave_user_group
from tests.gui.utils.generic import parse_seq
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.re(
        'user of (?P<browser_id>.*) renames group "(?P<group>.*)" '
        'to "(?P<new_group>.*)" using '
        "(?P<confirm_type>.*) to confirm"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def rename_group(
    selenium: SeleniumDrivers,
    browser_id: Any,
    group: Any,
    new_group: Any,
    confirm_type: Any,
) -> Any:
    option = "Rename"
    text = new_group

    click_on_group_menu_button(selenium, browser_id, option, group)
    input_new_group_name_into_rename_group_inpux_box(selenium, browser_id, text)
    if confirm_type == "button":
        click_on_confirmation_button_to_rename_group(selenium, browser_id)
    else:
        press_enter_on_active_element(selenium, browser_id)
        selenium[browser_id].switch_to.active_element.send_keys(Keys.RETURN)


@wt(parsers.parse('user of {browser_id} leaves group "{group}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def leave_group(selenium: SeleniumDrivers, browser_id: Any, group: Any) -> Any:
    option = "Leave"
    modal = "LEAVE GROUP"

    click_on_group_menu_button(selenium, browser_id, option, group)
    click_modal_button(selenium, browser_id, option, modal)


@given(parsers.parse("{user} user does not have access to any group"))
def g_leave_user_groups_in_onezone_using_rest(
    hosts: Hosts, users: Users, user: Any
) -> Any:
    leave_user_groups_in_onezone_using_rest(hosts, users, user)


def leave_user_groups_in_onezone_using_rest(
    hosts: Hosts, users: Users, user: Any
) -> Any:
    zone_hostname = hosts["onezone"]["hostname"]
    user_groups = get_user_groups(zone_hostname, user, users)
    for group_id in user_groups:
        # don`t remove admin user from admins group
        if group_id == "admins":
            continue
        leave_user_group(zone_hostname, user, users, group_id)


@wt(parsers.parse('user of {browser_id} removes group "{group_list}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_group(selenium: SeleniumDrivers, browser_id: Any, group_list: Any) -> Any:
    option = "Remove"
    modal = "REMOVE GROUP"

    for group in parse_seq(group_list):
        click_on_group_menu_button(selenium, browser_id, option, group)
        click_modal_button(selenium, browser_id, option, modal)


@wt(parsers.parse('user of {browser_id} creates group "{group_list}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_groups_using_op_gui(
    selenium: SeleniumDrivers, browser_id: Any, group_list: Any
) -> Any:
    for group in parse_seq(group_list):
        click_create_group_button_in_panel(selenium, browser_id)
        input_name_into_input_box_on_main_groups_page(selenium, browser_id, group)
        confirm_name_input_on_main_groups_page(selenium, browser_id)


def see_groups_using_op_gui(
    selenium: SeleniumDrivers, user: Any, group_list: Any
) -> Any:
    option = "sees"

    for group in parse_seq(group_list):
        assert_group_exists(selenium, user, option, group)


def rename_groups_using_op_gui(
    selenium: SeleniumDrivers, user: Any, group_list: Any, new_names: Any
) -> Any:
    confirm_type = "enter"

    for group, new_name in zip(parse_seq(group_list), parse_seq(new_names)):
        rename_group(selenium, user, group, new_name, confirm_type)


@repeat_failed(timeout=WAIT_FRONTEND)
def fail_to_see_groups_using_op_gui(
    selenium: SeleniumDrivers, user: Any, group_list: Any
) -> Any:
    option = "does not see"

    for group in parse_seq(group_list):
        assert_group_exists(selenium, user, option, group)


def leave_groups_using_op_gui(
    selenium: SeleniumDrivers, user: Any, group_list: Any
) -> Any:
    for group in parse_seq(group_list):
        leave_group(selenium, user, group)


def _open_member_from_list(selenium: SeleniumDrivers, user: Any, parent: Any) -> Any:
    where = "group"
    list_type = "users"
    subpage = "members"

    go_to_group_subpage(selenium, user, parent, subpage)
    click_element_in_members_list(selenium, user, user, where, list_type)


def assert_subgroups_using_op_gui(
    selenium: SeleniumDrivers, user: Any, group_list: Any, parent: Any
) -> Any:
    where = "group"

    _open_member_from_list(selenium, user, parent)
    for group in parse_seq(group_list):
        assert_element_is_member_of_parent_in_memberships(
            selenium, user, group, parent, where, where, where
        )


def fail_to_see_subgroups_using_op_gui(
    selenium: SeleniumDrivers, user: Any, group_list: Any, parent: Any
) -> Any:
    where = "group"

    _open_member_from_list(selenium, user, parent)
    for group in parse_seq(group_list):
        assert_element_is_not_member_of_parent_in_memberships(
            selenium, user, group, where, parent, where, where
        )


@repeat_failed(timeout=WAIT_FRONTEND)
def _create_group_token(
    selenium: SeleniumDrivers,
    user: Any,
    user2: Any,
    name: Any,
    tmp_memory: Any,
    displays: Any,
    clipboard: Any,
    member: Any,
) -> Any:
    item_type = "token"
    where = "group"
    button = f"Invite {member} using token"
    member += "s"
    modal = "Invite using token"
    subpage = "members"

    go_to_group_subpage(selenium, user, name, subpage)
    click_on_option_in_members_list_menu(selenium, user, button, where, member)
    copy_token_from_modal(selenium, user)
    close_modal(selenium, user, modal)
    send_copied_item_to_other_users(
        user, item_type, user2, tmp_memory, displays, clipboard
    )


@wt(
    parsers.re(
        r"(?P<user>\w+) invites (?P<user2>\w+) to group "
        '"(?P<name>.*)" using Oneprovider web GUI'
    )
)
def create_group_token_to_invite_user_using_op_gui(
    selenium: SeleniumDrivers,
    user: Any,
    user2: Any,
    name: Any,
    tmp_memory: Any,
    displays: Any,
    clipboard: Any,
) -> Any:
    member = "user"
    _create_group_token(
        selenium,
        user,
        user2,
        name,
        tmp_memory,
        displays,
        clipboard,
        member,
    )


def create_group_token_to_invite_group_using_op_gui(
    selenium: SeleniumDrivers,
    user: Any,
    user2: Any,
    name: Any,
    tmp_memory: Any,
    displays: Any,
    clipboard: Any,
) -> Any:
    member = "group"
    _create_group_token(
        selenium,
        user,
        user2,
        name,
        tmp_memory,
        displays,
        clipboard,
        member,
    )


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) joins group he was invited to in Onezone service"
    )
)
def join_group_using_op_gui(
    selenium: SeleniumDrivers, browser_id: Any, tmp_memory: Any
) -> Any:
    consume_received_token(selenium, browser_id, tmp_memory)


def add_subgroups_using_op_gui(
    selenium: SeleniumDrivers,
    user: Any,
    parent: Any,
    group_list: Any,
    tmp_memory: Any,
    displays: Any,
    clipboard: Any,
) -> Any:
    for child in parse_seq(group_list):
        create_group_token_to_invite_group_using_op_gui(
            selenium,
            user,
            user,
            parent,
            tmp_memory,
            displays,
            clipboard,
        )
        add_element_with_copied_token(selenium, user, child, clipboard, displays)


def remove_subgroups_using_op_gui(
    selenium: SeleniumDrivers, user: Any, group_list: Any, tmp_memory: Any, parent: Any
) -> Any:
    member_type = "group"

    for child in parse_seq(group_list):
        remove_member_from_parent(
            selenium,
            user,
            child,
            member_type,
            parent,
            tmp_memory,
            member_type,
        )


def fail_to_rename_groups_using_op_gui(
    selenium: SeleniumDrivers, user: Any, group_list: Any, new_names: Any
) -> Any:
    text = "failed"

    for group, new_name in zip(parse_seq(group_list), parse_seq(new_names)):
        rename_groups_using_op_gui(selenium, user, group, new_name)
        assert_error_modal_with_text_appeared(selenium, user, text)


def fail_to_add_subgroups_using_op_gui(
    selenium: SeleniumDrivers,
    user: Any,
    parent: Any,
    group_list: Any,
    tmp_memory: Any,
    displays: Any,
    clipboard: Any,
) -> Any:
    create_group_token_to_invite_group_using_op_gui(
        selenium,
        user,
        user,
        parent,
        tmp_memory,
        displays,
        clipboard,
    )
    for child in parse_seq(group_list):
        error = "Consuming token failed"
        modal = "error"

        add_element_with_copied_token(selenium, user, child, clipboard, displays)
        assert_error_modal_with_text_appeared(selenium, user, error)
        close_modal(selenium, user, modal)
