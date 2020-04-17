"""This module contains meta steps for operations on clusters in Onezone
using web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.meta_steps.onezone.tokens import (
    consume_token_from_copied_token)
from tests.gui.steps.onezone.members import *
from tests.utils.utils import repeat_failed
from tests.gui.steps.onezone.spaces import click_on_option_in_the_sidebar
from tests.gui.steps.onezone.clusters import click_on_record_in_clusters_menu
from tests.gui.steps.onepanel.common import wt_click_on_subitem_for_item
from tests.gui.steps.common.copy_paste import send_copied_item_to_other_users
from tests.gui.steps.onezone.discovery import (
    choose_element_from_dropdown_in_add_element_modal)
from tests.gui.steps.modal import click_modal_button


@wt(parsers.parse('user of {browser_id} invites user of {browser} '
                  'to "{cluster}" cluster'))
@repeat_failed(timeout=WAIT_FRONTEND)
def invite_user_to_cluster(selenium, browser_id, browser, cluster, oz_page,
                           hosts, onepanel, tmp_memory, displays,
                           clipboard, popups):
    option = 'Clusters'
    sub_item = 'Members'
    button = 'Invite user using token'
    where = option.lower()[:-1]
    member = 'users'
    modal = 'Invite using token'
    item_type = 'token'
    cancel_button = 'Cancel'

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_on_record_in_clusters_menu(selenium, browser_id, oz_page, cluster,
                                     hosts)
    wt_click_on_subitem_for_item(selenium, browser_id, option,
                                 sub_item, cluster, onepanel, hosts)

    click_on_option_in_members_list_menu(selenium, browser_id, button,
                                         where, member, oz_page,
                                         onepanel, popups)
    copy_token_from_modal(selenium, browser_id)
    click_modal_button(selenium, browser_id, cancel_button, modal, modals)
    send_copied_item_to_other_users(browser_id, item_type, browser,
                                    tmp_memory, displays, clipboard)


@wt(parsers.parse('user of {browser_id} joins to cluster'))
@repeat_failed(timeout=WAIT_FRONTEND)
def join_to_cluster(selenium, browser_id, oz_page, displays, clipboard):
    consume_token_from_copied_token(selenium, browser_id, oz_page,
                                    clipboard, displays)


@wt(parsers.parse('user of {browser_id} {option} nested "{nested_privilege}" '
                  'privilege in "{parent_privilege}" privilege '
                  'for {user_name} user in {where} page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_nested_privilege_in_cluster(selenium, browser_id, oz_page,
                                       onepanel, nested_privilege, option,
                                       parent_privilege, where, user_name):
    member_type = 'user'
    button = 'Save'
    list_type = 'users'

    click_element_in_members_list(selenium, browser_id, user_name,
                                  oz_page, where, list_type, onepanel)
    see_privileges_for_member(selenium, browser_id, oz_page, where,
                              member_type, user_name, onepanel)
    expand_privilege_for_member(selenium, browser_id, parent_privilege,
                                oz_page, where, user_name,
                                member_type, onepanel)
    click_nested_privilege_toggle_for_member(selenium, browser_id, option,
                                             where, nested_privilege,
                                             user_name, oz_page, member_type,
                                             parent_privilege, onepanel)
    click_button_on_element_header_in_members(selenium, browser_id, button,
                                              oz_page, where, user_name,
                                              member_type, onepanel)


@wt(parsers.parse('user of {browser_id} adds "{group_name}" group to '
                  '"{cluster_name}" cluster'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_group_to_cluster(selenium, browser_id, oz_page, onepanel, hosts,
                         group_name, cluster_name, popups):
    sidebar = 'CLUSTERS'
    menu_option = 'Members'
    sub_item = 'Add one of your groups'
    button_name = 'Add'
    modal = 'Add one of groups'
    where = 'cluster'
    member = 'groups'
    element_type = 'group'

    click_on_option_in_the_sidebar(selenium, browser_id, sidebar, oz_page)
    click_on_record_in_clusters_menu(selenium, browser_id, oz_page,
                                     cluster_name, hosts)
    wt_click_on_subitem_for_item(selenium, browser_id, sidebar,
                                 menu_option, cluster_name, onepanel, hosts)
    click_on_option_in_members_list_menu(selenium, browser_id, sub_item,
                                         where, member, oz_page,
                                         onepanel, popups)
    choose_element_from_dropdown_in_add_element_modal(selenium, browser_id,
                                                      group_name, modals,
                                                      element_type)
    click_modal_button(selenium, browser_id, button_name, modal, modals)

