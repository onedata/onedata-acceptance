"""This module contains meta steps for operations on groups in Onezone
using web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.meta_steps.onezone.members import remove_member_from_parent
from tests.gui.meta_steps.onezone.tokens import (
    add_element_with_copied_token,
    fail_to_add_element_with_copied_token,
    paste_and_consume_received_token,
)
from tests.gui.meta_steps.rest.groups import delete_group_if_present_using_rest
from tests.gui.steps.common.common import (
    close_alert_popup_if_present,
    wait_for_error_modal_to_disappear,
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
    click_on_option_in_group_menu_and_get_group,
    confirm_name_input_on_main_groups_page,
    go_to_group_subpage,
    input_name_into_input_box_on_main_groups_page,
    press_enter_on_active_element,
)
from tests.gui.steps.onezone.members import (
    assert_element_is_member_of_parent_in_memberships,
    assert_element_is_not_member_of_parent_in_memberships,
    click_element_in_members_list,
    click_on_option_in_members_list_menu,
    copy_token_from_modal,
)
from tests.gui.steps.rest.groups import get_user_groups, leave_user_group
from tests.gui.type_definitions import Clipboard, TmpMemory
from tests.gui.utils.common.popups.generic import AlertPopup
from tests.gui.utils.generic import parse_elements_sequence
from tests.gui.utils.onezone.groups.groups_page import Group
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.entities_setup.users import CredentialsLike
from tests.utils.user_utils import Users
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_confirmation_button_to_rename_group(group: Group) -> None:
    group.edit_box.confirm()


@repeat_failed(timeout=WAIT_FRONTEND)
def input_new_group_name_into_rename_group_inpux_box(group: Group, text: str) -> None:
    group.edit_box.value = text


def get_group_and_click_menu_button(
    selenium: SeleniumDrivers, browser_id: str, option: str, group_name: str
) -> Group:
    driver = selenium[browser_id]
    go_to_group_subpage(selenium, browser_id, group_name, "main")
    return click_on_option_in_group_menu_and_get_group(driver, group_name, option)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) clicks on "
        r'"(?P<option>Rename|Leave|Remove|Copy ID)" '
        r'button in group "(?P<group>.*)" menu in the sidebar'
    )
)
def click_menu_button_for_group(
    selenium: SeleniumDrivers, browser_id: str, option: str, group: str
) -> None:
    _ = get_group_and_click_menu_button(selenium, browser_id, option, group)


@wt(
    parsers.parse(
        'user of {browser_id} renames group "{group_name}" '
        'to "{new_group_name}" using {confirm_type} to confirm'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def rename_group(
    selenium: SeleniumDrivers,
    browser_id: str,
    group_name: str,
    new_group_name: str,
    confirm_type: str,
) -> None:
    group = get_group_and_click_menu_button(selenium, browser_id, "Rename", group_name)
    input_new_group_name_into_rename_group_inpux_box(group, new_group_name)
    if confirm_type == "button":
        click_on_confirmation_button_to_rename_group(group)
    else:
        press_enter_on_active_element(selenium, browser_id)


@wt(parsers.parse('user of {browser_id} leaves group "{group}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def leave_group(selenium: SeleniumDrivers, browser_id: str, group: str) -> None:
    option = "Leave"
    modal = "LEAVE GROUP"

    _ = get_group_and_click_menu_button(selenium, browser_id, option, group)
    click_modal_button(selenium, browser_id, option, modal)


@given(parsers.parse("{user} user does not have access to any group"))
def g_leave_user_groups_in_onezone_using_rest(
    hosts: Hosts, users: Users, user: str
) -> None:
    leave_user_groups_in_onezone_using_rest(hosts, users, user)


def leave_user_groups_in_onezone_using_rest(
    hosts: Hosts, users: Users, user: str
) -> None:
    zone_hostname = hosts["onezone"]["hostname"]
    user_groups = get_user_groups(zone_hostname, user, users)
    for group_id in user_groups:
        # don`t remove admin user from admins group
        if group_id == "admins":
            continue
        leave_user_group(zone_hostname, user, users, group_id)


@wt(
    parsers.parse(
        'user of {browser_id} removes group "{group_list:ElementsSequence}"',
        extra_types={"ElementsSequence": parse_elements_sequence},
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_group(
    selenium: SeleniumDrivers, browser_id: str, group_list: list[str]
) -> None:
    option = "Remove"
    modal = "REMOVE GROUP"

    for group in group_list:
        _ = get_group_and_click_menu_button(selenium, browser_id, option, group)
        click_modal_button(selenium, browser_id, option, modal)


@wt(
    parsers.parse(
        'user of {browser_id} creates group "{group_list:ElementsSequence}"',
        extra_types={"ElementsSequence": parse_elements_sequence},
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def create_groups_using_op_gui(
    selenium: SeleniumDrivers,
    browser_id: str,
    group_list: list[str],
    clipboard: Clipboard,
    displays: dict[str, str],
    request: pytest.FixtureRequest,
    hosts: Hosts,
    admin_credentials: CredentialsLike,
) -> None:
    for group_name in group_list:
        create_single_group_using_op_gui(selenium, browser_id, group_name)
        group_id = get_group_id_from_groups_sidebar_list(
            selenium, browser_id, group_name, clipboard, displays
        )
        _register_finalizer_to_remove_group(request, hosts, group_id, admin_credentials)


def _register_finalizer_to_remove_group(
    request: pytest.FixtureRequest,
    hosts: Hosts,
    group_id: str,
    admin_credentials: CredentialsLike,
) -> None:
    zone_hostname = hosts["onezone"]["hostname"]
    request.addfinalizer(
        lambda: delete_group_if_present_using_rest(
            zone_hostname,
            admin_credentials.username,
            admin_credentials.password,
            group_id,
        )
    )


def create_single_group_using_op_gui(
    selenium: SeleniumDrivers, browser_id: str, group_name: str
) -> None:
    click_create_group_button_in_panel(selenium, browser_id)
    input_name_into_input_box_on_main_groups_page(selenium, browser_id, text=group_name)
    confirm_name_input_on_main_groups_page(selenium, browser_id)


def see_groups_using_op_gui(
    selenium: SeleniumDrivers, user: str, group_list: list[str]
) -> None:
    option = "sees"

    for group in group_list:
        assert_group_exists(selenium, [user], option, group)


def rename_groups_using_op_gui(
    selenium: SeleniumDrivers,
    user: str,
    group_list: list[str],
    new_names: list[str],
) -> None:
    confirm_type = "enter"

    for group, new_name in zip(group_list, new_names):
        rename_group(selenium, user, group, new_name, confirm_type)


@repeat_failed(timeout=WAIT_FRONTEND)
def fail_to_see_groups_using_op_gui(
    selenium: SeleniumDrivers, user: str, group_list: list[str]
) -> None:
    option = "does not see"

    for group in group_list:
        assert_group_exists(selenium, [user], option, group)


def leave_groups_using_op_gui(
    selenium: SeleniumDrivers, user: str, group_list: list[str]
) -> None:
    for group in group_list:
        leave_group(selenium, user, group)


def _open_member_from_list(selenium: SeleniumDrivers, user: str, parent: str) -> None:
    where = "group"
    list_type = "users"
    subpage = "members"

    go_to_group_subpage(selenium, user, parent, subpage)
    click_element_in_members_list(selenium, user, user, where, list_type)


def assert_subgroups_using_op_gui(
    selenium: SeleniumDrivers, user: str, group_list: list[str], parent: str
) -> None:
    where = "group"

    _open_member_from_list(selenium, user, parent)
    for group in group_list:
        assert_element_is_member_of_parent_in_memberships(
            selenium, user, group, parent, where, where, where
        )


def fail_to_see_subgroups_using_op_gui(
    selenium: SeleniumDrivers, user: str, group_list: list[str], parent: str
) -> None:
    where = "group"

    _open_member_from_list(selenium, user, parent)
    for group in group_list:
        assert_element_is_not_member_of_parent_in_memberships(
            selenium, user, group, where, parent, where, where
        )


@repeat_failed(timeout=WAIT_FRONTEND)
def _create_group_token(
    selenium: SeleniumDrivers,
    user: str,
    user2: str,
    name: str,
    tmp_memory: TmpMemory,
    displays: dict[str, str],
    clipboard: Clipboard,
    member: str,
) -> None:
    item_type = "token"
    where = "group"
    button = f"Invite {member} using token"
    member += "s"
    modal = "Invite using token"
    subpage = "members"

    go_to_group_subpage(selenium, user, name, subpage)
    click_on_option_in_members_list_menu(selenium, user, button, where, member)
    copy_token_from_modal(selenium, user)
    close_alert_popup_if_present(selenium[user], AlertPopup.SUCCESSFULLY_COPIED)
    close_modal(selenium, user, modal)
    send_copied_item_to_other_users(
        user, item_type, [user2], tmp_memory, displays, clipboard
    )


@wt(
    parsers.re(
        r"(?P<user>\w+) invites (?P<user2>\w+) to group "
        r'"(?P<name>.*)" using Oneprovider web GUI'
    )
)
def create_group_token_to_invite_user_using_op_gui(
    selenium: SeleniumDrivers,
    user: str,
    user2: str,
    name: str,
    tmp_memory: TmpMemory,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:
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
    user: str,
    user2: str,
    name: str,
    tmp_memory: TmpMemory,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:
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
        r"user of (?P<browser_id>.*) joins group he was invited to in Onezone service"
    )
)
def join_group_using_op_gui(
    selenium: SeleniumDrivers, browser_id: str, tmp_memory: TmpMemory
) -> None:
    paste_and_consume_received_token(selenium, browser_id, tmp_memory)


def add_subgroups_using_op_gui(
    selenium: SeleniumDrivers,
    user: str,
    parent: str,
    group_list: list[str],
    tmp_memory: TmpMemory,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:
    for child in group_list:
        create_group_token_to_invite_group_using_op_gui(
            selenium,
            user,
            user,
            parent,
            tmp_memory,
            displays,
            clipboard,
        )
        add_element_with_copied_token(
            selenium,
            user,
            child,
            clipboard,
            displays,
        )


def remove_subgroups_using_op_gui(
    selenium: SeleniumDrivers,
    user: str,
    group_list: list[str],
    tmp_memory: TmpMemory,
    parent: str,
) -> None:
    member_type = "group"

    for child in group_list:
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
    selenium: SeleniumDrivers,
    user: str,
    group_list: list[str],
    new_names: list[str],
) -> None:
    text = "failed"

    for group, new_name in zip(group_list, new_names):
        rename_groups_using_op_gui(selenium, user, [group], [new_name])
        assert_error_modal_with_text_appeared(selenium, user, text)


def fail_to_add_subgroups_using_op_gui(
    selenium: SeleniumDrivers,
    user: str,
    parent: str,
    group_list: list[str],
    tmp_memory: TmpMemory,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:
    create_group_token_to_invite_group_using_op_gui(
        selenium,
        user,
        user,
        parent,
        tmp_memory,
        displays,
        clipboard,
    )
    for child in group_list:
        fail_to_add_element_with_copied_token(
            selenium,
            user,
            child,
            clipboard,
            displays,
        )
        wait_for_error_modal_to_disappear(selenium[user])


def get_group_id_from_groups_sidebar_list(
    selenium: SeleniumDrivers,
    browser_id: str,
    group_name: str,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> str:
    click_menu_button_for_group(selenium, browser_id, "Copy ID", group_name)
    return clipboard.paste(display=displays[browser_id])
