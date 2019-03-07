"""This module contains gherkin steps to run acceptance tests featuring
spaces management in onezone web GUI.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import parsers
from tests.utils.acceptance_utils import wt
from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.utils import repeat_failed
from tests.gui.utils.generic import parse_seq, transform
from tests.gui.utils.common.modals import Modals as modals
from tests.gui.steps.common.miscellaneous import press_enter_on_active_element


@wt(parsers.parse('user of {browser_id} clicks on Create space button '
                  'in spaces sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_new_space_on_spaces_on_left_sidebar_menu(selenium, browser_id,
                                                          oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].create_space_button()


@wt(parsers.parse('user of {browser_id} writes "{space_name}" '
                  'into space name text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_space_name_on_input_on_create_new_space_page(selenium, browser_id,
                                                      space_name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].input_box.value = space_name


@wt(parsers.parse('user of {browser_id} clicks on Create new space button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_new_space_by_click_on_create_new_space_button(selenium, browser_id,
                                                         oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].input_box.confirm()


@wt(parsers.parse('user of {browser_id} creates space "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_new_space_on_onezone_page(selenium, browser_id, space_name, oz_page):
    page = oz_page(selenium[browser_id])['spaces']
    page.create_space_button()
    page.input_box.value = space_name
    page.input_box.confirm()


@wt(parsers.parse('user of {browser_id} sees that there is no supporting '
                  'provider "{provider_name}" for space named "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_no_provider_for_space(selenium, browser_id, provider_name,
                                 space_name, hosts, oz_page):
    page = oz_page(selenium[browser_id])['spaces']
    page.elements_list[space_name]()
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
    assert space_name in oz_page(driver)['spaces'].elements_list, \
        'space "{}" not found'.format(space_name)


@wt(parsers.re('user of (?P<browser_id>.*?) clicks on '
               '(?P<option>Data|Tokens|Spaces|Groups|Clusters) in the main menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)[str(option).lower()]


@wt(parsers.re('user of (?P<browser_id>.*?) clicks "(?P<name>.*?)" '
               'on the (?P<option>spaces|groups) list in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_space_on_spaces_on_left_sidebar_menu(selenium, browser_id, option,
                                               name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)[option].elements_list[name].click()


@wt(parsers.parse('user of {browser_id} writes "{space_name}" '
                  'into rename space text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_space_name_on_rename_space_input_on_overview_page(selenium, browser_id,
                                                           space_name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].overview_page.rename()
    oz_page(driver)['spaces'].overview_page.edit_name_box.value = space_name


@wt(parsers.parse('user of {browser_id} clicks on confirmation button '
                  'on overview page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def rename_space_by_click_on_confirmation_button_on_overview_page(selenium,
                                                                  browser_id,
                                                                  oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].overview_page.edit_name_box.confirm()


@wt(parsers.parse('user of {browser_id} clicks on cancel button '
                  'on overview page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_cancel_rename_button_on_overview_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].overview_page.edit_name_box.cancel()


@wt(parsers.re('user of (?P<browser_id>.*) clicks on '
               '"(?P<button>Leave space|Toggle default space)" button '
               'in space menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_in_menu(selenium, browser_id, button, oz_page):
    driver = selenium[browser_id]
    page = oz_page(driver)['spaces']
    page.menu_button()
    page.menu[button].click()


@wt(parsers.re('user of (?P<browser_id>.*?) clicks on '
               '(?P<button_name>yes|no) button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_confirm_or_cancel_button_on_leave_space_page(selenium, browser_id,
                                                       button_name):
    getattr(modals(selenium[browser_id]).leave_space, button_name).click()


@wt(parsers.parse('user of {browser_id} sees that "{space_name}" '
                  'has disappeared on the spaces list in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_space_has_disappeared_on_spaces(selenium, browser_id, space_name,
                                           oz_page):
    driver = selenium[browser_id]
    assert space_name not in oz_page(driver)['spaces'].elements_list, \
        'space "{}" found'.format(space_name)


@wt(parsers.parse('user of {browser_id} sees that home of "{space_name}" '
                  'has appeared in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_home_space_has_appeared_on_spaces_on_left_sidebar_menu(selenium,
                                                                  browser_id,
                                                                  space_name,
                                                                  oz_page):
    driver = selenium[browser_id]
    assert oz_page(driver)['spaces'].elements_list[space_name].is_home_icon(), \
        'home of space "{}" not found'.format(space_name)


@wt(parsers.parse('user of {browser_id} sees that home of "{space_name}" '
                  'has disappeared in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_home_space_has_disappeared_on_spaces_on_left_sidebar_menu(selenium,
                                                                     browser_id,
                                                                     space_name,
                                                                     oz_page):
    driver = selenium[browser_id]
    assert not oz_page(driver)['spaces'].elements_list[space_name].is_home_icon(), \
        'home of space "{}" found'.format(space_name)


@wt(parsers.parse('user of {browser_id} sees {number} number of supporting '
                  'providers of "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_number_of_supporting_providers_of_space(selenium, browser_id,
                                                   number, space_name, oz_page):
    driver = selenium[browser_id]
    assert (number == oz_page(driver)['spaces']
            .elements_list[space_name]
            .supporting_providers_number), \
        'number of supporting providers is not equal {}'.format(number)


@wt(parsers.parse('user of {browser_id} sees {number} size of '
                  'the "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_size_of_space_on_left_sidebar_menu(selenium, browser_id, number,
                                              space_name, oz_page):
    driver = selenium[browser_id]
    assert (number == oz_page(driver)['spaces']
            .elements_list[space_name]
            .support_size), ('size of space "{}" is not equal {}'
                             .format(space_name, number))


@wt(parsers.re(
    'user of (?P<browser_id>.*?) clicks (?P<option>Members|Overview|Providers) '
    'of "(?P<space_name>.*?)" in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_members_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                   space_name, option, oz_page):
    driver = selenium[browser_id]
    getattr(oz_page(driver)['spaces'].elements_list[space_name],
            transform(option)).click()


@wt(parsers.parse('user of {browser_id} clicks Get started in spaces sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_get_started_on_spaces_on_left_sidebar_menu(selenium, browser_id,
                                                     oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].get_started()


@wt(parsers.re('user of (?P<browser_id>.*?) clicks '
               '(?P<option>Create a space|join an existing space) '
               'on Welcome page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_on_welcome_page(selenium, browser_id, option, oz_page):
    driver = selenium[browser_id]
    getattr(oz_page(driver)['spaces'].welcome_page, transform(option)).click()


@wt(parsers.parse('user of {browser_id} writes "{token}" '
                  'into space token text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_token_to_input_on_join_to_a_space_page(selenium, browser_id,
                                                token, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].input_box.value = token


@wt(parsers.parse('user of {browser_id} sees that error popup has appeared'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_error_popup_has_appeared(selenium, browser_id):
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
    providers_list = oz_page(driver)['spaces'].providers_page.providers_list
    assert provider in providers_list, 'provider "{}" not found'.format(provider)


@wt(parsers.parse('user of {browser_id} sees that length of providers list '
                  'equals number of supporting providers of "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_length_of_providers_list(selenium, browser_id, space_name, oz_page):
    driver = selenium[browser_id]
    providers_list = oz_page(driver)['spaces'].providers_page.providers_list
    number_of_providers = int(oz_page(driver)['spaces']
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
    providers_list = oz_page(driver)['spaces'].providers_page.providers_list
    assert len(providers_list) == int(number_of_providers), \
        ('length of providers list of space "{}" is not equal {}'
         .format(space_name, number_of_providers))


@wt(parsers.parse('user of {browser_id} clicks Get support button '
                  'on providers page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_get_support_button_on_providers_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].providers_page.get_support()


@wt(parsers.parse('user of {browser_id} clicks Deploy your own provider tab '
                  'on get support page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_deploy_your_own_provider_tab_on_get_support_page(selenium, browser_id,
                                                           oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].providers_page.get_support_page \
        .deploy_provider_modal()


@wt(parsers.parse('user of {browser_id} clicks Expose existing data collection '
                  'tab on get support page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_expose_existing_data_collection_tab_on_get_support_page(selenium,
                                                                  browser_id,
                                                                  oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].providers_page.get_support_page \
        .expose_existing_data_modal()


@wt(parsers.parse(
    'user of {browser_id} clicks Copy button on Get support page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_copy_button_on_request_support_page(selenium, browser_id, oz_page,
                                              displays, clipboard, tmp_memory):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].providers_page.get_support_page.copy()

    item = clipboard.paste(display=displays[browser_id])
    tmp_memory[browser_id]['mailbox']['token'] = item


@wt(parsers.parse('user of {browser_id} clicks Generate another token '
                  'on Get support page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_generate_another_token_on_request_support_page(selenium, browser_id,
                                                         oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].providers_page.get_support_page \
        .generate_another_token()


@wt(parsers.parse('user of {browser_id} sees that another token is different '
                  'than first one'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_two_tokens_are_different(selenium, browser_id, oz_page, displays,
                                       clipboard, tmp_memory):
    driver = selenium[browser_id]
    first_token = tmp_memory[browser_id]['mailbox']['token']
    oz_page(driver)['spaces'].providers_page.get_support_page.copy()

    second_token = clipboard.paste(display=displays[browser_id])
    assert first_token != second_token, 'two tokens are the same'


@wt(parsers.parse('user of {browser_id} sees copy token and token '
                  'in support token text field are the same'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_copy_token_and_input_token_are_the_same(selenium, browser_id,
                                                      oz_page, tmp_memory):
    driver = selenium[browser_id]
    first_token = tmp_memory[browser_id]['mailbox']['token']
    second_token = oz_page(driver)['spaces'].providers_page.get_support_page \
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
    assert oz_page(driver)['spaces'].overview_page.space_name == space_name, \
        'space "{}" not found on overview page'.format(space_name)


@wt(parsers.parse('user of {browser_id1} generates space support token for '
                  'space "{space_name}" and sends it to user of {browser_id2}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def generate_and_send_support_token(selenium, browser_id1, space_name, oz_page,
                                    browser_id2, clipboard, displays,
                                    tmp_memory):
    page = oz_page(selenium[browser_id1])['spaces']
    page.elements_list[space_name]()
    page.elements_list[space_name].providers()
    page.providers_page.get_support()
    copy_token(selenium, browser_id1, oz_page)
    item = clipboard.paste(display=displays[browser_id1])
    tmp_memory[browser_id2]['mailbox']['token'] = item


@wt(parsers.re('user of (?P<browser_id>.*) copies invitation token '
               'from Spaces page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_token(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['spaces'].providers_page.get_support_page.copy()


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
