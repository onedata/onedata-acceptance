"""This module contains gherkin steps to run acceptance tests featuring members
management in onezone web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time
from typing import cast

import yaml
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.meta_steps.onezone.common import search_for_members
from tests.gui.steps.modals.modal import (
    assert_element_text,
    wt_wait_for_modal_to_appear,
)
from tests.gui.steps.onepanel.common import wt_click_on_subitem_for_item
from tests.gui.steps.onezone.automation.automation_basic import (
    click_on_option_of_inventory_on_left_sidebar_menu,
)
from tests.gui.steps.onezone.clusters import click_on_record_in_clusters_menu
from tests.gui.steps.onezone.groups import go_to_group_subpage
from tests.gui.steps.onezone.harvesters.discovery import (
    click_on_option_of_harvester_on_left_sidebar_menu,
)
from tests.gui.steps.onezone.spaces import (
    click_element_on_lists_on_left_sidebar_menu,
    click_on_option_of_space_on_left_sidebar_menu,
)
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils import Modals, Onepanel, OZLoggedIn, Popups
from tests.gui.utils.common.privilege_tree import PrivilegeTree
from tests.gui.utils.core.web_objects import PageObjectsSequence
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    parse_elements_sequence,
    transform,
)
from tests.gui.utils.onezone import PageName
from tests.gui.utils.onezone.groups.groups_page import GroupsPage
from tests.gui.utils.onezone.members_subpage import MembershipRow, MembersPage
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import element_has_class, repeat_failed

MENU_ELEM_TO_TAB_NAME = {
    "space": "data",
    "harvester": "discovery",
    "automation": "automation",
    "inventory": "automation",
}


def _change_to_tab_name(element: str) -> str:
    return MENU_ELEM_TO_TAB_NAME.get(element, element + "s")


def _find_members_page(driver: WebDriver, where: str) -> MembersPage:
    tab_name = _change_to_tab_name(where)
    if tab_name == "clusters":
        return Onepanel(driver).content.members
    page_name = cast(PageName, tab_name)
    tab = getattr(OZLoggedIn(driver), page_name)
    return tab.members_page


def _change_membership_to_name(membership_type: str, subject_type: str) -> str:
    if not subject_type.endswith("s"):
        subject_type += "s"
    return membership_type + "_" + subject_type


def get_privilege_tree(
    selenium: SeleniumDrivers,
    browser_id: str,
    where: str,
    list_type: str,
    member_name: str,
) -> PrivilegeTree:
    driver = selenium[browser_id]
    page = _find_members_page(driver, where)
    elem = getattr(page, list_type).items[member_name]

    if not element_has_class(elem.web_elem, "active"):
        elem.web_elem.click()

    WebDriverWait(driver, WAIT_FRONTEND).until(
        lambda _: "active" in elem.web_elem.get_attribute("class"),
        message=f"did not manage to expand {list_type} panel of {member_name}",
    )

    return elem.privilege_tree


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) sees that "(?P<member_name>.*)" '
        r"(?P<member_type>user|group) is member of "
        r'"(?P<parent_name>.*)" (?P<parent_type>space|group) '
        r"in (?P<where>space|group) memberships mode"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_element_is_member_of_parent_in_memberships(
    selenium: SeleniumDrivers,
    browser_id: str,
    member_name: str,
    parent_name: str,
    member_type: str,
    parent_type: str,
    where: str,
) -> None:
    driver = selenium[browser_id]
    where = cast(PageName, _change_to_tab_name(where))
    tab = getattr(OZLoggedIn(driver), where)
    records = tab.members_page.memberships

    def fun(_record: MembershipRow, member_index: int) -> bool:
        if member_type != "user":
            return True
        if member_index == 0:
            return True
        return False

    if not search_for_members(driver, records, member_name, parent_name, fun):
        raise RuntimeError(
            f'not found "{member_name}" {member_type} as a member of'
            f' "{parent_name}" {parent_type}'
        )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) does not see that "
        r'"(?P<member_name>.*)" (?P<member_type>user|group) is '
        r'member of "(?P<parent_name>.*)" (?P<parent_type>space|group) '
        r"in (?P<where>space|group) memberships mode"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_element_is_not_member_of_parent_in_memberships(
    selenium: SeleniumDrivers,
    browser_id: str,
    member_name: str,
    where: str,
    parent_name: str,
    member_type: str,
    parent_type: str,
) -> None:
    driver = selenium[browser_id]
    where = cast(PageName, _change_to_tab_name(where))
    tab = getattr(OZLoggedIn(driver), where)
    records = tab.members_page.memberships

    def fun(_record: MembershipRow, member_index: int) -> bool:
        if member_type != "user":
            raise RuntimeError(
                f'found "{member_name}" {member_type} as a member of'
                f' "{parent_name}" {parent_type}'
            )
        if member_index == 0:
            raise RuntimeError(
                f'found "{member_name}" {member_type} as a member of'
                f' "{parent_name}" {parent_type}'
            )
        return False

    search_for_members(driver, records, member_name, parent_name, fun)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees (?P<number>.*) "
        r"membership rows? in (?P<where>space|group) memberships mode"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_count_membership_rows(
    selenium: SeleniumDrivers, browser_id: str, number: str, where: str
) -> None:
    driver = selenium[browser_id]
    where = cast(PageName, _change_to_tab_name(where))
    tab = getattr(OZLoggedIn(driver), where)
    records = tab.members_page.memberships
    count_records = len(records)

    assert count_records == int(
        number
    ), f"found {number} membership rows instead of {count_records}"


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees "
        r"(?P<number_direct_groups>.*) direct, "
        r"(?P<number_effective_groups>.*) effective groups and "
        r"(?P<number_direct_users>.*) direct, "
        r"(?P<number_effective_users>.*) effective users in space members tile"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_all_members_number_in_space_members_tile(
    selenium: SeleniumDrivers,
    browser_id: str,
    number_direct_groups: str,
    number_effective_groups: str,
    number_direct_users: str,
    number_effective_users: str,
) -> None:
    direct = "direct"
    effective = "effective"
    groups = "groups"
    users = "users"

    assert_members_number_in_space_members_tile(
        selenium, browser_id, number_direct_groups, direct, groups
    )
    assert_members_number_in_space_members_tile(
        selenium,
        browser_id,
        number_effective_groups,
        effective,
        groups,
    )
    assert_members_number_in_space_members_tile(
        selenium, browser_id, number_direct_users, direct, users
    )
    assert_members_number_in_space_members_tile(
        selenium, browser_id, number_effective_users, effective, users
    )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees (?P<number>\d+) "
        r"(?P<membership_type>direct|effective) "
        r"(?P<subject_type>groups?|users?) in space members tile"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_members_number_in_space_members_tile(
    selenium: SeleniumDrivers,
    browser_id: str,
    number: str,
    membership_type: str,
    subject_type: str,
) -> None:
    driver = selenium[browser_id]
    members_tile = OZLoggedIn(driver).data.overview_page.members_tile
    name = _change_membership_to_name(membership_type, subject_type)
    members_count = getattr(members_tile, name)
    error_msg = (
        f"found {number} {membership_type} {subject_type} instead of {members_count}"
    )
    assert int(members_count) == int(number), error_msg


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) clicks on "(?P<member_name>.*)" '
        r"member relation menu button to "
        r'"(?P<name>.*)" (?P<where>space|group)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_relation_menu_button(
    selenium: SeleniumDrivers, browser_id: str, member_name: str, name: str, where: str
) -> None:
    driver = selenium[browser_id]
    where = cast(PageName, _change_to_tab_name(where))
    tab = getattr(OZLoggedIn(driver), where)
    records = tab.members_page.memberships

    def click_on_menu(record: MembershipRow, member_index: int) -> bool:
        record.relations[member_index].click_relation_menu_button(driver)
        return True

    search_for_members(driver, records, member_name, name, click_on_menu)


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) clicks on "(?P<option>.*)" '
        r"in (?P<where>space|group) membership relation menu"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_relation_menu_button(
    selenium: SeleniumDrivers, browser_id: str, option: str
) -> None:
    driver = selenium[browser_id]
    Popups(driver).membership_relation_menu.options[option].click()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) clicks "(?P<type_name>.*)" '
        r"(?P<type>user|group) to close his dropdown list in "
        r'"(?P<member_name>.*)" (?P<where>space|group|cluster|harvester) '
        r"members (?P<list_type>users|groups) list"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_element_to_close_its_dropdown(
    selenium: SeleniumDrivers,
    browser_id: str,
    type_name: str,
    where: str,
    list_type: str,
) -> None:
    driver = selenium[browser_id]
    page = _find_members_page(driver, where)
    getattr(page, list_type).items[type_name].header.click()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) clicks "(?P<member_name>.*)" '
        r'(?P<member_type>user|group) in "(?P<name>.*)" '
        r"(?P<where>space|group|cluster|harvester|automation) members "
        r"(?P<list_type>users|groups) list"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def click_element_in_members_list(
    selenium: SeleniumDrivers,
    browser_id: str,
    member_name: str,
    where: str,
    list_type: str,
) -> None:
    driver = selenium[browser_id]
    page = _find_members_page(driver, where)

    members_list = getattr(page, list_type).items
    for member in members_list:
        if member.is_opened():
            member.header.click()

    members_list[member_name].click()


@wt(
    parsers.parse(
        "user of {browser_id} clicks on "
        '"generate an invitation token" text in group '
        '"{group}" members {member} list'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_generate_token_in_subgroups_list(
    selenium: SeleniumDrivers, browser_id: str, group: str, member: str
) -> None:
    oz_page = OZLoggedIn(selenium[browser_id])
    oz_page.open_panel(GroupsPage)
    page = oz_page.groups
    page.groups_list[group]()
    page.groups_list[group].members()
    getattr(page.main_page.members, member).generate_token()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) clicks on "(?P<button>.*)" button '
        r"in (?P<member>users|groups) list menu in "
        r'"(?P<name>.*)" (?P<where>group|space|cluster|harvester'
        r"|automation) members view"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_in_members_list_menu(
    selenium: SeleniumDrivers,
    browser_id: str,
    button: str,
    where: str,
    member: str,
) -> None:
    driver = selenium[browser_id]
    page = _find_members_page(driver, where)
    getattr(page, member).header.menu_button()
    Popups(driver).menu_popup_with_text.menu[button]()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees that area with "
        r"(?P<who>user|group) invitation token has appeared"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_token_area_appeared(
    selenium: SeleniumDrivers, browser_id: str, who: str, tmp_memory: TmpMemory
) -> None:
    modal_name = f"invite {who} using token"
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)


@wt(parsers.parse("user of {browser_id} sees non-empty token in token area"))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_generated_token_is_present(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    try:
        text = Modals(selenium[browser_id]).invite_using_token.token
        assert len(text) > 0, "Token is empty, while it should be non-empty"
    except RuntimeError as exc:
        raise RuntimeError("No token area found on page") from exc


@wt(parsers.re(r"user of (?P<browser_id>.*) copies invitation token from modal"))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_token_from_modal(selenium: SeleniumDrivers, browser_id: str) -> None:
    Modals(selenium[browser_id]).invite_using_token.copy()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) (?P<option>does not see|sees) "
        r'"(?P<child>.*)" as "(?P<parent>.*)" child'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_element_is_groups_child(
    selenium: SeleniumDrivers,
    browser_id: str,
    option: str | bool,
    child: str,
    parent: str,
) -> None:
    oz_page = OZLoggedIn(selenium[browser_id])
    oz_page.open_panel(GroupsPage)
    page = oz_page.groups
    page.groups_list[parent]()
    page.groups_list[parent].members()

    try:
        page.members_page.groups.items[child]
    except RuntimeError:
        assert option == "does not see", f'"{child}" is not "{parent}" child'
    else:
        assert option == "sees", f'"{child}" is "{parent}" child'


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) (?P<option>does not see|sees) "
        r'"(?P<member_name>.*)" (?P<member_type>user|group) '
        r'on "(?P<parent_name>.*)" ('
        r"?P<parent_type>user|group|space|cluster) members list"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_member_is_in_parent_members_list(
    selenium: SeleniumDrivers,
    browser_id: str,
    option: str,
    member_name: str,
    member_type: str,
    parent_name: str,
    parent_type: str,
) -> None:
    driver = selenium[browser_id]
    page = _find_members_page(driver, parent_type)

    if option == "sees":
        error_message = (
            f'{member_type} "{member_name}" not found on'
            f' {parent_type} "{parent_name}" members list'
        )
        try:
            if member_type == "user":
                assert page.users.items[member_name].is_displayed(), error_message
            else:
                assert page.groups.items[member_name].is_displayed(), error_message
        except RuntimeError as exc:
            raise AssertionError(error_message) from exc

    else:
        error_message = (
            f'{member_type} "{member_name}" found on'
            f' {parent_type} "{parent_name}" members list'
        )
        try:
            if member_type == "user":
                assert not page.users.items[member_name].is_displayed(), error_message
            else:
                assert not page.groups.items[member_name].is_displayed(), error_message
        except RuntimeError:
            pass


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) (?P<option>does not see|sees) "
        r'"(?P<username>.*)" user on "(?P<space_name>.*)" space members list'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def check_user_in_space_members_list(
    selenium: SeleniumDrivers,
    browser_id: str,
    option: str,
    username: str,
    space_name: str,
) -> None:
    driver = selenium[browser_id]
    page = OZLoggedIn(driver).data
    page.spaces_headers_list[space_name]()
    page.spaces_list[space_name].members()
    try:
        page.members_page.users.items[username]
    except RuntimeError:
        assert (
            option == "does not see"
        ), f'user "{username}" not found on "{space_name}" space members list'
    else:
        assert (
            option == "sees"
        ), f'user "{username}" found on "{space_name}" space members list'


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) clicks "(?P<option>( |.)*)" for '
        r'"(?P<username>.*)" user in users list'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_member_option_on_members_page(
    selenium: SeleniumDrivers, browser_id: str, option: str, username: str
) -> None:
    driver = selenium[browser_id]
    page = OZLoggedIn(driver).data.members_page
    page.users.items[username].click_member_menu_button(driver)
    Popups(driver).menu_popup_with_text.menu[option]()


@wt(
    parsers.re(
        rf"user of (?P<browser_id>.*) sees "
        rf"(?P<options>{ELEMENTS_SEQUENCE_PATTERN}) (is|are) "
        r'(?P<state>enabled|disabled) for "(?P<username>.*)" user in users list'
    ),
    converters={"options": parse_elements_sequence},
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_options_for_user_are_enabled_or_disabled(
    selenium: SeleniumDrivers,
    browser_id: str,
    options: list[str],
    username: str,
    state: str,
) -> None:
    driver = selenium[browser_id]
    page = OZLoggedIn(driver).data.members_page
    page.users.items[username].click_member_menu_button(driver)

    for option in options:
        enabled = Popups(driver).menu_popup_with_text.menu[option].is_enabled()
        error_msg = f"Popup {option} is in invalid state"
        if state == "enabled":
            assert enabled, error_msg
        else:
            assert not enabled, error_msg


def _get_cluster_members(
    selenium: SeleniumDrivers, browser_id: str
) -> PageObjectsSequence:
    driver = selenium[browser_id]
    where = "cluster"
    members_page = _find_members_page(driver, where)
    list_name = "users"
    return getattr(members_page, list_name).items


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) sees "(?P<member_name>.*)" user in cluster members'
    )
)
@repeat_failed(timeout=WAIT_BACKEND * 4)
def assert_user_in_cluster_members_page(
    selenium: SeleniumDrivers, browser_id: str, member_name: str
) -> None:
    cluster_members = _get_cluster_members(selenium, browser_id)

    assert (
        member_name in cluster_members
    ), f"{member_name} user is not found in cluster members list"


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) does not see "(?P<member_name>.*)" '
        r"user in cluster members"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_user_not_in_cluster_members_page(
    selenium: SeleniumDrivers, browser_id: str, member_name: str
) -> None:
    cluster_members = _get_cluster_members(selenium, browser_id)

    assert (
        member_name not in cluster_members
    ), f"{member_name} user is found in cluster members list"


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) copies "(?P<group>.*)" '
        r"(?P<who>user|group) invitation token"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_invitation_token(
    selenium: SeleniumDrivers,
    browser_id: str,
    group: str,
    who: str,
    tmp_memory: TmpMemory,
) -> None:
    driver = selenium[browser_id]
    oz_page = OZLoggedIn(driver)
    oz_page.open_panel(GroupsPage)
    page = oz_page.groups
    page.groups_list[group]()

    getattr(page.main_page.members, who + "s").header.menu_button()
    button = f"Invite {who} using token"

    Popups(driver).menu_popup_with_text.menu[button].click()

    wt_wait_for_modal_to_appear(selenium, browser_id, button, tmp_memory)
    Modals(selenium[browser_id]).invite_using_token.copy()
    Modals(selenium[browser_id]).invite_using_token.close()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) gets group "(?P<group>.*)" '
        r"(?P<who>user|group) invitation token"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def get_invitation_token(
    selenium: SeleniumDrivers,
    browser_id: str,
    group: str,
    who: str,
    tmp_memory: TmpMemory,
) -> None:
    driver = selenium[browser_id]
    page = OZLoggedIn(driver).groups
    page.groups_list[group]()
    page.main_page.menu_button()
    Popups(driver).menu_popup_with_text.menu["Invite " + who]()
    token = page.members_page.token.token
    tmp_memory[browser_id]["token"] = token


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) (?P<option>sets|fails to set) "
        r'following privileges for "(?P<member_name>.*)" '
        r"(?P<member_type>user|group) "
        r"in (?P<where>space|group|harvester|cluster|automation) members "
        r"subpage:\n(?P<config>(.|\s)*)"
    )
)
def try_setting_privileges_in_members_subpage(
    selenium: SeleniumDrivers,
    browser_id: str,
    member_name: str,
    member_type: str,
    where: str,
    config: str,
    option: str,
) -> None:
    try:
        assert_privileges_in_members_subpage(
            selenium,
            browser_id,
            member_name,
            member_type,
            where,
            config,
            True,
        )
    except AssertionError:
        button = "Save"
        member_type_new = member_type + "s"
        privileges = yaml.load(config, yaml.Loader)
        tree = get_privilege_tree(
            selenium,
            browser_id,
            where,
            member_type_new,
            member_name,
        )
        result = tree.set_privileges(selenium, browser_id, privileges, True)
        if option == "sets":
            click_button_on_element_header_in_members_and_wait(
                selenium, browser_id, button, where, tree
            )
        else:
            assert (
                not result
            ), f"Modify {member_type} privilege on {where} page should not be possible"


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sets all privileges (?P<value>true|false) for "
        r'"(?P<member_name>.*)" (?P<member_type>user|group) '
        r"in (?P<where>space|group|harvester|cluster|automation) members subpage"
    )
)
def set_all_privileges_true_in_members_subpage(
    selenium: SeleniumDrivers,
    browser_id: str,
    member_name: str,
    value: str,
    member_type: str,
    where: str,
) -> None:
    option = "Save"
    member_type_new = member_type + "s"

    tree = get_privilege_tree(
        selenium,
        browser_id,
        where,
        member_type_new,
        member_name,
    )
    if value == "true":
        tree.set_all_true()
    elif value == "false":
        tree.set_all_false()

    click_button_on_element_header_in_members(selenium, browser_id, option, where)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sets following privileges for "
        r'"(?P<member_name>.*)" (?P<member_type>user|group) '
        r"in (?P<where>space|group|harvester|cluster) members subpage "
        r"when all other (?P<are_granted>are|are not) granted:\n(?P<config>(.|\s)*)"
    )
)
def set_some_privileges_in_members_subpage_other_granted(
    selenium: SeleniumDrivers,
    browser_id: str,
    member_name: str,
    member_type: str,
    where: str,
    are_granted: str,
    config: str,
) -> None:
    option = "sets"
    tree = get_privilege_tree(
        selenium,
        browser_id,
        where,
        member_type + "s",
        member_name,
    )

    if are_granted == "are":
        tree.set_all_true()
    elif are_granted == "are not":
        tree.set_all_false()

    try_setting_privileges_in_members_subpage(
        selenium,
        browser_id,
        member_name,
        member_type,
        where,
        config,
        option,
    )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sets following privileges on "
        r"modal:\n(?P<config>(.|\s)*)"
    )
)
def set_privileges_in_members_subpage_on_modal(
    selenium: SeleniumDrivers, browser_id: str, config: str
) -> None:
    driver = selenium[browser_id]
    privileges = yaml.load(config, yaml.Loader)
    tree = Modals(driver).change_privileges.privilege_tree
    tree.set_privileges(selenium, browser_id, privileges)
    Modals(driver).change_privileges.save_button.click()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees following "
        r"(?P<option>effective |)privileges of "
        r'"(?P<member_name>.*)" (?P<member_type>user|group) '
        r"in (?P<where>space|group|harvester|automation|cluster) "
        r"members subpage:\n(?P<config>(.|\s)*)"
    )
)
def assert_privileges_in_members_subpage(
    selenium: SeleniumDrivers,
    browser_id: str,
    member_name: str,
    member_type: str,
    where: str,
    config: str,
    option: str | bool,
) -> None:
    member_type = member_type + "s"
    privileges = yaml.load(config, yaml.Loader)
    tree = get_privilege_tree(selenium, browser_id, where, member_type, member_name)
    is_direct_privileges = option != "effective "
    # wait for set privileges to be visible in gui
    try:
        tree.assert_privileges(selenium, browser_id, privileges, is_direct_privileges)
    except AssertionError:
        time.sleep(2)
        tree.assert_privileges(selenium, browser_id, privileges, is_direct_privileges)
    driver = selenium[browser_id]
    page = _find_members_page(driver, where)
    page.close_member(driver)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees following privileges on "
        r"modal:\n(?P<config>(.|\s)*)"
    )
)
def assert_privileges_in_members_subpage_on_modal(
    selenium: SeleniumDrivers, browser_id: str, config: str
) -> None:
    driver = selenium[browser_id]
    privileges = yaml.load(config, yaml.Loader)
    tree = Modals(driver).change_privileges.privilege_tree
    tree.assert_privileges(selenium, browser_id, privileges)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) clicks (?P<option>Save|Discard) "
        r'button for "(?P<member_name>.*)" (?P<member_type>user|group) '
        r"in (?P<where>space|group|cluster|harvester) members subpage"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_on_element_header_in_members(
    selenium: SeleniumDrivers, browser_id: str, option: str, where: str
) -> None:
    driver = selenium[browser_id]
    option_selector = f".{option.lower()}-btn"
    page = _find_members_page(driver, where)
    page.close_member(driver)
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, ".list-header-row " + option_selector).click()


def click_button_on_element_header_in_members_and_wait(
    selenium: SeleniumDrivers,
    browser_id: str,
    option: str,
    where: str,
    tree: PrivilegeTree,
) -> None:
    driver = selenium[browser_id]
    option_selector = f".{option.lower()}-btn"
    page = _find_members_page(driver, where)

    driver.execute_script("window.scrollBy(0,0)")
    driver.find_element(By.CSS_SELECTOR, ".list-header-row " + option_selector).click()
    tree.wait_for_load_privileges()
    page.close_member(driver)


@wt(
    parsers.re(
        rf"user of (?P<browser_id>.*) sees "
        rf"(?P<labels>{ELEMENTS_SEQUENCE_PATTERN}) status "
        r'labels? for "(?P<member_name>.*)" (?P<member_type>user|group) '
        r"in (?P<where>space|group|cluster|harvester) members subpage"
    ),
    converters={"labels": parse_elements_sequence},
)
@repeat_failed(timeout=WAIT_FRONTEND)
def check_status_labels_for_member_of_space(
    selenium: SeleniumDrivers,
    browser_id: str,
    labels: list[str],
    member_name: str,
    member_type: str,
    where: str,
) -> None:
    driver = selenium[browser_id]

    member_type = member_type + "s"
    page = _find_members_page(driver, where)
    member = getattr(page, member_type).items[member_name]
    status_labels = [x.text for x in member.status_labels]

    assert len(status_labels) == len(labels), f"Invalid status labels for {member_name}"
    for x in labels:
        assert x in status_labels, f'"{x}" label not found for {member_name}'


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees "
        r"(?P<alert_text>Insufficient privileges) alert "
        r'for "(?P<member_name>.*)" (?P<member_type>user|group) '
        r"in (?P<where>space|group|cluster) members subpage"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def see_insufficient_permissions_alert_for_member(
    selenium: SeleniumDrivers,
    browser_id: str,
    where: str,
    member_name: str,
    member_type: str,
    alert_text: str,
) -> None:
    driver = selenium[browser_id]
    member_type = member_type + "s"
    page = _find_members_page(driver, where)

    members_list = getattr(page, member_type)
    forbidden_alert = members_list.items[member_name].forbidden_alert.text
    assert alert_text in forbidden_alert, f'alert with text "{alert_text}" not found'


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees "
        r'"(?P<alert_text>Insufficient privileges)" alert '
        r"in (?P<where>space|group|cluster|harvester) members subpage"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_insufficient_permission_alert_in_members_subpage(
    selenium: SeleniumDrivers, browser_id: str, where: str, alert_text: str
) -> None:
    driver = selenium[browser_id]
    page = _find_members_page(driver, where)
    assert_element_text(page, "forbidden_alert", alert_text)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees privileges for "
        r'"(?P<member_name>.*)" (?P<member_type>user|group) '
        r"in (?P<where>space|group|cluster|harvester|automation) members subpage"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def see_privileges_for_member(
    selenium: SeleniumDrivers,
    browser_id: str,
    where: str,
    member_type: str,
    member_name: str,
) -> None:
    driver = selenium[browser_id]
    member_type = member_type + "s"
    page = _find_members_page(driver, where)
    members_list = getattr(page, member_type)
    member_item_row = members_list.items[member_name]

    assert member_item_row.are_privileges_visible(), "not found privileges"


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) (?P<option>does not see|sees) "
        r'"(?P<member_name>.*)" (?P<member_type>user|group) '
        r'in "(?P<item_name>.*)" (?P<item_type>automation|harvester) '
        r"members (users|groups) list"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def check_element_in_members_subpage(
    selenium: SeleniumDrivers,
    browser_id: str,
    option: str,
    member_name: str,
    member_type: str,
    item_type: str,
) -> None:
    if item_type == "harvester":
        item_type = "discovery"

    driver = selenium[browser_id]
    page = getattr(OZLoggedIn(driver), item_type)
    member_list = getattr(page.members_page, f"{member_type}s").items
    if option == "sees":
        try:
            error_message = f"{member_name} {member_type} not found"
            assert member_name in member_list, error_message
        except RuntimeError as exc:
            raise AssertionError(error_message) from exc
    else:
        try:
            assert member_name not in member_list, f"{member_name} {member_type}"
        except RuntimeError:
            pass


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees (?P<number>\d+) "
        r"(?P<member_type>user|group)s? in "
        r"(?P<where>space|group|cluster|harvester) members subpage"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def check_list_length_on_members_subpage(
    selenium: SeleniumDrivers,
    browser_id: str,
    member_type: str,
    where: str,
    number: str,
) -> None:
    driver = selenium[browser_id]
    member_type = member_type + "s"
    page = _find_members_page(driver, where)
    members_list = getattr(page, member_type)
    error_msg = f"Wrong number of {member_type} in {where} members subpage"
    assert len(members_list.items) == int(number), error_msg


@wt(
    parsers.parse(
        'user of {browser_id} sees that {item_type} "{item_name}" has '
        'following privilege configuration for {target} "{name}":\n{config}'
    )
)
def assert_privilege_config_for_user(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_name: str,
    item_type: str,
    name: str,
    config: str,
    target: str,
    hosts: Hosts,
) -> None:
    list_type = target + "s"

    option = item_type + "s" if item_type != "inventory" else "automation"
    option2 = "Members"

    data = yaml.load(config, yaml.Loader)
    privileges = data["privileges"]

    if item_type != "cluster":
        click_element_on_lists_on_left_sidebar_menu(
            selenium, browser_id, option, item_name
        )

    if item_type == "space":
        click_on_option_of_space_on_left_sidebar_menu(
            selenium, browser_id, item_name, option2
        )
    elif item_type == "harvester":
        click_on_option_of_harvester_on_left_sidebar_menu(
            selenium, browser_id, item_name, option2
        )
    elif item_type == "inventory":
        click_on_option_of_inventory_on_left_sidebar_menu(
            selenium, browser_id, item_name, option2
        )
    elif item_type == "group":
        go_to_group_subpage(selenium, browser_id, item_name, option2.lower())
    elif item_type == "cluster":
        click_on_record_in_clusters_menu(selenium, browser_id, item_name, hosts)
        wt_click_on_subitem_for_item(
            selenium, [browser_id], option, option2, item_name, hosts
        )

    click_element_in_members_list(selenium, browser_id, name, item_type, list_type)
    privilege_tree = get_privilege_tree(
        selenium, browser_id, item_type, list_type, name
    )
    privilege_tree.assert_privileges(selenium, browser_id, privileges)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) clicks on (?P<member_type>users|groups) checkbox"
    )
)
def click_on_bulk_checkbox(
    browser_id: str, member_type: str, selenium: SeleniumDrivers
) -> None:
    driver = selenium[browser_id]
    page = OZLoggedIn(driver).groups.members_page
    members_list = getattr(page, member_type)
    members_list.header.checkbox.click()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) clicks on "(?P<member_name>.*)" '
        r"(?P<list_type>users|groups) checkbox"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_member_checkbox(
    selenium: SeleniumDrivers, browser_id: str, member_name: str, list_type: str
) -> None:
    driver = selenium[browser_id]
    page = OZLoggedIn(driver).groups.members_page
    page.close_member(driver)
    members = getattr(page, list_type)
    item_checkbox = members.items[member_name].header.checkbox
    item_checkbox.click()


@wt(parsers.parse("user of {browser_id} clicks on bulk edit button"))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_bulk_edit(browser_id: str, selenium: SeleniumDrivers) -> None:
    driver = selenium[browser_id]
    OZLoggedIn(driver).groups.members_page.bulk_edit_button.click()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) sees "(?P<alert_text>As a '
        r"space owner, you are authorized to perform all operations, "
        r'regardless of the assigned privileges.)" warning '
        r'for "(?P<username>.*)" user in space members subpage'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_ownership_privileges_warning_appeared_for_user(
    selenium: SeleniumDrivers, browser_id: str, username: str, alert_text: str
) -> None:
    driver = selenium[browser_id]
    members_list = OZLoggedIn(driver).data.members_page.users
    error_msg = f'alert with text "{alert_text}" not found'
    ownership_warning = members_list.items[username].ownership_warning.text
    assert alert_text in ownership_warning, error_msg


@wt(
    parsers.parse(
        "user of {browser_id} sees {number} {item_type} in "
        "Onezone clusters members page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_number_items_in_members_onezone(
    selenium: SeleniumDrivers, browser_id: str, number: str, item_type: str
) -> None:
    driver = selenium[browser_id]
    page = OZLoggedIn(driver).clusters.members_page
    actual_number = getattr(page, f"{transform(item_type)}_number")
    assert (
        actual_number == number
    ), f"expected {number} but got {actual_number} of {item_type}"


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "{button_name}" in Onezone {where} members page'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_button_in_members_onezone(
    selenium: SeleniumDrivers, browser_id: str, button_name: str, where: str
) -> None:
    driver = selenium[browser_id]
    page = getattr(OZLoggedIn(driver), where).members_page
    getattr(page, transform(button_name)).click()


@wt(
    parsers.parse("user of {browser_id} can see Onezone {where} members page is opened")
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_onezone_members_page_opened(
    selenium: SeleniumDrivers, browser_id: str, where: str
) -> None:
    driver = selenium[browser_id]
    _ = getattr(OZLoggedIn(driver), where).members_page
