"""This module contains meta steps for common operations in Onezone
using web GUI
"""

from pytest_bdd import given, parsers

from itertools import izip_longest
from tests.gui.steps.common.browser_creation import \
    create_instances_of_webdriver
from tests.utils.acceptance_utils import wt
from tests.gui.steps.oneprovider.common import g_wait_for_op_session_to_start
from tests.gui.steps.onezone.providers import parse_seq
from tests.gui.steps.common.url import g_open_onedata_service_page
from tests.gui.steps.common.login import g_login_using_basic_auth
from tests.utils.acceptance_utils import list_parser
from tests.gui.utils.generic import repeat_failed
from tests.gui.conftest import WAIT_FRONTEND


@given(parsers.re('opened (?P<browser_id_list>.*) with (?P<user_list>.*) logged'
                  ' to (?P<host_list>.*) service'))
@repeat_failed(timeout=WAIT_FRONTEND)
def login_using_gui(host_list, selenium, driver, tmpdir, tmp_memory, xvfb,
                    driver_kwargs, driver_type, firefox_logging, displays,
                    firefox_path, screen_width, screen_height, hosts,
                    users, login_page, browser_id_list, user_list):
    create_instances_of_webdriver(selenium, driver, user_list, tmpdir,
                                  tmp_memory, driver_kwargs, driver_type,
                                  firefox_logging, firefox_path, xvfb,
                                  screen_width, screen_height, displays)
    g_open_onedata_service_page(selenium, user_list, host_list, hosts)

    for browser, user in zip(parse_seq(browser_id_list), parse_seq(user_list)):
        selenium[browser] = selenium[user]
        tmp_memory[browser] = tmp_memory[user]
        displays[browser] = displays[user]

    for user, host_name in zip(parse_seq(user_list),
                               parse_seq(host_list)):
        g_login_using_basic_auth(selenium, user, user, login_page, users)


def visit_op(selenium, browser_id, oz_page, provider_name):
    providers_panel = oz_page(selenium[browser_id])['providers']
    providers_panel[provider_name]()
    providers_panel.popover.visit_provider()


@given(parsers.re('opened (?P<providers_list>.*) Oneprovider view in web GUI by '
                  '(users? of )?(?P<browser_id_list>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND * 50)
def g_visit_op(selenium, oz_page, browser_id_list, providers_list, hosts):
    providers_list = list_parser(providers_list)
    for browser_id, provider in izip_longest(list_parser(browser_id_list),
                                             providers_list,
                                             fillvalue=providers_list[-1]):
        visit_op(selenium, browser_id, oz_page, hosts[provider]['name'])
    g_wait_for_op_session_to_start(selenium, browser_id_list)


@wt(parsers.re('users? of (?P<browser_id_list>.*) opened (?P<providers_list>.*) '
               'Oneprovider view in web GUI'))
@repeat_failed(timeout=WAIT_FRONTEND * 50)
def wt_visit_op(selenium, oz_page, browser_id_list, providers_list, hosts):
    providers_list = list_parser(providers_list)
    for browser_id, provider in izip_longest(list_parser(browser_id_list),
                                             providers_list,
                                             fillvalue=providers_list[-1]):
        visit_op(selenium, browser_id, oz_page, hosts[provider]['name'])
    g_wait_for_op_session_to_start(selenium, browser_id_list)

