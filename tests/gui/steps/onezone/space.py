"""Steps for test suite for space.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import parsers
from tests.utils.acceptance_utils import wt
from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.utils.generic import parse_seq, repeat_failed


@wt(parsers.parse('user of {browser_id} clicks create new space on spaces on left menu'))
def choose_space_on_menu(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].create_space_button.click()


@wt(parsers.parse('user of {browser_id} types "{space_name}" on input'))
def type_on_create_new_space_input(selenium, browser_id, space_name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].input_box.value = space_name


@wt(parsers.parse('user of {browser_id} clicks on create new space button'))
def create_new_space(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].input_box.confirm.click()


@wt(parsers.parse('user of {browser_id} sees "{space_name}" has appeared on spaces'))
def assert_new_created_space(selenium, browser_id, space_name, oz_page):
    driver = selenium[browser_id]
    assert space_name in oz_page(driver)['spaces'].elements_list


@wt(parsers.parse('user of {browser_id} clicks "{space_name}" on spaces on left menu'))
def choose_space_on_spaces_menu(selenium, browser_id, space_name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].elements_list[space_name].click()


@wt(parsers.parse('user of {browser_id} types "{space_name}" on rename input'))
def type_on_rename_space_input(selenium, browser_id, space_name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].overview_page.rename.click()
    oz_page(driver)['spaces'].overview_page.edit_name_box.value = space_name


@wt(parsers.parse('user of {browser_id} clicks on confirmation button'))
def rename_space(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].overview_page.edit_name_box.confirm.click()


@wt(parsers.parse('user of {browser_id} clicks on cancel button'))
def rename_space(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].overview_page.edit_name_box.cancel.click()


@wt(parsers.parse('user of {browser_id} clicks on leave space button'))
def click_leave_space_button(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].overview_page.leave_space.click()


@wt(parsers.parse('user of {browser_id} clicks on yes leave button'))
def click_yes_leave_button(selenium, browser_id):
    driver = selenium[browser_id]
    driver.find_element_by_css_selector('.webui-popover-content button[type="submit"]').click()


@wt(parsers.parse('user of {browser_id} sees "{space_name}" has disappeared on spaces'))
def assert_leave_space(selenium, browser_id, space_name, oz_page):
    driver = selenium[browser_id]
    assert space_name not in oz_page(driver)['spaces'].elements_list


@wt(parsers.parse('user of {browser_id} clicks on toggle default space'))
def click_toggle_default_space_button(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].overview_page.set_default_space.click()


@wt(parsers.parse('user of {browser_id} sees home space on spaces on left menu'))
def assert_default_space_for_user(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    assert driver.find_element_by_css_selector('.status-toolbar-icon .oneicon-home')


@wt(parsers.parse('user of {browser_id} sees home space has disappeared on spaces on left menu'))
def assert_default_space_for_user(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    elem = driver.find_element_by_css_selector('div[class="status-toolbar-icon  not-clickable ember-view"] '
                                                 'span:first-of-type')
    assert 'oneicon-null' in elem.get_attribute("class")


@wt(parsers.parse('user of {browser_id} sees {number} number of supporting providers of "{space_name}"'))
def assert_number_of_supporting_providers(selenium, browser_id, number, space_name, oz_page):
    driver = selenium[browser_id]
    assert number == oz_page(driver)['spaces'].elements_list[space_name].supporting_providers_number


@wt(parsers.parse('user of {browser_id} sees {number} size of the "{space_name}"'))
def assert_number_of_supporting_providers(selenium, browser_id, number, space_name, oz_page):
    driver = selenium[browser_id]
    assert number == oz_page(driver)['spaces'].elements_list[space_name].support_size


@wt(parsers.parse('user of {browser_id} clicks Members of "{space_name}" on left menu'))
def choose_members_on_left_menu(selenium, browser_id, space_name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].elements_list[space_name].members.click()


@wt(parsers.parse('user of {browser_id} clicks "{user_name}" on list of users'))
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_user_on_list_of_users(selenium, browser_id, user_name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].members_page.users_list[user_name].click()


@wt(parsers.parse('user of {browser_id} clicks Space management toggle control'))
def change_space_management_toggle_control(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].members_page.users_list['user1'].privileges_list['Space management'].click()


@wt(parsers.parse('user of {browser_id} clicks Save button'))
def click_save_button(selenium, browser_id):
    driver = selenium[browser_id]
    pass


@wt(parsers.parse('user of {browser_id} sees Space management toggle control is inactive'))
def assert_space_management_toggle_control_inactive(selenium, browser_id):
    driver = selenium[browser_id]
    pass


@wt(parsers.parse('user of {browser_id} debugger'))
def debugger(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    import pdb
    pdb.set_trace()
