"""This module contains gherkin steps to run acceptance tests featuring
providers management in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from tests.utils.acceptance_utils import *
from itertools import izip_longest

from pytest_bdd import parsers, given
from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.utils.generic import repeat_failed, parse_seq, transform


@when(parsers.parse('user of {browser_id} sees that provider popup for '
                    'provider named "{provider_name}" has appeared on '
                    'world map'))
@then(parsers.parse('user of {browser_id} sees that provider popup for '
                    'provider named "{provider_name}" has appeared on '
                    'world map'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_popup_for_provider_with_name_has_appeared_on_map(selenium, browser_id,
                                                            provider_name,
                                                            oz_page):
    driver = selenium[browser_id]
    err_msg = 'Popup displayed for provider named "{}" ' \
              'instead of "{}"'
    prov = oz_page(driver)['world map'].get_provider_with_displayed_popup()
    assert provider_name == prov.name, err_msg.format(prov.name, provider_name)


@when(parsers.parse('user of {browser_id} sees that provider popup for '
                    'provider "{provider}" has appeared on world map'))
@then(parsers.parse('user of {browser_id} sees that provider popup for '
                    'provider "{provider}" has appeared on world map'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_popup_for_provider_has_appeared_on_map(selenium, browser_id,
                                                  provider, oz_page, hosts):
    driver = selenium[browser_id]
    provider_name = hosts[provider]['name']
    err_msg = 'Popup displayed for provider named "{}" ' \
              'instead of "{}"'
    prov = oz_page(driver)['world map'].get_provider_with_displayed_popup()
    assert provider_name == prov.name, err_msg.format(prov.name, provider_name)


@when(parsers.parse('user of {browser_id} sees that hostname in displayed '
                    'provider popup matches that of "{host}" provider'))
@then(parsers.parse('user of {browser_id} sees that hostname in displayed '
                    'provider popup matches that of "{host}" provider'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_provider_hostname_matches_known_domain(selenium, browser_id,
                                                  host, oz_page, hosts):
    driver = selenium[browser_id]
    prov = oz_page(driver)['world map'].get_provider_with_displayed_popup()
    domain = hosts[host]['hostname']
    displayed_domain = prov.hostname
    assert displayed_domain == domain, \
        'displayed {} provider hostname instead ' \
        'of expected {}'.format(displayed_domain, domain)


@when(parsers.parse('user of {browser_id} sees that hostname in displayed '
                    'provider popup matches test hostname of provider '
                    '"{provider}"'))
@then(parsers.parse('user of {browser_id} sees that hostname in displayed '
                    'provider popup matches test hostname of provider '
                    '"{provider}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_provider_hostname_matches_test_hostname(selenium, browser_id,
                                                   provider, hosts, oz_page):
    driver = selenium[browser_id]
    prov = oz_page(driver)['world map'].get_provider_with_displayed_popup()
    expected_domain = "{}.test".format(hosts[provider]['hostname'])
    displayed_domain = prov.hostname
    assert displayed_domain == expected_domain, \
        'displayed {} provider hostname instead ' \
        'of expected {}'.format(displayed_domain, expected_domain)


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
    for browser_id, provider in izip_longest(browser_ids, providers,
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
    _click_on_btn_in_provider_popup(selenium[browser_id], btn, provider, oz_page,
                                    hosts)


@given(parsers.re('users? of (?P<browser_id_list>.*) clicked on the '
                  '"(?P<btn_name>.+?)" button in provider popup'))
def g_click_on_go_to_files_provider(selenium, browser_id_list, btn_name, oz_page):
    for browser_id in parse_seq(browser_id_list):
        driver = selenium[browser_id]
        popup = oz_page(driver)['world map'].get_provider_with_displayed_popup()
        getattr(popup, transform(btn_name)).click()


@when(parsers.re('users? of (?P<browser_id_list>.*) clicks on the '
                 '"(?P<btn_name>.+?)" button in provider popup'))
@then(parsers.re('users? of (?P<browser_id_list>.*) clicks on the '
                 '"(?P<btn_name>.+?)" button in provider popup'))
def wt_click_on_go_to_files_provider(selenium, browser_id_list, btn_name, oz_page):
    for browser_id in parse_seq(browser_id_list):
        driver = selenium[browser_id]
        popup = oz_page(driver)['world map'].get_provider_with_displayed_popup()
        getattr(popup, transform(btn_name)).click()


@when(parsers.parse(r'user of {browser_id} unsets provider named "{provider}" '
                    r'from home by clicking on home icon in that provider '
                    r'record in expanded "GO TO YOUR FILES" Onezone panel'))
@then(parsers.parse(r'user of {browser_id} unsets provider named "{provider}" '
                    r'from home by clicking on home icon in that provider '
                    r'record in expanded "GO TO YOUR FILES" Onezone panel'))
@repeat_failed(timeout=WAIT_BACKEND)
def unset_given_item_from_home_by_clicking_on_home_icon(selenium, browser_id,
                                                        provider_name, oz_page,
                                                        hosts):
    driver = selenium[browser_id]
    provider_name = hosts[provider_name]['name']
    provider = oz_page(driver)['go to your files'].providers[provider_name]
    provider.unset_from_home()
    assert not provider.is_home(), ('provider named "{}" is still set as home '
                                    'but it should not'.format(provider))


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
@when(parsers.re(r'user of (?P<browser_id>.+?) sees that provider popup next to '
                 r'(?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|'
                 r'\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) '
                 r'provider circle on Onezone world map has disappeared'))
@then(parsers.re(r'user of (?P<browser_id>.+?) sees that provider popup next to '
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


@when(parsers.parse('user of {browser_id} clicks on Onezone world map'))
@then(parsers.parse('user of {browser_id} clicks on Onezone world map'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_world_map(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['world map'].click()


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
    for browser_id, provider in izip_longest(browser_ids, providers,
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
    assert count == 0, 'Providers count is {} instead of expected 0'.format(count)


@when(parsers.parse('user of {browser_id} sees that provider "{provider}" '
                    'in expanded "GO TO YOUR FILES" Onezone panel is working'))
@then(parsers.parse('user of {browser_id} sees that provider "{provider}" '
                    'in expanded "GO TO YOUR FILES" Onezone panel is working'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_provider_working_in_oz_panel(selenium, browser_id,
                                        provider, oz_page, hosts):
    driver = selenium[browser_id]
    provider = hosts[provider]['name']
    provider_record = oz_page(driver)['go to your files'].providers[provider]
    assert provider_record.is_working(), ('provider icon in GO TO YOUR FILES '
                                          'oz panel for "{}" is not green'
                                          ''.format(provider))


@when(parsers.parse('user of {browser_id} sees that provider named "{provider}" '
                    'in expanded "GO TO YOUR FILES" Onezone panel is not working'))
@then(parsers.parse('user of {browser_id} sees that provider named "{provider}" '
                    'in expanded "GO TO YOUR FILES" Onezone panel is not working'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_provider_not_working_in_oz_panel(selenium, browser_id,
                                            provider, oz_page, hosts):
    driver = selenium[browser_id]
    provider = hosts[provider]['name']
    provider_record = oz_page(driver)['go to your files'].providers[provider]
    assert provider_record.is_not_working(), ('provider icon in GO TO YOUR FILES '
                                              'oz panel for "{}" is not gray'
                                              ''.format(provider))
