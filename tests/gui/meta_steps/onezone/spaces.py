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
from tests.gui.steps.onezone.spaces import *
from tests.gui.steps.onepanel.common import wt_click_on_sidebar_item
from tests.gui.steps.onepanel.spaces import *
from tests.gui.steps.onezone.groups import *
from tests.gui.steps.onezone.multibrowser_spaces import *
from tests.gui.steps.onezone.members import *


def create_spaces_in_oz_using_gui(selenium, user, oz_page, space_list):
    option = 'enter'

    for space_name in parse_seq(space_list):
        click_create_new_space_on_spaces_on_left_sidebar_menu(selenium, user,
                                                              oz_page)
        type_space_name_on_input_on_create_new_space_page(selenium, user,
                                                          space_name, oz_page)
        confirm_create_new_space(selenium, user, option, oz_page)


def leave_spaces_in_oz_using_gui(selenium, user, space_list, oz_page):
    option = 'spaces'
    button = 'Leave space'
    button_name = 'yes'

    for space_name in parse_seq(space_list):
        click_space_on_spaces_on_left_sidebar_menu(selenium, user, option,
                                                   space_name, oz_page)
        click_on_option_in_menu(selenium, user, button, oz_page)
        click_confirm_or_cancel_button_on_leave_space_page(selenium, user,
                                                           button_name)


def rename_spaces_in_oz_using_gui(selenium, user, oz_page, space_list,
                                  new_names_list):
    where = 'spaces'
    option = 'enter'
    for space_name, new_space_name in zip(parse_seq(space_list),
                                          parse_seq(new_names_list)):
        click_space_on_spaces_on_left_sidebar_menu(selenium, user, where,
                                                   space_name, oz_page)
        type_space_name_on_rename_space_input_on_overview_page(selenium,
                                                               user,
                                                               new_space_name,
                                                               oz_page)
        confirm_rename_the_space(selenium, user, option, oz_page)


def set_space_as_home_in_oz_using_gui(selenium, user, oz_page, space_name):
    where = 'spaces'
    button = 'Toggle default space'
    click_space_on_spaces_on_left_sidebar_menu(selenium, user, where,
                                               space_name, oz_page)
    click_on_option_in_menu(selenium, user, button, oz_page)


def remove_provider_support_for_space_in_oz_using_gui(selenium, user,
                                                      space_name, onepanel,
                                                      popups):
    sidebar = 'CLUSTERS'
    record = 'Spaces'
    option = 'Revoke space support'
    button = 'Yes, revoke'
    notify_type = 'info'
    text_regexp = '.*[Ss]upport.*revoked.*'

    wt_click_on_sidebar_item(selenium, user, sidebar, record, onepanel)
    wt_expands_toolbar_icon_for_space_in_onepanel(selenium, user,
                                                  space_name, onepanel)
    wt_clicks_on_btn_in_space_toolbar_in_panel(selenium, user,
                                               option, popups)
    wt_clicks_on_btn_in_revoke_space_support(selenium, user,
                                             button, modals)
    notify_visible_with_text(selenium, user, notify_type, text_regexp)


def invite_other_users_to_space_using_gui(selenium, user,
                                          space_name, user_list,
                                          oz_page, tmp_memory, displays,
                                          clipboard):
    option = 'spaces'
    option_in_space = 'Members'
    button = 'Invite user using token'
    where = 'space'
    item_type = 'space invitation token'
    member = 'users'

    click_space_on_spaces_on_left_sidebar_menu(selenium, user, option,
                                               space_name, oz_page)
    click_on_members_of_space_on_left_sidebar_menu(selenium, user,
                                                   space_name, option_in_space,
                                                   oz_page)
    click_on_option_in_members_list_menu(selenium, user, button,
                                         space_name, where, member, oz_page)
    copy_token_from_modal(selenium, user)
    send_invitation_token_to_browser(selenium, user, item_type, oz_page,
                                     displays, clipboard, user_list,
                                     tmp_memory)
    close_invite_token_modal(selenium, user)


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
    option = 'enter'

    for user in parse_seq(user_list):
        click_join_some_space_using_space_invitation_token_button(selenium,
                                                                  user,
                                                                  oz_page)
        paste_space_invitation_token_to_input_on_join_to_space_page(selenium,
                                                                    user,
                                                                    tmp_memory,
                                                                    item_type,
                                                                    oz_page)
        confirm_join_the_space(selenium, user, option, oz_page)


def assert_spaces_have_appeared_in_oz_gui(selenium, user, oz_page, space_list):
    for space_name in parse_seq(space_list):
        assert_new_created_space_has_appeared_on_spaces(selenium, user,
                                                        space_name, oz_page)


def assert_there_are_no_spaces_in_oz_gui(selenium, user, oz_page, space_list):
    for space_name in parse_seq(space_list):
        assert_space_has_disappeared_on_spaces(selenium, user, space_name,
                                               oz_page)


def assert_spaces_have_been_renamed_in_oz_gui(selenium, user, oz_page,
                                              space_list, new_names_list):
    for space_name, new_space_name in zip(parse_seq(space_list),
                                          parse_seq(new_names_list)):
        assert_new_created_space_has_appeared_on_spaces(selenium, user,
                                                        new_space_name, oz_page)
        assert_space_has_disappeared_on_spaces(selenium, user, space_name,
                                               oz_page)


def assert_space_is_home_space_in_oz_gui(selenium, user, oz_page, space_name):
    assert_home_space_has_appeared_on_spaces_on_left_sidebar_menu(selenium,
                                                                  user,
                                                                  space_name,
                                                                  oz_page)


def assert_there_is_no_provider_for_space_in_oz_gui(selenium, user, oz_page,
                                                    space_name):
    number = 0
    assert_number_of_supporting_providers_of_space(selenium, user,
                                                   number, space_name, oz_page)


def assert_user_is_member_of_space_gui(selenium, user, space_name, oz_page,
                                       user_list):
    where = 'Members'
    option = 'sees'
    click_on_members_of_space_on_left_sidebar_menu(selenium, user,
                                                   space_name, where, oz_page)

    for username in parse_seq(user_list):

        assert_user_is_in_space_members_list(selenium, user, option,
                                             username, space_name, oz_page)


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
                                                provider_name, oz_page, hosts)
