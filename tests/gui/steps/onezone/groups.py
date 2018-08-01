"""This module contains gherkin steps to run acceptance tests featuring groups
management in onezone web GUI
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from pytest_bdd import parsers, when, then, given
from tests.utils.acceptance_utils import wt
from tests.gui.steps.common import *
from tests.gui.utils.common.modals import Modals as modals
from tests.gui.utils.generic import repeat_failed, parse_seq
from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND


@wt(parsers.re('user of (?P<browser_id>.*) clicks on the '
               '(?P<operation>create|join) button in '
               '"(?P<panel>.*)" Onezone panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_in_panel(selenium, browser_id, operation, panel, oz_page):
    if operation == 'create':
        oz_page(selenium[browser_id])[panel].create_group.click()
    else:
        oz_page(selenium[browser_id])[panel].join_group.click()


@wt(parsers.parse('user of {browser_id} creates "{group}" group'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_group(selenium, browser_id, group, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.create_group.click()
    page.input_box.value = group
    page.input_box.confirm.click()


@wt(parsers.parse('user of {browser_id} joins group using received token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def join_group(selenium, browser_id, oz_page, tmp_memory):
    page = oz_page(selenium[browser_id])['groups']
    token = tmp_memory[browser_id]['token']
    page.join_group.click()
    page.input_box.value = token
    page.input_box.confirm.click()


@wt(parsers.parse('user of {browser_id} renames group "{group}" '
                  'to "{new_group}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def rename_group(selenium, browser_id, group, new_group, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group].menu.click()
    page.menu['Rename'].click()
    page.elements_list[''].edit_box.value = new_group
    page.elements_list[''].edit_box.confirm()


@wt(parsers.parse('user of {browser_id} leaves "{group}" group'))
@repeat_failed(timeout=WAIT_FRONTEND)
def leave_group(selenium, browser_id, group, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group].menu.click()
    page.menu['Leave'].click()
    modals(selenium[browser_id]).leave_group.leave.click()


@wt(parsers.parse('user of {browser_id} removes "{group}" group'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_group(selenium, browser_id, group, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group].menu.click()
    page.menu['Remove'].click() 
    modals(selenium[browser_id]).remove_group.remove.click() 


@wt(parsers.parse('user of {browser1_id} sends token to user of {browser2_id}'))
def send_token(selenium, browser1_id, browser2_id, tmp_memory): 
    token = tmp_memory[browser1_id]['token']
    tmp_memory[browser2_id]['token'] = token


@wt(parsers.parse('user of {browser_id} writes "{text}" '
                  'into group token text field'))
@wt(parsers.parse('user of {browser_id} writes "{text}" '
                  'into group name text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def input_name_or_token(selenium, browser_id, text, oz_page):
    oz_page(selenium[browser_id])['groups'].input_box.value = text


@wt(parsers.parse('user of {browser_id} clicks on confirmation button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_name_or_token(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['groups'].input_box.confirm.click()


def _find_groups(page, group):
    return filter(lambda g : g.name == group, page.elements_list)


@wt(parsers.re('user of (?P<browser_ids>.*) (?P<option>do|dont) '
               'see group "(?P<group>.*)" on groups list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_group_exists(selenium, browser_ids, option, group, oz_page):
    for browser_id in parse_seq(browser_ids):
        groups_count = len(_find_groups(oz_page(selenium[browser_id])['groups'],
                                        group))
        if option == 'do':
            assert groups_count > 0, "no such group exists"
        else:
            assert groups_count == 0, "such group exists"            


@wt(parsers.re('user of (?P<browser_id>.*) clicks on '
               '"(?P<option>Rename|Join space|Leave|Remove)" button in '
               '"(?P<group>.*)" group menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_menu(selenium, browser_id, option, group, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group].menu.click()
    page.menu[option].click()


@wt(parsers.parse('user of {browser_id} writes '
                  '"{text}" into rename group text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def input_new_name(selenium, browser_id, text, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[''].edit_box.value = text
    

@wt(parsers.parse('user of {browser_id} confirms group rename'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_rename(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['groups'].elements_list[''].edit_box.confirm()


@wt(parsers.parse('user of browser see that create group button is inactive'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_create_button_inactive(selenium, browser_id, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    assert not page.input_box.confirm.is_enabled()


@wt(parsers.parse('user of {browser_id} clicks on "{button}" button in '
                  '"{modal}" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_modal_button(selenium, browser_id, button, modal, oz_page):
    button = button.lower()
    modal = modal.lower().replace(' ', '_')
    getattr(getattr(modals(selenium[browser_id]), modal), button).click()


@wt(parsers.parse('user of {browser_id} see that error modal with '
                  '"{text}" text appeared'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_modal_appeared(selenium, browser_id, text, oz_page):
    try:
        assert text in modals(selenium[browser_id]).error.content
    except RuntimeError:
        assert False


@wt(parsers.parse('user of {browser_id} clicks on '
                  '"generate an invitation token" text in '
                  '"{group}" members groups list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_generate_token(selenium, browser_id, group, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group].members.click()
    page.main_page.members.groups.generate_token.click()


@wt(parsers.parse('user of {browser_id} copies generated token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_token(selenium, browser_id, oz_page, tmp_memory):
    token = (oz_page(selenium[browser_id])['groups']
             .main_page.members.token.token)
    tmp_memory[browser_id]['token'] = token


@wt(parsers.re('user of (?P<browser_id>.*) goes to "(?P<group>.*)" '
               '(?P<subpage>members|parents) subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def go_to_page(selenium, browser_id, group, subpage, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group].click()
    getattr(page.elements_list[group], subpage).click()


@wt(parsers.parse('user of {browser_id} pastes copied token into group '
                  'token text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def paste_token(selenium, browser_id, oz_page, tmp_memory):
    page = oz_page(selenium[browser_id])['groups']
    page.input_box.value = tmp_memory[browser_id]['token']


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>do|dont) '
               'see "(?P<child>.*)" as "(?P<parent>.*)" child'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_child(selenium, browser_id, option, child, parent, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[parent].click()
    page.elements_list[parent].members.click()
    try:
        page.main_page.members.groups.items[child]
    except RuntimeError:
        assert option == 'dont'
    else:
        assert option == 'do'


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>do|dont) '
               'see "(?P<parent>.*)" as "(?P<child>.*)" parent'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_parent(selenium, browser_id, option, parent, child, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[child].click()
    page.elements_list[child].parents.click()
    try:
        page.main_page.parents.items[parent]
    except RuntimeError:
        assert option == 'dont'
    else:
        assert option == 'do'


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>do|dont) '
               'see user "(?P<username>.*)" on group "(?P<group_name>.*)" '
               'members list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_member(selenium, browser_id, option, username, group_name, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group_name].click()
    page.elements_list[group_name].members.click()
    try:
        page.main_page.members.users.items[username]
    except RuntimeError:
        assert option == 'dont'
    else:
        assert option == 'do'


@wt(parsers.re('user of (?P<browser_id>.*) removes "(?P<name>.*)" '
               '(?P<member_type>user|group) from group '
               '"(?P<group>.*)" members'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_member(selenium, browser_id, name, member_type, group, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group].click()
    page.elements_list[group].members.click()
    if member_type == 'user':
        page.main_page.members.users.items[name].header.menu_button.click()
    else:
        page.main_page.members.groups.items[name].header.menu_button.click()
    page.menu['Remove this member'].click()
    if member_type == 'user':
        modals(selenium[browser_id]).remove_user.remove.click()
    else:
        modals(selenium[browser_id]).remove_group.remove.click()


@wt(parsers.parse('user of {browser_Iid} removes group "{parent}" from '
                  'group "{child}" parents list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def leave_parent_group(selenium, browser_id, parent, child, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[child].click()
    page.elements_list[child].parents.click()
    page.main_page.parents.items[parent].menu.click()
    page.menu['Leave parent group'].click()
    modals(selenium[browser_id]).leave_parent.leave.click()
    

@wt(parsers.parse('user of {browser_id} adds "{group}" group as subgroup '
                  'using received token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_group_as_subgroup(selenium, browser_id, group, oz_page, tmp_memory): 
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group].click()
    page.elements_list[group].parents.click()
    page.main_page.parents.header.menu.click()
    page.menu['Join as subgroup'].click()
    token = tmp_memory[browser_id]['token']
    page.input_box.value = token
    page.input_box.confirm.click()


@wt(parsers.re('user of (?P<browser_id>.*) gets "(?P<group>.*)" '
               '(?P<who>user|group) invitation token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def get_invitation_token(selenium, browser_id, group, who, oz_page, tmp_memory):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group].click()
    page.main_page.menu_button.click()
    page.menu['Invite ' + who].click()
    token = page.main_page.members.token.token
    tmp_memory[browser_id]['token'] = token




