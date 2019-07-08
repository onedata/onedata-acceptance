"""This module contains gherkin steps to run acceptance tests featuring members
management in onezone web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import parsers

import time

from tests.gui.steps.modal import wt_wait_for_modal_to_appear
from tests.utils.utils import repeat_failed
from tests.utils.acceptance_utils import wt
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.common.modals import Modals as modals
from tests.gui.meta_steps.onezone.common import search_for_members


def _change_to_tab_name(element):
    main_menu_element = 'data' if element == 'space' else element + 's'
    return main_menu_element


def _find_members_page(onepanel, oz_page, driver, where):
    tab_name = _change_to_tab_name(where)
    if tab_name == 'clusters':
        return onepanel(driver).content.members
    else:
        return oz_page(driver)[tab_name].members_page


@wt(parsers.re('user of (?P<browser_id>.*) clicks show view expand button in '
               '(?P<where>space|group|cluster) members subpage header'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_show_view_option(selenium, browser_id, oz_page, where, onepanel):
    driver = selenium[browser_id]
    page = _find_members_page(onepanel, oz_page, driver, where)
    page.show_view_option()


@wt(parsers.re('user of (?P<browser_id>.*) clicks '
               '(?P<mode>direct|effective|privileges|memberships) view mode '
               'in (?P<where>space|group|cluster) members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_mode_view_in_members_subpage(selenium, browser_id, mode,
                                       oz_page, where, onepanel):
    driver = selenium[browser_id]
    mode = mode + '_button'
    page = _find_members_page(onepanel, oz_page, driver, where)

    getattr(page, mode).click()


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

    if not search_for_members(records, member_name, parent_name, fun):
        raise RuntimeError('not found "{}" {} as a member of "{}" {}'.format(
            member_name, member_type, parent_name, parent_type))


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
                'found "{}" {} as a member of "{}" {}'.format(
                    member_name, member_type, parent_name, parent_type))
        elif member_index == 0:
            raise RuntimeError(
                'found "{}" {} as a member of "{}" {}'.format(
                    member_name, member_type, parent_name, parent_type))
        return False

    search_for_members(records, member_name, parent_name, fun)


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


@wt(parsers.re('user of (?P<browser_id>.*) clicks on "(?P<member_name>.*)" '
               'member relation menu button to '
               '"(?P<name>.*)" (?P<where>space|group)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_relation_menu_button(selenium, browser_id, member_name,
                               name, oz_page, where):
    driver = selenium[browser_id]
    where = _change_to_tab_name(where)
    records = oz_page(driver)[where].members_page.memberships

    def click_on_menu(record, member_index):
        record.relations[member_index].click_relation_menu_button(driver)
        return True

    search_for_members(records, member_name, name, click_on_menu)


@wt(parsers.re('user of (?P<browser_id>.*) clicks on "(?P<option>.*)" '
               'in (?P<where>space|group) membership relation menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_relation_menu_button(selenium, browser_id, option):
    driver = selenium[browser_id]
    modals(driver).membership_relation_menu.options[option].click()


@wt(parsers.re('user of (?P<browser_id>.*) clicks "(?P<member_name>.*)" '
               '(?P<member_type>user|group) in "(?P<name>.*)" '
               '(?P<where>space|group|cluster) members '
               '(?P<list_type>users|groups) list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_element_in_members_list(selenium, browser_id, member_name,
                                  oz_page, where, list_type, onepanel):
    driver = selenium[browser_id]
    page = _find_members_page(onepanel, oz_page, driver, where)

    getattr(page, list_type).items[member_name].click()


@wt(parsers.parse('user of {browser_id} clicks on '
                  '"generate an invitation token" text in group '
                  '"{group}" members {member} list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_generate_token_in_subgroups_list(selenium, browser_id, group,
                                           oz_page, member):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group]()
    page.elements_list[group].members()
    getattr(page.main_page.members, member).generate_token()


@wt(parsers.re('user of (?P<browser_id>.*) clicks on "(?P<button>.*)" button '
               'in (?P<member>users|groups) list menu in '
               '"(?P<name>.*)" (?P<where>group|space|cluster) members view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_in_members_list_menu(selenium, browser_id, button,
                                         where, member, oz_page,
                                         onepanel, popups):
    driver = selenium[browser_id]

    page = _find_members_page(onepanel, oz_page, driver, where)
    getattr(page, member).header.menu_button()

    popups(driver).member_menu.menu[button]()


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
def assert_element_is_groups_child(selenium, browser_id, option, child,
                                   parent, oz_page):
    page = oz_page(selenium[browser_id])['groups']
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
               'on "(?P<parent_name>.*)" (?P<parent_type>user|group|space|cluster) '
               'members list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_member_is_in_parent_members_list(selenium, browser_id, option,
                                            member_name, member_type,
                                            parent_name, parent_type,
                                            oz_page, onepanel):
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
        assert option == 'sees', ('{} "{}" found on {} "{}" members list'
                                  .format(member_type, member_name,
                                          parent_type, parent_name))


@wt(parsers.re('user of (?P<browser_id>.*) removes "(?P<member_name>.*)" '
               '(?P<member_type>user|group) from "(?P<name>.*)" '
               '(?P<where>cluster|group) members'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_member_from_parent(selenium, browser_id, member_name, member_type,
                              name, oz_page, tmp_memory, onepanel, where, popups):
    driver = selenium[browser_id]
    page = _find_members_page(onepanel, oz_page, driver, where)
    tab_name = _change_to_tab_name(where)
    list_name = member_type + 's'
    (getattr(page, list_name)
     .items[member_name].header.click_menu(selenium[browser_id]))

    if member_type == 'user':
        modal_name = 'remove user from '
    elif member_type == 'group' and tab_name == 'clusters':
        modal_name = 'remove group from '
    else:
        modal_name = 'remove subgroup from '
    modal_name += where

    popups(driver).member_menu.menu['Remove this member']()

    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    modals(driver).remove_member.remove()


@wt(parsers.re('user of (?P<browser_id>.*) copies "(?P<group>.*)" '
               '(?P<who>user|group) invitation token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_invitation_token(selenium, browser_id, group, who, oz_page,
                          tmp_memory, popups):
    driver = selenium[browser_id]
    page = oz_page(driver)['groups']
    page.elements_list[group]()

    getattr(page.main_page.members, who + 's').header.menu_button()
    button = 'Invite {} using token'.format(who)

    popups(driver).member_menu.menu[button].click()

    wt_wait_for_modal_to_appear(selenium, browser_id, button, tmp_memory)
    modals(selenium[browser_id]).invite_using_token.copy()
    modals(selenium[browser_id]).invite_using_token.close()


@wt(parsers.re('user of (?P<browser_id>.*) gets group "(?P<group>.*)" '
               '(?P<who>user|group) invitation token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def get_invitation_token(selenium, browser_id, group, who, oz_page,
                         tmp_memory, popups):
    driver = selenium[browser_id]
    page = oz_page(driver)['groups']
    page.elements_list[group]()
    page.main_page.menu_button()
    popups(driver).member_menu.menu['Invite ' + who]()
    token = page.members_page.token.token
    tmp_memory[browser_id]['token'] = token


@wt(parsers.re('user of (?P<browser_id>.*) clicks Invite (?P<who>user|group) '
               'on Menu of Members of (?P<where>Spaces|Groups)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_invite_on_menu_of_members(selenium, browser_id, who, where,
                                    oz_page, popups):
    driver = selenium[browser_id]
    where = _change_to_tab_name(where)
    elem = oz_page(driver)[where]
    elem.menu_button()
    popups(driver).member_menu.menu['Invite ' + who]()


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>checks|unchecks) '
               '"(?P<privilege_name>.*)" privilege toggle for '
               '"(?P<member_name>.*)" (?P<member_type>user|group) '
               'in (?P<where>space|group) members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_privilege_toggle_for_member(selenium, browser_id, option, where,
                                      privilege_name, member_name, oz_page,
                                      member_type):
    driver = selenium[browser_id]
    where = _change_to_tab_name(where)
    member_type = member_type + 's'
    members_list = getattr(oz_page(driver)[where].members_page, member_type)
    privilege = (members_list.items[member_name]
                 .privileges[privilege_name].toggle)
    if option == 'checks':
        privilege.check()
    else:
        privilege.uncheck()


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>checks|unchecks) '
               '"(?P<privilege_name>.*)" privilege toggle in '
               '"(?P<parent_privilege_name>.*)" for "(?P<member_name>.*)" '
               '(?P<member_type>user|group) in (?P<where>space|group|cluster) '
               'members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_nested_privilege_toggle_for_member(selenium, browser_id, option,
                                             where, privilege_name, member_name,
                                             oz_page, member_type,
                                             parent_privilege_name, onepanel):
    driver = selenium[browser_id]
    member_type = member_type + 's'
    page = _find_members_page(onepanel, oz_page, driver, where)
    members_list = getattr(page, member_type)
    privilege = (members_list.items[member_name]
                 .privileges[parent_privilege_name]
                 .privileges[privilege_name].toggle)
    time.sleep(1)
    if option == 'checks':
        privilege.check()
    else:
        privilege.uncheck()


@wt(parsers.re('user of (?P<browser_id>.*) sees that "(?P<privilege>.*)" '
               '(?P<option>is|is not) checked for "(?P<member_name>.*)" '
               '(?P<member_type>user|group) in (?P<where>space|group) '
               'members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_privilege_toggle_is_checked_for_member(selenium, browser_id, option,
                                                  oz_page, where, member_name,
                                                  privilege, member_type):
    driver = selenium[browser_id]
    where = _change_to_tab_name(where)
    member_type = member_type + 's'
    members_list = getattr(oz_page(driver)[where].members_page, member_type)
    is_checked = (members_list.items[member_name].privileges[privilege]
                  .toggle.is_checked())
    if option == 'is':
        assert is_checked, 'found that toggle is unchecked'
    else:
        assert not is_checked, 'found that toggle is checked'


@wt(parsers.re('user of (?P<browser_id>.*) clicks (?P<option>Save|Cancel) '
               'button for "(?P<member_name>.*)" (?P<member_type>user|group) '
               'in (?P<where>space|group|cluster) members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_on_element_header_in_members(selenium, browser_id, option,
                                              oz_page, where, member_name,
                                              member_type, onepanel):
    driver = selenium[browser_id]
    option = option.lower() + '_button'
    member_type = member_type + 's'
    page = _find_members_page(onepanel, oz_page, driver, where)

    members_list = getattr(page, member_type)
    header = members_list.items[member_name].header
    getattr(header, option).click()


@wt(parsers.re('user of (?P<browser_id>.*) expands "(?P<privilege_name>.*)" '
               'privilege for "(?P<member_name>.*)" (?P<member_type>user|group) '
               'in (?P<where>space|group|cluster) members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def expand_privilege_for_member(selenium, browser_id, privilege_name, oz_page,
                                where, member_name, member_type, onepanel):
    driver = selenium[browser_id]
    member_type = member_type + 's'
    page = _find_members_page(onepanel, oz_page, driver, where)

    members_list = getattr(page, member_type)
    members_list.items[member_name].privileges[privilege_name].show_hide_button()


@wt(parsers.re('user of (?P<browser_id>.*) sees '
               '(?P<alert_text>Insufficient permissions) alert '
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
    assert alert_text in forbidden_alert, ('not found alert with {} text'
                                           .format(alert_text))


@wt(parsers.re('user of (?P<browser_id>.*) sees '
               '(?P<alert_text>Insufficient permissions) alert '
               'in (?P<where>space|group|cluster) members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def see_insufficient_permissions_alert(selenium, browser_id, oz_page,
                                       where, alert_text, onepanel):
    driver = selenium[browser_id]
    page = _find_members_page(onepanel, oz_page, driver, where)

    forbidden_alert = page.forbidden_alert.text
    assert alert_text in forbidden_alert, ('not found alert with {} text'
                                           .format(alert_text))


@wt(parsers.re('user of (?P<browser_id>.*) sees privileges for '
               '"(?P<member_name>.*)" (?P<member_type>user|group) '
               'in (?P<where>space|group|cluster) members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def see_privileges_for_member(selenium, browser_id, oz_page, where,
                              member_type, member_name, onepanel):
    driver = selenium[browser_id]
    member_type = member_type + 's'
    page = _find_members_page(onepanel, oz_page, driver, where)
    members_list = getattr(page, member_type)

    assert len(members_list.items[member_name].privileges) > 0, ('not found '
                                                                 'privileges')
