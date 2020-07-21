"""This module contains gherkin steps to run acceptance tests featuring groups
management in onezone web GUI
"""

__author__ = "Michal Stanisz, Lukasz Niemiec"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.utils.utils import repeat_failed
from tests.utils.bdd_utils import wt, parsers
from tests.gui.utils.common.modals import Modals as modals
from tests.gui.utils.generic import parse_seq, transform
from tests.gui.conftest import WAIT_FRONTEND
from selenium.webdriver.common.keys import Keys
from tests.gui.steps.common.miscellaneous import press_enter_on_active_element


@wt(parsers.re('user of (?P<browser_id>.*) clicks on Create '
               'group button in groups sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_group_button_in_panel(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['groups'].create_group()


@wt(parsers.parse('user of {browser_id} writes "{text}" '
                  'into group name text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def input_name_into_input_box_on_main_groups_page(selenium, browser_id,
                                                  text, oz_page):
    oz_page(selenium[browser_id])['groups'].input_box.value = text


@wt(parsers.parse('user of {browser_id} clicks on confirmation button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_name_input_on_main_groups_page(selenium, browser_id,
                                           oz_page):
    oz_page(selenium[browser_id])['groups'].input_box.confirm()


def _find_groups(page, group_name):
    return list(filter(lambda g: g.name == group_name, page.elements_list))


@wt(parsers.re('users? of (?P<browser_ids>.*) (?P<option>does not see|sees) '
               'group "(?P<group>.*)" on groups list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_group_exists(selenium, browser_ids, option, group, oz_page):
    for browser_id in parse_seq(browser_ids):
        groups_count = len(_find_groups(oz_page(selenium[browser_id])['groups'],
                                        group))
        if option == 'does not see':
            assert groups_count == 0, 'group "{}" found'.format(group)
        else:
            assert groups_count == 1, 'group "{}" not found'.format(group)


@wt(parsers.re('user of (?P<browser_id>.*) clicks on '
               '"(?P<option>Rename|Leave|Remove)" '
               'button in group "(?P<group>.*)" menu in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_group_menu_button(selenium, browser_id, option, group,
                               oz_page, popups):
    driver = selenium[browser_id]
    page = oz_page(driver)['groups']
    page.elements_list[group]()
    page.elements_list[group].menu()
    popups(driver).member_menu.menu[option]()


@wt(parsers.parse('user of {browser_id} writes '
                  '"{text}" into rename group text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def input_new_group_name_into_rename_group_inpux_box(selenium, browser_id, text,
                                                     oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[''].edit_box.value = text


@wt(parsers.parse('user of {browser_id} clicks on confirmation button '
                  'to rename group'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_confirmation_button_to_rename_group(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['groups'].elements_list[''].edit_box.confirm()


@wt(parsers.parse('user of {browser_id} sees that '
                  'create group button is inactive'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_create_button_inactive(selenium, browser_id, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    assert not page.input_box.confirm.is_enabled(), ('"Create group" button '
                                                     'is enabled')


@wt(parsers.re('user of (?P<browser_id>.*) goes to group "(?P<group>.*)" '
               '(?P<subpage>members|hierarchy|main) subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def go_to_group_subpage(selenium, browser_id, group, subpage, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    page.elements_list[group]()
    if subpage != 'main':
        getattr(page.elements_list[group], subpage)()


@wt(parsers.parse('user of {browser_id} see that page with text '
                  '"{text}" appeared'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_error_page_appeared(selenium, browser_id, text, oz_page):
    page = oz_page(selenium[browser_id])['groups']
    assert page.main_page.error_label == text, \
        'page with text "{}" not found'.format(text)


@wt(parsers.re('user of (?P<browser_id>.*) confirms group rename '
               'using (?P<option>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_rename_the_group(selenium, browser_id, option, oz_page):
    if option == 'enter':
        press_enter_on_active_element(selenium, browser_id)
    else:
        click_on_confirmation_button_to_rename_group(selenium, browser_id,
                                                     oz_page)


@wt(parsers.re('user of (?P<browser_id>.*) confirms using (?P<option>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_add_group(selenium, browser_id, option, oz_page):
    if option == 'enter':
        press_enter_on_active_element(selenium, browser_id)
    else:
        confirm_name_input_on_main_groups_page(selenium, browser_id,
                                               oz_page)


@wt(parsers.re('user of (?P<browser_id>.*) clicks on group '
               '"(?P<group_name>.*)" menu button in hierarchy subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_group_trigger(selenium, browser_id, oz_page, group_name):
    driver = selenium[browser_id]
    (oz_page(driver)['groups'].main_page.hierarchy.groups[group_name]
     .click_group_menu_button(driver))


@wt(parsers.re('user of (?P<browser_id>.*) clicks on group '
               '"(?P<group_name>.*)" menu button to (?P<relation>.*) relation '
               'in hierarchy subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_group_trigger(selenium, browser_id, oz_page, group_name, relation):
    driver = selenium[browser_id]
    (oz_page(driver)['groups'].main_page.hierarchy.groups[group_name]
     .click_relation_menu_button(driver, relation))


@wt(parsers.parse('user of {browser_id} clicks on "{option}" '
                  'in group hierarchy menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_in_group_hierarchy_menu(selenium, browser_id, option):
    driver = selenium[browser_id]
    modals(driver).group_hierarchy_menu.options[option].click()


@wt(parsers.parse('user of {browser_id} clicks on "{option}" '
                  'in relation menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_in_group_hierarchy_menu(selenium, browser_id, option):
    driver = selenium[browser_id]
    modals(driver).relation_menu.options[option].click()


@wt(parsers.parse('user of {browser_id} writes "{group_name}" '
                  'into group name text field in create group modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def write_name_group_in_create_new_child_group_modal(selenium, browser_id,
                                                     group_name):
    driver = selenium[browser_id]
    modals(driver).create_group.input_name = group_name


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>does not see|sees) '
               '"(?P<group_name>.*)" as a (?P<relation>child|parent) '
               'of "(?P<active_group>.*)" in hierarchy subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_list_of_children_contains_group(selenium, browser_id, oz_page,
                                           group_name, relation, active_group,
                                           option):
    relation = 'children' if relation == 'child' else 'parents'

    groups = getattr(oz_page(selenium[browser_id])['groups'].main_page.hierarchy,
                     relation)
    if option == 'sees':
        assert group_name in groups
    else:
        assert group_name not in groups


@wt(parsers.re('user of (?P<browser_id>.*) clicks show parent groups '
               'in hierarchy subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_list_of_children_contains_group(selenium, browser_id, oz_page):
    (oz_page(selenium[browser_id])['groups'].main_page.hierarchy
     .show_parent_groups())


@wt(parsers.parse('user of {browser_id} sees "{text}" in error details'
                  ' on groups page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_error_detail_text(selenium, browser_id, oz_page, text):
    page = oz_page(selenium[browser_id])['groups']
    assert text in page.main_page.error_details, ('page with text "{}" '
                                                  'not found'.format(text))


@wt(parsers.parse('user of {browser_id} clicks on "{button_name}" button '
                  'in popup group menu on hierarchy subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_group_menu_popup_button(selenium, browser_id, button_name,
                                     popups):
    driver = selenium[browser_id]
    popups(driver).group_menu.menu[button_name]()


@wt(parsers.parse('user of {browser_id} sees "{group_name}" group '
                  'members page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_user_sees_group_page(selenium, oz_page, browser_id, group_name):
    driver = selenium[browser_id]
    assert oz_page(driver)['groups'].selected_group_name == group_name


@wt(parsers.parse('user of {browser_id} sees default group hierarchy view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def default_hierarchy_view(selenium, browser_id, oz_page, tmp_memory):
    driver = selenium[browser_id]
    default_groups_view = []
    for group in oz_page(driver)['groups'].main_page.hierarchy.groups:
        default_groups_view.append(group.name)
    tmp_memory['default_groups_view'] = default_groups_view


@wt(parsers.parse('user of {browser_id} toggles show "{group_name}" '
                  'group {relation_type} button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def expand_all_relations(selenium, browser_id, oz_page, relation_type):
    driver = selenium[browser_id]
    getattr(oz_page(driver)['groups'].main_page.hierarchy,
             transform('show '+relation_type+' groups')).click()


@wt(parsers.parse('user of {browser_id} clicks "{btn_name}" button in group '
                  'hierarchy view menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def expand_all_relations(selenium, browser_id, btn_name, oz_page, popups):
    driver = selenium[browser_id]
    oz_page(driver)['groups'].main_page.hierarchy.hierarchy_view_menu.click()
    popups(selenium[browser_id]).toolbar.options[btn_name].click()


@wt(parsers.parse('user of {browser_id} sees the same group hierarchy view '
                  'as default one'))
@repeat_failed(timeout=WAIT_FRONTEND)
def expand_all_relations(selenium, browser_id, oz_page, tmp_memory):
    driver = selenium[browser_id]
    reset_groups_view = []
    for group in oz_page(driver)['groups'].main_page.hierarchy.groups:
        reset_groups_view.append(group.name)
    default_groups_view = tmp_memory['default_groups_view']

    assert default_groups_view == reset_groups_view
