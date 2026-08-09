"""This module contains meta steps for operations on members page in Onezone
using web GUI
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import cast

from tests.gui.steps.common.common import wait_till_alert_popup_or_error_modal_disappear
from tests.gui.steps.modals.modal import (
    assert_element_text_in_modal,
    wt_wait_for_modal_to_appear,
)
from tests.gui.steps.onezone.groups import go_to_group_subpage
from tests.gui.steps.onezone.members import (
    _change_to_tab_name,
    _find_members_page,
    assert_member_is_in_parent_members_list,
    assert_privileges_in_members_subpage,
    click_element_in_members_list,
    click_member_checkbox,
    click_on_bulk_edit,
    click_on_option_in_members_list_menu,
    see_privileges_for_member,
    set_privileges_in_members_subpage_on_modal,
    try_setting_privileges_in_members_subpage,
)
from tests.gui.steps.onezone.spaces import click_on_option_of_space_on_left_sidebar_menu
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils import Modals, OZLoggedIn, Popups
from tests.gui.utils.common.popups.generic import AlertPopup
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    parse_elements_sequence,
)
from tests.gui.utils.onezone import PageName
from tests.gui.utils.onezone.members_subpage import MembersPage
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.entities_setup.spaces import WAIT_FRONTEND
from tests.utils.utils import repeat_failed


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) removes "(?P<member_name>.*)" '
        r'(?P<member_type>user|group) from "(?P<name>.*)" '
        r"(?P<where>cluster|group|harvester|space|automation) members"
    )
)
def remove_member_from_parent(
    selenium: SeleniumDrivers,
    browser_id: str,
    member_name: str,
    member_type: str,
    name: str,
    tmp_memory: TmpMemory,
    where: str,
) -> None:
    driver = selenium[browser_id]
    if where != "cluster":
        page_name = cast(PageName, _change_to_tab_name(where))
        oz_page = OZLoggedIn(selenium[browser_id])
        oz_page.open_panel(OZLoggedIn.get_page_class(page_name))
        main_page = getattr(oz_page, page_name)
        list_name = f"{where}s_list"
        getattr(main_page, list_name)[name]()
        getattr(main_page, list_name)[name].members()
    members_page = _find_members_page(driver, where)
    list_name = member_type + "s"
    (
        getattr(members_page, list_name)
        .items[member_name]
        .header.click_menu(selenium[browser_id])
    )

    if member_type == "user":
        modal_name = "remove user from "
    elif member_type == "group" and where != "group":
        modal_name = "remove group from "
    else:
        modal_name = "remove subgroup from "

    if where == "automation":
        where = "atm. inventory"
    modal_name += where

    Popups(driver).menu_popup_with_text.menu["Remove this member"]()
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    Modals(driver).remove_modal.remove()
    for popup_enum in (AlertPopup.MEMBER_ADDED, AlertPopup.GROUP_REMOVED_FROM_CLUSTER):
        try:
            popup = Popups(driver).alert_popups.get_alert_popup(popup_enum)
            wait_till_alert_popup_or_error_modal_disappear(
                selenium,
                popup.web_elem,
                lambda _, current_popup=popup: current_popup.close,  # type: ignore[misc]
            )
        except RuntimeError:
            pass


def fail_to_set_privileges_using_op_gui(
    user: str,
    space_name: str,
    member_name: str,
    member_type: str,
    config: str,
    selenium: SeleniumDrivers,
) -> None:
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
    user: str,
    space_name: str,
    member_name: str,
    member_type: str,
    config: str,
    selenium: SeleniumDrivers,
) -> None:
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
    user: str, space_name: str, selenium: SeleniumDrivers
) -> None:
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
    user: str, space_name: str, member_name: str, selenium: SeleniumDrivers
) -> None:
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
    selenium: SeleniumDrivers, user: str, space_name: str, group_name: str
) -> None:
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


@repeat_failed(timeout=WAIT_FRONTEND)
def _assert_message_and_bulk_edit_btn(
    members_page: MembersPage, expected_message: str
) -> None:
    message_groups = members_page.lack_groups_view_privileges.text
    message_users = members_page.lack_users_view_privileges.text
    bulk_edit_button = members_page.bulk_edit_button

    error_message = (
        "The message about lack of privileges to view membership is not visible"
    )
    assert message_groups == expected_message, f"{error_message} for groups"
    assert message_users == expected_message, f"{error_message} for users"
    assert (
        not bulk_edit_button.is_enabled()
    ), "Bulk edit button is supposed to be disabled"


@wt(
    parsers.re(
        rf"users? of (?P<browser_ids>{ELEMENTS_SEQUENCE_PATTERN}) cannot view "
        r'group "(?P<group>.*)" membership due to lack of privileges'
    ),
    converters={
        "browser_ids": parse_elements_sequence,
    },
)
def assert_cannot_view_group_membership(
    selenium: SeleniumDrivers, browser_ids: list[str], group: str
) -> None:
    for browser_id in browser_ids:
        driver = selenium[browser_id]
        oz_page = OZLoggedIn(driver)
        go_to_group_subpage(selenium, browser_id, group, "members")

        members_page = oz_page.groups.members_page
        expected_message = "Insufficient privileges to access this resource."

        _assert_message_and_bulk_edit_btn(members_page, expected_message)


@wt(
    parsers.re(
        r"user of (?P<browser_id>\w+) changes privileges for"
        r' (?P<member_type>user|group) "(?P<member_name>\w+)" in group'
        r' "(?P<group_name>\w+)" members subpage into following:\n(?P<config>(.|\s)*)'
    )
)
def choose_member_and_set_privileges_on_groups_subpage(
    selenium: SeleniumDrivers,
    group_name: str,
    browser_id: str,
    member_name: str,
    member_type: str,
    config: str,
) -> None:
    go_to_group_subpage(selenium, browser_id, group_name, "members")
    click_element_in_members_list(
        selenium, browser_id, member_name, "group", f"{member_type}s"
    )
    see_privileges_for_member(selenium, browser_id, "group", member_type, member_name)
    click_member_checkbox(selenium, browser_id, member_name, f"{member_type}s")
    click_on_bulk_edit(browser_id, selenium)
    set_privileges_in_members_subpage_on_modal(selenium, browser_id, config)


@wt(
    parsers.re(
        r"user of (?P<browser_id>\w+) sees following "
        r"(?P<option>effective |)privileges for "
        r'(?P<member_type>user|group) "(?P<member_name>[^"]+)" in group '
        r'"(?P<group_name>[^"]+)" members subpage:\n(?P<config>(.|\s)*)'
    )
)
def choose_member_and_assert_privileges_on_groups_subpage(
    selenium: SeleniumDrivers,
    group_name: str,
    browser_id: str,
    member_name: str,
    member_type: str,
    option: str,
    config: str,
) -> None:
    go_to_group_subpage(selenium, browser_id, group_name, "members")
    click_element_in_members_list(
        selenium, browser_id, member_name, "group", f"{member_type}s"
    )
    assert_privileges_in_members_subpage(
        selenium, browser_id, member_name, member_type, "group", config, option
    )
