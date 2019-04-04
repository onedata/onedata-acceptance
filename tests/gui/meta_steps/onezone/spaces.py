"""This module contains meta steps for operations on spaces in Onezone
using web GUI
"""

__author__ = "Michal Cwiertnia, Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.steps.common.notifies import *
from tests.gui.steps.common.copy_paste import *
from tests.gui.steps.common.url import refresh_site
from tests.gui.steps.onezone.spaces import *
from tests.gui.steps.onepanel.common import wt_click_on_sidebar_item
from tests.gui.steps.onepanel.spaces import *
from tests.gui.steps.onezone.multibrowser_spaces import *
from tests.gui.steps.onezone.members import *
from tests.gui.steps.common.miscellaneous import close_modal


def create_spaces_in_oz_using_gui(selenium, user, oz_page, space_list):
    option = 'enter'

    for space_name in parse_seq(space_list):
        click_create_new_space_on_spaces_on_left_sidebar_menu(selenium, user,
                                                              oz_page)
        type_space_name_on_input_on_create_new_space_page(selenium, user,
                                                          space_name, oz_page)
        confirm_create_new_space(selenium, user, option, oz_page)


def leave_spaces_in_oz_using_gui(selenium, user, space_list, oz_page):
    where = 'spaces'
    option = 'Leave space'
    confirmation_button = 'yes'

    for space_name in parse_seq(space_list):
        click_element_on_lists_on_left_sidebar_menu(selenium, user, where,
                                                    space_name, oz_page)
        click_on_option_in_menu(selenium, user, option, oz_page)
        click_confirm_or_cancel_button_on_leave_space_page(selenium, user,
                                                           confirmation_button)


def rename_spaces_in_oz_using_gui(selenium, user, oz_page, space_list,
                                  new_names_list):
    where = 'spaces'
    option = 'enter'

    for space_name, new_space_name in zip(parse_seq(space_list),
                                          parse_seq(new_names_list)):
        click_element_on_lists_on_left_sidebar_menu(selenium, user, where,
                                                    space_name, oz_page)
        type_space_name_on_rename_space_input_on_overview_page(selenium,
                                                               user,
                                                               new_space_name,
                                                               oz_page)
        confirm_rename_the_space(selenium, user, option, oz_page)


def set_space_as_home_in_oz_using_gui(selenium, user, oz_page, space_name):
    where = 'spaces'
    button = 'Toggle default space'

    click_element_on_lists_on_left_sidebar_menu(selenium, user, where,
                                                space_name, oz_page)
    click_on_option_in_menu(selenium, user, button, oz_page)


def remove_provider_support_for_space_in_oz_using_gui(selenium, user,
                                                      space_name, onepanel,
                                                      popups):
    sidebar = 'CLUSTERS'
    record = 'Spaces'
    option = 'Revoke space support'
    confirmation_button = 'Yes, revoke'
    notify_type = 'info'
    text_regexp = '.*[Ss]upport.*revoked.*'

    wt_click_on_sidebar_item(selenium, user, sidebar, record, onepanel)
    wt_expands_toolbar_icon_for_space_in_onepanel(selenium, user,
                                                  space_name, onepanel)
    wt_clicks_on_btn_in_space_toolbar_in_panel(selenium, user,
                                               option, popups)
    wt_clicks_on_btn_in_revoke_space_support(selenium, user,
                                             confirmation_button, modals)
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
    modal = 'Invite using token'

    click_element_on_lists_on_left_sidebar_menu(selenium, user, option,
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
    close_modal(selenium, user, modal, modals)


def request_space_support_using_gui(selenium, user, oz_page, space_name,
                                    tmp_memory, displays, clipboard, receiver):
    where = 'Spaces'
    option = 'Providers'
    notify_type = 'info'
    text_regexp = '.*copied.*'
    item_type = 'token'

    click_on_spaces_in_the_sidebar(selenium, user, where, oz_page)
    click_element_on_lists_on_left_sidebar_menu(selenium, user, where.lower(),
                                                space_name, oz_page)
    click_on_members_of_space_on_left_sidebar_menu(selenium, user,
                                                   space_name, option, oz_page)
    click_get_support_button_on_providers_page(selenium, user, oz_page)
    click_copy_button_on_request_support_page(selenium, user, oz_page,
                                              displays, clipboard, tmp_memory)
    notify_visible_with_text(selenium, user, notify_type, text_regexp)
    send_copied_item_to_other_users(user, item_type, receiver,
                                    tmp_memory, displays, clipboard)


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
    where = 'spaces'
    option = 'Providers'

    click_element_on_lists_on_left_sidebar_menu(selenium, user, where,
                                                space_name, oz_page)
    click_on_members_of_space_on_left_sidebar_menu(selenium, user,
                                                   space_name, option, oz_page)
    refresh_site(selenium, user)
    assert_no_provider_for_space(selenium, user, provider_name,
                                 space_name, hosts, oz_page)


def assert_space_is_supported_by_provider_in_oz_gui(selenium, user, oz_page,
                                                    space_name, provider_name,
                                                    hosts):
    where = 'Spaces'
    option = 'Providers'

    click_on_spaces_in_the_sidebar(selenium, user, where, oz_page)
    click_element_on_lists_on_left_sidebar_menu(selenium, user, where.lower(),
                                                space_name, oz_page)
    click_on_members_of_space_on_left_sidebar_menu(selenium, user,
                                                   space_name, option, oz_page)
    assert_providers_list_contains_provider(selenium, user, provider_name,
                                            hosts, oz_page)

