"""This module contains gherkin steps to run acceptance tests featuring
login page in web GUI.
"""

__author__ = "Bartosz Walkowicz, Michal Stanisz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


import time

from pytest_bdd import given, parsers
from tests.utils.utils import repeat_failed
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.acceptance_utils import wt
from tests.gui.steps.common.notifies import notify_visible_with_text


def _login_using_basic_auth(login_page, username, password):
    login_page.username = username
    login_page.password = password
    login_page.sign_in()


def _login_using_passphrase(login_page, password):
    login_page.passphrase = password
    login_page.sign_in()


@wt(parsers.re('user of (?P<browser_id>.*) clicks Log in to emergency '
               'interface in Onepanel login page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_log_in_to_emergency_interface(selenium, browser_id, login_page):
    login_page(selenium[browser_id]).log_in_to_emergency_interface()


def _login_to_service(selenium, browser_id_list, user_id_list, service_list,
                      login_page, users):
    for browser_id, username, service in zip(parse_seq(browser_id_list),
                                             parse_seq(user_id_list),
                                             parse_seq(service_list)):
        driver = selenium[browser_id]

        if 'emergency interface' in service:
            click_log_in_to_emergency_interface(selenium, browser_id, login_page)
            time.sleep(1)
            _login_using_passphrase(login_page(driver),
                                    users[username].password)
        else:
            _login_using_basic_auth(login_page(driver), username,
                                    users[username].password)
        notify_visible_with_text(selenium, browser_id, 'info',
                                 'Authentication succeeded!')


@given(parsers.re('users? of (?P<browser_id_list>.*) logged '
                  'as (?P<user_id_list>.*) to (?P<service_list>.*) service'))
@repeat_failed(timeout=WAIT_FRONTEND)
def g_login_using_basic_auth(selenium, browser_id_list, user_id_list,
                             login_page, users, service_list):
    _login_to_service(selenium, browser_id_list, user_id_list, service_list,
                      login_page, users)


@wt(parsers.re('users? of (?P<browser_id_list>.*) logs? '
               'as (?P<user_id_list>.*) to (?P<service_list>.*) service'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_login_using_basic_auth(selenium, browser_id_list, user_id_list,
                              login_page, users, service_list):
    _login_to_service(selenium, browser_id_list, user_id_list, service_list,
                      login_page, users)


@wt(parsers.re(r'user of (?P<browser_id>.*?) types "(?P<text>.*?)" to '
               r'(?P<in_box>Username|Password|Passphrase) input '
               r'in (Onepanel|Onezone) login form'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_enter_text_to_field_in_login_form(selenium, browser_id, in_box,
                                         text, login_page):
    setattr(login_page(selenium[browser_id]),
            transform(in_box), text)


@wt(parsers.re('user of (?P<browser_id>.*) presses Sign in button '
               'in (Onepanel|Onezone) login page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_press_sign_in_btn_on_login_page(selenium, browser_id, login_page):
    login_page(selenium[browser_id]).sign_in()


@wt(parsers.re('user of (?P<browser_id>.*) sees that he successfully '
               'logged in (?P<service>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_successful_login(selenium, browser_id, onepage, service):
    logged_in_service = onepage(selenium[browser_id]).service
    assert service.lower() in logged_in_service.lower(), \
        'logged in {} instead of {}'.format(logged_in_service, service)


@wt(parsers.re('user of (?P<browser_id>.*) sees that he was logged out '
               'from (Onepanel|Onezone)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_login_page(selenium, browser_id, login_page):
    _ = login_page(selenium[browser_id]).header


@wt(parsers.re('user of (?P<browser_id>.*) sees error message '
               'about invalid credentials in (Onepanel|Onezone) '
               'login page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_err_msg_about_credentials(selenium, browser_id, login_page):
    assert login_page(selenium[browser_id]).err_msg, \
        'no err msg about invalid credentials found'
