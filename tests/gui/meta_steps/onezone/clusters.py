"""This module contains meta steps for operations on clusters in Onezone
using web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time
from functools import partial

import pytest
from selenium.common.exceptions import TimeoutException

from tests.gui.meta_steps.onezone.members import remove_member_from_parent
from tests.gui.meta_steps.onezone.tokens import consume_token_from_copied_token
from tests.gui.steps.common.common import close_alert_popup_if_present
from tests.gui.steps.common.copy_paste import send_copied_item_to_other_users
from tests.gui.steps.common.miscellaneous import click_option_in_popup_text_menu
from tests.gui.steps.modals.modal import click_modal_button, close_modal
from tests.gui.steps.onepanel.common import wt_click_on_subitem_for_item
from tests.gui.steps.onezone.clusters import (
    click_button_in_gui_settings_page,
    click_cluster_menu_button,
    click_on_record_in_clusters_menu,
    click_option_of_record_in_the_sidebar,
    remove_notification_in_gui_settings_page,
    write_input_in_gui_settings_page,
)
from tests.gui.steps.onezone.harvesters.discovery import (
    choose_element_from_dropdown_in_add_element_modal,
)
from tests.gui.steps.onezone.members import (
    click_element_in_members_list,
    click_on_option_in_members_list_menu,
    copy_token_from_modal,
    see_privileges_for_member,
    try_setting_privileges_in_members_subpage,
    wt_wait_for_modal_to_appear,
)
from tests.gui.steps.onezone.spaces import click_on_option_in_the_sidebar
from tests.gui.steps.rest.provider import GuiMessageType, modify_gui_setting_message
from tests.gui.type_definitions import Clipboard, TmpMemory
from tests.gui.utils.common.popups.generic import AlertPopup
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.user_utils import User


@wt(
    parsers.parse(
        'user of {browser_id} invites user of {browser} to "{cluster}" cluster'
    )
)
def invite_user_to_cluster(
    selenium: SeleniumDrivers,
    browser_id: str,
    browser: str,
    cluster: str,
    hosts: Hosts,
    tmp_memory: TmpMemory,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:
    option = "Clusters"
    sub_item = "Members"
    button = "Invite user using token"
    where = option.lower()[:-1]
    member = "users"
    modal = "Invite using token"
    item_type = "token"

    click_on_option_in_the_sidebar(selenium, browser_id, option)
    click_on_record_in_clusters_menu(selenium, browser_id, cluster, hosts)
    wt_click_on_subitem_for_item(
        selenium, [browser_id], option, sub_item, cluster, hosts
    )

    click_on_option_in_members_list_menu(selenium, browser_id, button, where, member)
    copy_token_from_modal(selenium, browser_id)
    close_alert_popup_if_present(selenium[browser_id], AlertPopup.SUCCESSFULLY_COPIED)
    close_modal(selenium, browser_id, modal)
    send_copied_item_to_other_users(
        browser_id, item_type, [browser], tmp_memory, displays, clipboard
    )


@wt(parsers.parse("user of {browser_id} joins to cluster"))
def join_to_cluster(
    selenium: SeleniumDrivers,
    browser_id: str,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:
    consume_token_from_copied_token(selenium, browser_id, clipboard, displays)


@wt(
    parsers.parse(
        "user of {browser_id} sets following privileges "
        "for {user_name} user in {where} page:\n{config}"
    )
)
def change_privilege_config_in_cluster(
    selenium: SeleniumDrivers,
    browser_id: str,
    where: str,
    user_name: str,
    hosts: Hosts,
    config: str,
) -> None:
    member_type = "user"
    list_type = "users"
    option = "sets"
    cluster = "oneprovider-1"

    wt_click_on_subitem_for_item(
        selenium, [browser_id], "CLUSTERS", "Members", cluster, hosts
    )
    click_element_in_members_list(selenium, browser_id, user_name, where, list_type)
    see_privileges_for_member(selenium, browser_id, where, member_type, user_name)
    try_setting_privileges_in_members_subpage(
        selenium,
        browser_id,
        user_name,
        member_type,
        where,
        config,
        option,
    )


@wt(
    parsers.parse(
        'user of {browser_id} adds "{group_name}" group to "{cluster_name}" cluster'
    )
)
def add_group_to_cluster(
    selenium: SeleniumDrivers,
    browser_id: str,
    hosts: Hosts,
    group_name: str,
    cluster_name: str,
    tmp_memory: TmpMemory,
) -> None:
    sidebar = "CLUSTERS"
    menu_option = "Members"
    sub_item = "Add one of your groups"
    button_name = "Add"
    modal = "Add one of groups"
    where = "cluster"
    member = "groups"
    modal_name = "add one of your groups"
    click_on_option_in_the_sidebar(selenium, browser_id, sidebar)
    click_on_record_in_clusters_menu(selenium, browser_id, cluster_name, hosts)
    wt_click_on_subitem_for_item(
        selenium,
        [browser_id],
        sidebar,
        menu_option,
        cluster_name,
        hosts,
    )
    click_on_option_in_members_list_menu(selenium, browser_id, sub_item, where, member)
    for _ in range(5):
        try:
            wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
            break
        except TimeoutException:
            click_on_option_in_members_list_menu(
                selenium, browser_id, sub_item, where, member
            )

    choose_element_from_dropdown_in_add_element_modal(selenium, browser_id, group_name)
    click_modal_button(selenium, browser_id, button_name, modal)
    close_alert_popup_if_present(selenium[browser_id], AlertPopup.MEMBER_ADDED)


@given(
    parsers.re(
        r'user of (?P<browser_id>.*) sees no "(?P<member_name>.*)" '
        r'(?P<member_type>user|group) in "(?P<name>.*)" '
        r"(?P<where>cluster|group|harvester) members"
    )
)
def no_member_in_parent(
    selenium: SeleniumDrivers,
    browser_id: str,
    member_name: str,
    member_type: str,
    name: str,
    tmp_memory: TmpMemory,
    where: str,
) -> None:
    try:
        remove_member_from_parent(
            selenium,
            browser_id,
            member_name,
            member_type,
            name,
            tmp_memory,
            where,
        )
    except RuntimeError:
        pass


@wt(parsers.parse('user of {browser_id} remembers "{provider}" cluster id'))
def remember_cluster_id(
    selenium: SeleniumDrivers,
    browser_id: str,
    provider: str,
    hosts: Hosts,
    tmp_memory: TmpMemory,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
    option = "Copy ID"
    click_on_record_in_clusters_menu(selenium, browser_id, provider, hosts)
    click_cluster_menu_button(selenium, browser_id, provider, hosts)
    click_option_in_popup_text_menu(selenium, browser_id, option)
    cluster_id = clipboard.paste(display=displays[browser_id])
    tmp_memory[provider]["cluster id"] = cluster_id


@wt(
    parsers.re(
        r"user of (?P<browser_id>\w+) (?P<operation>removes) "
        r'"(?P<text>.*)" text from (?P<kind_of_agreement>.*) in GUI'
        r' settings page of "(?P<record>.*)"'
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>\w+) (?P<operation>sets) "
        r'(?P<kind_of_agreement>.*): "(?P<text>.*)" in GUI settings '
        r'page of "(?P<record>.*)"'
    )
)
def set_gui_settings(
    selenium: SeleniumDrivers,
    browser_id: str,
    record: str,
    hosts: Hosts,
    kind_of_agreement: GuiMessageType,
    text: str,
    operation: str,
    onepanel_credentials: User,
    request: pytest.FixtureRequest,
) -> None:
    request.addfinalizer(
        partial(
            modify_gui_setting_message,
            hosts,
            host=record,
            message_id=kind_of_agreement,
            onepanel_credentials=onepanel_credentials,
            new_message="",
        )
    )
    menu = "Clusters"
    option = "GUI settings"
    box = kind_of_agreement + " input"
    button = "save " + kind_of_agreement
    click_on_option_in_the_sidebar(selenium, browser_id, menu)
    click_on_record_in_clusters_menu(selenium, browser_id, record, hosts)
    click_option_of_record_in_the_sidebar(selenium, browser_id, option)
    click_button_in_gui_settings_page(selenium, browser_id, kind_of_agreement)
    if operation == "sets":
        write_input_in_gui_settings_page(selenium, browser_id, box, text)
    else:
        remove_notification_in_gui_settings_page(
            selenium, browser_id, kind_of_agreement
        )
    click_button_in_gui_settings_page(selenium, browser_id, button)

    # wait for save button to be clicked
    time.sleep(0.1)


@wt(
    parsers.parse(
        "user of {browser_id} inserts {kind_of_agreement} link in "
        'cookie consent notification in GUI settings page of "{record}"'
    )
)
def insert_setting_link(
    selenium: SeleniumDrivers, browser_id: str, kind_of_agreement: str
) -> None:
    link = "insert " + kind_of_agreement + " link"
    button = "save cookie consent notification"
    click_button_in_gui_settings_page(selenium, browser_id, link)
    click_button_in_gui_settings_page(selenium, browser_id, button)
