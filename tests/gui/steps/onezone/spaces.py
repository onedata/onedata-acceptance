"""This module contains gherkin steps to run acceptance tests featuring
spaces management in onezone web GUI.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.steps.common.miscellaneous import (press_enter_on_active_element,
                                                  switch_to_iframe)
from tests.gui.steps.modals.modal import wt_wait_for_modal_to_appear
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed

SPACE_TABS = ["overview", "files", "shares_open_data", "transfers",
              "datasets_archives", "providers", "members",
              "harvesters_discovery", "automation_workflows"]


@repeat_failed(timeout=WAIT_FRONTEND)
def _choose_space_from_menu_list(oz_page, driver, name):
    option = 'data'
    # select data in main menu if not selected
    if not oz_page(driver).is_panel_clicked(option):
        oz_page(driver).get_page_and_click(option)
    click_on_space_in_menu_list(oz_page, driver, name)


def click_on_space_in_menu_list(oz_page, driver, name, force=True):
    # function assumes data page is active
    page = oz_page(driver)['data']
    if force:
        page.spaces_header_list[name]()
    else:
        if not page.spaces_header_list[name].is_active():
            page.spaces_header_list[name].click()
    return page


def _parse_tabs_list(tabs):
    tabs = tabs.split('"')[1:-1]
    tabs = [
        transform(e).replace(',', '') for e in tabs if e != ', '
    ]
    return tabs


@wt(parsers.re('user of (?P<browser_id>.*?) clicks on '
               '"(?P<button_name>Create space|Marketplace)" button in '
               'spaces sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_on_spaces_sidebar_menu(selenium, browser_id, button_name,
                                        oz_page):
    driver = selenium[browser_id]
    button_name = transform(button_name) + "_button"
    getattr(oz_page(driver)['data'], button_name).click()


@wt(parsers.parse('user of {browser_id} clicks {button_name} button '
                  'in space harvesters page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_in_space_harvesters_page(selenium, browser_id, oz_page,
                                          button_name):
    driver = selenium[browser_id]
    button_name = transform(button_name)
    getattr(oz_page(driver)['data'].harvesters_page, button_name).click()


@wt(parsers.parse('user of {browser_id} writes "{space_name}" '
                  'into space name text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_space_name_on_input_on_create_new_space_page(selenium, browser_id,
                                                      space_name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['data'].input_box.value = space_name


@wt(parsers.parse('user of {browser_id} clicks on Create new space button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_new_space_by_click_on_create_new_space_button(selenium, browser_id,
                                                         oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['data'].input_box.confirm()


@wt(parsers.parse('user of {browser_id} creates space "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_new_space_on_onezone_page(selenium, browser_id, space_name, oz_page):
    page = oz_page(selenium[browser_id])['data']
    page.create_space_button()
    page.input_box.value = space_name
    page.input_box.confirm()


@wt(parsers.parse('user of {browser_id} sees that there is no supporting '
                  'provider "{provider_name}" for space named "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_no_provider_for_space(selenium, browser_id, provider_name,
                                 space_name, hosts, oz_page):
    page = oz_page(selenium[browser_id])['data']
    page.spaces_header_list[space_name]()
    page.elements_list[space_name].providers()
    provider = hosts[provider_name]['name']
    try:
        page.providers_page.providers_list[provider]
    except RuntimeError:
        pass
    else:
        assert False, ('provider "{}" found on space "{}" providers list'
                       .format(provider, space_name))


@wt(parsers.parse('user of {browser_id} sees that "{space_name}" has appeared '
                  'on the spaces list in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_new_created_space_has_appeared_on_spaces(selenium, browser_id,
                                                    space_name, oz_page):
    driver = selenium[browser_id]
    assert space_name in oz_page(driver)['data'].elements_list, \
        'space "{}" not found'.format(space_name)


@wt(parsers.re('user of (?P<browser_id>.*?) clicks on Automation '
               'in the main menu'))
def click_on_automation_option_in_the_sidebar(
        selenium, browser_id, oz_page, tmp_memory):
    option = 'Automation'
    page = _click_on_option_in_the_sidebar(
        selenium, browser_id, option, oz_page)
    err_msg = 'Clicking on the "Automation" in the main menu did not succeed'
    assert page, err_msg
    tmp_memory[browser_id]['oz_page'] = page


@wt(parsers.re('user of (?P<browser_id>.*?) clicks on '
               '(?P<option>Data|Shares|Providers|Groups|Tokens|Discovery|'
               'Clusters) in the main menu'))
def click_on_option_in_the_sidebar(
        selenium, browser_id, option, oz_page):
    _click_on_option_in_the_sidebar(
        selenium, browser_id, option, oz_page, force=True)


@repeat_failed(timeout=WAIT_BACKEND)
def _click_on_option_in_the_sidebar(
        selenium, browser_id, option, oz_page, force=True):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    name = str(option).lower()
    # call get_page in Onezone page
    if force:
        page = oz_page(driver).get_page_and_click(name)
        return page
    else:
        if not oz_page(driver).is_panel_clicked(name):
            oz_page(driver).get_page_and_click(name)


@wt(parsers.re('user of (?P<browser_id>.*?) clicks "(?P<name>.*?)" '
               'on the (?P<option>spaces|groups|harvesters) list in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_element_on_lists_on_left_sidebar_menu(selenium, browser_id, option,
                                                name, oz_page):
    driver = selenium[browser_id]
    if option == 'harvesters':
        option = 'discovery'

    if option == 'spaces':
        _choose_space_from_menu_list(oz_page, driver, name)
    else:
        oz_page(driver).get_page_and_click(option).elements_list[name].click()


@wt(parsers.parse('user of {browser_id} clicks on "{button}" button '
                  'in space "{space_name}" menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_in_space_menu(selenium, browser_id, space_name, button,
                                  oz_page, popups):
    driver = selenium[browser_id]
    oz_page(driver)['data'].spaces_header_list[space_name].click_menu()
    popups(driver).menu_popup_with_text.menu[button]()


@wt(parsers.re('user of (?P<browser_id>.*) clicks on '
               '"(?P<button>.*)" button in space menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_in_menu(selenium, browser_id, button, oz_page, popups):
    driver = selenium[browser_id]
    page = oz_page(driver)['data']
    page.menu_button()
    popups(driver).menu_popup_with_text.menu[button]()


@wt(parsers.re('user of (?P<browser_id>.*?) clicks on '
               '(?P<button_name>Leave|Cancel) button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_confirm_or_cancel_button_on_leave_space_page(selenium, browser_id,
                                                       button_name, modals):
    getattr(modals(selenium[browser_id]).leave_modal, button_name.lower())()


@wt(parsers.re('user of (?P<browser_id>.*?) clicks on '
               'understand notice checkbox in "Remove space" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_remove_space_understand_notice(selenium, browser_id, modals):
    modals(selenium[browser_id]).remove_modal.understand_notice()


@wt(parsers.re('user of (?P<browser_id>.*?) clicks on '
               '"Remove" button in "Remove space" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_remove_space_button(selenium, browser_id, modals):
    modals(selenium[browser_id]).remove_modal.remove()


@wt(parsers.parse('user of {browser_id} sees that "{space_name}" '
                  'has disappeared on the spaces list in the sidebar'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_space_has_disappeared_on_spaces(selenium, browser_id, space_name,
                                           oz_page):
    driver = selenium[browser_id]
    spaces = oz_page(driver)['data'].elements_list
    assert space_name not in spaces, 'space "{}" found'.format(space_name)


@wt(parsers.parse('user of {browser_id} sees {number:d} number of supporting '
                  'providers of "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_number_of_supporting_providers_of_space(selenium, browser_id,
                                                   number: int, space_name,
                                                   oz_page):
    driver = selenium[browser_id]
    supporting_providers_number = int(oz_page(driver)['data']
                                      .elements_list[space_name]
                                      .supporting_providers_number)
    assert number == supporting_providers_number, (
        f'found {supporting_providers_number} supporting providers instead of '
        f'{number}')


@wt(parsers.parse('user of {browser_id} sees {number} size of '
                  'the "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_size_of_space_on_left_sidebar_menu(selenium, browser_id, number,
                                              space_name, oz_page):
    driver = selenium[browser_id]
    assert (number == oz_page(driver)['data']
            .elements_list[space_name]
            .support_size), ('size of space "{}" is not equal {}'
                             .format(space_name, number))


def _get_subpage_name(subpage):
    return transform(subpage) + '_page'


@wt(parsers.re('user of (?P<browser_id>.*) clicks "(?P<provider>.*)" '
               'provider icon on the map on (?P<page>overview|providers) data '
               'page'))
def click_provider_on_the_map_on_data_page(selenium, browser_id, provider,
                                           oz_page, page, hosts):
    driver = selenium[browser_id]
    current_page = getattr(oz_page(driver)['data'], _get_subpage_name(page))
    provider_name = hosts[provider]['name']
    current_page.map.click_provider(provider_name, driver)


@wt(parsers.re('user of (?P<browser_id>.*) hovers over '
               'provider icon on the map on (?P<page>overview|providers) data '
               'page and sees that provider name is "(?P<provider>.*)"'))
def hover_provider_on_the_map_on_data_page(selenium, browser_id, provider,
                                           oz_page, page, hosts):
    driver = selenium[browser_id]
    current_page = getattr(oz_page(driver)['data'], _get_subpage_name(page))
    provider_name = hosts[provider]['name']
    current_page.map.hover_and_check_provider(provider_name, driver)


@wt(parsers.re('user of (?P<browser_id>.*?) clicks the map on '
               '(?P<space_name>.*) space (?P<page>overview|providers) data '
               'page'))
def click_the_map_on_data_page(selenium, browser_id, oz_page, page, space_name):
    driver = selenium[browser_id]
    getattr(oz_page(driver)['data'], _get_subpage_name(page)).map()


@wt(parsers.re('user of (?P<browser_id>.*?) clicks "(?P<option>.*?)" '
               'of "(?P<space_name>.*?)" space in the sidebar'))
def click_on_option_of_space_on_left_sidebar_menu(
        selenium, browser_id, space_name, option, oz_page):
    _click_on_option_of_space_on_left_sidebar_menu(
        selenium, browser_id, space_name, option, oz_page)


@repeat_failed(timeout=WAIT_BACKEND)
def _click_on_option_of_space_on_left_sidebar_menu(
        selenium, browser_id, space_name, option, oz_page, force=True):
    submenu_option = transform(option).replace(',', '')
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    page = click_on_space_in_menu_list(oz_page, driver, space_name, force=force)
    getattr(page.elements_list[space_name], submenu_option).click()


def _get_number_of_disabled_elements_on_left_sidebar_menu(space):
    page_names = ['overview', 'files', 'shares_open_data', 'transfers',
                  'providers', 'members', 'harvesters_discovery']
    return len([x for x in page_names if space.is_element_disabled(x)])


@wt(parsers.re('user of (?P<browser_id>.*?) sees that (?P<element_list>.*) '
               'of "(?P<space_name>.*?)" in the sidebar are disabled'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_option_of_space_on_left_sidebar_menu_disabled(selenium, browser_id,
                                                         space_name,
                                                         element_list,
                                                         oz_page):
    driver = selenium[browser_id]
    element_list = _parse_tabs_list(element_list)
    space = oz_page(driver)['data'].elements_list[space_name]
    error_msg = f'Number of disabled elements is incorrect'
    assert _get_number_of_disabled_elements_on_left_sidebar_menu(space) == len(
        element_list), error_msg

    for element_name in element_list:
        error_msg = f' "{element_name}" button is not in disabled state'
        assert space.is_element_disabled(element_name), error_msg


@wt(parsers.re('user of (?P<browser_id>.*) sees (?P<correct_number>.*) '
               'providers? on the map on (?P<space_name>.*) '
               'space (?P<page>.*) data page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_number_of_providers_on_the_map_on_data_page(
        selenium, browser_id, correct_number, space_name, page, oz_page):
    if correct_number == 'no':
        correct_number = 0
    driver = selenium[browser_id]
    current_page = getattr(oz_page(driver).get_page_and_click('data'),
                           _get_subpage_name(page))
    number_providers = len(current_page.map.providers)
    error_msg = f'found {number_providers} instead of {correct_number}'
    assert number_providers == int(correct_number), error_msg


@wt(parsers.parse('user of {browser_id} clicks Get started in data sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_get_started_on_data_on_left_sidebar_menu(selenium, browser_id,
                                                   oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['data'].get_started()


@wt(parsers.re('user of (?P<browser_id>.*?) clicks '
               '(?P<option>Create a space|join an existing space) '
               'on Welcome page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_on_welcome_page(selenium, browser_id, option, oz_page):
    driver = selenium[browser_id]
    getattr(oz_page(driver)['data'].welcome_page, transform(option)).click()


@wt(parsers.parse('user of {browser_id} sees that error popup has appeared'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_error_popup_has_appeared(selenium, browser_id, modals):
    assert "failed" in modals(selenium[browser_id]).error.content, \
        'error popup not found'


@wt(parsers.re('user of (?P<browser_id>.*) (?P<see>does not see|sees) '
               '"(?P<harvester_name>.*)" in harvesters list '
               'on space harvesters subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_harvester_on_list_on_space_harvesters_subpage(selenium, browser_id,
                                                         harvester_name,
                                                         oz_page, see):
    driver = selenium[browser_id]
    harvesters_list = oz_page(driver)['data'].harvesters_page.harvesters_list
    if see == 'sees':
        error_msg = f' Harvester {harvester_name} not found on harvesters list'
        assert harvester_name in harvesters_list, error_msg
    elif see == 'does not see':
        error_msg = f' Harvester {harvester_name} found on harvesters list'
        assert harvester_name not in harvesters_list, error_msg


@wt(parsers.parse('user of {browser_id} sees "{provider}" is on '
                  'the providers list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_providers_list_contains_provider(selenium, browser_id, provider,
                                            hosts, oz_page):
    driver = selenium[browser_id]
    if provider in hosts:
        provider = hosts[provider]['name']
    providers_list = oz_page(driver)['data'].providers_page.providers_list
    assert provider in providers_list, 'provider "{}" not found'.format(
        provider)


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>check|uncheck)s '
               '(?P<toggle>.*) toggle in selected provider settings '
               'on providers page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_toggle_on_providers_subpage(browser_id, toggle, selenium,
                                      op_container, option):
    driver = selenium[browser_id]
    getattr(getattr(op_container(driver).provider_configuration,
                    transform(toggle)), option)()


@wt(parsers.parse('user of {browser_id} sees that length of providers list '
                  'equals number of supporting providers of "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_length_of_providers_list(selenium, browser_id, space_name, oz_page):
    driver = selenium[browser_id]
    providers_list = oz_page(driver)['data'].providers_page.providers_list
    number_of_providers = int(oz_page(driver)['data']
                              .elements_list[space_name]
                              .supporting_providers_number)
    assert len(providers_list) == number_of_providers, \
        ('length of providers list is not equal to number of '
         'supporting providers of space "{}"'.format(space_name))


@wt(parsers.parse('user of {browser_id} sees that length of providers list of '
                  '"{space_name}" equals "{number_of_providers}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_length_of_providers_list_of_space(selenium, browser_id, space_name,
                                             number_of_providers, oz_page):
    driver = selenium[browser_id]
    providers_list = oz_page(driver)['data'].providers_page.providers_list
    assert len(providers_list) == int(number_of_providers), \
        ('length of providers list of space "{}" is not equal {}'
         .format(space_name, number_of_providers))


@wt(parsers.parse('user of {browser_id} clicks Add support button '
                  'on providers page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_get_support_button_on_providers_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['data'].providers_page.add_support()


@wt(parsers.parse('user of {browser_id} sees {text} alert on providers page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def see_insufficient_privileges_label_on_providers_page(selenium, browser_id,
                                                        oz_page, text):
    driver = selenium[browser_id]
    item_text = (oz_page(driver)['data'].providers_page.get_support_page
                 .insufficient_privileges)
    assert item_text == text, f'found {item_text} alert instead of expected' \
                              f' {text}'


@wt(parsers.parse('user of {browser_id} clicks Deploy your own provider tab '
                  'on Add support page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_deploy_your_own_provider_tab_on_get_support_page(selenium, browser_id,
                                                           oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['data'].providers_page.get_support_page \
        .deploy_provider_modal()


@wt(parsers.parse('user of {browser_id} clicks Expose existing data set '
                  'tab on Add support page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_expose_existing_data_collection_tab_on_get_support_page(selenium,
                                                                  browser_id,
                                                                  oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['data'].providers_page.get_support_page \
        .expose_existing_data_modal()


@wt(parsers.parse('user of {browser_id} removes "{harvester_name}" harvester '
                  'from "{space_name}" space'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_harvester_from_harvesters_list(selenium, browser_id, oz_page,
                                          harvester_name, popups, modals,
                                          space_name, tmp_memory):
    modal_name = 'remove harvester from space'
    popup_name = 'Remove this harvester'

    driver = selenium[browser_id]
    harvesters_list = oz_page(driver)['data'].harvesters_page.harvesters_list
    harvesters_list[harvester_name].click_harvester_menu_button(driver)
    popups(driver).menu_popup_with_text.menu[popup_name]()
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    modals(driver).remove_modal.remove()


@wt(parsers.parse('user of {browser_id} clicks '
                  'Copy button on Add support page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_copy_button_on_request_support_page(selenium, browser_id, oz_page,
                                              displays, clipboard, tmp_memory):
    driver = selenium[browser_id]
    oz_page(driver)['data'].providers_page.get_support_page.copy()

    item = clipboard.paste(display=displays[browser_id])
    tmp_memory[browser_id]['mailbox']['token'] = item


@wt(parsers.parse('user of {browser_id} sees copy token and token '
                  'in support token text field are the same'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_copy_token_and_input_token_are_the_same(selenium, browser_id,
                                                   oz_page, tmp_memory):
    driver = selenium[browser_id]
    first_token = tmp_memory[browser_id]['mailbox']['token']
    second_token = oz_page(driver)['data'].providers_page.get_support_page \
        .token_textarea
    assert first_token == second_token, 'two tokens are not the same'


@wt(parsers.parse('user of {browser_id} sees that copied token is non-empty'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_copy_token_is_not_empty(selenium, browser_id, tmp_memory):
    token = tmp_memory[browser_id]['mailbox']['token']
    assert len(token) > 0, 'token is empty, while it should be non-empty'


@wt(parsers.parse('user of {browser_id1} generates space support token for '
                  'space "{space_name}" and sends it to user of {browser_id2}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def generate_and_send_support_token(selenium, browser_id1, space_name, oz_page,
                                    browser_id2, clipboard, displays,
                                    tmp_memory):
    page = oz_page(selenium[browser_id1])['data']
    page.spaces_header_list[space_name]()
    page.elements_list[space_name].providers()
    page.providers_page.add_support()
    copy_token(selenium, browser_id1, oz_page)
    item = clipboard.paste(display=displays[browser_id1])
    tmp_memory[browser_id2]['mailbox']['token'] = item


@wt(parsers.re('user of (?P<browser_id>.*) copies invitation token '
               'from Spaces page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_token(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['data'].providers_page.get_support_page.copy()


@wt(parsers.re('user of (?P<browser_id>.*) confirms create new space '
               'using (?P<option>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_create_new_space(selenium, browser_id, option, oz_page):
    if option == 'enter':
        press_enter_on_active_element(selenium, browser_id)
    else:
        create_new_space_by_click_on_create_new_space_button(selenium,
                                                             browser_id,
                                                             oz_page)


@wt(parsers.parse('user of {browser_id} sees "{tab_name}" '
                  'label of current page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_tab_name_label(selenium, browser_id, tab_name, oz_page):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    label = oz_page(driver)['data'].tab_name
    assert label.lower() == tab_name, f'User not on {tab_name} page'


@wt(parsers.parse('user of {browser_id} sees that opened space name is '
                  '"{space}"'))
def assert_opened_space_name(selenium, browser_id, space, oz_page):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    msg = f'{space} space view is not opened'
    assert oz_page(driver)['data'].elements_list[space].is_active(), msg


@wt(parsers.re('user of (?P<browser_id>.*) sees that (?P<tabs_list>.*) tabs? '
               'of "(?P<space_name>.*)" are enabled'))
@repeat_failed(WAIT_BACKEND*3)
def assert_tabs_of_space_enabled(selenium, browser_id, tabs_list, space_name,
                                 oz_page):
    page = oz_page(selenium[browser_id])['data']
    page.spaces_header_list[space_name]()
    space = page.elements_list[space_name]
    tabs = SPACE_TABS if tabs_list == "all" else _parse_tabs_list(tabs_list)

    for tab in tabs:
        assert space.is_element_enabled(tab), (
            f'Tab {tab} is not enabled for {space}'
        )


@wt(parsers.re('user of (?P<browser_id>.*) sees that (?P<tabs_list>.*) tabs? '
               'of "(?P<space_name>.*)" (are|is) disabled'))
@repeat_failed(WAIT_BACKEND*2)
def assert_tabs_of_space_disabled(selenium, browser_id, tabs_list, space_name,
                                  oz_page):
    page = oz_page(selenium[browser_id])['data']
    page.spaces_header_list[space_name]()
    space = page.elements_list[space_name]

    for tab in _parse_tabs_list(tabs_list):
        assert space.is_element_disabled(tab), (
            f'Tab {tab} is not disabled for {space}'
        )


@wt(parsers.parse('user of {browser_id} sees "{text}" error on spaces page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_error_detail_text_spaces(selenium, browser_id, oz_page, text):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    page = oz_page(driver)['data']
    assert text in page.error_header, f'page with text "{text}" not found'


@wt(parsers.parse('user of {browser_id} sees that provider "{provider1}" is '
                  'placed east of "{provider2}" on world map'))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_two_providers_places(selenium, browser_id, oz_page, hosts,
                               provider1, provider2):
    driver = selenium[browser_id]
    page = 'providers'
    current_page = getattr(oz_page(driver)['data'], _get_subpage_name(page))

    provider1_name = hosts[provider1]['name']
    provider2_name = hosts[provider2]['name']

    provider1_position = current_page.map.get_provider_horizontal_position(
        provider1_name, driver)
    provider2_position = current_page.map.get_provider_horizontal_position(
        provider2_name, driver)

    # the higher value of position the further on the east provider appears
    assert provider1_position > provider2_position, (f'Provider "{provider1}" '
                                                     f'appears west of provider'
                                                     f' "{provider2}"')


@wt(parsers.parse('user of {browser_id} writes "{text}" into '
                  'input box in space title sidebar item'))
def write_into_input_box_in_space_title_sidebar_item(selenium, browser_id,
                                                     text, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['data'].input_rename = text


@wt(parsers.parse('user of {browser_id} clicks on save icon in space title '
                  'sidebar item'))
def click_save_in_space_title_sidebar_item(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['data'].save_icon()
