"""This module contains gherkin steps to run acceptance tests featuring groups
management in onezone web GUI
"""

__author__ = "Michal Stanisz, Lukasz Niemiec"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from pytest_bdd import parsers, when, then, given
from tests.utils.acceptance_utils import wt
from tests.gui.steps.common import *
from tests.gui.utils.common.modals import Modals as modals
from tests.gui.utils.generic import repeat_failed, parse_seq
from tests.gui.conftest import WAIT_FRONTEND
from selenium.webdriver.common.keys import Keys


@wt(parsers.re('user of (?P<browser_id>.*) clicks on the '
               '(?P<operation>create|join) button in '
               '"(?P<panel>.*)" Onezone panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_or_join_group_button_in_panel(selenium, browser_id, operation, 
                                               panel, oz_page):
    button_name = operation + '_group'
    getattr(oz_page(selenium[browser_id])[panel], button_name)()


@wt(parsers.parse('user of {browser_id} creates group "{group}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_group(selenium, browser_id, group, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.create_group()
    page.input_box.value = group
    page.input_box.confirm()


@wt(parsers.re('user of (?P<browser_id>.*) joins group using received token '
                  'and (?P<confirm_type>button|enter) to confirm'))
@repeat_failed(timeout=WAIT_FRONTEND)
def join_group(selenium, browser_id, confirm_type, oz_page, tmp_memory):
    page = oz_page(selenium[browser_id])['groups']
    token = tmp_memory[browser_id]['mailbox']['token']
    page.join_group()
    page.input_box.value = token
    if confirm_type == 'button':
        page.input_box.confirm()
    else:
        selenium[browser_id].switch_to.active_element.send_keys(Keys.RETURN)



@wt(parsers.re('user of (?P<browser_id>.*) renames group "(?P<group>.*)" '
                  'to "(?P<new_group>.*)" using '
                  '(?P<confirm_type>button|enter) to confirm'))
@repeat_failed(timeout=WAIT_FRONTEND)
def rename_group(selenium, browser_id, group, new_group, confirm_type, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group]()
    page.elements_list[group].menu()
    page.menu['Rename']()
    page.elements_list[''].edit_box.value = new_group
    if confirm_type == 'button':
        page.elements_list[''].edit_box.confirm()
    else:
        selenium[browser_id].switch_to.active_element.send_keys(Keys.RETURN)


@wt(parsers.parse('user of {browser_id} leaves group "{group}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def leave_group(selenium, browser_id, group, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group]()
    page.elements_list[group].menu()
    page.menu['Leave']()
    modals(selenium[browser_id]).leave_group.leave()


@wt(parsers.parse('user of {browser_id} removes group "{group}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_group(selenium, browser_id, group, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group]()
    page.elements_list[group].menu()
    page.menu['Remove']() 
    modals(selenium[browser_id]).remove_group.remove()


@wt(parsers.parse('user of {browser_id} joins group "{group}" to space'))
@repeat_failed(timeout=WAIT_FRONTEND)
def join_space(selenium, browser_id, group, token, oz_page, tmp_memory):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group]()
    page.elements_list[group].menu()
    page.menu['Join space']()
    token = tmp_memory[browser_id]['mailbox']['token']
    page.input_box.value = token
    page.input_box.edit_box.confirm()


@wt(parsers.parse('user of {browser_id} writes "{text}" '
                  'into group token text field'))
@wt(parsers.parse('user of {browser_id} writes "{text}" '
                  'into group name text field'))
@wt(parsers.parse('user of {browser_id} writes "{text}" '
                  'into space token text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def input_name_or_token_into_input_box_on_main_groups_page(selenium, browser_id, 
                                                           text, oz_page):
    oz_page(selenium[browser_id])['groups'].input_box.value = text


@wt(parsers.parse('user of {browser_id} clicks on confirmation button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_name_or_token_input_on_main_groups_page(selenium, browser_id, 
                                                    oz_page):
    oz_page(selenium[browser_id])['groups'].input_box.confirm()


def _find_groups(page, group_name):
    return filter(lambda g : g.name == group_name, page.elements_list)


@wt(parsers.re('user of (?P<browser_ids>.*) (?P<option>does not see|sees) '
               'group "(?P<group>.*)" on groups list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_group_exists(selenium, browser_ids, option, group, oz_page):
    for browser_id in parse_seq(browser_ids):
        groups_count = len(_find_groups(oz_page(selenium[browser_id])['groups'],
                                        group))
        if option == 'does not see':
            assert groups_count == 0, "such group exists"
        else:
            assert groups_count > 0, "no such group exists"


@wt(parsers.re('user of (?P<browser_id>.*) clicks on button '
               '"(?P<option>Rename|Join space|Leave|Remove)" in group '
               '"(?P<group>.*)" menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_group_menu_button(selenium, browser_id, option, group, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group]()
    page.elements_list[group].menu()
    page.menu[option]()


@wt(parsers.parse('user of {browser_id} writes '
                  '"{text}" into rename group text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def input_new_group_name_into_rename_group_inpux_box(selenium, browser_id, text,
                                                     oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[''].edit_box.value = text
    

@wt(parsers.parse('user of {browser_id} confirms group rename'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_group_rename(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['groups'].elements_list[''].edit_box.confirm()


@wt(parsers.parse('user of browser sees that create group button is inactive'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_create_button_inactive(selenium, browser_id, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    assert not page.input_box.confirm.is_enabled(), ('"Create group" button '
                                                     'is enabled')


@wt(parsers.parse('user of {browser_id} clicks on button "{button}" in '
                  'modal "{modal}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_modal_button(selenium, browser_id, button, modal, oz_page):
    button = button.lower()
    modal = modal.lower().replace(' ', '_')
    getattr(getattr(modals(selenium[browser_id]), modal), button)()


@wt(parsers.parse('user of {browser_id} sees that error modal with '
                  'text "{text}" appeared'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_error_modal_with_text_appeared(selenium, browser_id, text, oz_page):
    message = 'Modal does not contain text "{}\"'.format(text) 
    assert text in modals(selenium[browser_id]).error.content, message


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
        page.main_page.members.token
    except RuntimeError:
        assert False, "Token area has not appeared"


@wt(parsers.parse('user of {browser_id} sees non-empty token in token area'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_generated_token_is_present(selenium, browser_id, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    try:
        text = page.main_page.members.token.token
        assert len(text) > 0
    except RuntimeError:
        assert False, "No token area found on page"


@wt(parsers.parse('user of {browser_id} copies generated token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_token(selenium, browser_id, oz_page, tmp_memory):
    
    oz_page(selenium[browser_id])['groups'].main_page.members.token.copy()


@wt(parsers.re('user of (?P<browser_id>.*) goes to group "(?P<group>.*)" '
               '(?P<subpage>members|parents|main) subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def go_to_group_subpage(selenium, browser_id, group, subpage, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group]()
    if subpage != 'main':
        getattr(page.elements_list[group], subpage)()


@wt(parsers.parse('user of {browser_id} pastes copied token into group '
                  'token text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def input_token_into_token_input_field(selenium, browser_id, oz_page, 
                                       displays, clipboard):
    token = clipboard.paste(display=displays[browser_id])
    page = oz_page(selenium[browser_id])['groups']
    page.input_box.value = token


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>does not see|sees) '
               '"(?P<child>.*)" as "(?P<parent>.*)" child'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_group_is_groups_child(selenium, browser_id, option, child, 
                                           parent, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[parent]()
    page.elements_list[parent].members()
    try:
        page.main_page.members.groups.items[child]
    except RuntimeError:
        assert option == 'does not see', ("\"{}\" is \"{}\" child"
                                          .format(child, parent))
    else:
        assert option == 'sees', ("\"{}\" is not \"{}\" child"
                                  .format(child, parent))


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
        assert option == 'does not see', ("\"{}\" is \"{}\" parent"
                                          .format(parent, child))
    else:
        assert option == 'sees', ("\"{}\" is not \"{}\" parent"
                                          .format(parent, child))


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>does not see|sees) '
               'user "(?P<username>.*)" on group "(?P<group_name>.*)" '
               'members list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_member(selenium, browser_id, option, username, group_name, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group_name]()
    page.elements_list[group_name].members()
    try:
        page.main_page.members.users.items[username]
    except RuntimeError:
        assert option == 'does not see'
    else:
        assert option == 'sees'


@wt(parsers.re('user of (?P<browser_id>.*) removes (?P<member_type>user|group) '
               '"(?P<name>.*)" from group '
               '"(?P<group>.*)" members'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_member_from_group(selenium, browser_id, name, member_type, group, 
                             oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group]()
    page.elements_list[group].members()
    list_name = member_type + 's'
    (getattr(page.main_page.members, list_name)
     .items[name].header.menu_button())
    page.menu['Remove this member']()
    modal_name = 'remove_' + member_type
    getattr(modals(selenium[browser_id]), modal_name).remove()


@wt(parsers.parse('user of {browser_id} removes group "{parent}" from '
                  'group "{child}" parents list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def leave_parent_group(selenium, browser_id, parent, child, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[child]()
    page.elements_list[child].parents()
    page.main_page.parents.items[parent].menu()
    page.menu['Leave parent group']()
    modals(selenium[browser_id]).leave_parent.leave()
    

@wt(parsers.parse('user of {browser_id} adds group "{group}" as subgroup '
                  'using received token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_group_as_subgroup(selenium, browser_id, group, oz_page, tmp_memory): 
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group]()
    page.elements_list[group].parents()
    page.main_page.parents.header.menu()
    page.menu['Join as subgroup']()
    token = tmp_memory[browser_id]['mailbox']['token']
    page.input_box.value = token
    page.input_box.confirm()


@wt(parsers.re('user of (?P<browser_id>.*) copies group "(?P<group>.*)" '
               '(?P<who>user|group) invitation token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_invitation_token(selenium, browser_id, group, who, oz_page, tmp_memory):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group]()
    page.main_page.menu_button()
    page.menu['Invite ' + who]()
    page.main_page.members.token.copy()


@wt(parsers.re('user of (?P<browser_id>.*) gets group "(?P<group>.*)" '
               '(?P<who>user|group) invitation token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def get_invitation_token(selenium, browser_id, group, who, oz_page, tmp_memory):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group]()
    page.main_page.menu_button()
    page.menu['Invite ' + who]()
    token = page.main_page.members.token.token
    tmp_memory[browser_id]['token'] = token


@wt(parsers.parse('user of {browser_id} see that page with text '
                  '"{text}" appeared'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_error_page_appeared(selenium, browser_id, text, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    assert page.main_page.error_label == text

