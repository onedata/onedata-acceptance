"""This module contains gherkin steps to run acceptance tests featuring
providers management in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from itertools import zip_longest

from pytest_bdd import parsers, given

from tests.gui.steps.common.notifies import notify_visible_with_text
from tests.gui.steps.onepanel.spaces import (
    wt_clicks_on_understand_risk_in_cease_support_modal,
    wt_clicks_on_btn_in_cease_support_modal)
from tests.utils.acceptance_utils import *
from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.utils import repeat_failed


@when(parsers.parse('user of {browser_id} sees that provider popup for '
                    'provider named "{provider_name}" has appeared on '
                    'world map'))
@then(parsers.parse('user of {browser_id} sees that provider popup for '
                    'provider named "{provider_name}" has appeared on '
                    'world map'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_popup_for_provider_with_name_has_appeared_on_map(selenium,
                                                            browser_id,
                                                            provider_name,
                                                            modals):
    driver = selenium[browser_id]
    err_msg = 'Popup displayed for provider named "{}" ' \
              'instead of "{}"'
    prov = modals(driver).provider_popover.provider_name
    assert provider_name == prov, err_msg.format(prov, provider_name)


@when(parsers.parse('user of {browser_id} sees that provider popup for '
                    'provider "{provider}" has appeared on world map'))
@then(parsers.parse('user of {browser_id} sees that provider popup for '
                    'provider "{provider}" has appeared on world map'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_popup_for_provider_has_appeared_on_map(selenium, browser_id,
                                                  provider, hosts, modals):
    driver = selenium[browser_id]
    err_msg = 'Popup displayed for provider named "{}" ' \
              'instead of "{}"'
    prov = modals(driver).provider_popover.provider_name
    provider_name = hosts[provider]['name']
    assert provider_name == prov, err_msg.format(prov, provider_name)


@when(parsers.parse('user of {browser_id} sees that hostname in displayed '
                    'provider popup matches that of "{host}" provider'))
@then(parsers.parse('user of {browser_id} sees that hostname in displayed '
                    'provider popup matches that of "{host}" provider'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_provider_hostname_matches_known_domain(selenium, browser_id,
                                                  host, hosts, modals):
    driver = selenium[browser_id]
    displayed_domain = modals(driver).provider_popover.provider_hostname
    domain = hosts[host]['hostname']
    assert displayed_domain == domain, \
        ('displayed {} provider hostname instead of expected {}'
         .format(displayed_domain, domain))


@when(parsers.parse('user of {browser_id} sees that hostname in displayed '
                    'provider popup matches test hostname of provider '
                    '"{provider}"'))
@then(parsers.parse('user of {browser_id} sees that hostname in displayed '
                    'provider popup matches test hostname of provider '
                    '"{provider}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_provider_hostname_matches_test_hostname(selenium, browser_id,
                                                   provider, hosts, oz_page,
                                                   displays, clipboard, modals):
    driver = selenium[browser_id]
    expected_domain = "{}.test".format(hosts[provider]['hostname'])
    page = oz_page(driver)['providers']
    page.elements_list[0]()
    _click_copy_hostname(driver, modals)
    displayed_domain = clipboard.paste(display=displays[browser_id])
    assert displayed_domain == expected_domain, \
        'displayed {} provider hostname instead ' \
        'of expected {}'.format(displayed_domain, expected_domain)


@repeat_failed(timeout=WAIT_FRONTEND)
def _click_copy_hostname(driver, modals):
    modals(driver).provider_popover.copy_hostname()


def _click_on_btn_in_provider_popup(driver, btn, provider, oz_page, hosts):
    err_msg = 'Popup displayed for provider named "{}" ' \
              'instead of "{}"'
    provider = hosts[provider]['name']
    prov = oz_page(driver)['world map'].get_provider_with_displayed_popup()
    assert provider == prov.name, err_msg.format(prov.name, provider)
    getattr(prov, transform(btn)).click()


@given(parsers.re(r'users? of (?P<browser_id_list>.+?) clicked on the '
                  r'"(?P<btn>Go to your files|copy hostname)" button in '
                  r'"(?P<provider_list>.+?)" provider\'s popup displayed '
                  r'on world map'))
@repeat_failed(timeout=WAIT_BACKEND)
def g_click_on_btn_in_provider_popup(selenium, browser_id_list, btn,
                                     provider_list, oz_page, hosts):
    browser_ids = parse_seq(browser_id_list)
    providers = parse_seq(provider_list)
    for browser_id, provider in zip_longest(browser_ids, providers,
                                            fillvalue=providers[-1]):
        _click_on_btn_in_provider_popup(selenium[browser_id], btn,
                                        provider, oz_page, hosts)


@when(parsers.re(r'user of (?P<browser_id>.+?) clicks on the '
                 r'"(?P<btn>Go to your files|copy hostname)" button in '
                 r'"(?P<provider>.+?)" provider\'s popup displayed on world map'))
@then(parsers.re(r'user of (?P<browser_id>.+?) clicks on the '
                 r'"(?P<btn>Go to your files|copy hostname)" button in '
                 r'"(?P<provider>.+?)" provider\'s popup displayed on world map'))
@repeat_failed(timeout=WAIT_BACKEND)
def wt_click_on_btn_in_provider_popup(selenium, browser_id, btn,
                                      provider, oz_page, hosts):
    _click_on_btn_in_provider_popup(selenium[browser_id], btn, provider,
                                    oz_page,
                                    hosts)


@given(parsers.re('users? of (?P<browser_id_list>.*) clicked on the '
                  '"(?P<btn_name>.+?)" button in provider popup'))
def g_click_on_go_to_files_provider(selenium, browser_id_list, btn_name,
                                    oz_page):
    for browser_id in parse_seq(browser_id_list):
        driver = selenium[browser_id]
        popup = oz_page(driver)['world map'].get_provider_with_displayed_popup()
        getattr(popup, transform(btn_name)).click()


@when(parsers.re('users? of (?P<browser_id_list>.*) clicks on the '
                 '"(?P<btn_name>.+?)" button in provider popup'))
@then(parsers.re('users? of (?P<browser_id_list>.*) clicks on the '
                 '"(?P<btn_name>.+?)" button in provider popup'))
def wt_click_on_go_to_files_provider(selenium, browser_id_list, btn_name,
                                     oz_page):
    for browser_id in parse_seq(browser_id_list):
        driver = selenium[browser_id]
        popup = oz_page(driver)['world map'].get_provider_with_displayed_popup()
        getattr(popup, transform(btn_name)).click()


@when(parsers.re(r'user of (?P<browser_id>.+?) sees that there is no '
                 r'displayed provider popup next to '
                 r'(?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|'
                 r'\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) '
                 r'provider circle on Onezone world map'))
@then(parsers.re(r'user of (?P<browser_id>.+?) sees that there is no '
                 r'displayed provider popup next to '
                 r'(?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|'
                 r'\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) '
                 r'provider circle on Onezone world map'))
@when(
    parsers.re(r'user of (?P<browser_id>.+?) sees that provider popup next to '
               r'(?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|'
               r'\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) '
               r'provider circle on Onezone world map has disappeared'))
@then(
    parsers.re(r'user of (?P<browser_id>.+?) sees that provider popup next to '
               r'(?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|'
               r'\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) '
               r'provider circle on Onezone world map has disappeared'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_no_provider_popup_next_to_provider_circle(selenium, browser_id,
                                                     ordinal, oz_page):
    driver = selenium[browser_id]
    prov_circle = oz_page(driver)['world map'].providers[int(ordinal[:-2]) - 1]
    assert not prov_circle.is_displayed(), ('provider popup for {} circle is '
                                            'displayed while it should not be'
                                            ''.format(ordinal))


@wt(parsers.re(r'user of (?P<browser_id>.+?) does not see provider popover '
               r'on Onezone world map'))
def assert_no_provider_popup_on_world_map(selenium, browser_id, modals):
    driver = selenium[browser_id]
    try:
        modals(driver).provider_popover
    except RuntimeError:
        pass
    else:
        raise RuntimeError('found provider popover on world map')


@when(parsers.re(r'user of (?P<browser_id>.+?) clicks on '
                 r'(?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|'
                 r'\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) '
                 r'provider circle on Onezone world map'))
@then(parsers.re(r'user of (?P<browser_id>.+?) clicks on '
                 r'(?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|'
                 r'\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) '
                 r'provider circle on Onezone world map'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_provider_circle(selenium, browser_id, ordinal, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['world map'].providers[int(ordinal[:-2]) - 1].click()


@wt(parsers.re(r'user of (?P<browser_id>.+?) clicks on the other provider '
               r'circle on Onezone world map'))
def click_other_provider_icons(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['providers'].icons[0].icon()


@when(parsers.re(r'user of (?P<browser_id>.+?) sees that provider popup has '
                 r'appeared next to (?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|'
                 r'\d*?11th|\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|'
                 r'\d*?[^1]3rd) provider circle on Onezone world map'))
@then(parsers.re(r'user of (?P<browser_id>.+?) sees that provider popup has '
                 r'appeared next to (?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|'
                 r'\d*?11th|\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|'
                 r'\d*?[^1]3rd) provider circle on Onezone world map'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_provider_popup_next_to_provider_circle(selenium, browser_id,
                                                  ordinal, oz_page):
    driver = selenium[browser_id]
    prov_circle = oz_page(driver)['world map'].providers[int(ordinal[:-2]) - 1]
    assert prov_circle.is_displayed(), ('provider popup for {} circle is not '
                                        'displayed while it should be'
                                        ''.format(ordinal))


@wt(parsers.parse('user of {browser_id} clicks on Onezone world map'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_world_map(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['providers'].map_point.click()


@when(parsers.parse('user of {browser_id} sees that the list of spaces '
                    'in provider popup and in expanded "GO TO YOUR FILES" '
                    'Onezone panel are the same for provider named "{provider}"'))
@then(parsers.parse('user of {browser_id} sees that the list of spaces '
                    'in provider popup and in expanded "GO TO YOUR FILES" '
                    'Onezone panel are the same for provider named "{provider}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_consistent_list_of_spaces_for_provider(selenium, browser_id,
                                                  provider, oz_page, hosts):
    driver = selenium[browser_id]
    provider = hosts[provider]['name']
    provider_record_spaces = {(space.name, space.is_home())
                              for space in (oz_page(driver)['go to your files']
                                            .providers[provider]
                                            .spaces)}
    provider_popup_spaces = {(space.name, space.is_home())
                             for space in (oz_page(driver)['world map']
                                           .get_provider_with_displayed_popup()
                                           .spaces)}
    assert provider_record_spaces == provider_popup_spaces, \
        ('spaces (space_name, is_home) displayed in "{}" provider record in '
         'GO TO YOUR FILES panel: {} does not match those displayed in '
         'provider popup: {}'.format(provider, provider_record_spaces,
                                     provider_popup_spaces))


@given(parsers.re(r'users? of (?P<browser_id_list>.*?) clicked on '
                  r'(?P<providers>.*?) provider in expanded '
                  r'"GO TO YOUR FILES" Onezone panel'))
@repeat_failed(timeout=WAIT_BACKEND)
def g_click_on_provider_in_go_to_your_files_oz_panel(selenium, browser_id_list,
                                                     providers, oz_page,
                                                     hosts):
    browser_ids = parse_seq(browser_id_list)
    providers = parse_seq(providers)
    for browser_id, provider in zip_longest(browser_ids, providers,
                                            fillvalue=providers[-1]):
        provider_name = hosts[provider]['name']
        (oz_page(selenium[browser_id])['go to your files']
         .providers[provider_name]
         .click())


@when(parsers.parse('user of {browser_id} clicks on "{provider}" provider '
                    'in expanded "GO TO YOUR FILES" Onezone panel'))
@then(parsers.parse('user of {browser_id} clicks on "{provider}" provider '
                    'in expanded "GO TO YOUR FILES" Onezone panel'))
@repeat_failed(timeout=WAIT_BACKEND)
def wt_click_on_provider_in_go_to_your_files_oz_panel(selenium, browser_id,
                                                      provider, oz_page, hosts):
    provider = hosts[provider]['name']
    (oz_page(selenium[browser_id])['go to your files']
     .providers[provider]
     .click())


@wt(parsers.parse('user of {browser_id} clicks on provider named '
                  '"{provider}" in expanded "GO TO YOUR FILES" Onezone '
                  'panel'))
@repeat_failed(timeout=WAIT_BACKEND)
def wt_click_on_provider_with_name_in_go_to_your_files_oz_panel(selenium,
                                                                browser_id,
                                                                provider,
                                                                oz_page):
    (oz_page(selenium[browser_id])['go to your files']
     .providers[provider]
     .click())


@when(parsers.parse('user of {browser_id} sees that there is no provider '
                    'in "GO TO YOUR FILES" Onezone panel'))
@then(parsers.parse('user of {browser_id} sees that there is no provider '
                    'in "GO TO YOUR FILES" Onezone panel'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_list_of_providers_is_empty(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    count = oz_page(driver)['go to your files'].providers.count()
    assert count == 0, 'Providers count is {} instead of expected 0'.format(
        count)


@when(parsers.parse('user of {browser_id} sees that provider "{provider}" '
                    'in Onezone is working'))
@then(parsers.parse('user of {browser_id} sees that provider "{provider}" '
                    'in Onezone is working'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_provider_working_in_oz_panel(selenium, browser_id,
                                        provider, oz_page, hosts):
    driver = selenium[browser_id]
    provider = hosts[provider]['name']
    page = oz_page(driver)['providers']
    try:
        provider_record = page.elements_list[provider]
        provider_record.click()
    except RuntimeError:
        assert False, 'no provider "{}" found on providers list'.format(
            provider)
    else:
        pass
        assert page.is_working(), ('provider icon in Onezone for "{}" '
                                   'is not green'.format(provider))


@when(
    parsers.parse('user of {browser_id} sees that provider named "{provider}" '
                  'in expanded "GO TO YOUR FILES" Onezone panel is not working'))
@then(
    parsers.parse('user of {browser_id} sees that provider named "{provider}" '
                  'in expanded "GO TO YOUR FILES" Onezone panel is not working'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_provider_not_working_in_oz_panel(selenium, browser_id,
                                            provider, oz_page, hosts):
    driver = selenium[browser_id]
    provider = hosts[provider]['name']
    provider_record = oz_page(driver)['go to your files'].providers[provider]
    assert provider_record.is_not_working(), (
        'provider icon in GO TO YOUR FILES '
        'oz panel for "{}" is not gray'
        ''.format(provider))


def click_on_provider_in_providers_sidebar_with_provider_name(selenium,
                                                              browser_id,
                                                              oz_page,
                                                              provider_name):
    driver = selenium[browser_id]
    oz_page(driver)['providers'].elements_list[provider_name]()


@wt(parsers.parse('user of {browser_id} clicks on provider "{provider}" '
                  'in providers sidebar'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_provider_in_data_sidebar(selenium, browser_id, oz_page,
                                      provider, hosts):
    provider = hosts[provider]['name']
    click_on_provider_in_providers_sidebar_with_provider_name(selenium,
                                                              browser_id,
                                                              oz_page, provider)


@wt(parsers.parse('user of {browser_id} sees that "{provider}" provider is not '
                  'in providers list in data sidebar'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_provider_is_not_in_providers_list_in_data_sidebar(selenium,
                                                             browser_id,
                                                             oz_page, provider,
                                                             hosts):
    driver = selenium[browser_id]
    provider = hosts[provider]['name']
    providers_list = oz_page(driver)['providers'].elements_list
    assert provider not in providers_list, ('{} is in providers list '
                                            'in data sidebar'.format(provider))


@wt(parsers.re('user of (?P<browser_id>.+?) clicks on '
               '(?P<option>Visit provider|Toggle home provider) button '
               'on provider popover'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_visit_provider_in_provider_popover(selenium, browser_id, option,
                                                modals):
    driver = selenium[browser_id]
    getattr(modals(driver).provider_popover, transform(option)).click()


@wt(parsers.parse('user of {browser_id} sees "{space_name}" is '
                  'on the spaces list on provider popover'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_space_is_in_spaces_list_in_provider_popover(selenium, browser_id,
                                                       space_name, modals):
    driver = selenium[browser_id]
    spaces_list = modals(driver).provider_popover.spaces_list
    assert space_name in spaces_list


@wt(parsers.parse('user of {browser_id} sees that home of "{provider}" has '
                  'appeared in the data sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_home_space_has_appeared_on_provider_on_left_sidebar_menu(selenium,
                                                                    browser_id,
                                                                    provider,
                                                                    oz_page,
                                                                    hosts):
    driver = selenium[browser_id]
    provider = hosts[provider]['name']
    assert oz_page(driver)['providers'].elements_list[provider].is_home_icon(), \
        'home of provider "{}" not found'.format(provider)


@wt(parsers.parse('user of {browser_id} sees that spaces counter for '
                  '"{provider}" provider displays {number} in data sidebar'))
def assert_number_of_supported_spaces_in_data_sidebar(selenium, browser_id,
                                                      oz_page, provider,
                                                      number, hosts):
    driver = selenium[browser_id]
    provider = hosts[provider]['name']
    supported_spaces_number = (oz_page(driver)['providers']
                               .elements_list[provider]
                               .supported_spaces_number)
    assert number == supported_spaces_number, ('number of supported spaces '
                                               'is not equal {}'.format(number))


@wt(parsers.parse('user of {browser_id} sees that length of spaces list on '
                  'provider popover is {number}'))
def assert_len_of_spaces_list_in_provider_popover(selenium, browser_id,
                                                  number, modals):
    driver = selenium[browser_id]
    spaces_list = modals(driver).provider_popover.spaces_list
    assert int(number) == len(spaces_list), ('number of supported spaces '
                                             'is not equal {}'.format(number))


def click_on_menu_button_of_provider_on_providers_list(driver, provider_name,
                                                       oz_page):
    oz_page(driver)['data'].providers_page.providers_list[
        provider_name].menu_button()


def click_on_cease_support_in_menu_of_provider_on_providers_list(driver,
                                                                 popups):
    popups(driver).popover_menu.cease_support_from_providers_list_menu()


@wt(parsers.parse('user of {browser_id} waits until provider "{provider_name}" '
                  'goes offline on providers map'))
def wait_until_provider_goes_offline(selenium, browser_id, oz_page,
                                     hosts, provider_name):
    driver = selenium[browser_id]
    provider = hosts[provider_name]['name']
    page = oz_page(driver)['providers']
    provider_record = page.elements_list[provider]
    provider_record.click()
    while page.is_working():
        pass
