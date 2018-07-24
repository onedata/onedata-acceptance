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


@wt(parsers.re('user of (?P<browser_id>.*) clicks on the (?P<operation>CREATE|JOIN) button in "(?P<panel>.*)" Onezone panel'))
def click_button_in_panel(selenium, browser_id, operation, panel, oz_page):
    if operation == 'CREATE':
        oz_page(selenium[browser_id])[panel].create_group.click()
    elif operation == 'JOIN':
        oz_page(selenium[browser_id])[panel].join_group.click()


@wt(parsers.parse('user of {browser_id} writes "{text}" into group name text field'))
def input_new_group_name(selenium, browser_id, text, oz_page):
    oz_page(selenium[browser_id])['groups'].input_box.value = text


@wt(parsers.parse('user of {browser_id} confirms group name'))
def confirm_group_name(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['groups'].input_box.confirm.click()


def _find_groups(selenium, browser_id, oz_page, group):
    return filter(lambda g : g.name == group, oz_page(selenium[browser_id])['groups'].elements_list)


@wt(parsers.parse('user of {browser_id} sees group "{group}"'))
def check_group_existance(selenium, browser_id, group, oz_page):
    assert len(_find_groups(selenium, browser_id, oz_page, group)) > 0, "no such group exists"


@wt(parsers.re('user of (?P<browser_id>.*) clicks on (?P<operation>RENAME|JOIN|LEAVE|REMOVE) button in "(?P<group>.*)" group options menu'))
def click_group_option_button(selenium, browser_id, operation, group, oz_page):
    _find_groups(selenium, browser_id, oz_page, group)[0]()
    oz_page(selenium[browser_id])['groups'].overview_page.rename.click()
    



