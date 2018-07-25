"""This module contains gherkin steps to run acceptance tests featuring groups
management in onezone web GUI
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from pytest_bdd import parsers, when, then
from tests.utils.acceptance_utils import wt
from tests.gui.steps.common import *

@wt(parsers.re('user of (?P<browser_id>.*) clicks on the '
               '(?P<operation>create|join) button in '
               '"(?P<panel>.*)" Onezone panel'))
def click_button_in_panel(selenium, browser_id, operation, panel, oz_page):
    if operation == 'create':
        oz_page(selenium[browser_id])[panel].create_group.click()
    else:
        oz_page(selenium[browser_id])[panel].join_group.click()


@wt(parsers.parse('user of {browser_id} writes "{text}" '
                  'into group name text field'))
def input_new_group_name(selenium, browser_id, text, oz_page):
    oz_page(selenium[browser_id])['groups'].input_box.value = text


@wt(parsers.parse('user of {browser_id} confirms group name'))
def confirm_group_name(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['groups'].input_box.confirm.click()


def _find_groups(page, group):
    return filter(lambda g : g.name == group, page.elements_list)


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>do|dont) '
               'see group "(?P<group>.*)" on groups list'))
def check_group_existance(selenium, browser_id, option, group, oz_page):
    groups_count = len(_find_groups(oz_page(selenium[browser_id])['groups'], group))
    if option == 'do':
        assert groups_count > 0, "no such group exists"
    else:
        assert groups_count == 0, "such group exists"


@wt(parsers.parse('user of {browser_id} clicks on "{group}" group menu button'))
def open_group_menu(selenium, browser_id, group, oz_page, tmp_memory):
    groups = oz_page(selenium[browser_id])['groups']
    tmp_memory['group'] = groups
    groups.elements_list[group].menu.click()

@wt(parsers.re('user of (?P<browser_id>.*) clicks on '
               '(?P<option>rename|join|leave|delete) button in active menu'))
def click_on_menu(selenium, browser_id, option, oz_page, tmp_memory):
    button_id = {'rename': 0, 'join': 1, 'leave': 2, 'delete': 3}[option]
    groups = tmp_memory['group'] #oz_page(selenium[browser_id])['groups']
    groups.group_menu[button_id].click()

@wt(parsers.parse('user of {browser_id} writes '
                  '"{text}" into rename group text field'))
def input_new_name(selenium, browser_id, text, oz_page):
    groups = oz_page(selenium[browser_id])['groups']
    groups.elements_list[''].input_field = text
    
@wt(parsers.parse('user of {browser_id} confirms group rename'))
def confirm_rename(selenium, browser_id, oz_page):
    groups = oz_page(selenium[browser_id])['groups']
    groups.elements_list[''].confirm_button.click()
        



