"""Steps used for modal handling in various GUI testing scenarios
"""

__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2016 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import re
import itertools

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND

from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.common.keys import Keys
from pytest_bdd import parsers, given, when, then

from tests.gui.utils.generic import click_on_web_elem
from tests.utils.utils import repeat_failed


in_type_to_id = {'username': 'login-form-username-input',
                 'password': 'login-form-password-input'}


@when(parsers.parse('user of {browser_id} sees that '
                    'modal "Add storage" has appeared'))
@then(parsers.parse('user of {browser_id} sees that '
                    'modal "Add storage" has appeared'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wait_for_add_storage_modal_to_appear(selenium, browser_id, tmp_memory,
                                         modals):
    driver = selenium[browser_id]
    modal = modals(driver).add_storage
    tmp_memory[browser_id]['window']['modal'] = modal


@when(parsers.parse('user of {browser_id} copies token from '
                    '"Add storage" modal'))
@then(parsers.parse('user of {browser_id} copies token from '
                    '"Add storage" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def cp_token_from_add_storage_modal(browser_id, tmp_memory):
    modal = tmp_memory[browser_id]['window']['modal']
    modal.copy()


@when(parsers.parse('user of {browser_id} generate another token '
                    'in "Add storage" modal'))
@then(parsers.parse('user of {browser_id} generate another token '
                    'in "Add storage" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def gen_another_token_in_add_storage_modal(browser_id, tmp_memory):
    modal = tmp_memory[browser_id]['window']['modal']
    modal.generate_token()


@when(parsers.parse('user of {browser_id} sees non-empty token '
                    'in "Add storage" modal'))
@then(parsers.parse('user of {browser_id} sees non-empty token '
                    'in "Add storage" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_non_empty_token_in_add_storage_modal(browser_id, tmp_memory):
    token = tmp_memory[browser_id]['window']['modal'].token
    assert len(token) > 0, 'expected token in Add storage modal, ' \
                           'but token field is empty'
    tmp_memory[browser_id]['token'] = token


def _find_modal(driver, modal_name):
    def _find():
        modals = driver.find_elements_by_css_selector('.modal.in, '
                                                      '.modal.in .modal-title')
        for name, modal in zip(modals[1::2], modals[::2]):
            if name.text.lower() == modal_name:
                return modal

    modal_name = modal_name.lower()
    return Wait(driver, WAIT_BACKEND).until(
        lambda _: _find(),
        message='waiting for {:s} modal to appear'.format(modal_name)
    )


def _wait_for_modal_to_appear(driver, browser_id, modal_name, tmp_memory):
    modal = _find_modal(driver, modal_name)
    tmp_memory[browser_id]['window']['modal'] = modal


@when(parsers.parse('user of {browser_id} sees that '
                    '"{modal_name}" modal has appeared'))
@then(parsers.parse('user of {browser_id} sees that '
                    '"{modal_name}" modal has appeared'))
def wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory):
    driver = selenium[browser_id]
    _wait_for_modal_to_appear(driver, browser_id, modal_name, tmp_memory)


@given(parsers.parse('user of {browser_id} seen that '
                     '"{modal_name}" modal has appeared'))
def g_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory):
    driver = selenium[browser_id]
    _wait_for_modal_to_appear(driver, browser_id, modal_name, tmp_memory)


def _wait_for_modal_to_disappear(driver, browser_id, tmp_memory):
    modal = tmp_memory[browser_id]['window']['modal']
    Wait(driver, WAIT_BACKEND).until_not(
        lambda _: not staleness_of(modal) or modal.is_displayed(),
        message='waiting for modal to disappear'
    )
    tmp_memory[browser_id]['window']['modal'] = None


@when(parsers.parse('user of {browser_id} sees that '
                    'the modal has disappeared'))
@then(parsers.parse('user of {browser_id} sees that '
                    'the modal has disappeared'))
def wt_wait_for_modal_to_disappear(selenium, browser_id, tmp_memory):
    driver = selenium[browser_id]
    _wait_for_modal_to_disappear(driver, browser_id, tmp_memory)


@given(parsers.parse('user of {browser_id} seen that '
                     'the modal has disappeared'))
def g_wait_for_modal_to_disappear(selenium, browser_id, tmp_memory):
    driver = selenium[browser_id]
    _wait_for_modal_to_disappear(driver, browser_id, tmp_memory)


def _click_on_confirmation_btn_in_modal(driver, browser_id, button_name,
                                        tmp_memory):
    @repeat_failed(attempts=WAIT_BACKEND, timeout=True)
    def click_on_btn(d, elem, msg):
        click_on_web_elem(d, elem, msg)

    button_name = button_name.lower()
    modal = tmp_memory[browser_id]['window']['modal']
    buttons = modal.find_elements_by_css_selector('button')
    err_msg = 'clicking on {} in displayed modal disabled'.format(button_name)
    for btn in buttons:
        if btn.text.lower() == button_name:
            click_on_btn(driver, btn, err_msg)
            break
    else:
        raise RuntimeError('no button named {} found'.format(button_name))


@when(parsers.re('user of (?P<browser_id>\w+) clicks "(?P<button_name>.*)" '
                 '(confirmation )?button in displayed modal'))
@then(parsers.re('user of (?P<browser_id>\w+) clicks "(?P<button_name>.*)" '
                 '(confirmation )?button in displayed modal'))
def wt_click_on_confirmation_btn_in_modal(selenium, browser_id, button_name,
                                          tmp_memory):
    driver = selenium[browser_id]
    _click_on_confirmation_btn_in_modal(driver, browser_id, button_name,
                                        tmp_memory)


@given(parsers.parse('user of {browser_id} clicked "{button_name}" '
                     'confirmation button in displayed modal'))
def g_click_on_confirmation_btn_in_modal(selenium, browser_id, button_name,
                                         tmp_memory):
    driver = selenium[browser_id]
    _click_on_confirmation_btn_in_modal(driver, browser_id, button_name,
                                        tmp_memory)


@when(parsers.parse('user of {browser_id} sees that message '
                    'displayed in modal matches: {regexp}'))
@then(parsers.parse('user of {browser_id} sees that message '
                    'displayed in modal matches: {regexp}'))
def is_modal_msg_matching(browser_id, regexp, tmp_memory):
    modal = tmp_memory[browser_id]['window']['modal']
    msg = modal.find_element_by_css_selector('.modal-body .message-text').text
    assert re.match(regexp, msg), \
        'mag displayed in modal: {msg} ' \
        'does not match {regexp}'.format(regexp=regexp, msg=msg)


@when(parsers.parse('user of {browser_id} sees '
                    'non-empty token in active modal'))
@then(parsers.parse('user of {browser_id} sees '
                    'non-empty token in active modal'))
def get_token_from_modal(selenium, browser_id, tmp_memory):
    driver = selenium[browser_id]
    modal = tmp_memory[browser_id]['window']['modal']
    token_box = modal.find_element_by_css_selector('input[readonly]')
    token = Wait(driver, WAIT_BACKEND).until(
        lambda _: token_box.get_attribute('value'),
        message='waiting for token to appear'
    )
    tmp_memory[browser_id]['token'] = token


@when(parsers.re(r'user of (?P<browser_id>.*?) clicks on '
                 r'((?P<in_type>.*?) )?input box in active modal'))
@then(parsers.re(r'user of (?P<browser_id>.*?) clicks on '
                 r'((?P<in_type>.*?) )?input box in active modal'))
def activate_input_box_in_modal(browser_id, in_type, tmp_memory):
    modal = tmp_memory[browser_id]['window']['modal']
    css_path = 'input#{}'.format(in_type_to_id[in_type]) if in_type else 'input'
    in_box = modal.find_element_by_css_selector(css_path)
    # send NULL to activates input box
    in_box.send_keys(Keys.NULL)


@when(parsers.parse('user of {browser_id} clicks on '
                    'copy button in active modal'))
@then(parsers.parse('user of {browser_id} clicks on '
                    'copy button in active modal'))
def click_on_copy_btn_in_modal(selenium, browser_id, tmp_memory):
    driver = selenium[browser_id]
    modal = tmp_memory[browser_id]['window']['modal']
    copy_btn = modal.find_element_by_css_selector('button.copy-btn')

    @repeat_failed(attempts=WAIT_FRONTEND, timeout=True)
    def click_on_cp_btn(d, btn, err_msg):
        click_on_web_elem(d, btn, err_msg)

    click_on_cp_btn(driver, copy_btn, 'copy btn for displayed modal disabled')


@when(parsers.parse('user of {browser_id} sees that "{text}" option '
                    'in modal is not selected'))
@then(parsers.parse('user of {browser_id} sees that "{text}" option '
                    'in modal is not selected'))
def assert_modal_option_is_not_selected(browser_id, text, tmp_memory):
    modal = tmp_memory[browser_id]['window']['modal']
    options = modal.find_elements_by_css_selector('.one-option-button',
                                                  '.one-option-button .oneicon')
    err_msg = 'option "{}" is selected while it should not be'.format(text)
    for option, checkbox in itertools.izip(options[::2], options[1::2]):
        if option.text == text:
            checkbox_css = checkbox.get_attribute('class')
            assert '.oneicon-checkbox-empty' in checkbox_css, err_msg


@when(parsers.parse('user of {browser_id} sees that "{text}" option '
                    'in modal is not selected'))
@then(parsers.parse('user of {browser_id} sees that "{text}" option '
                    'in modal is not selected'))
def assert_modal_option_is_not_selected(browser_id, text, tmp_memory):
    modal = tmp_memory[browser_id]['window']['modal']
    options = modal.find_elements_by_css_selector('.one-option-button, '
                                                  '.one-option-button .oneicon')
    err_msg = 'option "{}" is selected while it should not be'.format(text)
    for option, checkbox in itertools.izip(options[::2], options[1::2]):
        if option.text == text:
            checkbox_css = checkbox.get_attribute('class')
            assert 'oneicon-checkbox-empty' in checkbox_css, err_msg


@when(parsers.parse('user of {browser_id} sees that "{btn_name}" item displayed '
                    'in modal is disabled'))
@then(parsers.parse('user of {browser_id} sees that "{btn_name}" item displayed '
                    'in modal is disabled'))
def assert_btn_in_modal_is_disabled(browser_id, btn_name, tmp_memory):
    button_name = btn_name.lower()
    modal = tmp_memory[browser_id]['window']['modal']
    buttons = modal.find_elements_by_css_selector('button')
    for btn in buttons:
        if btn.text.lower() == button_name:
            assert not btn.is_enabled(), '{} is not disabled'.format(btn_name)
            break
    else:
        raise RuntimeError('no button named {} found'.format(button_name))


@when(parsers.parse('user of {browser_id} selects "{text}" option '
                    'in displayed modal'))
@then(parsers.parse('user of {browser_id} selects "{text}" option '
                    'in displayed modal'))
def select_option_with_text_in_modal(browser_id, text, tmp_memory):
    modal = tmp_memory[browser_id]['window']['modal']
    options = modal.find_elements_by_css_selector('.one-option-button, '
                                                  '.one-option-button .oneicon')
    for option, checkbox in itertools.izip(options[::2], options[1::2]):
        if option.text == text:
            checkbox_css = checkbox.get_attribute('class')
            if 'oneicon-checkbox-empty' in checkbox_css:
                checkbox.click()


@when(parsers.parse('user of browser sees that "{btn_name}" item displayed '
                    'in modal is enabled'))
@then(parsers.parse('user of browser sees that "{btn_name}" item displayed '
                    'in modal is enabled'))
def assert_btn_in_modal_is_enabled(browser_id, btn_name, tmp_memory):
    button_name = btn_name.lower()
    modal = tmp_memory[browser_id]['window']['modal']
    buttons = modal.find_elements_by_css_selector('button')
    for btn in buttons:
        if btn.text.lower() == button_name:
            assert btn.is_enabled(), '{} is disabled'.format(btn_name)
            break
    else:
        raise RuntimeError('no button named {} found'.format(button_name))
