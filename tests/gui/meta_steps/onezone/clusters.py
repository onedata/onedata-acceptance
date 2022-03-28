"""This module contains meta steps for operations on clusters in Onezone
using web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time

from tests.gui.meta_steps.onezone.tokens import (
    consume_token_from_copied_token)
from tests.gui.steps.common.miscellaneous import click_option_in_popup_text_menu
from tests.gui.steps.onezone.members import *
from tests.utils.bdd_utils import given
from tests.utils.utils import repeat_failed
from tests.gui.steps.onezone.spaces import click_on_option_in_the_sidebar
from tests.gui.steps.onezone.clusters import (
    click_on_record_in_clusters_menu, click_cluster_menu_button,
    click_button_in_gui_settings_page,
    click_option_of_record_in_the_sidebar, write_input_in_gui_settings_page,
    remove_notification_in_gui_settings_page)
from tests.gui.steps.onepanel.common import wt_click_on_subitem_for_item
from tests.gui.steps.common.copy_paste import send_copied_item_to_other_users
from tests.gui.steps.onezone.harvesters.discovery import (
    choose_element_from_dropdown_in_add_element_modal)
from tests.gui.steps.modal import click_modal_button, close_modal


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

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_on_record_in_clusters_menu(selenium, browser_id, oz_page, cluster,
                                     hosts)
    wt_click_on_subitem_for_item(selenium, browser_id, option,
                                 sub_item, cluster, onepanel, hosts)

    click_on_option_in_members_list_menu(selenium, browser_id, button,
                                         where, member, oz_page,
                                         onepanel, popups)
    copy_token_from_modal(selenium, browser_id)
    close_modal(selenium, browser_id, modal, modals)
    send_copied_item_to_other_users(browser_id, item_type, browser,
                                    tmp_memory, displays, clipboard)


@wt(parsers.parse('user of {browser_id} joins to cluster'))
@repeat_failed(timeout=WAIT_FRONTEND)
def join_to_cluster(selenium, browser_id, oz_page, displays, clipboard):
    consume_token_from_copied_token(selenium, browser_id, oz_page,
                                    clipboard, displays)


@wt(parsers.parse('user of {browser_id} sets following privileges '
                  'for {user_name} user in {where} page:\n{config}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_privilege_config_in_cluster(selenium, browser_id, oz_page,
                                       onepanel, where, user_name, config):
    member_type = 'user'
    list_type = 'users'

    click_element_in_members_list(selenium, browser_id, user_name,
                                  oz_page, where, list_type, onepanel)
    see_privileges_for_member(selenium, browser_id, oz_page, where,
                              member_type, user_name, onepanel)
    set_privileges_in_members_subpage(selenium, browser_id, user_name,
                                      member_type, where, config, onepanel,
                                      oz_page)


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
                                                      element_type, popups)
    click_modal_button(selenium, browser_id, button_name, modal, modals)


@given(parsers.re('user of (?P<browser_id>.*) sees no "(?P<member_name>.*)" '
                  '(?P<member_type>user|group) in "(?P<name>.*)" '
                  '(?P<where>cluster|group|harvester) members'))
def no_member_in_parent(selenium, browser_id, member_name, member_type, name,
                        oz_page, tmp_memory, onepanel, where, popups):
    try:
        remove_member_from_parent(selenium, browser_id, member_name,
                                  member_type, name, oz_page, tmp_memory,
                                  onepanel, where, popups)
    except RuntimeError:
        pass


@wt(parsers.parse('user of {browser_id} remembers "{provider}" cluster id'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remember_cluster_id(selenium, browser_id, provider, oz_page, hosts,
                        popups, tmp_memory, clipboard, displays):
    option = 'Copy ID'
    click_on_record_in_clusters_menu(selenium, browser_id, oz_page, provider,
                                     hosts)
    click_cluster_menu_button(selenium, browser_id, provider, oz_page, hosts)
    click_option_in_popup_text_menu(selenium, browser_id, option, popups)
    cluster_id = clipboard.paste(display=displays[browser_id])
    tmp_memory[provider]['cluster id'] = cluster_id


@wt(parsers.re(r'user of (?P<browser_id>\w+) (?P<operation>removes) '
               '"(?P<text>.*)" text from (?P<kind_of_agreement>.*) in GUI'
               ' settings page of "(?P<record>.*)"'))
@wt(parsers.re(r'user of (?P<browser_id>\w+) (?P<operation>sets) '
               '(?P<kind_of_agreement>.*): "(?P<text>.*)" in GUI settings page'
               ' of "(?P<record>.*)"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def set_gui_settings(selenium, browser_id, oz_page, record, hosts,
                     kind_of_agreement, text, operation):
    menu = 'Clusters'
    option = 'GUI settings'
    box = kind_of_agreement + ' input'
    button = 'save ' + kind_of_agreement
    click_on_option_in_the_sidebar(selenium, browser_id, menu, oz_page)
    click_on_record_in_clusters_menu(selenium, browser_id, oz_page, record,
                                     hosts)
    click_option_of_record_in_the_sidebar(selenium, browser_id, oz_page, option)
    click_button_in_gui_settings_page(selenium, browser_id, oz_page,
                                      kind_of_agreement)
    if operation == 'sets':
        write_input_in_gui_settings_page(selenium, browser_id, oz_page, box,
                                         text)
    else:
        remove_notification_in_gui_settings_page(selenium, browser_id, oz_page,
                                                 kind_of_agreement)
    click_button_in_gui_settings_page(selenium, browser_id, oz_page,
                                      button)
    # wait for save button to be clicked
    time.sleep(0.1)


@wt(parsers.parse('user of {browser_id} inserts {kind_of_agreement} link in '
                  'cookie consent notification in GUI settings page of '
                  '"{record}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def insert_setting_link(selenium, browser_id, oz_page, kind_of_agreement):
    link = 'insert ' + kind_of_agreement + ' link'
    button = 'save cookie consent notification'
    click_button_in_gui_settings_page(selenium, browser_id, oz_page,
                                      link)
    click_button_in_gui_settings_page(selenium, browser_id, oz_page,
                                      button)

