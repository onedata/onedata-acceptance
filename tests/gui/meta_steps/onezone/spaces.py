"""This module contains meta steps for operations on spaces in Onezone
using web GUI
"""

__author__ = "Michal Cwiertnia, Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time

from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
)
from selenium.webdriver.support.ui import WebDriverWait

from tests.gui.meta_steps.onezone.tokens import paste_and_consume_received_token
from tests.gui.steps.common.common import (
    close_alert_popup_if_present,
    get_visible_items_list,
)
from tests.gui.steps.common.copy_paste import send_copied_item_to_other_users
from tests.gui.steps.common.notifies import notify_visible_with_text
from tests.gui.steps.common.url import refresh_site
from tests.gui.steps.modals.modal import click_modal_button, close_modal
from tests.gui.steps.onepanel.common import wt_click_on_subitem_for_item
from tests.gui.steps.onepanel.spaces import (
    wt_clicks_on_btn_in_cease_support_modal,
    wt_clicks_on_btn_in_space_toolbar_in_panel,
    wt_clicks_on_understand_risk_in_cease_support_modal,
    wt_expands_toolbar_icon_for_space_in_onepanel,
)
from tests.gui.steps.onezone.documentation import (
    choose_rest_api_command_from_dropdown,
)
from tests.gui.steps.onezone.groups import go_to_group_subpage
from tests.gui.steps.onezone.harvesters.discovery import (
    choose_element_from_dropdown_in_add_element_modal,
)
from tests.gui.steps.onezone.members import (
    assert_member_is_in_parent_members_list,
    click_on_option_in_members_list_menu,
    copy_token_from_modal,
)
from tests.gui.steps.onezone.multibrowser_spaces import send_invitation_token_to_browser
from tests.gui.steps.onezone.overview import (
    confirm_rename_the_space,
    type_space_name_on_rename_space_input_on_overview_page,
)
from tests.gui.steps.onezone.spaces import (
    assert_new_created_space_has_appeared_on_spaces,
    assert_no_provider_for_space,
    assert_number_of_supporting_providers_of_space,
    assert_providers_list_contains_provider,
    assert_space_has_disappeared_on_spaces,
    check_remove_space_understand_notice,
    click_button_in_space_harvesters_page,
    click_button_on_spaces_sidebar_menu,
    click_confirm_or_cancel_button_on_leave_space_page,
    click_copy_button_on_request_support_page,
    click_element_on_lists_on_left_sidebar_menu,
    click_get_support_button_on_providers_page,
    click_on_option_in_space_menu,
    click_on_option_in_the_sidebar,
    click_on_option_of_space_on_left_sidebar_menu,
    confirm_create_new_space,
    copy_token,
    get_space_names_from_sidebar,
    type_space_name_on_input_on_create_new_space_page,
    wt_wait_for_modal_to_appear,
)
from tests.gui.steps.rest.spaces import get_user_spaces, leave_user_space
from tests.gui.type_definitions import Clipboard, TmpMemory
from tests.gui.utils import Modals, OZLoggedIn
from tests.gui.utils.common.constants import WAIT_FRONTEND
from tests.gui.utils.common.popups.generic import AlertPopup
from tests.gui.utils.core.base import NamedElement
from tests.gui.utils.core.web_objects import PageObjectNotFoundError
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    ListElement,
    parse_elements_sequence,
)
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.user_utils import Users


@wt(parsers.parse('user of {browser_id} clicks "Copy" button on Add support page'))
def copy_support_token_from_add_support_page(
    selenium: SeleniumDrivers,
    browser_id: str,
    displays: dict[str, str],
    clipboard: Clipboard,
    tmp_memory: TmpMemory,
) -> None:
    click_copy_button_on_request_support_page(
        selenium, browser_id, displays, clipboard, tmp_memory
    )
    notify_visible_with_text(
        selenium,
        browser_id,
        AlertPopup.SUCCESSFULLY_COPIED,
    )


@wt(
    parsers.parse(
        'user of {user} creates "{space_list:ElementsSequence}" space in Onezone',
        extra_types={"ElementsSequence": parse_elements_sequence},
    ),
)
def create_spaces_in_oz_using_gui(
    selenium: SeleniumDrivers,
    user: str,
    space_list: list[str],
    spaces: dict[str, str],
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
    option = "enter"
    button = "Create space"
    button_copy_id = "Copy ID"
    where = "Data"

    for space_name in space_list:
        click_on_option_in_the_sidebar(selenium, user, where)
        click_button_on_spaces_sidebar_menu(selenium, user, button)
        type_space_name_on_input_on_create_new_space_page(selenium, user, space_name)
        confirm_create_new_space(selenium, user, option)
        click_on_option_in_space_menu(selenium, user, space_name, button_copy_id)
        spaces[space_name] = clipboard.paste(display=displays[user])


@wt(
    parsers.parse(
        'user of {user} sends support token for "{space_name}" to user of {browser_id}'
    )
)
def send_support_token_in_oz_using_gui(
    selenium: SeleniumDrivers,
    user: str,
    space_name: str,
    browser_id: str,
    tmp_memory: TmpMemory,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:
    option = "spaces"
    where = "Providers"
    item_type = "token"

    click_element_on_lists_on_left_sidebar_menu(selenium, user, option, space_name)
    click_on_option_of_space_on_left_sidebar_menu(selenium, user, space_name, where)
    click_get_support_button_on_providers_page(selenium, user)
    copy_token(selenium, user)
    send_copied_item_to_other_users(
        user, item_type, [browser_id], tmp_memory, displays, clipboard
    )


@wt(
    parsers.re(
        rf'user of (?P<user>.*) leaves "(?P<space_list>{ELEMENTS_SEQUENCE_PATTERN})"'
        r" spaces? in Onezone page"
    ),
    converters={"space_list": parse_elements_sequence},
)
def leave_spaces_in_oz_using_gui(
    selenium: SeleniumDrivers, user: str, space_list: list[str]
) -> None:
    where = "spaces"
    option = "Leave"
    confirmation_button = "Leave"
    driver = selenium[user]
    driver.switch_to.default_content()

    if space_list == ["all"]:
        space_names = get_space_names_from_sidebar(selenium, user)
    else:
        space_names = space_list

    for space_name in space_names:
        click_element_on_lists_on_left_sidebar_menu(selenium, user, where, space_name)
        click_on_option_in_space_menu(selenium, user, space_name, option)
        click_confirm_or_cancel_button_on_leave_space_page(
            selenium, user, confirmation_button
        )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) removes"
        rf' "(?P<space_list>{ELEMENTS_SEQUENCE_PATTERN})" '
        r"spaces? in Onezone page"
    ),
    converters={
        "space_list": parse_elements_sequence,
    },
)
def remove_spaces_in_oz_using_gui(
    selenium: SeleniumDrivers, browser_id: str, space_list: list[str]
) -> None:
    where = "Data"
    option = "Remove"
    modal = "Remove space"

    driver = selenium[browser_id]
    driver.switch_to.default_content()

    click_on_option_in_the_sidebar(selenium, browser_id, where)
    for space_name in space_list:
        click_on_option_in_space_menu(selenium, browser_id, space_name, option)
        check_remove_space_understand_notice(selenium, browser_id)
        click_modal_button(selenium, browser_id, option, modal)


def rename_spaces_in_oz_using_gui(
    selenium: SeleniumDrivers,
    user: str,
    space_list: list[str],
    new_names_list: list[str],
) -> None:
    where = "spaces"
    option = "enter"
    option_in_submenu = "overview"

    for space_name, new_space_name in zip(space_list, new_names_list):
        click_on_option_of_space_on_left_sidebar_menu(
            selenium, user, space_name, option_in_submenu
        )
        click_element_on_lists_on_left_sidebar_menu(selenium, user, where, space_name)
        type_space_name_on_rename_space_input_on_overview_page(
            selenium, user, new_space_name
        )
        confirm_rename_the_space(selenium, user, option)


def remove_provider_support_for_space_in_oz_using_gui(
    selenium: SeleniumDrivers, user: str, space_name: str, hosts: Hosts
) -> None:
    sidebar = "CLUSTERS"
    record = "Spaces"
    option = "Revoke space support"
    confirmation_button = "Cease support"
    provider_name = "oneprovider-1"

    wt_click_on_subitem_for_item(
        selenium, [user], sidebar, record, provider_name, hosts
    )
    wt_expands_toolbar_icon_for_space_in_onepanel(selenium, user, space_name)
    wt_clicks_on_btn_in_space_toolbar_in_panel(selenium, user, option)
    wt_clicks_on_understand_risk_in_cease_support_modal(selenium, user)
    wt_clicks_on_btn_in_cease_support_modal(selenium, user, confirmation_button)
    notify_visible_with_text(selenium, user, AlertPopup.CEASED_SUPPORT)


def invite_other_users_to_space_using_gui(
    selenium: SeleniumDrivers,
    user: str,
    space_name: str,
    user_list: list[str],
    tmp_memory: TmpMemory,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:
    option = "spaces"
    option_in_space = "Members"
    button = "Invite user using token"
    where = "space"
    item_type = "token"
    member = "users"
    modal = "Invite using token"

    click_element_on_lists_on_left_sidebar_menu(selenium, user, option, space_name)
    click_on_option_of_space_on_left_sidebar_menu(
        selenium, user, space_name, option_in_space
    )
    click_on_option_in_members_list_menu(selenium, user, button, where, member)
    copy_token_from_modal(selenium, user)
    close_alert_popup_if_present(selenium[user], AlertPopup.SUCCESSFULLY_COPIED)
    send_invitation_token_to_browser(
        user,
        item_type,
        displays,
        clipboard,
        user_list,
        tmp_memory,
    )
    close_modal(selenium, user, modal)


def request_space_support_using_gui(
    selenium: SeleniumDrivers,
    user: str,
    space_name: str,
    tmp_memory: TmpMemory,
    displays: dict[str, str],
    clipboard: Clipboard,
    receiver: str,
) -> None:
    click_on_option_in_the_sidebar(selenium, user, "Data")
    click_element_on_lists_on_left_sidebar_menu(selenium, user, "spaces", space_name)
    click_on_option_of_space_on_left_sidebar_menu(
        selenium, user, space_name, "Providers"
    )
    click_get_support_button_on_providers_page(selenium, user)
    click_copy_button_on_request_support_page(
        selenium, user, displays, clipboard, tmp_memory
    )
    notify_visible_with_text(
        selenium,
        user,
        AlertPopup.SUCCESSFULLY_COPIED,
    )
    send_copied_item_to_other_users(
        user, "token", [receiver], tmp_memory, displays, clipboard
    )


def join_space_in_oz_using_gui(
    selenium: SeleniumDrivers, user_list: list[str], tmp_memory: TmpMemory
) -> None:
    for user in user_list:
        paste_and_consume_received_token(selenium, user, tmp_memory)


def assert_spaces_have_appeared_in_oz_gui(
    selenium: SeleniumDrivers, user: str, space_list: list[str]
) -> None:
    for space_name in space_list:
        assert_new_created_space_has_appeared_on_spaces(selenium, user, space_name)


def assert_there_are_no_spaces_in_oz_gui(
    selenium: SeleniumDrivers, user: str, space_list: list[str]
) -> None:
    for space_name in space_list:
        assert_space_has_disappeared_on_spaces(selenium, user, space_name)


def assert_spaces_have_been_renamed_in_oz_gui(
    selenium: SeleniumDrivers,
    user: str,
    space_list: list[str],
    new_names_list: list[str],
) -> None:
    for space_name, new_space_name in zip(space_list, new_names_list):
        assert_new_created_space_has_appeared_on_spaces(selenium, user, new_space_name)
        assert_space_has_disappeared_on_spaces(selenium, user, space_name)


def assert_there_is_no_provider_for_space_in_oz_gui(
    selenium: SeleniumDrivers, user: str, space_name: str
) -> None:
    number = 0

    assert_number_of_supporting_providers_of_space(selenium, user, number, space_name)


def assert_user_is_member_of_space_gui(
    selenium: SeleniumDrivers, user: str, space_name: str, user_list: list[str]
) -> None:
    where = "Members"
    option = "sees"
    member_type = "user"
    parent_type = "space"

    click_on_option_of_space_on_left_sidebar_menu(selenium, user, space_name, where)

    for username in user_list:
        assert_member_is_in_parent_members_list(
            selenium,
            user,
            option,
            username,
            member_type,
            space_name,
            parent_type,
        )


def assert_provider_does_not_support_space_in_oz_gui(
    selenium: SeleniumDrivers,
    user: str,
    space_name: str,
    provider_name: str,
    hosts: Hosts,
) -> None:
    where = "spaces"
    option = "Providers"

    click_element_on_lists_on_left_sidebar_menu(selenium, user, where, space_name)
    click_on_option_of_space_on_left_sidebar_menu(selenium, user, space_name, option)
    refresh_site(selenium, [user])
    assert_no_provider_for_space(selenium, user, provider_name, space_name, hosts)


def assert_space_is_supported_by_provider_in_oz_gui(
    selenium: SeleniumDrivers,
    user: str,
    space_name: str,
    provider_name: str,
    hosts: Hosts,
) -> None:
    click_on_option_in_the_sidebar(selenium, user, "Data")
    click_element_on_lists_on_left_sidebar_menu(selenium, user, "Spaces", space_name)
    click_on_option_of_space_on_left_sidebar_menu(
        selenium, user, space_name, "Providers"
    )
    assert_providers_list_contains_provider(selenium, user, provider_name, hosts)


@given(
    parsers.parse(
        'there is no "{space_name}" space in Onezone used by user of {browser_id}'
    )
)
def leave_space_in_onezone(
    selenium: SeleniumDrivers, browser_id: str, space_name: str
) -> None:
    option = "Data"

    click_on_option_in_the_sidebar(selenium, browser_id, option)
    time.sleep(2)
    try:
        leave_spaces_in_oz_using_gui(selenium, browser_id, [space_name])
    except (
        ElementNotInteractableException,
        NoSuchElementException,
        PageObjectNotFoundError,
    ):
        pass


@given(parsers.parse("{user} user does not have access to any space"))
@given(
    parsers.parse(
        "{user} user does not have access to any space other than defined in next steps"
    )
)
def g_leave_user_spaces_in_onezone_using_rest(
    hosts: Hosts, users: Users, user: str
) -> None:
    leave_user_spaces_in_onezone_using_rest(hosts, users, user)


def leave_user_spaces_in_onezone_using_rest(
    hosts: Hosts, users: Users, user: str
) -> None:
    zone_hostname = hosts["onezone"]["hostname"]
    user_spaces = get_user_spaces(zone_hostname, user, users)
    for space_id in user_spaces:
        leave_user_space(zone_hostname, user, users, space_id)


@wt(
    parsers.parse(
        'user of {browser_id} adds "{harvester_name}" harvester to '
        '"{space_name}" space using available harvesters dropdown'
    )
)
def add_harvester_to_existing_space(
    selenium: SeleniumDrivers,
    browser_id: str,
    space_name: str,
    harvester_name: str,
    tmp_memory: TmpMemory,
) -> None:
    option = "Harvesters, Discovery"
    button_name = "add one of harvesters"
    button_in_modal = "Add"
    modal = "Add one of spaces"
    modal_name = "Add one of your harvesters"
    panel_name = "Data"

    click_on_option_in_the_sidebar(selenium, browser_id, panel_name)

    click_on_option_of_space_on_left_sidebar_menu(
        selenium, browser_id, space_name, option
    )

    click_button_in_space_harvesters_page(selenium, browser_id, button_name)

    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)

    choose_element_from_dropdown_in_add_element_modal(
        selenium, browser_id, harvester_name
    )
    click_modal_button(selenium, browser_id, button_in_modal, modal)


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) adds "(?P<group_name>.*)" group to '
        r'"(?P<where_name>.*)" (?P<where>group|space) using available groups dropdown'
    )
)
def add_group_to_space_or_group(
    browser_id: str,
    group_name: str,
    where_name: str,
    selenium: SeleniumDrivers,
    where: str,
) -> None:
    option = where + "s"
    option_in_function = "Members"
    button = "Add one of your groups"
    modal = "Add one of groups"
    member = "groups"
    button_in_modal = "Add"
    click_element_on_lists_on_left_sidebar_menu(
        selenium, browser_id, option, where_name
    )
    if where == "space":
        click_on_option_of_space_on_left_sidebar_menu(
            selenium, browser_id, where_name, option_in_function
        )
    elif where == "group":
        go_to_group_subpage(
            selenium,
            browser_id,
            where_name,
            option_in_function.lower(),
        )

    click_on_option_in_members_list_menu(selenium, browser_id, button, where, member)
    choose_element_from_dropdown_in_add_element_modal(selenium, browser_id, group_name)

    click_modal_button(selenium, browser_id, button_in_modal, modal)
    close_alert_popup_if_present(selenium[browser_id], AlertPopup.MEMBER_ADDED)


@wt(parsers.parse('user of {browser_id} copies invite token to "{space_name}" space'))
def copy_user_space_invite_token(
    browser_id: str, space_name: str, selenium: SeleniumDrivers
) -> None:
    option = "spaces"
    option_in_space = "Members"
    where = "space"
    member = "users"
    button = "Invite user using token"
    modal = "Invite using token"

    click_element_on_lists_on_left_sidebar_menu(
        selenium, browser_id, option, space_name
    )
    click_on_option_of_space_on_left_sidebar_menu(
        selenium, browser_id, space_name, option_in_space
    )
    click_on_option_in_members_list_menu(selenium, browser_id, button, where, member)
    copy_token_from_modal(selenium, browser_id)
    close_alert_popup_if_present(selenium[browser_id], AlertPopup.SUCCESSFULLY_COPIED)
    close_modal(selenium, browser_id, modal)


@wt(
    parsers.parse(
        'user of {browser_id} copies command "{command}" from "REST API" modal'
    )
)
def copy_command_from_rest_api_modal(
    selenium: SeleniumDrivers, browser_id: str, command: str
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).rest_api

    modal.api.operations.click()
    choose_rest_api_command_from_dropdown(selenium, browser_id, command)
    modal.api.copy_button.click()


@wt(
    parsers.parse(
        'user of {browser_id} opens "{space_name}" space on the '
        "spaces list in the sidebar"
    )
)
def open_space_in_spaces_list(
    selenium: SeleniumDrivers, browser_id: str, space_name: str
) -> None:
    driver = selenium[browser_id]
    page = OZLoggedIn(driver).data
    seen_spaces = set()
    stop_scrolling_flag = False
    while not stop_scrolling_flag:
        new_spaces = get_visible_items_list(
            page, items_type=ListElement.SPACES_HEADERS, main_field="name"
        )
        currently_seen_names = [new_space.name for new_space in new_spaces]

        if space_name in currently_seen_names:
            space = [space for space in new_spaces if space.name == space_name][0]
            driver.execute_script(
                "arguments[0].scrollIntoView();",
                space.web_elem,
            )
            space.click()
            return

        stop_scrolling_flag = not any(
            el not in seen_spaces for el in currently_seen_names
        )
        seen_spaces.update(currently_seen_names)
        driver.execute_script("arguments[0].scrollIntoView();", new_spaces[-1].web_elem)

    raise AssertionError(f"did not manage to open space {space_name}")


@wt(
    parsers.parse(
        'user of {browser_id} can see that opened space is "{space_name}" on the '
        "spaces list in the sidebar"
    )
)
def assert_opened_space(
    selenium: SeleniumDrivers, browser_id: str, space_name: str
) -> None:
    driver = selenium[browser_id]
    page = OZLoggedIn(driver).data
    vis_spaces = get_visible_items_list(
        page, items_type=ListElement.SPACES, main_field="name"
    )

    def get_opened_spaces_with_name(space_name: str) -> list[NamedElement]:
        return [space for space in vis_spaces if space.name == space_name]

    WebDriverWait(driver, WAIT_FRONTEND).until(
        lambda _: len(get_opened_spaces_with_name(space_name)) > 0,
        message=f"Could not find opened space {space_name} in visible spaces",
    )

    space = get_opened_spaces_with_name(space_name)[0]

    error_message = f"Space {space_name} is not opened."
    assert space.is_displayed(), error_message
    assert "active" in space.web_elem.get_attribute("class"), error_message
