"""This module contains meta steps for operations on harvesters in Onezone
using web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.conftest import WAIT_FRONTEND
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
    click_element_on_lists_on_left_sidebar_menu,
    click_on_option_in_the_sidebar,
)
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} removes "{space_name}" space from harvester'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_space_from_harvester(selenium, browser_id, oz_page, space_name, modals):
    button = "Remove"
    modal = "Remove space from harvester"

    click_remove_space_option_in_menu_in_discover_spaces_page(
        selenium, browser_id, space_name, oz_page
    )
    click_modal_button(selenium, browser_id, button, modal, modals)


@wt(
    parsers.parse(
        'user of {browser_id} removes "{space_name}" space '
        'from harvester "{harvester_name}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_space_from_given_harvester(
    selenium, browser_id, oz_page, space_name, harvester_name, modals
):
    button = "Remove"
    modal = "Remove space from harvester"
    option = "Spaces"

    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester_name, option, oz_page
    )
    click_remove_space_option_in_menu_in_discover_spaces_page(
        selenium, browser_id, space_name, oz_page
    )
    click_modal_button(selenium, browser_id, button, modal, modals)


@wt(
    parsers.parse(
        'user of {browser_id} removes "{harvester_name}" harvester in Onezone page'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_harvester(selenium, browser_id, oz_page, harvester_name, modals):
    where = "Discovery"
    list_type = "harvesters"
    option = "Remove"
    modal = "Remove harvester"

    click_on_option_in_the_sidebar(selenium, browser_id, where, oz_page)
    click_element_on_lists_on_left_sidebar_menu(
        selenium, browser_id, list_type, harvester_name, oz_page
    )
    click_on_option_in_harvester_menu(
        selenium, browser_id, option, harvester_name, oz_page
    )
    click_modal_button(selenium, browser_id, option, modal, modals)


@wt(
    parsers.parse(
        'user of {browser_id} creates "{harvester_name}" harvester in Onezone page'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def create_harvester(
    selenium,
    browser_id,
    oz_page,
    harvester_name,
    hosts,
    harvesters,
    clipboard,
    displays,
):
    where = "Discovery"
    input_name = "name"
    endpoint_input = "endpoint"
    button_name = "create new harvester"
    option = "Copy ID"

    click_on_option_in_the_sidebar(selenium, browser_id, where, oz_page)
    click_button_on_discovery_on_left_sidebar_menu(
        selenium, browser_id, button_name, oz_page
    )
    type_text_to_input_field_in_discovery_page(
        selenium, browser_id, oz_page, harvester_name, input_name
    )
    type_endpoint_to_input_field_in_discovery_page(
        selenium, browser_id, oz_page, endpoint_input, hosts
    )
    click_create_button_in_discovery_page(selenium, browser_id, oz_page)
    click_on_option_in_harvester_menu(
        selenium, browser_id, option, harvester_name, oz_page
    )
    harvesters[harvester_name] = clipboard.paste(display=displays[browser_id])


@wt(
    parsers.parse(
        'user of {browser_id} adds "{space_name}" space to '
        '"{harvester_name}" harvester using available spaces '
        "dropdown"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def join_space_to_harvester(
    selenium,
    browser_id,
    oz_page,
    space_name,
    harvester_name,
    tmp_memory,
    popups,
    modals,
):
    option = "Spaces"
    option2 = "Discovery"
    option3 = "harvesters"
    button_name = "add one of your spaces"
    button_in_modal = "Add"
    modal = "Add one of spaces"
    modal_name = "Add one of your spaces"

    click_on_option_in_the_sidebar(selenium, browser_id, option2, oz_page)
    click_element_on_lists_on_left_sidebar_menu(
        selenium, browser_id, option3, harvester_name, oz_page
    )
    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester_name, option, oz_page
    )
    try:
        click_button_in_harvester_spaces_page(
            selenium, browser_id, oz_page, button_name
        )
    except RuntimeError:
        click_option_in_discovery_page_menu(
            selenium, browser_id, oz_page, button_name.capitalize()
        )

    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    choose_element_from_dropdown_in_add_element_modal(
        selenium, browser_id, space_name, modals, popups
    )
    click_modal_button(selenium, browser_id, button_in_modal, modal, modals)


@wt(
    parsers.parse(
        'user of {browser_id} adds "{group_name}" group to '
        '"{harvester_name}" harvester '
        "using available groups dropdown"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def add_group_to_harvester(
    selenium,
    browser_id,
    oz_page,
    group_name,
    harvester_name,
    onepanel,
    popups,
    tmp_memory,
    modals,
):
    option = "Members"
    button = "Add one of your groups"
    where = "group"
    member = "harvester"
    button_in_modal = "Add"
    modal = "Add one of groups"
    modal_name = "Add one of your groups"

    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester_name, option, oz_page
    )
    click_on_option_in_members_list_menu(
        selenium,
        browser_id,
        button,
        member,
        where + "s",
        oz_page,
        onepanel,
        popups,
    )
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    choose_element_from_dropdown_in_add_element_modal(
        selenium, browser_id, group_name, modals, popups
    )
    click_modal_button(selenium, browser_id, button_in_modal, modal, modals)


@wt(
    parsers.parse(
        'user of {browser_id} creates "{index_name}" index '
        'in "{harvester_name}" harvester in Discovery page'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def create_index_in_harvester(
    selenium, browser_id, oz_page, index_name, harvester_name, popups
):
    option = "Indices"
    member_menu_option = "Create new index"

    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester_name, option, oz_page
    )
    click_on_member_menu_option_in_harvester_indices_page(
        selenium, browser_id, member_menu_option, oz_page, popups
    )
    type_index_name_to_input_field_in_indices_page(
        selenium, browser_id, oz_page, index_name
    )
    click_create_button_in_indices_page(selenium, browser_id, oz_page)


@wt(
    parsers.parse(
        "user of {browser_id1} sends invitation token "
        'from "{harvester_name}" harvester to user of {browser_id2}'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def send_invitation_token(
    selenium,
    browser_id1,
    oz_page,
    harvester_name,
    browser_id2,
    tmp_memory,
    displays,
    clipboard,
    onepanel,
    popups,
    modals,
):
    where = "Discovery"
    list_type = "harvester"
    option = "Members"
    button = "Invite user using token"
    member = "users"
    modal = "Invite using token"
    item_type = "token"

    click_on_option_in_the_sidebar(selenium, browser_id1, where, oz_page)
    click_element_on_lists_on_left_sidebar_menu(
        selenium, browser_id1, list_type + "s", harvester_name, oz_page
    )
    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id1, harvester_name, option, oz_page
    )
    click_on_option_in_members_list_menu(
        selenium,
        browser_id1,
        button,
        list_type,
        member,
        oz_page,
        onepanel,
        popups,
    )
    copy_token_from_modal(selenium, browser_id1)
    close_modal(selenium, browser_id1, modal, modals)
    send_copied_item_to_other_users(
        browser_id1, item_type, browser_id2, tmp_memory, displays, clipboard
    )


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) (?P<option>sets|fails to set) "
        'following privileges for "(?P<user_name>.*)" user in '
        r'"(?P<harvester_name>.*)" harvester:\n(?P<config>(.|\s)*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def change_privilege_config_in_harvester(
    selenium,
    browser_id,
    oz_page,
    onepanel,
    config,
    user_name,
    harvester_name,
    option,
):
    where = "harvester"
    list_type = "user"
    menu_option = "Members"

    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester_name, menu_option, oz_page
    )
    click_element_in_members_list(
        selenium,
        browser_id,
        user_name,
        oz_page,
        where,
        list_type + "s",
        onepanel,
    )
    try_setting_privileges_in_members_subpage(
        selenium,
        browser_id,
        user_name,
        list_type,
        where,
        config,
        onepanel,
        oz_page,
        option,
    )


@wt(
    parsers.parse(
        'user of {browser_id} renames "{harvester_name}" harvester '
        'to "{harvester_renamed}" in Onezone page'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def rename_harvester(selenium, browser_id, oz_page, harvester_name, harvester_renamed):
    option = "harvesters"
    menu_option = "Rename"

    click_element_on_lists_on_left_sidebar_menu(
        selenium, browser_id, option, harvester_name, oz_page
    )
    click_on_option_in_harvester_menu(
        selenium, browser_id, menu_option, harvester_name, oz_page
    )
    type_text_to_rename_input_field_in_discovery_page(
        selenium, browser_id, oz_page, harvester_renamed
    )
    confirm_harvester_rename_using_button(selenium, browser_id, oz_page)


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{space}" has appeared on '
        'the spaces list of "{harvester}" harvester'
    )
)
def assert_space_on_harvester_list(selenium, browser_id, space, harvester, oz_page):
    option = "Discovery"
    option2 = "harvesters"
    option3 = "Spaces"

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_element_on_lists_on_left_sidebar_menu(
        selenium, browser_id, option2, harvester, oz_page
    )
    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester, option3, oz_page
    )
    assert_space_has_appeared_in_discovery_page(selenium, browser_id, space, oz_page)


@wt(parsers.parse('user of {browser_id} configures "{harvester}" harvester as public'))
def configure_harvester_as_public(selenium, browser_id, harvester, oz_page):
    action = "checks"
    discovery_tab = "Discovery"
    config_tab = "Configuration"
    scope = "harvesters"
    edit_button = "Edit"
    save_button = "Save"
    is_checked = "checked"
    general_tab = "General tab"

    click_on_option_in_the_sidebar(selenium, browser_id, discovery_tab, oz_page)
    click_element_on_lists_on_left_sidebar_menu(
        selenium, browser_id, scope, harvester, oz_page
    )
    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester, config_tab, oz_page
    )

    click_button_in_tab_of_harvester_config_page(
        selenium, browser_id, oz_page, edit_button, general_tab
    )
    check_public_toggle_on_harvester_config_page(selenium, browser_id, oz_page, action)
    click_button_in_tab_of_harvester_config_page(
        selenium, browser_id, oz_page, save_button, general_tab
    )
    assert_public_toggle_on_harvester_config_page(
        selenium, browser_id, oz_page, is_checked
    )


@wt(
    parsers.parse(
        "user of {browser_id} waits until harvesting process in "
        '"{harvester}" is finished for all spaces in "{index}"'
    )
)
def check_harvesting_process_in_harvester(
    selenium, browser_id, harvester, index, oz_page
):
    discovery_tab = "Discovery"
    scope = "harvesters"
    indices_tab = "Indices"

    click_on_option_in_the_sidebar(selenium, browser_id, discovery_tab, oz_page)
    click_element_on_lists_on_left_sidebar_menu(
        selenium, browser_id, scope, harvester, oz_page
    )
    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester, indices_tab, oz_page
    )
    assert_used_by_gui_tag_on_indices_page(selenium, browser_id, oz_page, index)
    expand_index_record_in_indices_page(selenium, browser_id, oz_page, index)
    assert_progress_in_harvesting(selenium, browser_id, oz_page, index)


@wt(
    parsers.parse(
        'user of {browser_id} creates new index "{index_name}" that '
        'includes {toggles_list} toggles for "{harvester_name}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def create_index_with_toggles_list(
    browser_id,
    selenium,
    index_name,
    popups,
    toggles_list,
    harvester_name,
    oz_page,
):
    option = "Indices"
    text = "Create new index"
    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester_name, option, oz_page
    )
    click_on_member_menu_option_in_harvester_indices_page(
        selenium, browser_id, text, oz_page, popups
    )
    type_index_name_to_input_field_in_indices_page(
        selenium, browser_id, oz_page, index_name
    )
    uncheck_toggles_on_create_index_page(selenium, browser_id, oz_page, toggles_list)
    click_create_button_in_indices_page(selenium, browser_id, oz_page)


@wt(
    parsers.parse(
        'user of {browser_id} changes indices to "{index_name}"'
        ' on GUI plugin tab for "{harvester_name}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def change_indices_for_harvester(
    browser_id, selenium, index_name, harvester_name, oz_page, popups
):
    option = "Configuration"
    tab_name = "GUI plugin"
    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester_name, option, oz_page
    )
    click_on_tab_of_harvester_config_page(selenium, browser_id, tab_name, oz_page)
    change_indices_on_gui_plugin_tab(selenium, browser_id, oz_page, index_name, popups)
