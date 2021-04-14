"""This module contains gherkin steps to run acceptance tests in web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import json
import os
import subprocess

import yaml
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from tests.gui.utils.generic import transform
from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.utils import repeat_failed
from tests.utils.bdd_utils import given, wt, parsers


@repeat_failed(attempts=WAIT_FRONTEND)
def _enter_text(input_box, text):
    input_box.clear()
    input_box.send_keys(text)
    if input_box.get_attribute('value') != text:
        raise RuntimeError('entering "{}" to input box failed'.format(text))


@wt(parsers.parse('user of {browser_id} types "{text}" on keyboard'))
def type_string_into_active_element(selenium, browser_id, text):
    _enter_text(selenium[browser_id].switch_to.active_element, text)


@wt(parsers.parse('user of {browser_id} types received '
                  '{item_type} on keyboard'))
def type_item_into_active_element(selenium, browser_id, item_type,
                                  tmp_memory):
    item = tmp_memory[browser_id]['mailbox'][item_type]
    _enter_text(selenium[browser_id].switch_to.active_element, item)


@wt(parsers.parse('user of {browser_id} presses enter on keyboard'))
def press_enter_on_active_element(selenium, browser_id):
    driver = selenium[browser_id]
    driver.switch_to.active_element.send_keys(Keys.RETURN)


@wt(parsers.parse('user of {browser_id} presses tab on keyboard'))
def press_tab_on_active_element(selenium, browser_id):
    driver = selenium[browser_id]
    driver.switch_to.active_element.send_keys(Keys.TAB)


@wt(parsers.parse('user of {browser_id} presses backspace on keyboard'))
def press_backspace_on_active_element(selenium, browser_id):
    driver = selenium[browser_id]
    driver.switch_to.active_element.send_keys(Keys.BACKSPACE)


@wt(parsers.parse('user of {browser_id} should see that the page title '
                  'contains "{text}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def title_contains(selenium, browser_id, text):
    page_title = selenium[browser_id].title
    assert text in page_title, \
        '{} page title should contain {}'.format(page_title, text)


@wt(parsers.re('users? of (?P<browser_id_list>.*) clicks on '
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


@wt(parsers.parse('user of {browser_id} clicks "{option}" option in menu popup'))
def click_option_in_popover_menu(selenium, browser_id, option, popups):
    driver = selenium[browser_id]
    popups(driver).menu_popup_with_label.menu[option]()


@wt(parsers.re('pass'))
def pass_test():
    pass


@repeat_failed(interval=1, timeout=90, exceptions=NoSuchElementException)
def switch_to_iframe(selenium, browser_id, selector=None):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    iframe = driver.find_element_by_tag_name('iframe')
    driver.switch_to.frame(iframe)


@wt(parsers.parse('user of {browser_id} sets copied {elem} as {var_name} '
                  'environment variable'))
def set_env_variable_with_copied_val(clipboard, var_name, displays, browser_id):
    var_value = clipboard.paste(display=displays[browser_id])
    _set_env_variable(var_name, var_value)


def _set_env_variable(var_name, var_value):
    os.environ[var_name] = var_value


@wt(parsers.parse('user of {browser_id} runs curl command copied from {page} '
                  'page'))
def run_curl_command(clipboard, displays, browser_id, tmp_memory, page):
    curl_cmd = clipboard.paste(display=displays[browser_id])

    # -k option avoids certificate check
    curl_cmd = curl_cmd + ' -k'
    status, output = subprocess.getstatusoutput(curl_cmd)
    assert status == 0, 'CURL command did not succeeded'
    json_data = _process_curl_output(output, page)
    tmp_memory[browser_id]['curl result'] = json_data


def _process_curl_data_discovery_output(output):
    output = output.replace('\\"', '"')
    output = output.split('\n')
    output_json = output[-1].split('"body"')[-1]
    output_json = output_json.lstrip(':"')
    output_json = output_json.rstrip('"}')
    output_json = output_json + '}}'

    return json.loads(output_json)


def _process_onedata_curl_output(output):
    output = output.split('\n')
    output_json = output[-1]

    return json.loads(output_json)


def _process_curl_output(output, page):
    if page == 'data discovery':
        return _process_curl_data_discovery_output(output)
    else:
        return _process_onedata_curl_output(output)


@wt(parsers.parse('user of {browser_id} sees that curl result matches '
                  'following config:\n{config}'))
def assert_curl_result_with_config(browser_id, tmp_memory, config):
    curl_res = tmp_memory[browser_id]['curl result']
    expected_data = yaml.load(config)

    for key, val in expected_data.items():
        assert curl_res[_camel_transform(key)] == val, (f'{key}: {val} not '
                                                        f'in curl result')


def _camel_transform(phrase: str):
    output = phrase.title().replace(' ', '')
    return output[0].lower() + output[1:]

