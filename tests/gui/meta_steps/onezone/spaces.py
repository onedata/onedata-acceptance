"""This module contains meta steps for operations on spaces in Onezone
using web GUI
"""

__author__ = "Michal Cwiertnia, Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import pytest

from tests.gui.steps.onezone.data_space_management import *
from tests.gui.steps.common.miscellaneous import *
from tests.gui.steps.modal import *
from tests.gui.steps.oneprovider.spaces import *
from tests.gui.steps.common.notifies import *
from tests.gui.steps.common.copy_paste import *
from tests.gui.steps.onezone.logged_in_common import *
from tests.gui.steps.onezone.data_space_management import \
    type_text_into_space_creation_edit_box_in_oz
from tests.gui.steps.common.miscellaneous import press_enter_on_active_element
from tests.gui.steps.common.url import refresh_site
from tests.gui.utils.generic import parse_seq
from tests.gui.steps.onezone.providers import assert_list_of_providers_is_empty


def create_spaces_in_oz_using_gui(selenium, user, oz_page, space_list, hosts):
    panel_name = "DATA SPACE MANAGEMENT"
    button_name = "Create new space"
    item_type = "space"

    wt_expand_oz_panel(selenium, user, panel_name, oz_page)
    for space_name in parse_seq(space_list):
        click_on_btn_in_oz_panel(selenium, user, button_name, panel_name,
                                 oz_page)
        type_text_into_space_creation_edit_box_in_oz(selenium, user,
                                                     space_name, oz_page)
        press_enter_on_active_element(selenium, user)
        assert_there_is_item_named_in_oz_panel_list(selenium, user, item_type,
                                                    space_name, panel_name,
                                                    oz_page, hosts)


def leave_spaces_in_oz_using_gui(selenium, user, space_list, oz_page,
                                 tmp_memory):
    panel_name = "DATA SPACE MANAGEMENT"
    option_name = "Leave"
    modal_name = "Leave a space"
    notify_type = "info"

    wt_expand_oz_panel(selenium, user, panel_name, oz_page)
    for space_name in parse_seq(space_list):
        notify_text_regexp = ".*{}.*left".format(space_name)
        expand_settings_dropdown_for_space_in_oz(selenium, user, space_name,
                                                 oz_page)
        click_on_settings_option_for_space_in_oz(selenium, user, option_name,
                                                 space_name, oz_page)
        wt_wait_for_modal_to_appear(selenium, user, modal_name, tmp_memory)
        wt_click_on_confirmation_btn_in_modal(selenium, user, "yes", tmp_memory)
        wt_wait_for_modal_to_disappear(selenium, user, tmp_memory)
        notify_visible_with_text(selenium, user, notify_type,
                                 notify_text_regexp)


def rename_spaces_in_oz_using_gui(selenium, user, oz_page, space_list,
                                  new_names_list, tmp_memory):
    panel_name = "DATA SPACE MANAGEMENT"
    option_name = "Rename"
    modal_name = "Rename a space"
    notify_type = "info"

    wt_expand_oz_panel(selenium, user, panel_name, oz_page)
    for space_name, new_space_name in zip(parse_seq(space_list),
                                          parse_seq(new_names_list)):
        notify_text_regexp = ".*{}.*renamed.*{}".format(space_name,
                                                        new_space_name)
        expand_settings_dropdown_for_space_in_oz(selenium, user, space_name,
                                                 oz_page)
        click_on_settings_option_for_space_in_oz(selenium, user, option_name,
                                                 space_name, oz_page)
        wt_wait_for_modal_to_appear(selenium, user, modal_name, tmp_memory)
        activate_input_box_in_modal(user, "", tmp_memory)
        type_string_into_active_element(selenium, user, new_space_name)
        wt_click_on_confirmation_btn_in_modal(selenium, user, "ok", tmp_memory)
        wt_wait_for_modal_to_disappear(selenium, user, tmp_memory)
        notify_visible_with_text(selenium, user, notify_type,
                                 notify_text_regexp)


def set_space_as_home_in_oz_using_gui(selenium, user, oz_page, space_name):
    panel_name = "DATA SPACE MANAGEMENT"
    option_name = "set as home"

    wt_expand_oz_panel(selenium, user, panel_name, oz_page)
    expand_settings_dropdown_for_space_in_oz(selenium, user, space_name,
                                             oz_page)
    click_on_settings_option_for_space_in_oz(selenium, user, option_name,
                                             space_name, oz_page)


def remove_provider_support_for_space_in_oz_using_gui(selenium, user, oz_page,
                                                      space_name, provider_name,
                                                      tmp_memory, hosts):
    panel_name = "DATA SPACE MANAGEMENT"
    modal_name = "Unsupport space"
    option_name = "I understand the risk of data loss"
    item_type = "space"

    wt_expand_oz_panel(selenium, user, panel_name, oz_page)
    expand_items_submenu_in_oz_panel(selenium, user, item_type, space_name,
                                     panel_name, oz_page, hosts)
    click_on_unsupport_space_for_supporting_provider(selenium, user,
                                                     provider_name, space_name,
                                                     oz_page, hosts)
    wt_wait_for_modal_to_appear(selenium, user, modal_name, tmp_memory)
    select_option_with_text_in_modal(user, option_name, tmp_memory)
    assert_btn_in_modal_is_enabled(user, "yes", tmp_memory)
    wt_click_on_confirmation_btn_in_modal(selenium, user, "yes",
                                          tmp_memory)
    wt_wait_for_modal_to_disappear(selenium, user, tmp_memory)


def invite_other_users_to_space_using_gui(selenium, user,
                                          space_name, user_list,
                                          op_page, tmp_memory, displays,
                                          clipboard):
    option_name = "INVITE USER"
    modal_name = "Invite user to the space"
    notify_type = "info"
    notify_text_regexp = ".*copied to clipboard.*"
    token = "space invitation token"

    click_settings_icon_for_space(selenium, user, space_name, op_page)
    click_on_item_in_space_settings_dropdown(selenium, user, option_name,
                                             space_name, op_page)
    wt_wait_for_modal_to_appear(selenium, user, modal_name, tmp_memory)
    click_on_copy_btn_in_modal(selenium, user, tmp_memory)
    notify_visible_with_text(selenium, user, notify_type, notify_text_regexp)
    wt_click_on_confirmation_btn_in_modal(selenium, user, "ok", tmp_memory)
    wt_wait_for_modal_to_disappear(selenium, user, tmp_memory)
    for receiver in parse_seq(user_list):
        send_copied_item_to_other_users(user, token, receiver, tmp_memory,
                                        displays, clipboard)


def request_space_support_using_gui(selenium, user, oz_page, space_name,
                                    tmp_memory, modals, displays,
                                    clipboard, receiver):
    panel_name = "DATA SPACE MANAGEMENT"
    option_name = "ADD STORAGE"
    notify_type = "info"
    notify_text_regexp = ".*copied.*to.*clipboard.*"
    item_type = "token"

    wt_expand_oz_panel(selenium, user, panel_name, oz_page)
    expand_settings_dropdown_for_space_in_oz(selenium, user, space_name,
                                             oz_page)
    click_on_settings_option_for_space_in_oz(selenium, user, option_name,
                                             space_name, oz_page)

    wait_for_add_storage_modal_to_appear(selenium, user, tmp_memory, modals)
    assert_non_empty_token_in_add_storage_modal(user, tmp_memory)
    cp_token_from_add_storage_modal(user, tmp_memory)
    notify_visible_with_text(selenium, user, notify_type, notify_text_regexp)
    send_copied_item_to_other_users(user, item_type, receiver, tmp_memory,
                                    displays, clipboard)


def join_space_in_oz_using_gui(selenium, user_list, oz_page, tmp_memory,
                               item_type):
    panel_name = "DATA SPACE MANAGEMENT"
    button_name = "Join space"
    modal_name = "Join a space"

    for user in parse_seq(user_list):
        wt_expand_oz_panel(selenium, user, panel_name, oz_page)
        click_on_btn_in_oz_panel(selenium, user, button_name, panel_name,
                                 oz_page)
        wt_wait_for_modal_to_appear(selenium, user, modal_name, tmp_memory)
        activate_input_box_in_modal(user, "", tmp_memory)
        type_item_into_active_element(selenium, user, item_type, tmp_memory)
        press_enter_on_active_element(selenium, user)
        wt_wait_for_modal_to_disappear(selenium, user, tmp_memory)


def remove_space_in_oz_using_gui():
    pytest.skip("This feature is not supported yet")


def delete_users_from_space_in_oz_using_gui():
    pytest.skip("This feature is not supported yet")


def add_users_to_space_in_oz_using_gui():
    pytest.skip("This feature is not supported yet")


def assert_spaces_have_appeared_in_oz_gui(selenium, user, oz_page, space_list,
                                          hosts):
    panel_name = "DATA SPACE MANAGEMENT"
    item_type = "space"

    refresh_site(selenium, user)
    wt_expand_oz_panel(selenium, user, panel_name, oz_page)
    for space_name in parse_seq(space_list):
        assert_there_is_item_named_in_oz_panel_list(selenium, user, item_type,
                                                    space_name, panel_name,
                                                    oz_page, hosts)


def assert_there_are_no_spaces_in_oz_gui(selenium, user, oz_page, space_list):
    panel_name = "DATA SPACE MANAGEMENT"
    item_type = "space"

    refresh_site(selenium, user)
    wt_expand_oz_panel(selenium, user, panel_name, oz_page)
    for space_name in parse_seq(space_list):
        assert_there_is_no_item_named_in_oz_panel_list(selenium, user,
                                                       item_type, space_name,
                                                       panel_name, oz_page, hosts)


def assert_spaces_have_been_renamed_in_oz_gui(selenium, user, oz_page,
                                              space_list, new_names_list, hosts):
    panel_name = "DATA SPACE MANAGEMENT"
    item_type = "space"

    refresh_site(selenium, user)
    wt_expand_oz_panel(selenium, user, panel_name, oz_page)
    for space_name, new_space_name in zip(parse_seq(space_list),
                                          parse_seq(new_names_list)):
        assert_there_is_item_named_in_oz_panel_list(selenium, user, item_type,
                                                    new_space_name, panel_name,
                                                    oz_page, hosts)
        assert_there_is_no_item_named_in_oz_panel_list(selenium, user,
                                                       item_type, space_name,
                                                       panel_name, oz_page,
                                                       hosts)


def assert_space_is_home_space_in_oz_gui(selenium, user, oz_page, space_name):
    panel_name = "DATA SPACE MANAGEMENT"
    item_type = "space"

    refresh_site(selenium, user)
    wt_expand_oz_panel(selenium, user, panel_name, oz_page)
    assert_item_is_home_item_in_oz_panel(selenium, user, item_type, space_name,
                                         panel_name, oz_page, hosts)


def assert_there_is_no_provider_for_space_in_oz_gui(selenium, user, oz_page,
                                                    space_name, providers_list,
                                                    hosts):
    panel_name = "DATA SPACE MANAGEMENT"
    item_type = "space"

    refresh_site(selenium, user)
    wt_expand_oz_panel(selenium, user, panel_name, oz_page)
    expand_items_submenu_in_oz_panel(selenium, user, item_type, space_name,
                                     panel_name, oz_page, hosts)
    assert_no_such_supporting_providers_for_space(selenium, user, space_name,
                                                  providers_list, oz_page, hosts)


def assert_user_is_member_of_space_gui(selenium, user, space_name, op_page,
                                       user_list):
    caption = "USERS"

    select_sapce_from_sidebar_list(selenium, user, space_name, op_page)
    for username in parse_seq(user_list):
        assert_item_appeared_in_spaces_perm_table(selenium, user, username,
                                                  caption, op_page)


def assert_provider_does_not_support_space_in_oz_gui(selenium, user, oz_page,
                                                     space_name, provider_name,
                                                     hosts):
    spaces_panel_name = "DATA SPACE MANAGEMENT"
    providers_panel_name = "GO TO YOUR FILES"
    item_type = "space"

    refresh_site(selenium, user)
    wt_expand_oz_panel(selenium, user, spaces_panel_name, oz_page)
    expand_items_submenu_in_oz_panel(selenium, user, item_type, space_name,
                                     spaces_panel_name, oz_page, hosts)
    assert_no_such_supporting_providers_for_space(selenium, user, space_name,
                                                  provider_name, oz_page, hosts)
    wt_expand_oz_panel(selenium, user, providers_panel_name, oz_page)
    assert_list_of_providers_is_empty(selenium, user, oz_page)


def assert_space_is_supported_by_provider_in_oz_gui(selenium, user, oz_page,
                                                    space_name, provider_name,
                                                    hosts, with_refresh=False):
    panel_name = "DATA SPACE MANAGEMENT"
    item_type = "space"

    if with_refresh:
        refresh_site(selenium, user)
    wt_expand_oz_panel(selenium, user, panel_name, oz_page)
    expand_items_submenu_in_oz_panel(selenium, user, item_type, space_name,
                                     panel_name, oz_page, hosts)
    assert_supporting_providers_for_space_in_oz(selenium, user, space_name,
                                                provider_name, oz_page)
