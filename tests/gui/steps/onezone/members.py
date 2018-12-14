"""This module contains gherkin steps to run acceptance tests featuring members
management in onezone web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import parsers

from tests.gui.steps.modal import wt_wait_for_modal_to_appear
from tests.utils.utils import repeat_failed
from tests.utils.acceptance_utils import wt
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.common.modals import Modals as modals


@wt(parsers.re('user of (?P<browser_id>.*) clicks show view option in '
               '(?P<where>space|group) members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_show_view_option(selenium, browser_id, oz_page, where):
    driver = selenium[browser_id]
    where = where + 's'

    oz_page(driver)[where].members_page.show_view_option()


@wt(parsers.re('user of (?P<browser_id>.*) clicks '
               '(?P<mode>direct|effective|privileges|memberships) view mode '
               'in (?P<where>space|group) members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_mode_view_in_members_subpage(selenium, browser_id, mode,
                                       oz_page, where):
    driver = selenium[browser_id]
    mode = mode + '_button'
    where = where + 's'

    getattr(oz_page(driver)[where].members_page, mode).click()


@wt(parsers.re('user of (?P<browser_id>.*) sees (?P<member_type>user|group) '
               '"(?P<member_name>.*)" is member of '
               '(?P<parent_type>space|group) "(?P<parent_name>.*)" '
               'in (?P<where>space|group) memberships mode'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_member_is_member_of_parent_in_memberships(selenium, browser_id,
                                                     member_name, parent_name,
                                                     member_type, oz_page,
                                                     where):
    driver = selenium[browser_id]
    where = where + 's'
    records = oz_page(driver)[where].members_page.memberships

    for record in records:
        if member_name in record.elements and parent_name in record.elements:
            member_index = record.elements.index(member_name)
            group_index = record.elements.index(parent_name)
            if member_index + 1 == group_index:
                if member_type != 'user':
                    return
                elif member_index == 0:
                    return

    assert False


@wt(parsers.re('user of (?P<browser_id>.*) does not see '
               '(?P<member_type>user|group) "(?P<member_name>.*)" is '
               'member of (?P<parent_type>space|group) "(?P<parent_name>.*)" '
               'in (?P<where>space|group) memberships mode'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_member_is_not_member_of_group_in_memberships(selenium, browser_id,
                                                        member_name, where,
                                                        parent_name, oz_page,
                                                        member_type):
    driver = selenium[browser_id]
    where = where + 's'
    records = oz_page(driver)[where].members_page.memberships

    for record in records:
        if member_name in record.elements and parent_name in record.elements:
            member_index = record.elements.index(member_name)
            group_index = record.elements.index(parent_name)
            if member_index + 1 == group_index:
                if member_type != 'user':
                    assert False
                elif member_index == 0:
                    assert False


@wt(parsers.re('user of (?P<browser_id>.*) sees (?P<number>.*) '
               'membership rows in (?P<where>space|group) memberships mode'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_count_membership_rows(selenium, browser_id, number, oz_page, where):
    driver = selenium[browser_id]
    where = where + 's'
    records = oz_page(driver)[where].members_page.memberships

    assert len(records) == int(number)


@wt(parsers.re('user of (?P<browser_id>.*) clicks on member '
               '"(?P<member_name>.*)" relation menu button to '
               '(?P<where>space|group) "(?P<name>.*)"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_relation_menu_button(selenium, browser_id, member_name,
                               name, oz_page, where):
    driver = selenium[browser_id]
    where = where + 's'
    records = oz_page(driver)[where].members_page.memberships
    for record in records:
        if member_name in record.elements and name in record.elements:
            member_index = record.elements.index(member_name)
            group_index = record.elements.index(name)
            if member_index + 1 == group_index:
                record.relations[member_index].click_relation_menu_button(driver)
                break


@wt(parsers.re('user of (?P<browser_id>.*) clicks on "(?P<option>.*)" '
               'in (?P<where>space|group) membership relation menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_relation_menu_button(selenium, browser_id, option):
    driver = selenium[browser_id]
    modals(driver).membership_relation_menu.options[option].click()


@wt(parsers.re('user of (?P<browser_id>.*) clicks (?P<member_type>user|group) '
               '"(?P<member_name>.*)" in (?P<where>space|group) "(?P<name>.*)" '
               'members (?P<list_type>users|groups) list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_user_in_members_users_list(selenium, browser_id, member_name,
                                     oz_page, where, list_type):
    driver = selenium[browser_id]
    where = where + 's'
    (getattr(oz_page(driver)[where].members_page, list_type)
     .items[member_name].click())


@wt(parsers.parse('user of {browser_id} clicks on text '
                  '"generate an invitation token" in group '
                  '"{group}" members groups list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_generate_token_in_subgroups_list(selenium, browser_id, group,
                                           oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group]()
    page.elements_list[group].members()
    page.main_page.members.groups.generate_token()


@wt(parsers.re('user of (?P<browser_id>.*) clicks on button '
               '"(?P<button>Invite group|Invite user)" in group '
               '"(?P<group_name>.*)" members menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def generate_group_or_user_invitation_token(selenium, browser_id, button,
                                            group_name, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group_name]()
    page.elements_list[group_name]()
    page.main_page.menu_button()
    page.menu[button]()


@wt(parsers.parse('user of {browser_id} sees that area with '
                  'invitation token has appeared'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_token_area_appeared(selenium, browser_id, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    try:
        page.members_page.token
    except RuntimeError:
        assert False, 'Token area has not appeared'


@wt(parsers.parse('user of {browser_id} sees non-empty token in token area'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_generated_token_is_present(selenium, browser_id, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    try:
        text = page.members_page.token.token
        assert len(text) > 0, 'Token is empty, while it should be non-empty'
    except RuntimeError:
        assert False, 'No token area found on page'


@wt(parsers.re('user of (?P<browser_id>.*) copies invitation token '
               'from Groups page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_token(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['groups'].members_page.token.copy()


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>does not see|sees) '
               '"(?P<child>.*)" as "(?P<parent>.*)" child'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_group_is_groups_child(selenium, browser_id, option, child,
                                 parent, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[parent]()
    page.elements_list[parent].members()

    try:
        page.members_page.groups.items[child]
    except RuntimeError:
        assert (option == 'does not see',
                '"{}" is "{}" child'.format(child, parent))
    else:
        assert (option == 'sees',
                '"{}" is not "{}" child'.format(child, parent))


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>does not see|sees) '
               '"(?P<parent>.*)" as "(?P<child>.*)" parent'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_group_is_groups_parent(selenium, browser_id, option,
                                  parent, child, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[child]()
    page.elements_list[child].parents()
    try:
        page.main_page.parents.items[parent]
    except RuntimeError:
        assert (option == 'does not see',
                '"{}" is "{}" parent'.format(parent, child))
    else:
        assert (option == 'sees',
                '"{}" is not "{}" parent'.format(parent, child))


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>does not see|sees) user '
               '"(?P<username>.*)" on group "(?P<group_name>.*)" members list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_member(selenium, browser_id, option, username, group_name, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group_name]()
    page.elements_list[group_name].members()
    try:
        page.members_page.users.items[username]
    except RuntimeError:
        assert (option == 'does not see',
                'user "{}" found on group "{}" members list'.format(username,
                                                                    group_name))
    else:
        assert (option == 'sees',
                'user "{}" not found on group "{}" members list'
                .format(username, group_name))


@wt(parsers.re('user of (?P<browser_id>.*) removes (?P<member_type>user|group) '
               '"(?P<name>.*)" from group "(?P<group>.*)" members'))
def remove_member_from_group(selenium, browser_id, name, member_type, group,
                             oz_page, tmp_memory):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group]()
    page.elements_list[group].members()
    list_name = member_type + 's'
    (getattr(page.members_page, list_name)
     .items[name].header.menu_button())
    page.menu['Remove this member']()

    modal_name = "Remove member"
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    modals(selenium[browser_id]).remove_member.remove()


@wt(parsers.re('user of (?P<browser_id>.*) copies group "(?P<group>.*)" '
               '(?P<who>user|group) invitation token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_invitation_token(selenium, browser_id, group, who, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group]()
    page.main_page.menu_button()
    page.menu['Invite ' + who]()
    page.members_page.token.copy()


@wt(parsers.re('user of (?P<browser_id>.*) gets group "(?P<group>.*)" '
               '(?P<who>user|group) invitation token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def get_invitation_token(selenium, browser_id, group, who, oz_page, tmp_memory):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group]()
    page.main_page.menu_button()
    page.menu['Invite ' + who]()
    token = page.members_page.token.token
    tmp_memory[browser_id]['token'] = token


@wt(parsers.re('user of (?P<browser_id>.*) clicks Invite (?P<who>user|group) '
               'on Menu of Members of (?P<where>Spaces|Groups)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_invite_group_on_menu_of_members(selenium, browser_id, who, where,
                                          oz_page):
    driver = selenium[browser_id]
    elem = oz_page(driver)[where.lower()]
    elem.menu_button()
    elem.menu['Invite ' + who].click()


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>checks|unchecks) '
               '"(?P<privilege_name>.*)" privilege toggle for '
               '"(?P<member_name>.*)" (?P<member_type>user|group) '
               'in (?P<where>space|group) members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_privilege_toggle_for_group(selenium, browser_id, option, where,
                                     privilege_name, member_name, oz_page,
                                     member_type):
    driver = selenium[browser_id]
    where = where + 's'
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
               '(?P<member_type>user|group) in (?P<where>space|group) '
               'members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_privilege_toggle_for_group(selenium, browser_id, option, where,
                                     privilege_name, member_name, oz_page,
                                     member_type, parent_privilege_name):
    driver = selenium[browser_id]
    where = where + 's'
    member_type = member_type + 's'
    members_list = getattr(oz_page(driver)[where].members_page, member_type)
    privilege = (members_list.items[member_name]
                 .privileges[parent_privilege_name]
                 .privileges[privilege_name].toggle)
    if option == 'checks':
        privilege.check()
    else:
        privilege.uncheck()


@wt(parsers.re('user of (?P<browser_id>.*) sees that "(?P<option>.*)" '
               '(?P<is_positive>is|is not) checked for "(?P<member_name>.*)" '
               '(?P<member_type>user|group) in (?P<where>space|group) '
               'members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_privilege_toggle_is_checked_for_group(selenium, browser_id, option,
                                                 oz_page, where, member_name,
                                                 is_positive, member_type):
    driver = selenium[browser_id]
    where = where + 's'
    member_type = member_type + 's'
    members_list = getattr(oz_page(driver)[where].members_page, member_type)
    is_checked = (members_list.items[member_name].privileges[option]
                  .toggle.is_checked())
    if is_positive == 'is':
        assert is_checked
    else:
        assert not is_checked


@wt(parsers.re('user of (?P<browser_id>.*) clicks (?P<option>Save|Cancel) '
               'button for "(?P<member_name>.*)" (?P<member_type>user|group) '
               'in (?P<where>space|group) members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_on_group_header_in_members(selenium, browser_id, option,
                                            oz_page, where, member_name,
                                            member_type):
    driver = selenium[browser_id]
    option = option.lower() + '_button'
    where = where + 's'
    member_type = member_type + 's'

    members_list = getattr(oz_page(driver)[where].members_page, member_type)
    header = members_list.items[member_name].header
    getattr(header, option).click()


@wt(parsers.re('user of (?P<browser_id>.*) expands "(?P<privilege_name>.*)" '
               'privilege for "(?P<member_name>.*)" (?P<member_type>user|group) '
               'in (?P<where>space|group) members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def expand_privilege_for_member(selenium, browser_id, privilege_name, oz_page,
                                where, member_name, member_type):
    driver = selenium[browser_id]
    where = where + 's'
    member_type = member_type + 's'

    members_list = getattr(oz_page(driver)[where].members_page, member_type)
    members_list.items[member_name].privileges[privilege_name].show_hide_button()


@wt(parsers.re('user of (?P<browser_id>.*) sees '
               '(?P<alert_text>Insufficient permissions) alert '
               'for "(?P<member_name>.*)" (?P<member_type>user|group) '
               'in (?P<where>space|group) members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def see_insufficient_permissions_alert(selenium, browser_id, oz_page,
                                       where, member_name, member_type,
                                       alert_text):
    driver = selenium[browser_id]
    where = where + 's'
    member_type = member_type + 's'

    members_list = getattr(oz_page(driver)[where].members_page, member_type)
    assert alert_text in members_list.items[member_name].alert.text