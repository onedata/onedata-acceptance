"""This module contains meta steps for operations on members page in Onezone
using web GUI
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Any

from tests.gui.steps.modals.modal import assert_element_text_in_modal
from tests.gui.steps.onezone.members import (
    assert_member_is_in_parent_members_list,
    assert_privileges_in_members_subpage,
    click_element_in_members_list,
    click_on_option_in_members_list_menu,
    try_setting_privileges_in_members_subpage,
)
from tests.gui.steps.onezone.spaces import click_on_option_of_space_on_left_sidebar_menu
from tests.conftest import SeleniumDrivers


def fail_to_set_privileges_using_op_gui(
    user: Any,
    space_name: Any,
    member_name: Any,
    member_type: Any,
    config: Any,
    selenium: SeleniumDrivers,
) -> Any:
    button = "Members"
    option = "fails to set"
    list_type = "users"
    where = "space"

    click_on_option_of_space_on_left_sidebar_menu(selenium, user, space_name, button)
    click_element_in_members_list(selenium, user, member_name, where, list_type)
    try_setting_privileges_in_members_subpage(
        selenium,
        user,
        member_name,
        member_type,
        where,
        config,
        option,
    )


def assert_privileges_in_space_using_op_gui(
    user: Any,
    space_name: Any,
    member_name: Any,
    member_type: Any,
    config: Any,
    selenium: SeleniumDrivers,
) -> Any:
    option = "Members"
    list_type = "users"
    where = "space"
    click_on_option_of_space_on_left_sidebar_menu(selenium, user, space_name, option)
    click_element_in_members_list(selenium, user, member_name, where, list_type)
    assert_privileges_in_members_subpage(
        selenium,
        user,
        member_name,
        member_type,
        where,
        config,
        True,
    )


def fail_to_create_invitation_in_space_using_op_gui(
    user: Any, space_name: Any, selenium: SeleniumDrivers
) -> Any:
    option = "Members"
    button = "Invite user using token"
    where = "space"
    member = "users"
    modal = "Invite using token"
    text = "This resource could not be loaded"
    element = "alert"
    click_on_option_of_space_on_left_sidebar_menu(selenium, user, space_name, option)
    click_on_option_in_members_list_menu(selenium, user, button, where, member)
    assert_element_text_in_modal(selenium, user, modal, text, element)


def assert_not_user_in_space_using_op_gui(
    user: Any, space_name: Any, member_name: Any, selenium: SeleniumDrivers
) -> Any:
    option = "does not see"
    member_type = "user"
    parent_type = "space"
    assert_member_is_in_parent_members_list(
        selenium,
        user,
        option,
        member_name,
        member_type,
        space_name,
        parent_type,
    )


def assert_group_in_space_using_op_gui(
    selenium: SeleniumDrivers, user: Any, space_name: Any, group_name: Any
) -> Any:
    option1 = "Members"
    option2 = "sees"
    member_type = "group"
    parent_type = "space"
    click_on_option_of_space_on_left_sidebar_menu(selenium, user, space_name, option1)
    assert_member_is_in_parent_members_list(
        selenium,
        user,
        option2,
        group_name,
        member_type,
        space_name,
        parent_type,
    )
