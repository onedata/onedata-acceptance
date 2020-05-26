"""This module contains meta steps for operations on spaces in Onezone
using web GUI
"""

__author__ = "Michal Cwiertnia, Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import given

from tests.gui.meta_steps.onezone.tokens import (
    consume_received_token)
from tests.gui.steps.common.notifies import *
from tests.gui.steps.common.copy_paste import *
from tests.gui.steps.common.url import refresh_site
from tests.gui.steps.modal import close_modal
from tests.gui.steps.onezone.spaces import *
from tests.gui.steps.onepanel.common import wt_click_on_subitem_for_item
from tests.gui.steps.onepanel.spaces import *
from tests.gui.steps.onezone.multibrowser_spaces import *
from tests.gui.steps.onezone.members import *
from tests import OZ_REST_PORT
from tests.utils.rest_utils import http_get, get_zone_rest_path, http_delete


@wt(parsers.parse('user of {user} creates "{space_list}" space in Onezone'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_spaces_in_oz_using_gui(selenium, user, oz_page, space_list):
    option = 'enter'

    for space_name in parse_seq(space_list):
        click_create_new_space_on_spaces_on_left_sidebar_menu(selenium, user,
                                                              oz_page)
        type_space_name_on_input_on_create_new_space_page(selenium, user,
                                                          space_name, oz_page)
        confirm_create_new_space(selenium, user, option, oz_page)


@wt(parsers.parse('user of {user} sends support token for "{space_name}" '
                  'to user of {browser_id}'))
def send_support_token_in_oz_using_gui(selenium, user, space_name, browser_id,
                                       oz_page, tmp_memory, displays, clipboard):
    option = 'spaces'
    where = 'Providers'
    item_type = 'token'

    click_element_on_lists_on_left_sidebar_menu(selenium, user, option,
                                                space_name, oz_page)
    click_on_option_of_space_on_left_sidebar_menu(selenium, user,
                                                  space_name, where, oz_page)
    click_get_support_button_on_providers_page(selenium, user, oz_page)
    copy_token(selenium, user, oz_page)
    send_copied_item_to_other_users(user, item_type, browser_id,
                                    tmp_memory, displays, clipboard)


@wt(parsers.re('user of (?P<user>.*) leaves "(?P<space_list>.+?)" space '
               'in Onezone page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def leave_spaces_in_oz_using_gui(selenium, user, space_list, oz_page, popups):
    where = 'spaces'
    option = 'Leave space'
    confirmation_button = 'yes'

    for space_name in parse_seq(space_list):
        click_element_on_lists_on_left_sidebar_menu(selenium, user, where,
                                                    space_name, oz_page)
        click_on_option_in_menu(selenium, user, option, oz_page, popups)
        click_confirm_or_cancel_button_on_leave_space_page(selenium, user,
                                                           confirmation_button,
                                                           modals)


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


def remove_provider_support_for_space_in_oz_using_gui(selenium, user,
                                                      space_name, onepanel,
                                                      popups, hosts):
    sidebar = 'CLUSTERS'
    record = 'Spaces'
    option = 'Revoke space support'
    confirmation_button = 'Cease support'
    notify_type = 'info'
    text_regexp = 'Ceased.*[Ss]upport.*'
    provider_name = 'oneprovider-1'

    wt_click_on_subitem_for_item(selenium, user, sidebar, record,
                                 provider_name, onepanel, hosts)
    wt_expands_toolbar_icon_for_space_in_onepanel(selenium, user, space_name,
                                                  onepanel)
    wt_clicks_on_btn_in_space_toolbar_in_panel(selenium, user,
                                               option, popups)
    wt_clicks_on_understand_risk_in_cease_support_modal(selenium, user,
                                                        modals)
    wt_clicks_on_btn_in_cease_support_modal(selenium, user,
                                            confirmation_button, modals)
    notify_visible_with_text(selenium, user, notify_type, text_regexp)


def invite_other_users_to_space_using_gui(selenium, user,
                                          space_name, user_list,
                                          oz_page, tmp_memory, displays,
                                          clipboard, onepanel, popups):
    option = 'spaces'
    option_in_space = 'Members'
    button = 'Invite user using token'
    where = 'space'
    item_type = 'space invitation token'
    member = 'users'
    modal = 'Invite using token'

    click_element_on_lists_on_left_sidebar_menu(selenium, user, option,
                                                space_name, oz_page)
    click_on_option_of_space_on_left_sidebar_menu(selenium, user,
                                                  space_name, option_in_space,
                                                  oz_page)
    click_on_option_in_members_list_menu(selenium, user, button, where,
                                         member, oz_page, onepanel, popups)
    copy_token_from_modal(selenium, user)
    send_invitation_token_to_browser(selenium, user, item_type, oz_page,
                                     displays, clipboard, user_list,
                                     tmp_memory)
    close_modal(selenium, user, modal, modals)


def request_space_support_using_gui(selenium, user, oz_page, space_name,
                                    tmp_memory, displays, clipboard, receiver):
    where = 'Data'
    option = 'Providers'
    notify_type = 'info'
    text_regexp = '.*copied.*'
    item_type = 'token'

    click_on_option_in_the_sidebar(selenium, user, where, oz_page)
    click_element_on_lists_on_left_sidebar_menu(selenium, user, where.lower(),
                                                space_name, oz_page)
    click_on_option_of_space_on_left_sidebar_menu(selenium, user,
                                                  space_name, option, oz_page)
    click_get_support_button_on_providers_page(selenium, user, oz_page)
    click_copy_button_on_request_support_page(selenium, user, oz_page,
                                              displays, clipboard, tmp_memory)
    notify_visible_with_text(selenium, user, notify_type, text_regexp)
    send_copied_item_to_other_users(user, item_type, receiver,
                                    tmp_memory, displays, clipboard)


def join_space_in_oz_using_gui(selenium, user_list, oz_page, tmp_memory):
    for user in parse_seq(user_list):
        item_type = 'space invitation token'

        consume_received_token(selenium, user, oz_page,
                               tmp_memory, item_type)


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


def assert_there_is_no_provider_for_space_in_oz_gui(selenium, user, oz_page,
                                                    space_name):
    number = 0

    assert_number_of_supporting_providers_of_space(selenium, user,
                                                   number, space_name, oz_page)


def assert_user_is_member_of_space_gui(selenium, user, space_name, oz_page,
                                       user_list, onepanel):
    where = 'Members'
    option = 'sees'
    member_type = 'user'
    parent_type = 'space'

    click_on_option_of_space_on_left_sidebar_menu(selenium, user,
                                                  space_name, where, oz_page)

    for username in parse_seq(user_list):
        assert_member_is_in_parent_members_list(selenium, user, option,
                                                username, member_type,
                                                space_name, parent_type,
                                                oz_page, onepanel)


def assert_provider_does_not_support_space_in_oz_gui(selenium, user, oz_page,
                                                     space_name, provider_name,
                                                     hosts):
    where = 'spaces'
    option = 'Providers'

    click_element_on_lists_on_left_sidebar_menu(selenium, user, where,
                                                space_name, oz_page)
    click_on_option_of_space_on_left_sidebar_menu(selenium, user,
                                                  space_name, option, oz_page)
    refresh_site(selenium, user)
    assert_no_provider_for_space(selenium, user, provider_name,
                                 space_name, hosts, oz_page)


def assert_space_is_supported_by_provider_in_oz_gui(selenium, user, oz_page,
                                                    space_name, provider_name,
                                                    hosts):
    where = 'Data'
    option = 'Providers'

    click_on_option_in_the_sidebar(selenium, user, where, oz_page)
    click_element_on_lists_on_left_sidebar_menu(selenium, user, where.lower(),
                                                space_name, oz_page)
    click_on_option_of_space_on_left_sidebar_menu(selenium, user,
                                                  space_name, option, oz_page)
    assert_providers_list_contains_provider(selenium, user, provider_name,
                                            hosts, oz_page)


@given(parsers.parse('there is no "{space_name}" space in Onezone used '
                     'by user of {browser_id}'))
def leave_space_in_onezone(selenium, browser_id, space_name, oz_page, popups):
    option = 'Data'

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    time.sleep(2)
    try:
        leave_spaces_in_oz_using_gui(selenium, browser_id, space_name,
                                     oz_page, popups)
    except RuntimeError:
        pass


@given(parsers.parse('{user} user does not have access to any space'))
def leave_users_space_in_onezone_using_rest(hosts, users, user):
    zone_hostname = hosts['onezone']['hostname']

    list_users_spaces = http_get(ip=zone_hostname, port=OZ_REST_PORT,
                                 path=get_zone_rest_path('user', 'spaces'),
                                 auth=(user, users[user].password)).json()

    for space in list_users_spaces['spaces']:
        http_delete(ip=zone_hostname, port=OZ_REST_PORT,
                    path=get_zone_rest_path('user', 'spaces', space),
                    auth=(user, users[user].password))

