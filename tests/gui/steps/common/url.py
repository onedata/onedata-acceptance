"""This module contains gherkin steps to run acceptance tests featuring
url handling.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import re

from pytest_bdd import given, when, then, parsers
from tests.utils.acceptance_utils import wt
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support.expected_conditions import staleness_of

from tests.gui.utils.generic import parse_seq, parse_url
from tests.utils.utils import repeat_failed
from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND


def open_onedata_service_page(selenium, browser_id_list, hosts_list, hosts):
    """ hosts_list may contains:
            onezone,
            onezone zone panel,
            oneprovider-[0-9] provider panel,
            node[0-9] of oneprovider-[0-9] provider panel,
            emergency interface of Onepanel
    """
    for browser_id, host in zip(parse_seq(browser_id_list),
                                parse_seq(hosts_list)):
        driver = selenium[browser_id]
        if host == 'emergency interface of Onepanel':
            host = 'oneprovider-1 provider panel'
        host = host.lower().split()

        if 'node' in host[0]:
            node_number = int(host[0][-1:])
            host = host[2:]
        else:
            node_number = ''

        alias, service = host[0], '_'.join(host[1:])
        if 'panel' in service:
            hostname = hosts[alias]['panel']['hostname']

            if node_number != '':
                driver.get('https://{}-{}.{}'.format(hostname.split('.')[0],
                                                     node_number, hostname))
            else:
                driver.get('https://{}'.format(hostname))
        else:
            driver.get('https://{}'.format(hosts[alias]['hostname']))


@given(parsers.parse("user of {browser_id_list} opened {hosts_list} page"))
@given(parsers.parse("users of {browser_id_list} opened {hosts_list} page"))
def g_open_onedata_service_page(selenium, browser_id_list, hosts_list, hosts):
    open_onedata_service_page(selenium, browser_id_list, hosts_list, hosts)


@wt(parsers.re('users? of (?P<browser_id_list>.+) opens '
               '(?P<hosts_list>.+) page'))
def wt_open_onedata_service_page(selenium, browser_id_list, hosts_list, hosts):
    open_onedata_service_page(selenium, browser_id_list, hosts_list, hosts)


@wt(parsers.re('user of (?P<browser_id>.+) should be '
               'redirected to (?P<page>.+) page'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_being_redirected_to_page(page, selenium, browser_id):
    driver = selenium[browser_id]
    curr_page = re.match(r'https?://.*?(/#)?(/.*)',
                         driver.current_url).group(2)
    assert curr_page == page, ('currently on {} page instead of expected '
                               '{}'.format(curr_page, page))


@wt(parsers.re(r'user of (?P<browser_id>.+) changes '
               r'the relative URL to (?P<path>.+)'))
def change_relative_url(selenium, browser_id, path):
    driver = selenium[browser_id]
    driver.get(parse_url(driver.current_url).group('base_url') + path)


@wt(parsers.re(r'user of (?P<browser_id>.*?) changes '
               r'application path to plain (?P<path>.+)'))
def change_application_path(selenium, browser_id, path):
    driver = selenium[browser_id]
    driver.get(parse_url(driver.current_url).group('base_url') + '/#' + path)


@wt(parsers.re('user of (?P<browser_id>.+?) sees that '
               '(?:url|URL) matches: (?P<path>.+)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def is_url_matching(selenium, browser_id, path):
    driver = selenium[browser_id]
    regexp = r'{}$'.format(path.replace('\\', '\\\\'))
    err_msg = r'expected url: {} does not match current one: {{}}'.format(path)

    @repeat_failed(timeout=WAIT_BACKEND)
    def assert_url_match(d, regex, msg):
        curr_url = d.current_url
        assert re.match(regex, curr_url), msg.format(curr_url)

    assert_url_match(driver, regexp, err_msg)


def _open_url(selenium, browser_id, url):
    driver = selenium[browser_id]
    old_page = driver.find_element_by_css_selector('html')
    driver.get(url)

    Wait(driver, WAIT_BACKEND).until(
        staleness_of(old_page),
        message='waiting for page {:s} to load'.format(url)
    )


@wt(parsers.re('user of (?P<browser_id>.+?) opens received (?:url|URL)'))
def open_received_url_with_base_url(selenium, browser_id, tmp_memory, base_url):
    url = tmp_memory[browser_id]['mailbox']['url']
    url = url.replace(parse_url(url).group('base_url'), base_url, 1)

    _open_url(selenium, browser_id, url)


@wt(parsers.re('user of (?P<browser_id>.+?) opens (?:url|URL) received from '
               'user of (?P<browser_id2>.+?)'))
def open_exactly_received_url(selenium, browser_id, tmp_memory):
    url = tmp_memory[browser_id]['mailbox']['url']

    _open_url(selenium, browser_id, url)


@wt(parsers.re(r'user of (?P<browser_id>.*?) changes webapp path to '
               r'"?(?P<path>.+?)"? concatenated with copied item'))
def change_app_path_with_copied_item(selenium, browser_id, path,
                                     displays, clipboard):
    driver = selenium[browser_id]
    base_url = parse_url(driver.current_url).group('base_url')
    item = clipboard.paste(display=displays[browser_id])
    url = '{base_url}{path}/{item}'.format(base_url=base_url,
                                           path=path, item=item)
    # We use javascript instead of driver.get because of chromedriver being
    # unable to determine whether page has been loaded
    driver.execute_script('window.location = \'{}\''.format(url))


@wt(parsers.re(r'user of (?P<browser_id>.*?) changes webapp path to '
               r'"?(?P<path>.+?)"? concatenated with received (?P<item>.*)'))
def change_app_path_with_recv_item(selenium, browser_id, path,
                                   tmp_memory, item):
    driver = selenium[browser_id]
    base_url = parse_url(driver.current_url).group('base_url')
    item = tmp_memory[browser_id]['mailbox'][item.lower()]
    url = '{base_url}{path}/{item}'.format(base_url=base_url,
                                           path=path, item=item)
    # We use javascript instead of driver.get because of chromedriver being
    # unable to determine whether page has been loaded
    driver.execute_script('window.location = \'{}\''.format(url))


@wt(parsers.parse('user of {browser_id} copies url '
                  'from browser\'s location bar'))
def copy_site_url(selenium, browser_id, displays, clipboard):
    driver = selenium[browser_id]
    clipboard.copy(driver.current_url, display=displays[browser_id])


@wt(parsers.parse('user of {browser_id} opens copied URL '
                  'in browser\'s location bar'))
def open_site_url(selenium, browser_id, displays, clipboard):
    driver = selenium[browser_id]
    url = clipboard.paste(display=displays[browser_id])
    # We use javascript instead of driver.get because of chromedriver being
    # unable to determine whether page has been loaded
    driver.execute_script('window.location = \'{}\''.format(url))


@wt(parsers.parse('user of {browser_id} copies a first '
                  'resource {item} from URL'))
def cp_part_of_url(selenium, browser_id, item, displays, clipboard):
    driver = selenium[browser_id]
    clipboard.copy(parse_url(driver.current_url).group(item.lower()),
                   display=displays[browser_id])


@wt(parsers.parse('using web GUI, {browser_id_list} refreshes site'))
@wt(parsers.re('users? of (?P<browser_id_list>.*?) refreshes site'))
def refresh_site(selenium, browser_id_list):
    for browser_id in parse_seq(browser_id_list):
        selenium[browser_id].refresh()


@wt(parsers.parse('user of {browser_id} refreshes webapp'))
@repeat_failed(timeout=WAIT_FRONTEND, exceptions=AttributeError)
def refresh_webapp(selenium, browser_id):
    driver = selenium[browser_id]
    driver.get(parse_url(driver.current_url).group('base_url'))
