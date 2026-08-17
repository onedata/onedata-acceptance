"""This module contains meta steps for operations on harvesters in Onezone
using web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from pytest import FixtureRequest

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.common import close_alert_popup_if_present
from tests.gui.steps.common.copy_paste import send_copied_item_to_other_users
from tests.gui.steps.modals.modal import click_modal_button, close_modal
from tests.gui.steps.onezone.harvesters.configuration import (
    assert_public_toggle_on_harvester_config_page,
    check_public_toggle_on_harvester_config_page,
    click_button_in_tab_of_harvester_config_page,
    click_on_tab_of_harvester_config_page,
)
from tests.gui.steps.onezone.harvesters.discovery import (
    assert_space_has_appeared_in_discovery_page,
    check_element_exists_on_sidebar_list,
    choose_element_from_dropdown_in_add_element_modal,
    click_button_in_harvester_spaces_page,
    click_button_on_discovery_on_left_sidebar_menu,
    click_create_button_in_discovery_page,
    click_on_option_in_harvester_menu,
    click_option_in_discovery_page_menu,
    click_remove_space_option_in_menu_in_discover_spaces_page,
    confirm_harvester_rename_using_button,
    type_endpoint_to_input_field_in_discovery_page,
    type_text_to_input_field_in_discovery_page,
    type_text_to_rename_input_field_in_discovery_page,
)
from tests.gui.steps.onezone.harvesters.indices import (
    assert_progress_in_harvesting,
    assert_used_by_gui_tag_on_indices_page,
    change_indices_on_gui_plugin_tab,
    click_create_button_in_indices_page,
    click_on_member_menu_option_in_harvester_indices_page,
    expand_index_record_in_indices_page,
    type_index_name_to_input_field_in_indices_page,
    uncheck_toggles_on_create_index_page,
)
from tests.gui.steps.onezone.members import (
    click_element_in_members_list,
    click_on_option_in_members_list_menu,
    click_on_option_of_harvester_on_left_sidebar_menu,
    copy_token_from_modal,
    try_setting_privileges_in_members_subpage,
    wt_wait_for_modal_to_appear,
)
from tests.gui.steps.onezone.spaces import (
    assert_error_popup_has_appeared,
    click_element_on_lists_on_left_sidebar_menu,
    click_on_option_in_the_sidebar,
)
from tests.gui.steps.rest.harvesters import remove_harvester_using_rest
from tests.gui.type_definitions import Clipboard, TmpMemory
from tests.gui.utils.common.popups.generic import AlertPopup, CreatedItemAlertPopup
from tests.gui.utils.generic import parse_elements_sequence
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.user_utils import User
from tests.utils.utils import repeat_failed


def _register_harvester_finalizer(
    request: FixtureRequest,
    hosts: Hosts,
    admin_credentials: User,
    harvester_id: str,
) -> None:
    request.addfinalizer(
        lambda: remove_harvester_using_rest(
            harvester_id,
            hosts["onezone"]["hostname"],
            admin_credentials.username,
            admin_credentials.password,
        )
    )


@wt(
    parsers.parse(
        "user of {browser_id} clicks on Create button in discovery page "
        'and succeeds to create "{harvester_name}" harvester'
    )
)
def click_create_button_and_succeed_to_create_harvester(
    selenium: SeleniumDrivers,
    browser_id: str,
    harvester_name: str,
    hosts: Hosts,
    request: FixtureRequest,
    admin_credentials: User,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
    click_create_button_in_discovery_page(selenium, browser_id)
    check_element_exists_on_sidebar_list(
        selenium, browser_id, harvester_name, "appeared", "harvesters"
    )
    click_on_option_in_harvester_menu(selenium, browser_id, "Copy ID", harvester_name)
    harvester_id = clipboard.paste(display=displays[browser_id])
    _register_harvester_finalizer(request, hosts, admin_credentials, harvester_id)


@wt(
    parsers.parse(
        "user of {browser_id} clicks on Create button in discovery page "
        'and fails to create "{harvester_name}" harvester'
    )
)
def click_create_button_and_fail_to_create_harvester(
    selenium: SeleniumDrivers,
    browser_id: str,
    harvester_name: str,
) -> None:
    click_create_button_in_discovery_page(selenium, browser_id)
    assert_error_popup_has_appeared(selenium, browser_id)
    check_element_exists_on_sidebar_list(
        selenium, browser_id, harvester_name, "disappeared", "harvesters"
    )


@wt(parsers.parse('user of {browser_id} removes "{space_name}" space from harvester'))
def remove_space_from_harvester(
    selenium: SeleniumDrivers, browser_id: str, space_name: str
) -> None:
    button = "Remove"
    modal = "Remove space from harvester"

    click_remove_space_option_in_menu_in_discover_spaces_page(
        selenium, browser_id, space_name
    )
    click_modal_button(selenium, browser_id, button, modal)


@wt(
    parsers.parse(
        'user of {browser_id} removes "{space_name}" space '
        'from harvester "{harvester_name}"'
    )
)
def remove_space_from_given_harvester(
    selenium: SeleniumDrivers, browser_id: str, space_name: str, harvester_name: str
) -> None:
    button = "Remove"
    modal = "Remove space from harvester"
    option = "Spaces"

    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester_name, option
    )
    click_remove_space_option_in_menu_in_discover_spaces_page(
        selenium, browser_id, space_name
    )
    click_modal_button(selenium, browser_id, button, modal)


@wt(
    parsers.parse(
        'user of {browser_id} removes "{harvester_name}" harvester in Onezone page'
    )
)
def remove_harvester(
    selenium: SeleniumDrivers, browser_id: str, harvester_name: str
) -> None:
    where = "Discovery"
    list_type = "harvesters"
    option = "Remove"
    modal = "Remove harvester"

    click_on_option_in_the_sidebar(selenium, browser_id, where)
    click_element_on_lists_on_left_sidebar_menu(
        selenium, browser_id, list_type, harvester_name
    )
    click_on_option_in_harvester_menu(selenium, browser_id, option, harvester_name)
    click_modal_button(selenium, browser_id, option, modal)


@wt(
    parsers.parse(
        'user of {browser_id} creates "{harvester_name}" harvester in Onezone page'
    )
)
def create_harvester(
    selenium: SeleniumDrivers,
    browser_id: str,
    harvester_name: str,
    hosts: Hosts,
    harvesters: dict[str, str],
    clipboard: Clipboard,
    displays: dict[str, str],
    request: FixtureRequest,
    admin_credentials: User,
) -> None:
    where = "Discovery"
    input_name = "name"
    endpoint_input = "endpoint"
    button_name = "create new harvester"
    option = "Copy ID"

    click_on_option_in_the_sidebar(selenium, browser_id, where)
    click_button_on_discovery_on_left_sidebar_menu(selenium, browser_id, button_name)
    type_text_to_input_field_in_discovery_page(
        selenium, browser_id, harvester_name, input_name
    )
    type_endpoint_to_input_field_in_discovery_page(
        selenium, browser_id, endpoint_input, hosts
    )
    click_create_button_in_discovery_page(selenium, browser_id)
    click_on_option_in_harvester_menu(selenium, browser_id, option, harvester_name)
    harvester_id = clipboard.paste(display=displays[browser_id])

    _register_harvester_finalizer(request, hosts, admin_credentials, harvester_id)

    harvesters[harvester_name] = harvester_id
    close_alert_popup_if_present(
        selenium[browser_id], popup=CreatedItemAlertPopup.HARVESTER
    )


@wt(
    parsers.parse(
        'user of {browser_id} adds "{space_name}" space to '
        '"{harvester_name}" harvester using available spaces dropdown'
    )
)
def join_space_to_harvester(
    selenium: SeleniumDrivers,
    browser_id: str,
    space_name: str,
    harvester_name: str,
    tmp_memory: TmpMemory,
) -> None:
    option = "Spaces"
    option2 = "Discovery"
    option3 = "harvesters"
    button_name = "add one of your spaces"
    button_in_modal = "Add"
    modal = "Add one of spaces"
    modal_name = "Add one of your spaces"

    click_on_option_in_the_sidebar(selenium, browser_id, option2)
    click_element_on_lists_on_left_sidebar_menu(
        selenium, browser_id, option3, harvester_name
    )
    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester_name, option
    )
    try:
        click_button_in_harvester_spaces_page(selenium, browser_id, button_name)
    except RuntimeError:
        click_option_in_discovery_page_menu(
            selenium, browser_id, button_name.capitalize()
        )

    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    choose_element_from_dropdown_in_add_element_modal(selenium, browser_id, space_name)
    click_modal_button(selenium, browser_id, button_in_modal, modal)


@wt(
    parsers.parse(
        'user of {browser_id} adds "{group_name}" group to '
        '"{harvester_name}" harvester '
        "using available groups dropdown"
    )
)
def add_group_to_harvester(
    selenium: SeleniumDrivers,
    browser_id: str,
    group_name: str,
    harvester_name: str,
    tmp_memory: TmpMemory,
) -> None:
    option = "Members"
    button = "Add one of your groups"
    where = "group"
    member = "harvester"
    button_in_modal = "Add"
    modal = "Add one of groups"
    modal_name = "Add one of your groups"

    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester_name, option
    )
    click_on_option_in_members_list_menu(
        selenium,
        browser_id,
        button,
        member,
        where + "s",
    )
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    choose_element_from_dropdown_in_add_element_modal(selenium, browser_id, group_name)
    click_modal_button(selenium, browser_id, button_in_modal, modal)
    close_alert_popup_if_present(selenium[browser_id], AlertPopup.MEMBER_ADDED)


@wt(
    parsers.parse(
        'user of {browser_id} creates "{index_name}" index '
        'in "{harvester_name}" harvester in Discovery page'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def create_index_in_harvester(
    selenium: SeleniumDrivers, browser_id: str, index_name: str, harvester_name: str
) -> None:
    option = "Indices"
    member_menu_option = "Create new index"

    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester_name, option
    )
    click_on_member_menu_option_in_harvester_indices_page(
        selenium, browser_id, member_menu_option
    )
    type_index_name_to_input_field_in_indices_page(selenium, browser_id, index_name)
    click_create_button_in_indices_page(selenium, browser_id)


@wt(
    parsers.parse(
        "user of {browser_id1} sends invitation token "
        'from "{harvester_name}" harvester to user of {browser_id2}'
    )
)
def send_invitation_token(
    selenium: SeleniumDrivers,
    browser_id1: str,
    harvester_name: str,
    browser_id2: str,
    tmp_memory: TmpMemory,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:
    where = "Discovery"
    list_type = "harvester"
    option = "Members"
    button = "Invite user using token"
    member = "users"
    modal = "Invite using token"
    item_type = "token"

    click_on_option_in_the_sidebar(selenium, browser_id1, where)
    click_element_on_lists_on_left_sidebar_menu(
        selenium, browser_id1, list_type + "s", harvester_name
    )
    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id1, harvester_name, option
    )
    click_on_option_in_members_list_menu(
        selenium,
        browser_id1,
        button,
        list_type,
        member,
    )
    copy_token_from_modal(selenium, browser_id1)
    close_alert_popup_if_present(selenium[browser_id1], AlertPopup.SUCCESSFULLY_COPIED)
    close_modal(selenium, browser_id1, modal)
    send_copied_item_to_other_users(
        browser_id1, item_type, [browser_id2], tmp_memory, displays, clipboard
    )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) (?P<option>sets|fails to set) "
        r'following privileges for "(?P<user_name>.*)" user in '
        r'"(?P<harvester_name>.*)" harvester:\n(?P<config>(.|\s)*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def change_privilege_config_in_harvester(
    selenium: SeleniumDrivers,
    browser_id: str,
    config: str,
    user_name: str,
    harvester_name: str,
    option: str,
) -> None:
    where = "harvester"
    list_type = "user"
    menu_option = "Members"

    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester_name, menu_option
    )
    click_element_in_members_list(
        selenium,
        browser_id,
        user_name,
        where,
        list_type + "s",
    )
    try_setting_privileges_in_members_subpage(
        selenium,
        browser_id,
        user_name,
        list_type,
        where,
        config,
        option,
    )


@wt(
    parsers.parse(
        'user of {browser_id} renames "{harvester_name}" harvester '
        'to "{harvester_renamed}" in Onezone page'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def rename_harvester(
    selenium: SeleniumDrivers,
    browser_id: str,
    harvester_name: str,
    harvester_renamed: str,
) -> None:
    option = "harvesters"
    menu_option = "Rename"

    click_element_on_lists_on_left_sidebar_menu(
        selenium, browser_id, option, harvester_name
    )
    click_on_option_in_harvester_menu(selenium, browser_id, menu_option, harvester_name)
    type_text_to_rename_input_field_in_discovery_page(
        selenium, browser_id, harvester_renamed
    )
    confirm_harvester_rename_using_button(selenium, browser_id)


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{space}" has appeared on '
        'the spaces list of "{harvester}" harvester'
    )
)
def assert_space_on_harvester_list(
    selenium: SeleniumDrivers, browser_id: str, space: str, harvester: str
) -> None:
    option = "Discovery"
    option2 = "harvesters"
    option3 = "Spaces"

    click_on_option_in_the_sidebar(selenium, browser_id, option)
    click_element_on_lists_on_left_sidebar_menu(
        selenium, browser_id, option2, harvester
    )
    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester, option3
    )
    assert_space_has_appeared_in_discovery_page(selenium, browser_id, space)


@wt(parsers.parse('user of {browser_id} configures "{harvester}" harvester as public'))
def configure_harvester_as_public(
    selenium: SeleniumDrivers, browser_id: str, harvester: str
) -> None:
    action = "checks"
    discovery_tab = "Discovery"
    config_tab = "Configuration"
    scope = "harvesters"
    edit_button = "Edit"
    save_button = "Save"
    is_checked = "checked"
    general_tab = "General tab"

    click_on_option_in_the_sidebar(selenium, browser_id, discovery_tab)
    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id, scope, harvester)
    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester, config_tab
    )

    click_button_in_tab_of_harvester_config_page(
        selenium, browser_id, edit_button, general_tab
    )
    check_public_toggle_on_harvester_config_page(selenium, browser_id, action)
    click_button_in_tab_of_harvester_config_page(
        selenium, browser_id, save_button, general_tab
    )
    assert_public_toggle_on_harvester_config_page(selenium, browser_id, is_checked)


@wt(
    parsers.parse(
        "user of {browser_id} waits until harvesting process in "
        '"{harvester}" is finished for all spaces in "{index}"'
    )
)
def check_harvesting_process_in_harvester(
    selenium: SeleniumDrivers, browser_id: str, harvester: str, index: str | int
) -> None:
    discovery_tab = "Discovery"
    scope = "harvesters"
    indices_tab = "Indices"

    click_on_option_in_the_sidebar(selenium, browser_id, discovery_tab)
    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id, scope, harvester)
    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester, indices_tab
    )
    assert_used_by_gui_tag_on_indices_page(selenium, browser_id, index)
    expand_index_record_in_indices_page(selenium, browser_id, index)
    assert_progress_in_harvesting(selenium, browser_id, index)


@wt(
    parsers.parse(
        'user of {browser_id} creates new index "{index_name}" that '
        'includes {toggles_list:ElementsSequence} toggles for "{harvester_name}"',
        extra_types={"ElementsSequence": parse_elements_sequence},
    ),
)
@repeat_failed(timeout=WAIT_FRONTEND)
def create_index_with_toggles_list(
    browser_id: str,
    selenium: SeleniumDrivers,
    index_name: str,
    toggles_list: list[str],
    harvester_name: str,
) -> None:
    option = "Indices"
    text = "Create new index"
    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester_name, option
    )
    click_on_member_menu_option_in_harvester_indices_page(selenium, browser_id, text)
    type_index_name_to_input_field_in_indices_page(selenium, browser_id, index_name)
    uncheck_toggles_on_create_index_page(selenium, browser_id, toggles_list)
    click_create_button_in_indices_page(selenium, browser_id)


@wt(
    parsers.parse(
        'user of {browser_id} changes indices to "{index_name}"'
        ' on GUI plugin tab for "{harvester_name}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def change_indices_for_harvester(
    browser_id: str, selenium: SeleniumDrivers, index_name: str, harvester_name: str
) -> None:
    option = "Configuration"
    tab_name = "GUI plugin"
    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester_name, option
    )
    click_on_tab_of_harvester_config_page(selenium, browser_id, tab_name)
    change_indices_on_gui_plugin_tab(selenium, browser_id, index_name)
