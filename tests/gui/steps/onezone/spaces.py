"""This module contains gherkin steps to run acceptance tests featuring
spaces management in onezone web GUI.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.utils.utils import repeat_failed
from tests.utils.bdd_utils import wt, parsers
from tests.gui.utils.generic import transform
from tests.gui.steps.common.miscellaneous import press_enter_on_active_element
from selenium.webdriver import ActionChains


@wt(parsers.parse('user of {browser_id} clicks on Create space button '
                  'in spaces sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_new_space_on_spaces_on_left_sidebar_menu(selenium, browser_id,
                                                          oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['data'].create_space_button()


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


@wt(parsers.re('user of (?P<browser_id>.*?) clicks on '
               '(?P<option>Data|Providers|Groups|Tokens|Discovery|Clusters) '
               'in the main menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    oz_page(driver)[str(option).lower()]


@wt(parsers.re('user of (?P<browser_id>.*?) clicks "(?P<name>.*?)" '
               'on the (?P<option>spaces|groups|harvesters) list in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_element_on_lists_on_left_sidebar_menu(selenium, browser_id, option,
                                                name, oz_page):
    driver = selenium[browser_id]
    if option == 'harvesters':
        option = 'discovery'

    if option == 'spaces':
        option = 'data'
        oz_page(driver)[option].spaces_header_list[name]()
    else:
        oz_page(driver)[option].elements_list[name].click()


@wt(parsers.parse('user of {browser_id} writes "{space_name}" '
                  'into rename space text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_space_name_on_rename_space_input_on_overview_page(selenium, browser_id,
                                                           space_name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['data'].overview_page.info_tile.rename()
    oz_page(driver)[
        'data'].overview_page.info_tile.edit_name_box.value = space_name


@wt(parsers.parse('user of {browser_id} clicks on confirmation button '
                  'on overview page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def rename_space_by_click_on_confirmation_button_on_overview_page(selenium,
                                                                  browser_id,
                                                                  oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['data'].overview_page.info_tile.edit_name_box.confirm()


@wt(parsers.parse('user of {browser_id} clicks on cancel button '
                  'on overview page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_cancel_rename_button_on_overview_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['data'].overview_page.info_tile.edit_name_box.cancel()


@wt(parsers.re('user of (?P<browser_id>.*) clicks on '
               '"(?P<button>Leave space)" button '
               'in space menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_in_menu(selenium, browser_id, button, oz_page, popups):
    driver = selenium[browser_id]
    page = oz_page(driver)['data']
    page.menu_button()
    popups(driver).popover_menu.menu[button]()


@wt(parsers.re('user of (?P<browser_id>.*?) clicks on '
               '(?P<button_name>yes|no) button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_confirm_or_cancel_button_on_leave_space_page(selenium, browser_id,
                                                       button_name, modals):
    getattr(modals(selenium[browser_id]).leave_space, button_name).click()


@wt(parsers.parse('user of {browser_id} sees that "{space_name}" '
                  'has disappeared on the spaces list in the sidebar'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_space_has_disappeared_on_spaces(selenium, browser_id, space_name,
                                           oz_page):
    driver = selenium[browser_id]
    spaces = oz_page(driver)['data'].elements_list
    assert space_name not in spaces, 'space "{}" found'.format(space_name)


@wt(parsers.parse('user of {browser_id} sees {number} number of supporting '
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
    for prov in current_page.map.providers.items:
        ActionChains(driver).move_to_element(prov).perform()
        name = driver.find_element_by_css_selector(".tooltip-inner").text
        if name == provider_name:
            prov.click()
            return

    raise RuntimeError(f'provider {provider_name} was not found on the map')


@wt(parsers.re('user of (?P<browser_id>.*?) clicks the map on '
               '(?P<space_name>.*) space (?P<page>overview|providers) data '
               'page'))
def click_the_map_on_data_page(selenium, browser_id, oz_page, page,
                                    space_name):
    driver = selenium[browser_id]
    getattr(oz_page(driver)['data'], _get_subpage_name(page)).map()


@wt(parsers.re('user of (?P<browser_id>.*?) clicks '
               '(?P<option>Overview|Data|Shares|Transfers|Providers|Members) '
               'of "(?P<space_name>.*?)" in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                  space_name, option, oz_page):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    oz_page(driver)['data'].spaces_header_list[space_name].click()
    getattr(oz_page(driver)['data'].elements_list[space_name],
            transform(option)).click()


@wt(parsers.re('user of (?P<browser_id>.*) sees (?P<correct_number>.*) '
               'providers? on the map on (?P<space_name>.*) '
               'space (?P<page>.*) data page'))
def check_number_of_providers_on_the_map_on_data_page(selenium, browser_id,
                                                      correct_number,
                                                      space_name, page,
                                                      oz_page):
    if correct_number == 'no':
        correct_number = 0
    driver = selenium[browser_id]
    current_page = getattr(oz_page(driver)['data'], _get_subpage_name(page))
    number_providers = len(current_page.map.providers.items)
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


@wt(parsers.re('user of (?P<browser_id>.*) sees (?P<alert_text>.*) alert '
               'on providers page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def see_insufficient_permissions_alert_on_providers_page(selenium, browser_id,
                                                         oz_page, alert_text):
    driver = selenium[browser_id]

    forbidden_alert = (oz_page(driver)['data'].providers_page.get_support_page
                       .forbidden_alert.text)
    assert alert_text in forbidden_alert, ('alert with text "{}" not found'
                                           .format(alert_text))


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


@wt(parsers.parse(
    'user of {browser_id} clicks Copy button on Add support page'))
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


@wt(parsers.parse('user of {browser_id} sees non-empty copy token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_copy_token_is_not_empty(selenium, browser_id, tmp_memory):
    token = tmp_memory[browser_id]['mailbox']['token']
    assert len(token) > 0, 'token is empty, while it should be non-empty'


@wt(parsers.parse('user of {browser_id} sees "{space_name}" label '
                  'on overview page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_name_label_of_space_on_overview_page(selenium, browser_id,
                                                space_name, oz_page):
    driver = selenium[browser_id]
    assert oz_page(driver)[
               'data'].overview_page.space_name == space_name, \
        'space "{}" not found on overview page'.format(space_name)


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


@wt(parsers.re('user of (?P<browser_id>.*) confirms rename the space '
               'using (?P<option>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_rename_the_space(selenium, browser_id, option, oz_page):
    if option == 'enter':
        press_enter_on_active_element(selenium, browser_id)
    else:
        rename_space_by_click_on_confirmation_button_on_overview_page(selenium,
                                                                      browser_id,
                                                                      oz_page)


@wt(parsers.parse('user of {browser_id} sees "{tab_name}" '
                  'label of current page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_tab_name_label(selenium, browser_id, tab_name, oz_page):
    driver = selenium[browser_id]
    driver.switch_to.window(window_name=driver.window_handles[1])
    label = oz_page(selenium[browser_id])['data'].tab_name
    assert label.lower() == tab_name, f'User not on {tab_name} page'


@wt(parsers.parse('user of {browser_id} sees in the INFO section of Overview '
                  'page that number of shares is {number}'))
def assert_number_of_shares_on_overview_page(browser_id, selenium, oz_page,
                                             number: int):
    driver = selenium[browser_id]
    shares_count = int(
        oz_page(driver)['data'].overview_page.info_tile.shares_count)
    assert number == shares_count, (f'number of shares equals {shares_count},'
                                    ' not {number} as expected')
