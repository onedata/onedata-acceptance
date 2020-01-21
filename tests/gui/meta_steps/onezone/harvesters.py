"""This module contains meta steps for operations on harvesters in Onezone
using web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.steps.onezone.members import *
from tests.gui.steps.onezone.discovery import (
    click_on_option_in_harvester_menu,
    click_button_on_discovery_on_left_sidebar_menu,
    type_text_to_input_field_in_discovery_page,
    type_endpoint_to_input_field_in_discovery_page,
    click_remove_space_option_in_menu_in_discover_spaces_page,
    click_create_button_in_discovery_page,
    click_on_option_of_harvester_on_left_sidebar_menu,
    type_index_name_to_input_field_in_indices_page,
    click_create_button_in_indices_page, click_button_in_harvester_spaces_page,
    choose_element_from_dropdown_in_add_element_modal,
    click_join_harvester_button_in_discovery_page,
    type_text_to_rename_input_field_in_discovery_page,
    confirm_harvester_rename_using_button)
from tests.gui.steps.onezone.spaces import (
    click_on_option_in_the_sidebar,
    click_element_on_lists_on_left_sidebar_menu,
    paste_harvester_invitation_token_into_text_field)
from tests.gui.steps.common.copy_paste import send_copied_item_to_other_users
from tests.gui.steps.common.miscellaneous import close_modal
from tests.gui.steps.modal import click_modal_button


@wt(parsers.parse('user of {browser_id} removes "{space_name}" space '
                  'from harvester'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_space_from_harvester(selenium, browser_id, oz_page, space_name):
    button = 'Remove'
    modal = 'Remove space from harvester'

    click_remove_space_option_in_menu_in_discover_spaces_page(selenium, browser_id,
                                                              space_name, oz_page)
    click_modal_button(selenium, browser_id, button, modal, modals)


@wt(parsers.parse('user of {browser_id} removes "{harvester_name}" '
                  'harvester in Onezone page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_harvester(selenium, browser_id, oz_page, harvester_name):
    where = 'Discovery'
    list_type = 'harvesters'
    option = 'Remove'
    modal = 'Remove harvester'

    click_on_option_in_the_sidebar(selenium, browser_id, where, oz_page)
    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id, list_type,
                                                harvester_name, oz_page)
    click_on_option_in_harvester_menu(selenium, browser_id, option,
                                      harvester_name, oz_page)
    click_modal_button(selenium, browser_id, option, modal, modals)


@wt(parsers.parse('user of {browser_id} creates "{harvester_name}" harvester '
                  'in Onezone page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_harvester(selenium, browser_id, oz_page, harvester_name, hosts):
    where = 'Discovery'
    input_name = 'name'
    endpoint_input = 'endpoint'
    button_name = 'create new harvester'

    click_on_option_in_the_sidebar(selenium, browser_id, where, oz_page)
    click_button_on_discovery_on_left_sidebar_menu(selenium, browser_id,
                                                   button_name, oz_page)
    type_text_to_input_field_in_discovery_page(selenium, browser_id, oz_page,
                                               harvester_name, input_name)
    type_endpoint_to_input_field_in_discovery_page(selenium, browser_id,
                                                   oz_page, endpoint_input,
                                                   hosts)
    click_create_button_in_discovery_page(selenium, browser_id, oz_page)


@wt(parsers.parse('user of {browser_id} adds "{space_name}" space to '
                  '"{harvester_name}" harvester using available spaces dropdown'))
@repeat_failed(timeout=WAIT_FRONTEND)
def join_space_to_harvester(selenium, browser_id, oz_page, space_name,
                            harvester_name, tmp_memory):
    option = 'Spaces'
    button_name = 'add one of your spaces'
    button_in_modal = 'Add'
    modal = 'Add one of spaces'
    element_type = 'space'
    modal_name = 'Add one of your spaces'

    click_on_option_of_harvester_on_left_sidebar_menu(selenium, browser_id,
                                                      harvester_name, option,
                                                      oz_page)
    click_button_in_harvester_spaces_page(selenium, browser_id, oz_page,
                                          button_name)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    choose_element_from_dropdown_in_add_element_modal(selenium, browser_id,
                                                      space_name, modals,
                                                      element_type)
    click_modal_button(selenium, browser_id, button_in_modal, modal, modals)


@wt(parsers.parse('user of {browser_id} adds "{group_name}" group to '
                  '"{harvester_name}" harvester '
                  'using available groups dropdown'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_group_to_harvester(selenium, browser_id, oz_page, group_name,
                           harvester_name, onepanel, popups, tmp_memory):
    option = 'Members'
    button = 'Add one of your groups'
    where = 'group'
    member = 'harvester'
    button_in_modal = 'Add'
    modal = 'Add one of groups'
    modal_name = 'Add one of your groups'

    click_on_option_of_harvester_on_left_sidebar_menu(selenium, browser_id,
                                                      harvester_name, option,
                                                      oz_page)
    click_on_option_in_members_list_menu(selenium, browser_id, button,
                                         member, where + 's', oz_page,
                                         onepanel, popups)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    choose_element_from_dropdown_in_add_element_modal(selenium, browser_id,
                                                      group_name, modals,
                                                      where)
    click_modal_button(selenium, browser_id, button_in_modal, modal, modals)


@wt(parsers.parse('user of {browser_id} creates "{index_name}" index '
                  'in "{harvester_name}" harvester in Discovery page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_index_in_harvester(selenium, browser_id, oz_page, index_name,
                              harvester_name):
    option = 'Indices'

    click_on_option_of_harvester_on_left_sidebar_menu(selenium, browser_id,
                                                      harvester_name, option,
                                                      oz_page)
    type_index_name_to_input_field_in_indices_page(selenium, browser_id,
                                                   oz_page, index_name)
    click_create_button_in_indices_page(selenium, browser_id, oz_page)


@wt(parsers.parse('user of {browser_id1} sends invitation token '
                  'from "{harvester_name}" harvester to user of {browser_id2}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def send_invitation_token(selenium, browser_id1, oz_page, harvester_name,
                          browser_id2, tmp_memory, displays, clipboard,
                          onepanel, popups):
    where = 'Discovery'
    list_type = 'harvester'
    option = 'Members'
    button = 'Invite user using token'
    member = 'users'
    modal = 'Invite using token'
    item_type = 'token'

    click_on_option_in_the_sidebar(selenium, browser_id1, where, oz_page)
    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id1,
                                                list_type + 's',
                                                harvester_name, oz_page)
    click_on_option_of_harvester_on_left_sidebar_menu(selenium, browser_id1,
                                                      harvester_name, option,
                                                      oz_page)
    click_on_option_in_members_list_menu(selenium, browser_id1, button,
                                         list_type, member, oz_page,
                                         onepanel, popups)
    copy_token_from_modal(selenium, browser_id1)
    close_modal(selenium, browser_id1, modal, modals)
    send_copied_item_to_other_users(browser_id1, item_type, browser_id2,
                                    tmp_memory, displays, clipboard)


@wt(parsers.parse('user of {browser_id} joins to harvester in Onezone page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def join_to_harvester(selenium, browser_id, oz_page, clipboard, displays):
    button_name = 'Join to harvester'
    where = 'discovery'

    click_button_on_discovery_on_left_sidebar_menu(selenium, browser_id,
                                                   button_name, oz_page)
    paste_harvester_invitation_token_into_text_field(selenium, browser_id,
                                                     oz_page, clipboard,
                                                     displays, where)
    click_join_harvester_button_in_discovery_page(selenium, browser_id,
                                                  oz_page)


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>checks|unchecks) '
               '"(?P<privilege>.*)" privilege in '
               '"(?P<privilege_group>.*)" privileges group for '
               '(?P<user_name>.*) user in "(?P<harvester_name>.*)" harvester'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_nested_privilege_in_harvester(selenium, browser_id, oz_page,
                                         onepanel, privilege, option,
                                         privilege_group, user_name,
                                         harvester_name):
    where = 'harvester'
    list_type = 'user'
    button_name = 'Save'
    menu_option = 'Members'

    click_on_option_of_harvester_on_left_sidebar_menu(selenium, browser_id,
                                                      harvester_name,
                                                      menu_option, oz_page)
    click_element_in_members_list(selenium, browser_id, user_name,
                                  oz_page, where, list_type + 's', onepanel)
    expand_privilege_for_member(selenium, browser_id, privilege_group, oz_page,
                                where, user_name, list_type, onepanel)
    click_nested_privilege_toggle_for_member(selenium, browser_id, option,
                                             where, privilege, user_name,
                                             oz_page, list_type,
                                             privilege_group, onepanel)
    click_button_on_element_header_in_members(selenium, browser_id, button_name,
                                              oz_page, where, user_name,
                                              list_type, onepanel)


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>checks|unchecks) '
               '"(?P<privilege_name>.*?)" privileges group for '
               '(?P<user_name>.*) user in "(?P<harvester_name>.*)" harvester'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_privilege_in_harvester(selenium, browser_id, oz_page, onepanel,
                                  privilege_name, option, user_name,
                                  harvester_name):
    where = 'harvester'
    list_type = 'user'
    button_name = 'Save'
    menu_option = 'Members'

    click_on_option_of_harvester_on_left_sidebar_menu(selenium, browser_id,
                                                      harvester_name,
                                                      menu_option, oz_page)
    click_element_in_members_list(selenium, browser_id, user_name,
                                  oz_page, where, list_type + 's', onepanel)
    click_privilege_toggle_for_member(selenium, browser_id, option, where,
                                      privilege_name, user_name, oz_page,
                                      list_type)
    click_button_on_element_header_in_members(selenium, browser_id, button_name,
                                              oz_page, where, user_name,
                                              list_type, onepanel)


@wt(parsers.parse('user of {browser_id} renames "{harvester_name}" harvester '
                  'to "{harvester_renamed}" in Onezone page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def rename_harvester(selenium, browser_id, oz_page, harvester_name,
                     harvester_renamed):
    option = 'harvesters'
    menu_option = 'Rename'

    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id, option,
                                                harvester_name, oz_page)
    click_on_option_in_harvester_menu(selenium, browser_id, menu_option,
                                      harvester_name, oz_page)
    type_text_to_rename_input_field_in_discovery_page(selenium, browser_id,
                                                      oz_page, harvester_renamed)
    confirm_harvester_rename_using_button(selenium, browser_id, oz_page)

