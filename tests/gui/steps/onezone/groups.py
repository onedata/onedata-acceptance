"""This module contains gherkin steps to run acceptance tests featuring groups
management in onezone web GUI
"""

__author__ = "Michal Stanisz, Lukasz Niemiec"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import parsers

from tests.utils.utils import repeat_failed
from tests.utils.acceptance_utils import wt
from tests.gui.utils.common.modals import Modals as modals
from tests.gui.utils.generic import parse_seq
from tests.gui.conftest import WAIT_FRONTEND
from selenium.webdriver.common.keys import Keys
from tests.gui.steps.common.miscellaneous import press_enter_on_active_element
from tests.gui.steps.modal import wt_wait_for_modal_to_appear


@wt(parsers.re('user of (?P<browser_id>.*) clicks on (?P<operation>Create|Join) '
               'group button in groups sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_or_join_group_button_in_panel(selenium, browser_id, operation,
                                               oz_page):
    button_name = '{}_group'.format(operation.lower())
    getattr(oz_page(selenium[browser_id])['groups'], button_name)()


@wt(parsers.parse('user of {browser_id} joins group "{group}" to space'))
@repeat_failed(timeout=WAIT_FRONTEND)
def join_space(selenium, browser_id, group, oz_page, tmp_memory):
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
    return filter(lambda g: g.name == group_name, page.elements_list)


@wt(parsers.re('user of (?P<browser_id>.*) joins group using received token '
               'and uses (?P<confirm_type>button|enter) to confirm'))
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
               '"(?P<option>Rename|Join space|Join as subgroup|Leave|Remove)" '
               'button in group "(?P<group>.*)" menu in the sidebar'))
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


@wt(parsers.parse('user of {browser_id} clicks on "{button}" button in '
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
    message = 'Modal does not contain text "{}"'.format(text)
    assert text in modals(selenium[browser_id]).error.content, message


@wt(parsers.re('user of (?P<browser_id>.*) goes to group "(?P<group>.*)" '
               '(?P<subpage>members|hierarchy|main) subpage'))
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


@wt(parsers.parse('user of {browser_id} adds group "{group}" as subgroup '
                  'using received token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_group_as_subgroup(selenium, browser_id, group, oz_page, tmp_memory):
    option = 'Join as subgroup'
    click_on_group_menu_button(selenium, browser_id, option, group, oz_page)

    token = tmp_memory[browser_id]['mailbox']['token']
    page = oz_page(selenium[browser_id])['groups']
    page.input_box.value = token

    confirm_name_or_token_input_on_main_groups_page(selenium, browser_id,
                                                    oz_page)


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
        confirm_name_or_token_input_on_main_groups_page(selenium, browser_id,
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


@wt(parsers.parse('user of {browser_id} clicks Show details on groups page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_show_details_on_groups_page(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['groups'].main_page.show_details()


@wt(parsers.parse('user of {browser_id} sees "{text}" text on groups page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_error_detail_text(selenium, browser_id, oz_page, text):
    page = oz_page(selenium[browser_id])['groups']
    assert text in page.main_page.error_details, ('page with text "{}" '
                                                  'not found'.format(text))

