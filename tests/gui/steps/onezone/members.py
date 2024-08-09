"""This module contains gherkin steps to run acceptance tests featuring members
management in onezone web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import yaml
import time

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.meta_steps.onezone.common import search_for_members
from tests.gui.steps.modals.modal import (wt_wait_for_modal_to_appear,
                                          assert_element_text)
from tests.gui.steps.onepanel.common import wt_click_on_subitem_for_item
from tests.gui.steps.onezone.automation.automation_basic import \
    click_on_option_of_inventory_on_left_sidebar_menu
from tests.gui.steps.onezone.clusters import click_on_record_in_clusters_menu
from tests.gui.steps.onezone.harvesters.discovery import (
    click_on_option_of_harvester_on_left_sidebar_menu)
from tests.gui.steps.onezone.groups import go_to_group_subpage
from tests.gui.steps.onezone.spaces import (
    click_on_option_of_space_on_left_sidebar_menu,
    click_element_on_lists_on_left_sidebar_menu)
from tests.gui.utils.common.modals import Modals as modals
from tests.gui.utils.generic import parse_seq
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed

MENU_ELEM_TO_TAB_NAME = {'space': 'data', 'harvester': 'discovery',
                         'automation': 'automation', 'inventory': 'automation'}


def _change_to_tab_name(element):
    return MENU_ELEM_TO_TAB_NAME.get(element, element + 's')


def _find_members_page(onepanel, oz_page, driver, where):
    tab_name = _change_to_tab_name(where)
    if tab_name == 'clusters':
        return onepanel(driver).content.members
    else:
        return oz_page(driver)[tab_name].members_page


def _change_membership_to_name(membership_type, subject_type):
    if not subject_type.endswith('s'):
        subject_type += 's'
    return membership_type + '_' + subject_type


def get_privilege_tree(selenium, browser_id, onepanel, oz_page, where,
                       list_type, member_name):
    driver = selenium[browser_id]
    page = _find_members_page(onepanel, oz_page, driver, where)
    elem = getattr(page, list_type).items[member_name]
    # wait for panel to expand
    for _ in range(40):
        if 'active' in elem.web_elem.get_attribute('class'):
            break
        else:
            time.sleep(0.1)
    else:
        assert 'active' in elem.web_elem.get_attribute('class'), (
            f'did not manage to expand {list_type} panel of {member_name}')
    return elem.privilege_tree


@wt(parsers.re('user of (?P<browser_id>.*) sees that "(?P<member_name>.*)" '
               '(?P<member_type>user|group) is member of '
               '"(?P<parent_name>.*)" (?P<parent_type>space|group) '
               'in (?P<where>space|group) memberships mode'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_element_is_member_of_parent_in_memberships(selenium, browser_id,
                                                      member_name, parent_name,
                                                      member_type, parent_type,
                                                      oz_page, where):
    driver = selenium[browser_id]
    where = _change_to_tab_name(where)
    records = oz_page(driver)[where].members_page.memberships

    def fun(record, member_index):
        if member_type != 'user':
            return True
        elif member_index == 0:
            return True
        return False

    if not search_for_members(driver, records, member_name, parent_name, fun):
        raise RuntimeError(
            'not found "{}" {} as a member of "{}" {}'.format(member_name,
                                                              member_type,
                                                              parent_name,
                                                              parent_type))


@wt(parsers.re('user of (?P<browser_id>.*) does not see that '
               '"(?P<member_name>.*)" (?P<member_type>user|group) is '
               'member of "(?P<parent_name>.*)" (?P<parent_type>space|group) '
               'in (?P<where>space|group) memberships mode'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_element_is_not_member_of_parent_in_memberships(selenium, browser_id,
                                                          member_name, where,
                                                          parent_name, oz_page,
                                                          member_type,
                                                          parent_type):
    driver = selenium[browser_id]
    where = _change_to_tab_name(where)
    records = oz_page(driver)[where].members_page.memberships

    def fun(record, member_index):
        if member_type != 'user':
            raise RuntimeError(
                'found "{}" {} as a member of "{}" {}'.format(member_name,
                                                              member_type,
                                                              parent_name,
                                                              parent_type))
        elif member_index == 0:
            raise RuntimeError(
                'found "{}" {} as a member of "{}" {}'.format(member_name,
                                                              member_type,
                                                              parent_name,
                                                              parent_type))
        return False

    search_for_members(driver, records, member_name, parent_name, fun)


@wt(parsers.re('user of (?P<browser_id>.*) sees (?P<number>.*) '
               'membership rows? in (?P<where>space|group) memberships mode'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_count_membership_rows(selenium, browser_id, number, oz_page, where):
    driver = selenium[browser_id]
    where = _change_to_tab_name(where)
    records = oz_page(driver)[where].members_page.memberships
    count_records = len(records)

    assert count_records == int(number), ('found {} membership rows '
                                          'instead of {}'.format(number,
                                                                 count_records))


@wt(parsers.re('user of (?P<browser_id>.*) sees '
               '(?P<number_direct_groups>.*) direct, '
               '(?P<number_effective_groups>.*) effective groups and '
               '(?P<number_direct_users>.*) direct, '
               '(?P<number_effective_users>.*) effective users in space '
               'members tile'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_all_members_number_in_space_members_tile(selenium, oz_page,
                                                    browser_id,
                                                    number_direct_groups: int,
                                                    number_effective_groups: int,
                                                    number_direct_users: int,
                                                    number_effective_users: int):
    direct = 'direct'
    effective = 'effective'
    groups = 'groups'
    users = 'users'

    assert_members_number_in_space_members_tile(selenium, oz_page, browser_id,
                                                number_direct_groups, direct,
                                                groups)
    assert_members_number_in_space_members_tile(selenium, oz_page, browser_id,
                                                number_effective_groups,
                                                effective,
                                                groups)
    assert_members_number_in_space_members_tile(selenium, oz_page, browser_id,
                                                number_direct_users, direct,
                                                users)
    assert_members_number_in_space_members_tile(selenium, oz_page, browser_id,
                                                number_effective_users,
                                                effective,
                                                users)


@wt(parsers.re('user of (?P<browser_id>.*) sees (?P<number>\d+) '
               '(?P<membership_type>direct|effective) '
               '(?P<subject_type>groups?|users?) in space members tile'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_members_number_in_space_members_tile(selenium, oz_page, browser_id,
                                                number: int, membership_type,
                                                subject_type):
    driver = selenium[browser_id]
    members_tile = oz_page(driver)['data'].overview_page.members_tile
    name = _change_membership_to_name(membership_type, subject_type)
    members_count = getattr(members_tile, name)

    error_msg = (f'found {number} {membership_type} {subject_type} instead of '
                 f'{members_count}')
    assert int(members_count) == number, error_msg


@wt(parsers.re('user of (?P<browser_id>.*) clicks on "(?P<member_name>.*)" '
               'member relation menu button to '
               '"(?P<name>.*)" (?P<where>space|group)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_relation_menu_button(selenium, browser_id, member_name, name, oz_page,
                               where):
    driver = selenium[browser_id]
    where = _change_to_tab_name(where)
    records = oz_page(driver)[where].members_page.memberships

    def click_on_menu(record, member_index):
        record.relations[member_index].click_relation_menu_button(driver)
        return True

    search_for_members(driver, records, member_name, name, click_on_menu)


@wt(parsers.re('user of (?P<browser_id>.*) clicks on "(?P<option>.*)" '
               'in (?P<where>space|group) membership relation menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_relation_menu_button(selenium, browser_id, option, popups):
    driver = selenium[browser_id]
    popups(driver).membership_relation_menu.options[option].click()


@wt(parsers.re('user of (?P<browser_id>.*) clicks "(?P<type_name>.*)" '
               '(?P<type>user|group) to close his dropdown list in '
               '"(?P<member_name>.*)" (?P<where>space|group|cluster|harvester) '
               'members (?P<list_type>users|groups) list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_element_to_close_its_dropdown(selenium, browser_id, type_name,
                                        oz_page, where, list_type, onepanel):
    driver = selenium[browser_id]
    page = _find_members_page(onepanel, oz_page, driver, where)
    getattr(page, list_type).items[type_name].header.click()


@wt(parsers.re('user of (?P<browser_id>.*) clicks "(?P<member_name>.*)" '
               '(?P<member_type>user|group) in "(?P<name>.*)" '
               '(?P<where>space|group|cluster|harvester|automation) members '
               '(?P<list_type>users|groups) list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_element_in_members_list(selenium, browser_id, member_name, oz_page,
                                  where, list_type, onepanel):
    driver = selenium[browser_id]
    page = _find_members_page(onepanel, oz_page, driver, where)

    members_list = getattr(page, list_type).items
    for member in members_list:
        if member.is_opened():
            member.header.click()

    members_list[member_name].click()


@wt(parsers.parse('user of {browser_id} clicks on '
                  '"generate an invitation token" text in group '
                  '"{group}" members {member} list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_generate_token_in_subgroups_list(selenium, browser_id, group, oz_page,
                                           member):
    page = oz_page(selenium[browser_id]).get_page_and_click('groups')
    page.elements_list[group]()
    page.elements_list[group].members()
    getattr(page.main_page.members, member).generate_token()


@wt(parsers.re('user of (?P<browser_id>.*) clicks on "(?P<button>.*)" button '
               'in (?P<member>users|groups) list menu in '
               '"(?P<name>.*)" (?P<where>group|space|cluster|harvester'
               '|automation) members view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_in_members_list_menu(selenium, browser_id, button, where,
                                         member, oz_page, onepanel, popups):
    driver = selenium[browser_id]

    page = _find_members_page(onepanel, oz_page, driver, where)
    getattr(page, member).header.menu_button()

    popups(driver).menu_popup_with_text.menu[button]()


@wt(parsers.re('user of (?P<browser_id>.*) sees that area with '
               '(?P<who>user|group) invitation token has appeared'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_token_area_appeared(selenium, browser_id, who, tmp_memory):
    modal_name = 'invite {} using token'.format(who)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)


@wt(parsers.parse('user of {browser_id} sees non-empty token in token area'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_generated_token_is_present(selenium, browser_id):
    try:
        text = modals(selenium[browser_id]).invite_using_token.token
        assert len(text) > 0, 'Token is empty, while it should be non-empty'
    except RuntimeError:
        raise RuntimeError('No token area found on page')


@wt(parsers.re('user of (?P<browser_id>.*) copies invitation token '
               'from modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_token_from_modal(selenium, browser_id):
    modals(selenium[browser_id]).invite_using_token.copy()


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>does not see|sees) '
               '"(?P<child>.*)" as "(?P<parent>.*)" child'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_element_is_groups_child(selenium, browser_id, option, child, parent,
                                   oz_page):
    page = oz_page(selenium[browser_id]).get_page_and_click('groups')
    page.elements_list[parent]()
    page.elements_list[parent].members()

    try:
        page.members_page.groups.items[child]
    except RuntimeError:
        assert option == 'does not see', '"{}" is not "{}" child'.format(child,
                                                                         parent)
    else:
        assert option == 'sees', '"{}" is "{}" child'.format(child, parent)


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>does not see|sees) '
               '"(?P<member_name>.*)" (?P<member_type>user|group) '
               'on "(?P<parent_name>.*)" ('
               '?P<parent_type>user|group|space|cluster) '
               'members list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_member_is_in_parent_members_list(selenium, browser_id, option,
                                            member_name, member_type,
                                            parent_name, parent_type, oz_page,
                                            onepanel):
    driver = selenium[browser_id]
    page = _find_members_page(onepanel, oz_page, driver, parent_type)

    try:
        if member_type == 'user':
            page.users.items[member_name]
        else:
            page.groups.items[member_name]
    except RuntimeError:
        assert option == 'does not see', ('{} "{}" not found on {} "{}" '
                                          'members list'.format(member_type,
                                                                member_name,
                                                                parent_type,
                                                                parent_name))
    else:
        assert option == 'sees', (
            '{} "{}" found on {} "{}" members list'.format(member_type,
                                                           member_name,
                                                           parent_type,
                                                           parent_name))


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>does not see|sees) '
               '"(?P<username>.*)" user on "(?P<space_name>.*)" '
               'space members list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_user_in_space_members_list(selenium, browser_id, option, username,
                                     space_name, oz_page):
    driver = selenium[browser_id]
    page = oz_page(driver)['data']
    page.spaces_header_list[space_name]()
    page.elements_list[space_name].members()
    try:
        page.members_page.users.items[username]
    except RuntimeError:
        assert option == 'does not see', ('user "{}" not found on "{}" space '
                                          'members list'.format(username,
                                                                space_name))
    else:
        assert option == 'sees', ('user "{}" found on "{}" space '
                                  'members list'.format(username, space_name))


@wt(parsers.re('user of (?P<browser_id>.*) removes "(?P<member_name>.*)" '
               '(?P<member_type>user|group) from "(?P<name>.*)" '
               '(?P<where>cluster|group|harvester|space|automation) members'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_member_from_parent(selenium, browser_id, member_name, member_type,
                              name, oz_page, tmp_memory, onepanel, where,
                              popups):
    driver = selenium[browser_id]
    if where != 'cluster':
        main_page = oz_page(selenium[browser_id]).get_page_and_click(_change_to_tab_name(where))
        main_page.elements_list[name]()
        main_page.elements_list[name].members()
    members_page = _find_members_page(onepanel, oz_page, driver, where)
    list_name = member_type + 's'
    (getattr(members_page, list_name).items[member_name].header.click_menu(
        selenium[browser_id]))

    if member_type == 'user':
        modal_name = 'remove user from '
    elif member_type == 'group' and where != 'group':
        modal_name = 'remove group from '
    else:
        modal_name = 'remove subgroup from '

    if where == 'automation':
        where = 'atm. inventory'
    modal_name += where

    popups(driver).menu_popup_with_text.menu['Remove this member']()

    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    modals(driver).remove_modal.remove()


@wt(parsers.re('user of (?P<browser_id>.*) clicks "(?P<option>( |.)*)" for '
               '"(?P<username>.*)" user in users list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_member_option_on_members_page(selenium, browser_id, option,
                                        oz_page, popups, tmp_memory, username):
    driver = selenium[browser_id]

    page = oz_page(driver)['data'].members_page
    page.users.items[username].click_member_menu_button(driver)
    popups(driver).menu_popup_with_text.menu[option]()


@wt(parsers.re('user of (?P<browser_id>.*) sees (?P<options>( |.)*) (is|are) '
               '(?P<state>enabled|disabled) for "(?P<username>.*)" user in '
               'users list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_options_for_user_are_enabled_or_disabled(selenium, browser_id,
                                                    options,
                                                    oz_page, popups,
                                                    username, state):
    driver = selenium[browser_id]
    page = oz_page(driver)['data'].members_page
    page.users.items[username].click_member_menu_button(driver)

    for option in parse_seq(options):
        enabled = popups(driver).menu_popup_with_text.menu[option].is_enabled()
        error_msg = f'Popup {option} is in invalid state'
        if state == 'enabled':
            assert enabled, error_msg
        else:
            assert not enabled, error_msg


def _get_cluster_members(selenium, browser_id, oz_page, onepanel):
    driver = selenium[browser_id]
    where = 'cluster'
    members_page = _find_members_page(onepanel, oz_page, driver, where)
    list_name = 'users'
    return getattr(members_page, list_name).items


@wt(parsers.re('user of (?P<browser_id>.*) sees "(?P<member_name>.*)" '
               'user in cluster members'))
@repeat_failed(timeout=WAIT_BACKEND * 4)
def assert_user_in_cluster_members_page(selenium, browser_id, member_name,
                                        oz_page, onepanel):
    cluster_members = _get_cluster_members(selenium, browser_id, oz_page,
                                           onepanel)

    assert member_name in cluster_members, (f'{member_name} user is not found '
                                            f'in cluster members list')


@wt(parsers.re('user of (?P<browser_id>.*) does not see "(?P<member_name>.*)" '
               'user in cluster members'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_user_not_in_cluster_members_page(selenium, browser_id, member_name,
                                            oz_page, onepanel):
    cluster_members = _get_cluster_members(selenium, browser_id, oz_page,
                                           onepanel)

    assert member_name not in cluster_members, (f'{member_name} user is found '
                                                f'in cluster members list')


@wt(parsers.re('user of (?P<browser_id>.*) copies "(?P<group>.*)" '
               '(?P<who>user|group) invitation token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_invitation_token(selenium, browser_id, group, who, oz_page, tmp_memory,
                          popups):
    driver = selenium[browser_id]
    page = oz_page(driver).get_page_and_click('groups')
    page.elements_list[group]()

    getattr(page.main_page.members, who + 's').header.menu_button()
    button = 'Invite {} using token'.format(who)

    popups(driver).menu_popup_with_text.menu[button].click()

    wt_wait_for_modal_to_appear(selenium, browser_id, button, tmp_memory)
    modals(selenium[browser_id]).invite_using_token.copy()
    modals(selenium[browser_id]).invite_using_token.close()


@wt(parsers.re('user of (?P<browser_id>.*) gets group "(?P<group>.*)" '
               '(?P<who>user|group) invitation token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def get_invitation_token(selenium, browser_id, group, who, oz_page, tmp_memory,
                         popups):
    driver = selenium[browser_id]
    page = oz_page(driver)['groups']
    page.elements_list[group]()
    page.main_page.menu_button()
    popups(driver).menu_popup_with_text.menu['Invite ' + who]()
    token = page.members_page.token.token
    tmp_memory[browser_id]['token'] = token


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>sets|tries to set) '
               'following privileges for "(?P<member_name>.*)" '
               '(?P<member_type>user|group) '
               'in (?P<where>space|group|harvester|cluster|automation) members '
               r'subpage:\n(?P<config>(.|\s)*)'))
def set_privileges_in_members_subpage(selenium, browser_id, member_name,
                                      member_type, where, config, onepanel,
                                      oz_page, option):
    try:
        assert_privileges_in_members_subpage(selenium, browser_id, member_name,
                                             member_type, where, config,
                                             onepanel, oz_page, True)
    except AssertionError:
        button = 'Save'
        member_type_new = member_type + 's'
        privileges = yaml.load(config)
        tree = get_privilege_tree(selenium, browser_id, onepanel, oz_page, where,
                                  member_type_new, member_name)
        result = tree.set_privileges(selenium, browser_id, privileges, True)
        if option == 'sets':
            click_button_on_element_header_in_members_and_wait(
                selenium, browser_id, button, oz_page, where, onepanel, tree)
        else:
            assert not result, 'Modify privilege should not be possible'


@wt(parsers.re('user of (?P<browser_id>.*) sets all privileges true for '
               '"(?P<member_name>.*)" (?P<member_type>user|group) '
               'in (?P<where>space|group|harvester|cluster|automation) '
               'members subpage'))
def set_all_privileges_true_in_members_subpage(selenium, browser_id,
                                               member_name,  member_type, where,
                                               onepanel, oz_page):
    option = 'Save'
    member_type_new = member_type + 's'

    tree = get_privilege_tree(selenium, browser_id, onepanel, oz_page, where,
                              member_type_new, member_name)
    tree.set_all_true()
    click_button_on_element_header_in_members(selenium, browser_id, option,
                                              oz_page, where, onepanel)


@wt(parsers.re('user of (?P<browser_id>.*) sets following privileges for '
               '"(?P<member_name>.*)" (?P<member_type>user|group) '
               'in (?P<where>space|group|harvester|cluster) members subpage '
               'when all other are granted:'
               r'\n(?P<config>(.|\s)*)'))
def set_some_privileges_in_members_subpage_other_granted(selenium, browser_id,
                                                         member_name,
                                                         member_type, where,
                                                         config, onepanel,
                                                         oz_page):
    option = 'sets'
    tree = get_privilege_tree(selenium, browser_id, onepanel, oz_page, where,
                              member_type + 's', member_name)
    tree.set_all_true()
    set_privileges_in_members_subpage(selenium, browser_id, member_name,
                                      member_type, where, config, onepanel,
                                      oz_page, option)


@wt(parsers.re('user of (?P<browser_id>.*) sets following privileges on modal:'
               r'\n(?P<config>(.|\s)*)'))
def set_privileges_in_members_subpage_on_modal(selenium, browser_id, config,
                                               modals):
    driver = selenium[browser_id]
    privileges = yaml.load(config)
    tree = modals(driver).change_privileges.privilege_tree
    tree.set_privileges(selenium, browser_id, privileges)
    modals(driver).change_privileges.save_button.click()


@wt(parsers.re('user of (?P<browser_id>.*) sees following '
               '(?P<option>effective |)privileges of '
               '"(?P<member_name>.*)" (?P<member_type>user|group) '
               'in (?P<where>space|group|harvester|automation|cluster) '
               'members subpage:\n(?P<config>(.|\s)*)'))
def assert_privileges_in_members_subpage(selenium, browser_id, member_name,
                                         member_type, where, config, onepanel,
                                         oz_page, option):
    member_type = member_type + 's'
    privileges = yaml.load(config)
    tree = get_privilege_tree(selenium, browser_id, onepanel, oz_page, where,
                              member_type, member_name)
    is_direct_privileges = False if option == 'effective ' else True
    # wait for set privileges to be visible in gui
    try:
        tree.assert_privileges(selenium, browser_id, privileges,
                               is_direct_privileges)
    except AssertionError:
        time.sleep(2)
        tree.assert_privileges(selenium, browser_id, privileges,
                               is_direct_privileges)
    driver = selenium[browser_id]
    page = _find_members_page(onepanel, oz_page, driver, where)
    page.close_member(driver)


@wt(parsers.re('user of (?P<browser_id>.*) sees following privileges on modal:'
               '\n(?P<config>(.|\s)*)'))
def assert_privileges_in_members_subpage_on_modal(selenium, browser_id, config,
                                                  modals):
    driver = selenium[browser_id]
    privileges = yaml.load(config)
    tree = modals(driver).change_privileges.privilege_tree
    tree.assert_privileges(selenium, browser_id, privileges)


@wt(parsers.re('user of (?P<browser_id>.*) clicks (?P<option>Save|Discard) '
               'button for "(?P<member_name>.*)" (?P<member_type>user|group) '
               'in (?P<where>space|group|cluster|harvester) members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_on_element_header_in_members(selenium, browser_id, option,
                                              oz_page, where, onepanel):
    driver = selenium[browser_id]
    option_selector = f'.{option.lower()}-btn'

    page = _find_members_page(onepanel, oz_page, driver, where)
    page.close_member(driver)
    time.sleep(1)
    driver.find_element_by_css_selector(
        '.list-header-row ' + option_selector).click()


@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_on_element_header_in_members_and_wait(
        selenium, browser_id, option, oz_page, where, onepanel, tree):
    driver = selenium[browser_id]
    option_selector = f'.{option.lower()}-btn'
    page = _find_members_page(onepanel, oz_page, driver, where)

    driver.execute_script("window.scrollBy(0,0)")
    driver.find_element_by_css_selector(
        '.list-header-row ' + option_selector).click()
    tree.wait_for_load_privileges()
    page.close_member(driver)


@wt(parsers.re('user of (?P<browser_id>.*) sees (?P<labels>( |.)*) status '
               'labels? for "(?P<member_name>.*)" (?P<member_type>user|group) '
               'in (?P<where>space|group|cluster|harvester) members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def ckeck_status_labels_for_member_of_space(selenium, browser_id, oz_page,
                                            labels,
                                            member_name, onepanel, member_type,
                                            where):
    driver = selenium[browser_id]

    member_type = member_type + 's'
    page = _find_members_page(onepanel, oz_page, driver, where)
    member = getattr(page, member_type).items[member_name]
    status_labels = [x.text for x in member.status_labels]
    labels = parse_seq(labels)

    assert len(status_labels) == len(labels), (f'Invalid status labels for '
                                               f'{member_name}')
    for x in labels:
        assert x in status_labels, f'"{x}" label not found for {member_name}'


@wt(parsers.re('user of (?P<browser_id>.*) sees '
               '(?P<alert_text>Insufficient privileges) alert '
               'for "(?P<member_name>.*)" (?P<member_type>user|group) '
               'in (?P<where>space|group|cluster) members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def see_insufficient_permissions_alert_for_member(selenium, browser_id, oz_page,
                                                  where, member_name, onepanel,
                                                  member_type, alert_text):
    driver = selenium[browser_id]
    member_type = member_type + 's'
    page = _find_members_page(onepanel, oz_page, driver, where)

    members_list = getattr(page, member_type)
    forbidden_alert = members_list.items[member_name].forbidden_alert.text
    assert alert_text in forbidden_alert, (
        'alert with text "{}" not found'.format(alert_text))


@wt(parsers.re('user of (?P<browser_id>.*) sees '
               '"(?P<alert_text>Insufficient privileges)" alert '
               'in (?P<where>space|group|cluster|harvester) members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_insufficient_permission_alert_in_members_subpage(
        selenium, browser_id, oz_page, where, alert_text, onepanel):
    driver = selenium[browser_id]
    page = _find_members_page(onepanel, oz_page, driver, where)
    assert_element_text(page, 'forbidden_alert', alert_text)


@wt(parsers.re('user of (?P<browser_id>.*) sees privileges for '
               '"(?P<member_name>.*)" (?P<member_type>user|group) '
               'in (?P<where>space|group|cluster|harvester|automation) '
               'members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def see_privileges_for_member(selenium, browser_id, oz_page, where, member_type,
                              member_name, onepanel):
    driver = selenium[browser_id]
    member_type = member_type + 's'
    page = _find_members_page(onepanel, oz_page, driver, where)
    members_list = getattr(page, member_type)
    member_item_row = members_list.items[member_name]

    assert member_item_row.are_privileges_visible(), 'not found privileges'


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>does not see|sees) '
               '"(?P<member_name>.*)" (?P<member_type>user|group) '
               'in "(?P<name>.*)" harvester members '
               '(?P<list_type>users|groups) list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_element_in_members_subpage(selenium, browser_id, option, oz_page,
                                     member_name, member_type, list_type):
    driver = selenium[browser_id]
    member_list = getattr(oz_page(driver)['discovery'].members_page,
                          list_type).items
    if option == 'sees':
        try:
            err_msg = f'{member_name} {member_type} not found'
            assert member_name in member_list, err_msg
        except RuntimeError:
            raise AssertionError(err_msg)
    else:
        try:
            assert member_name not in member_list, f'{member_name} {member_type}'
        except RuntimeError:
            return True


@wt(parsers.re('user of (?P<browser_id>.*) sees (?P<number>\d+) '
               '(?P<member_type>user|group)s? in '
               '(?P<where>space|group|cluster|harvester) members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_list_length_on_members_subpage(selenium, browser_id, oz_page,
                                         onepanel, member_type, where,
                                         number: int):
    driver = selenium[browser_id]
    member_type = member_type + 's'
    page = _find_members_page(onepanel, oz_page, driver, where)
    members_list = getattr(page, member_type)
    error_msg = f'Wrong number of {member_type} in {where} members subpage'
    assert len(members_list.items) == number, error_msg


@wt(parsers.parse('user of {browser_id} sees that {where} {item_name} has '
                  'following privilege configuration for {target} {name}:'
                  '\n{config}'))
def assert_privilege_config_for_user(selenium, browser_id, item_name, where,
                                     name, config, oz_page, onepanel, target,
                                     hosts):
    list_type = target + 's'
    option = where + 's' if where != 'inventory' else 'automation'
    option2 = 'Members'

    data = yaml.load(config)
    privileges = data['privileges']

    if where != 'cluster':
        click_element_on_lists_on_left_sidebar_menu(selenium, browser_id,
                                                    option, item_name, oz_page)
    if where == 'space':
        click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                      item_name, option2,
                                                      oz_page)
    elif where == 'harvester':
        click_on_option_of_harvester_on_left_sidebar_menu(selenium, browser_id,
                                                          item_name, option2,
                                                          oz_page)
    elif where == 'inventory':
        click_on_option_of_inventory_on_left_sidebar_menu(selenium, browser_id,
                                                          item_name,
                                                          option2,
                                                          oz_page)
    elif where == 'group':
        go_to_group_subpage(selenium, browser_id, item_name, option2.lower(),
                            oz_page)
    elif where == 'cluster':
        click_on_record_in_clusters_menu(selenium, browser_id, oz_page,
                                         item_name, hosts)
        wt_click_on_subitem_for_item(selenium, browser_id, option, option2,
                                     item_name, onepanel, hosts)

    click_element_in_members_list(selenium, browser_id, name, oz_page, where,
                                  list_type, onepanel)
    privilege_tree = get_privilege_tree(selenium, browser_id, onepanel, oz_page,
                                        where, list_type, name)
    privilege_tree.assert_privileges(selenium, browser_id, privileges)


@wt(parsers.re('user of (?P<browser_id>.*) clicks on '
               '(?P<member_type>users|groups) checkbox'))
def click_on_bulk_checkbox(browser_id, member_type, selenium, oz_page):
    driver = selenium[browser_id]
    page = oz_page(driver)['groups'].members_page
    members_list = getattr(page, member_type)
    members_list.header.checkbox.click()


@wt(parsers.re('user of (?P<browser_id>.*) clicks on "(?P<member_name>.*)" '
               '(?P<member_type>users|groups) checkbox'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_member_checkbox(selenium, browser_id, member_name, oz_page,
                          member_type):
    driver = selenium[browser_id]
    page = oz_page(driver)['groups'].members_page

    getattr(page, member_type).items[member_name].header.checkbox.click()


@wt(parsers.parse('user of {browser_id} clicks on bulk edit button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_bulk_edit(browser_id, selenium, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['groups'].members_page.bulk_edit_button.click()


@wt(parsers.re('user of (?P<browser_id>.*) sees "(?P<alert_text>As a '
               'space owner, you are authorized to perform all operations, '
               'regardless of the assigned privileges.)" warning '
               'for "(?P<username>.*)" user in space members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_ownership_privileges_warning_appeared_for_user(selenium, browser_id,
                                                          oz_page,
                                                          username,
                                                          alert_text):
    driver = selenium[browser_id]
    members_list = oz_page(driver)['data'].members_page.users
    error_msg = f'alert with text "{alert_text}" not found'
    ownership_warning = members_list.items[username].ownership_warning.text
    assert alert_text in ownership_warning, error_msg
