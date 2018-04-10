"""This module contains gherkin steps to run acceptance tests in web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time

from pytest_bdd import given, when, then, parsers

from selenium.webdriver.common.keys import Keys

from tests.gui.utils.generic import repeat_failed, transform
from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.acceptance_utils import list_parser

from selenium.webdriver.support.ui import WebDriverWait as Wait


@repeat_failed(attempts=WAIT_FRONTEND)
def _enter_text(input_box, text):
    input_box.clear()
    input_box.send_keys(text)
    if input_box.get_attribute('value') != text:
        raise RuntimeError('entering "{}" to input box failed'.format(text))


@when(parsers.parse('user of {browser_id} types "{text}" on keyboard'))
@then(parsers.parse('user of {browser_id} types "{text}" on keyboard'))
def type_string_into_active_element(selenium, browser_id, text):
    _enter_text(selenium[browser_id].switch_to.active_element, text)


@when(parsers.parse('user of {browser_id} types received '
                    '{item_type} on keyboard'))
@then(parsers.parse('user of {browser_id} types received '
                    '{item_type} on keyboard'))
def type_item_into_active_element(selenium, browser_id, item_type,
                                  tmp_memory):
    item = tmp_memory[browser_id]['mailbox'][item_type]
    _enter_text(selenium[browser_id].switch_to.active_element, item)


@when(parsers.parse('user of {browser_id} presses enter on keyboard'))
@then(parsers.parse('user of {browser_id} presses enter on keyboard'))
def press_enter_on_active_element(selenium, browser_id):
    driver = selenium[browser_id]
    driver.switch_to.active_element.send_keys(Keys.RETURN)


@when(parsers.re('user of (?P<browser_id>.+?) is idle for '
                 '(?P<seconds>\d*\.?\d+([eE][-+]?\d+)?) seconds'))
@then(parsers.re('user of (?P<browser_id>.+?) is idle for '
                 '(?P<seconds>\d*\.?\d+([eE][-+]?\d+)?) seconds'))
def wait_given_time(seconds):
    time.sleep(float(seconds))


@when(parsers.parse('user of {browser_id} should see that the page title '
                    'contains "{text}"'))
@then(parsers.parse('user of {browser_id} should see that the page title '
                    'contains "{text}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def title_contains(selenium, browser_id, text):
    page_title = selenium[browser_id].title
    assert page_title == text, \
        'page title is {} instead of expected {}'.format(page_title, text)


@when(parsers.re('users? of (?P<browser_id_list>.*) clicks on '
                 '"(?P<btn_name>.+?)" button in "(?P<popup>.+?)" popup'))
@then(parsers.re('users? of (?P<browser_id_list>.*) clicks on '
                 '"(?P<btn_name>.+?)" button in "(?P<popup>.+?)" popup'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_btn_in_popup(selenium, browser_id, btn, popup, popups):
    getattr(popups(selenium[browser_id]),
            transform(popup)).buttons[btn].click()


@given(parsers.re('users? of (?P<browser_id_list>.*) clicked on '
                  '"(?P<btn_name>.+?)" button in "(?P<popup>.+?)" popup'))
@repeat_failed(timeout=WAIT_FRONTEND)
def g_click_on_btn_in_popup(selenium, browser_id, btn, popup, popups):
    getattr(popups(selenium[browser_id]),
            transform(popup)).buttons[btn].click()

#
#
#
# # TODO: check if i can merge this with steps above
# def _click_on_button_in_provider_popup(driver, name):
#     def go_to_files_button(s):
#         links = s.find_elements_by_css_selector('.provider-place-drop a, '
#                                                 '.provider-place-drop button')
#         for e in links:
#             if e.text == name:
#                 return e
#
#     Wait(driver, WAIT_FRONTEND).until(
#         go_to_files_button,
#         message='clicking on "{:s}" button in providers popup'.format(name)
#     ).click()
#
#
# @given(parsers.re('users? of (?P<browser_id_list>.*) clicked on the '
#                   '"(?P<btn_name>.+?)" button in provider popup'))
# def g_click_on_go_to_files_provider(selenium, browser_id_list, btn_name):
#     for browser_id in list_parser(browser_id_list):
#         driver = selenium[browser_id]
#         _click_on_button_in_provider_popup(driver, btn_name)
#
#
# @when(parsers.re('users? of (?P<browser_id_list>.*) clicks? on the '
#                  '"(?P<btn_name>.+?)" button in provider popup'))
# @then(parsers.re('users? of (?P<browser_id_list>.*) clicks? on the '
#                  '"(?P<btn_name>.+?)" button in provider popup'))
# def wt_click_on_go_to_files_provider(selenium, browser_id_list, btn_name):
#     for browser_id in list_parser(browser_id_list):
#         driver = selenium[browser_id]
#         _click_on_button_in_provider_popup(driver, btn_name)