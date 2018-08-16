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
from selenium.webdriver.common.keys import Keys


@wt(parsers.parse('user of {browser_id} clicks create new space on spaces on left sidebar menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_new_space_on_spaces_on_left_sidebar_menu(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].create_space_button()


@wt(parsers.parse('user of {browser_id} types "{space_name}" on input on create new space page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_space_name_on_input_on_create_new_space_page(selenium, browser_id, space_name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].input_box.value = space_name


@wt(parsers.parse('user of {browser_id} clicks on create new space button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_new_space_by_click_on_create_new_space_button(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].input_box.confirm()


@wt(parsers.parse('user of {browser_id} creates space "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_new_space(selenium, browser_id, space_name, oz_page):
    page = oz_page(selenium[browser_id])['spaces']
    page.create_space_button()
    page.input_box.value = space_name
    page.input_box.confirm()


@wt(parsers.parse('user of {browser_id} sees that there is no supporting '
                  'provider "{provider_name}" for space named "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_no_provider_for_space(selenium, browser_id, provider_name, space_name, hosts, oz_page):
    page = oz_page(selenium[browser_id])['spaces']
    page.elements_list[space_name]()
    page.elements_list[space_name].providers()
    provider = hosts[provider_name]['name']
    try:
        page.providers_page.providers_list[provider]
    except RuntimeError:
        pass
    else:
        assert False, 'provider "{}" found on space "{}" providers list'\
                      .format(provider, space_name)


@wt(parsers.parse('user of {browser_id} presses enter on keyboard'))
@repeat_failed(timeout=WAIT_FRONTEND)
def press_enter_on_keyboard(selenium, browser_id):
    driver = selenium[browser_id]
    driver.switch_to.active_element.send_keys(Keys.RETURN)


@wt(parsers.parse('user of {browser_id} sees "{space_name}" has appeared on spaces'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_new_created_space_has_appeared_on_spaces(selenium, browser_id, space_name, oz_page):
    driver = selenium[browser_id]
    assert space_name in oz_page(driver)['spaces'].elements_list


@wt(parsers.parse('user of {browser_id} clicks "{space_name}" on spaces on left sidebar menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_space_on_spaces_on_left_sidebar_menu(selenium, browser_id, space_name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].elements_list[space_name].click()


@wt(parsers.parse('user of {browser_id} types "{space_name}" on rename input on overview page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_space_name_on_rename_space_input_on_overview_page(selenium, browser_id, space_name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].overview_page.rename()
    oz_page(driver)['spaces'].overview_page.edit_name_box.value = space_name


@wt(parsers.parse('user of {browser_id} clicks on confirmation button on overview page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def rename_space_by_click_on_confirmation_button_on_overview_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].overview_page.edit_name_box.confirm()


@wt(parsers.parse('user of {browser_id} clicks on cancel button on overview page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_cancel_rename_button_on_overview_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].overview_page.edit_name_box.cancel()


@wt(parsers.parse('user of {browser_id} clicks on leave space button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_leave_space_button_on_overview_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].overview_page.leave_space()


@wt(parsers.parse('user of {browser_id} clicks on "{button_name}" button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_confirm_or_cancel_button_on_leave_space_page(selenium, browser_id, button_name):
    driver = selenium[browser_id]
    buttons_list = driver.find_elements_by_css_selector('.webui-popover-content span')
    for button in buttons_list:
        if button.text == button_name:
            button.click()


@wt(parsers.parse('user of {browser_id} sees "{space_name}" has disappeared on spaces'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_space_has_disappeared_on_spaces(selenium, browser_id, space_name, oz_page):
    driver = selenium[browser_id]
    assert space_name not in oz_page(driver)['spaces'].elements_list


@wt(parsers.parse('user of {browser_id} clicks on toggle default space'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_toggle_default_space_button_on_overview_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].overview_page.set_default_space()


@wt(parsers.parse('user of {browser_id} sees home space on spaces on left sidebar menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_home_space_has_appeared_on_spaces_on_left_sidebar_menu(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    assert driver.find_element_by_css_selector('.status-toolbar-icon .oneicon-home')


@wt(parsers.parse('user of {browser_id} sees home space has disappeared on spaces on left sidebar menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_home_space_has_disappeared_on_spaces_on_left_sidebar_menu(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    elem = driver.find_element_by_css_selector('div[class="status-toolbar-icon  not-clickable ember-view"] '
                                               'span:first-of-type')
    assert 'oneicon-null' in elem.get_attribute("class")


@wt(parsers.parse('user of {browser_id} sees {number} number of supporting providers of "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_check_number_of_supporting_providers_of_space(selenium, browser_id, number, space_name, oz_page):
    driver = selenium[browser_id]
    assert number == oz_page(driver)['spaces'].elements_list[space_name].supporting_providers_number


@wt(parsers.parse('user of {browser_id} sees {number} size of the "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_check_size_of_space_on_left_sidebar_menu(selenium, browser_id, number, space_name, oz_page):
    driver = selenium[browser_id]
    assert number == oz_page(driver)['spaces'].elements_list[space_name].support_size


@wt(parsers.parse('user of {browser_id} clicks Members of "{space_name}" on left sidebar menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_members_of_space_on_left_sidebar_menu(selenium, browser_id, space_name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].elements_list[space_name].members()


@wt(parsers.parse('user of {browser_id} clicks Overview of "{space_name}" on left sidebar menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_overview_of_space_on_left_sidebar_menu(selenium, browser_id, space_name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].elements_list[space_name].overview()


@wt(parsers.parse('user of {browser_id} clicks Get started on spaces on left sidebar menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_get_started_on_spaces_on_left_sidebar_menu(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].get_started()


@wt(parsers.parse('user of {browser_id} clicks Create a space on Welcome page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_space_on_welcome_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].welcome_page.create_a_space()


@wt(parsers.parse('user of {browser_id} types "{token_name}" to input on Join to a space page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_token_name_to_input_on_join_to_a_space_page(selenium, browser_id, token_name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].input_box.value = token_name


@wt(parsers.parse('user of {browser_id} sees error popup has appeared'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_error_popup_has_appeared(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    header = driver.find_element_by_css_selector('.modal-dialog h1')
    assert "ERROR" == header.text


@wt(parsers.parse('user of {browser_id} clicks Providers of "{space_name}" on left sidebar menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_providers_of_space_on_left_sidebar_menu(selenium, browser_id, space_name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].elements_list[space_name].providers()


@wt(parsers.parse('user of {browser_id} sees "{provider_name}" is on the providers list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_check_if_providers_list_contains_provider(selenium, browser_id, provider_name, hosts, oz_page):
    driver = selenium[browser_id]
    provider = hosts[provider_name]['name']
    providers_list = oz_page(driver)['spaces'].providers_page.providers_list
    assert provider in providers_list


@wt(parsers.parse('user of {browser_id} sees length of providers list is equal'
                  ' number of supporting providers of "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_check_if_providers_list_contains_provider(selenium, browser_id, space_name, oz_page):
    driver = selenium[browser_id]
    providers_list = oz_page(driver)['spaces'].providers_page.providers_list
    number_of_providers = int(oz_page(driver)['spaces'].elements_list[space_name].supporting_providers_number)
    assert len(providers_list) == number_of_providers


@wt(parsers.parse('user of {browser_id} sees length of providers list of "{space_name}" is equal'
                  ' "{number_of_providers}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_check_if_providers_list_contains_provider(selenium, browser_id, space_name, number_of_providers, oz_page):
    driver = selenium[browser_id]
    providers_list = oz_page(driver)['spaces'].providers_page.providers_list
    assert len(providers_list) == int(number_of_providers)


@wt(parsers.parse('user of {browser_id} clicks Get support button on providers page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_get_support_button_on_providers_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].providers_page.get_support()


@wt(parsers.parse('user of {browser_id} clicks Deploy your own provider tab on get support page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_deploy_your_own_provider_tab_on_get_support_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].providers_page.get_support_page.deploy_provider_modal()


@wt(parsers.parse('user of {browser_id} clicks Expose existing data collection tab on get support page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_expose_existing_data_collection_tab_on_get_support_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].providers_page.get_support_page.expose_existing_data_modal()


@wt(parsers.parse('user of {browser_id} clicks Copy button on Get support page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_copy_button_on_request_support_page(selenium, browser_id, oz_page, displays, clipboard, tmp_memory):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].providers_page.get_support_page.copy_button()

    item = clipboard.paste(display=displays[browser_id])
    tmp_memory[browser_id]['mailbox']['token'] = item


@wt(parsers.parse('user of {browser_id} clicks Generate another token on Get support page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_generate_another_token_on_request_support_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].providers_page.get_support_page.generate_another_token()


@wt(parsers.parse('user of {browser_id} sees another token is different than first one'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_check_if_two_tokens_are_different(selenium, browser_id, oz_page, displays, clipboard, tmp_memory):
    driver = selenium[browser_id]
    first_token = tmp_memory[browser_id]['mailbox']['token']
    oz_page(driver)['spaces'].providers_page.get_support_page.copy_button()

    second_token = clipboard.paste(display=displays[browser_id])
    assert first_token != second_token


@wt(parsers.parse('user of {browser_id} sees copy token and token in input are the same'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_check_if_copy_token_and_input_token_are_the_same(selenium, browser_id, oz_page, tmp_memory):
    driver = selenium[browser_id]
    first_token = tmp_memory[browser_id]['mailbox']['token']
    second_token = oz_page(driver)['spaces'].providers_page.get_support_page.token_textarea
    assert first_token == second_token


@wt(parsers.parse('user of {browser_id} sees non-empty copy token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_check_if_copy_token_is_not_empty(selenium, browser_id, oz_page, tmp_memory):
    driver = selenium[browser_id]
    token = tmp_memory[browser_id]['mailbox']['token']
    assert len(token) > 0


@wt(parsers.parse('user of {browser_id} reloads page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def reload_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    driver.refresh()


@wt(parsers.parse('user of {browser_id} sees "{space_name}" label on overview page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_check_name_label_of_space_on_overview_page(selenium, browser_id, space_name, oz_page):
    driver = selenium[browser_id]
    assert oz_page(driver)['spaces'].overview_page.space_name == space_name


@wt(parsers.parse('user of {browser_id1} generates space support token for '
                  'space "{space_name}" and sends it to user of {browser_id2}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def generate_and_send_support_token(selenium, browser_id1, space_name, oz_page,
                           browser_id2, clipboard, displays, tmp_memory):
    page = oz_page(selenium[browser_id1])['spaces']
    page.elements_list[space_name]()
    page.elements_list[space_name].providers()
    page.providers_page.get_support()
    page.providers_page.get_support_page.copy_button()
    item = clipboard.paste(display=displays[browser_id1])
    tmp_memory[browser_id2]['mailbox']['token'] = item

@wt(parsers.parse('user of {browser_id} clicks Copy button to send to "{browser_list}" on Get support page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def send_copy_token_to_browser_from_get_support_page(selenium, browser_id, oz_page, displays,
                                                     clipboard, browser_list, tmp_memory):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].providers_page.get_support_page.copy_button()

    item = clipboard.paste(display=displays[browser_id])
    for browser in parse_seq(browser_list):
        tmp_memory[browser]['mailbox']['token'] = item