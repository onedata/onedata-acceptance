"""Steps used for modal handling in various GUI testing scenarios
"""

__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2016 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import re
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.common.keys import Keys

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.utils import Modals as modals
from tests.gui.utils.generic import click_on_web_elem, transform
from tests.utils.bdd_utils import given, wt, parsers
from tests.utils.utils import repeat_failed


in_type_to_id = {'username': 'login-form-username-input',
                 'password': 'login-form-password-input'}


def check_modal_name(modal_name):
    modal_name = transform(modal_name)
    if 'remove' in modal_name:
        return 'remove_modal'
    elif 'leave' in modal_name:
        return 'leave_modal'
    elif 'add_one' in modal_name:
        return 'add_one_of_elements'
    elif 'rename' in modal_name:
        return 'rename_modal'
    elif 'invite' in modal_name:
        return 'invite_using_token'
    elif modal_name in ['file_details', 'directory_details']:
        return 'details_modal'
    elif 'share' in modal_name:
        return 'share'
    else:
        return modal_name


@wt(parsers.parse('user of {browser_id} sees that '
                  'modal "Add storage" has appeared'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wait_for_add_storage_modal_to_appear(selenium, browser_id, tmp_memory,
                                         modals):
    driver = selenium[browser_id]
    modal = modals(driver).add_storage
    tmp_memory[browser_id]['window']['modal'] = modal


@wt(parsers.parse('user of {browser_id} copies token from '
                  '"Add storage" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def cp_token_from_add_storage_modal(browser_id, tmp_memory):
    modal = tmp_memory[browser_id]['window']['modal']
    modal.copy()


@wt(parsers.parse('user of {browser_id} generate another token '
                  'in "Add storage" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def gen_another_token_in_add_storage_modal(browser_id, tmp_memory):
    modal = tmp_memory[browser_id]['window']['modal']
    modal.generate_token()


@wt(parsers.parse('user of {browser_id} sees non-empty token '
                  'in "Add storage" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_non_empty_token_in_add_storage_modal(browser_id, tmp_memory):
    token = tmp_memory[browser_id]['window']['modal'].token
    assert len(token) > 0, 'expected token in Add storage modal, ' \
                           'but token field is empty'
    tmp_memory[browser_id]['token'] = token


def _find_modal(driver, modal_name):
    def _find():
        elements_list = ['group', 'token', 'cluster', 'harvester',
                         'spaces', 'rename', 'permissions', 'directory', 'data',
                         'share', 'metadata', 'delete', 'remove', 'quality',
                         'file details', 'symbolic link', 'inventory',
                         'workflow', 'unsaved', 'cease', 'modify', 'create',
                         'unlink']
        if any([name for name in elements_list
                if name in modal_name.lower()]):
            modals = driver.find_elements_by_css_selector(
                '.modal, .modal .modal-header h1')
        elif 'leave this space' in modal_name:
            modals = driver.find_elements_by_css_selector(
                '.modal.in, .modal.in h1')
        else:
            modals = driver.find_elements_by_css_selector(
                '.modal.in, .modal.in .modal-title')

        for name, modal in zip(modals[1::2], modals[::2]):
            if name.text.lower() == modal_name.lower():
                return modal

    modal_name = modal_name.lower()
    return Wait(driver, WAIT_BACKEND).until(
        lambda _: _find(),
        message='waiting for {:s} modal to appear'.format(modal_name)
    )


def _wait_for_modal_to_appear(driver, browser_id, modal_name, tmp_memory):
    modal = _find_modal(driver, modal_name)
    tmp_memory[browser_id]['window']['modal'] = modal


def check_warning_modal(selenium, browser_id):
    driver = selenium[browser_id]
    if not driver.find_elements_by_css_selector('.question-modal'):
        return False
    else:
        return True


@wt(parsers.parse('user of {browser_id} sees that "{modal_name}" modal has not '
                  'appeared'))
def assert_modal_does_not_appear(selenium, browser_id, modal_name, tmp_memory):
    driver = selenium[browser_id]
    try:
        _wait_for_modal_to_appear(driver, browser_id, modal_name, tmp_memory)
        raise Exception(f'Modal {modal_name} has appeared')
    except TimeoutException:
        pass


@wt(parsers.parse('user of {browser_id} sees that '
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
        message='waiting for modal to disappear')
    tmp_memory[browser_id]['window']['modal'] = None


def _wait_for_named_modal_to_disappear(driver, modal_name):
    modal_name = check_modal_name(modal_name)
    try:
        modal = getattr(modals(driver), transform(modal_name))
    except RuntimeError:
        return
    Wait(driver, WAIT_FRONTEND).until_not(
        lambda _: not staleness_of(modal) or modal.is_displayed(),
        message='waiting for modal to disappear')


@wt(parsers.parse('user of {browser_id} sees that '
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


@wt(parsers.re(r'user of (?P<browser_id>\w+) clicks "(?P<button_name>.*)" '
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


@wt(parsers.parse('user of {browser_id} sees that message '
                  'displayed in modal matches: {regexp}'))
def is_modal_msg_matching(browser_id, regexp, tmp_memory):
    modal = tmp_memory[browser_id]['window']['modal']
    msg = modal.find_element_by_css_selector('.modal-body .message-text').text
    assert re.match(regexp, msg), 'mag displayed in modal: {msg} ' \
                                  'does not match {regexp}'.format(
        regexp=regexp, msg=msg)


@wt(parsers.parse('user of {browser_id} sees '
                  'non-empty token in active modal'))
def get_token_from_modal(selenium, browser_id, tmp_memory):
    driver = selenium[browser_id]
    modal = tmp_memory[browser_id]['window']['modal']
    token_box = modal.find_element_by_css_selector('input[readonly]')
    token = Wait(driver, WAIT_BACKEND).until(
        lambda _: token_box.get_attribute('value'),
        message='waiting for token to appear')
    tmp_memory[browser_id]['token'] = token


@wt(parsers.re(r'user of (?P<browser_id>.*?) clicks on '
               r'((?P<in_type>.*?) )?input box in active modal'))
def activate_input_box_in_modal(browser_id, in_type, tmp_memory):
    modal = tmp_memory[browser_id]['window']['modal']
    css_path = 'input#{}'.format(in_type_to_id[in_type]) if in_type else 'input'
    in_box = modal.find_element_by_css_selector(css_path)
    # send NULL to activates input box
    in_box.send_keys(Keys.NULL)


@wt(parsers.parse('user of {browser_id} clicks on '
                  '{option} button in active modal'))
def click_on_button_in_active_modal(selenium, browser_id, tmp_memory, option):
    driver = selenium[browser_id]
    modal = tmp_memory[browser_id]['window']['modal']
    if option == 'copy':
        button = modal.find_element_by_css_selector('button.copy-btn')
    else:
        button = modal.find_element_by_css_selector('.modal-footer '
                                                    'button.btn-default')

    @repeat_failed(attempts=WAIT_FRONTEND, timeout=True)
    def click_on_btn(d, btn, err_msg):
        click_on_web_elem(d, btn, err_msg)

    click_on_btn(driver, button,
                 '{} btn for displayed modal disabled'.format(option))


@wt(parsers.parse('user of {browser_id} sees that "{text}" option '
                  'in modal is not selected'))
def assert_modal_option_is_not_selected(browser_id, text, tmp_memory):
    modal = tmp_memory[browser_id]['window']['modal']
    options = modal.find_elements_by_css_selector('.one-option-button, '
                                                  '.one-option-button .oneicon')
    err_msg = 'option "{}" is selected while it should not be'.format(text)
    for option, checkbox in zip(options[::2], options[1::2]):
        if option.text == text:
            checkbox_css = checkbox.get_attribute('class')
            assert 'oneicon-checkbox-empty' in checkbox_css, err_msg


@wt(parsers.parse('user of {browser_id} sees that "{btn_name}" item displayed '
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


@wt(parsers.parse('user of {browser_id} selects "{text}" option '
                  'in displayed modal'))
def select_option_with_text_in_modal(browser_id, text, tmp_memory):
    modal = tmp_memory[browser_id]['window']['modal']
    options = modal.find_elements_by_css_selector('.one-option-button, '
                                                  '.one-option-button .oneicon')
    for option, checkbox in zip(options[::2], options[1::2]):
        if option.text == text:
            checkbox_css = checkbox.get_attribute('class')
            if 'oneicon-checkbox-empty' in checkbox_css:
                checkbox.click()


@wt(parsers.parse('user of browser sees that "{btn_name}" item displayed '
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


@wt(parsers.re('user of (?P<browser_id>.*) sees "(?P<text>.*)" '
               '(?P<element>info|alert) in "(?P<modal>.*)" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_element_text_in_modal(selenium, browser_id, modals, modal, text,
                                 element):
    driver = selenium[browser_id]
    modal = check_modal_name(modal)
    element_sel = 'forbidden_alert' if element == 'alert' else 'info'
    assert_element_text(getattr(modals(driver), modal), element_sel, text)


def assert_element_text(elem, selector, elem_text):
    text = getattr(elem, selector).text
    assert elem_text in text, (f'found {elem_text} text instead of '
                               f'{text}')


@wt(parsers.re('user of (?P<browser_id>.*?) clicks on "(?P<button>.*?)" '
               'button in (?P<panel_name>.*?) panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_panel_button(selenium, browser_id, button, panel_name, modals):
    tab = getattr(modals(selenium[browser_id]).details_modal, transform(panel_name))
    getattr(tab, transform(button))()


@wt(parsers.re('user of (?P<browser_id>.*?) sees that there is no '
               '"(?P<button>.*?)" button in (?P<panel_name>.*?) panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_there_is_no_button_in_panel(selenium, browser_id, button, panel_name,
                                       modals):
    modal = getattr(modals(selenium[browser_id]).details_modal,
                    check_modal_name(panel_name))

    try:
        getattr(modal, transform(button))
        raise Exception(f'There is a "{button}" button visible in {panel_name}'
                        f' panel when it shouldn\'t be')
    except RuntimeError:
        pass


@wt(parsers.re('user of (?P<browser_id>.*?) clicks on "(?P<button>.*?)" '
               'button in modal "(?P<modal_name>.*?)"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_modal_button(selenium, browser_id, button, modal_name, modals):
    modal = getattr(modals(selenium[browser_id]), check_modal_name(modal_name))
    button = button.replace('.', '')
    getattr(modal, transform(button))()


@wt(parsers.re('user of (?P<browser_id>.*?) writes "(?P<item_name>.*?)" '
               'into(?P<name_textfield>.*?) text field '
               'in (?P<panel_name>.*?) panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def write_name_into_text_field_in_panel(selenium, browser_id, item_name,
                                        panel_name, modals,
                                        name_textfield='input name'):
    if name_textfield == '':
        name_textfield = 'input name'
    driver = selenium[browser_id]
    modal = getattr(modals(driver).details_modal, check_modal_name(panel_name))
    setattr(modal, transform(name_textfield), item_name)


@wt(parsers.re('user of (?P<browser_id>.*?) writes "(?P<item_name>.*?)" '
               'into(?P<name_textfield>.*?) text field '
               'in modal "(?P<modal_name>.*?)"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def write_name_into_text_field_in_modal(selenium, browser_id, item_name,
                                        modal_name, modals,
                                        name_textfield='input name'):
    if name_textfield == '':
        name_textfield = 'input name'
    driver = selenium[browser_id]
    modal = getattr(modals(driver), check_modal_name(modal_name))
    setattr(modal, transform(name_textfield), item_name)


@wt(parsers.re(r'user of (?P<browser_id>.*?) sees that item named'
               r' "(?P<item_name>.*?)" '
               'is shared (?P<number>.*?) times? in modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_number_of_shares_in_modal(selenium, browser_id, item_name, number,
                                     modals):
    name = 'Shares'
    driver = selenium[browser_id]
    shares_tab = modals(driver).details_modal.shares
    navigation = modals(driver).details_modal.navigation
    links = shares_tab.share_options
    info = look_for_tab_name(navigation, name)
    err_msg = 'Item {item_name} is not shared {number} times'
    assert _assert_number_of_shares_in_modal(number, links, info), err_msg


def look_for_tab_name(navigation, name):
    for elem in navigation:
        if name in elem.name:
            return elem.name


def _assert_number_of_shares_in_modal(number, links, info):
    return number in info and len(links) == int(number)


@wt(parsers.parse('user of {browser_id} clicks on "{share_name}" share link '
                  'with icon in shares panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_share_info_icon_in_share_directory_modal(selenium, browser_id, modals,
                                                   share_name):
    modal = modals(selenium[browser_id]).details_modal.shares

    icon = modal.share_options[share_name].browser_share_icon
    icon.click()


@wt(parsers.re('user of (?P<browser_id>.*?) clicks on '
               r'("(?P<owner_name>.*?)" )?(?P<icon_name>copy) icon'
               ' in modal "(?P<modal_name>.*?)"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_icon_in_share_directory_modal(selenium, browser_id, modal_name,
                                        modals, owner_name, icon_name):
    elem_groups = modals(selenium[browser_id]
                         ).details_modal.shares.share_options
    icon_name = transform(icon_name) + '_icon'
    if owner_name:
        icon = getattr(elem_groups[owner_name], icon_name)
    else:
        icon = getattr(elem_groups[0], icon_name)
    icon.click()


@wt(parsers.parse('user of {browser_id} sees that error modal with '
                  'text "{text}" appeared'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_error_modal_with_text_appeared(selenium, browser_id, text):
    message = 'Modal does not contain text "{}"'.format(text)
    modal_text = modals(selenium[browser_id]).error.content.lower()
    assert text.lower() in modal_text, message


@wt(parsers.parse('user of {browser_id} sees that "{title}" '
                  'error modal appeared'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_titled_error_modal_appeared(selenium, browser_id, title):
    message = f'Modal is not titled "{title}"'
    modal_text = modals(selenium[browser_id]).error.title.lower()
    assert title.lower() in modal_text, message


@wt(parsers.parse('user of {browser_id} sees error modal with info about '
                  'invalid target with id of "{target_name}" {target_type}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_invalid_id_in_error_modal(
        selenium, browser_id, target_name, target_type, groups, spaces,
        inventories, harvesters):
    modal_text = modals(selenium[browser_id]).error.content.lower()
    assert 'is invalid' in modal_text, ('There is no info about invalid target '
                                        'in error modal')
    err_msg = (f'There is no info about id of invalid target '
               f'{target_name} in error modal')
    if target_type == 'group':
        assert groups[target_name] in modal_text, err_msg
    elif target_type == 'space':
        assert spaces[target_name] in modal_text, err_msg
    elif target_type == 'inventory':
        assert inventories[target_name] in modal_text, err_msg
    elif target_type == 'harvester':
        assert harvesters[target_name] in modal_text, err_msg
    else:
        raise ValueError(f'Unknown type {target_type}')


@wt(parsers.re('user of (?P<browser_id>.*) closes "(?P<modal>.*)" '
               '(modal|panel)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def close_modal(selenium, browser_id, modal, modals):
    modal = check_modal_name(modal)
    try:
        getattr(modals(selenium[browser_id]), modal).close()
    except AttributeError:
        try:
            getattr(modals(selenium[browser_id]), modal).cancel()
        except AttributeError:
            getattr(modals(selenium[browser_id]), modal).x()
    except RuntimeError:
        return

    _wait_for_named_modal_to_disappear(selenium[browser_id], modal)


@wt(parsers.parse('user of {browser_id} clicks copy command icon in REST API '
                  'modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_copy_icon_in_rest_api_modal(selenium, browser_id, modals):
    modals(selenium[browser_id]).rest_api_modal.copy_command_button()


@wt(parsers.parse('user of {browser_id} chooses "{option}" in {dropdown_name} '
                  'in modal "{modal_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_option_in_dropdown_menu_in_modal(selenium, browser_id, modals,
                                            dropdown_name, popups, option,
                                            modal_name):
    driver = selenium[browser_id]
    modal = getattr(modals(driver), transform(modal_name))
    dropdown_menu = getattr(modal, transform(dropdown_name))
    dropdown_menu.click()

    popups(driver).power_select.choose_item(option)


@wt(parsers.parse('user of {browser_id} sees that path where symbolic link '
                  'points is "{expected_path}" in {modal} modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_path_where_symbolic_link_points(selenium, browser_id,
                                           expected_path, modal):
    driver = selenium[browser_id]
    modal = transform(modal)
    modal = getattr(modals(driver), modal)
    time.sleep(0.1)
    path = modal.path.replace('\n', '')
    assert expected_path == path, (f'Expected path: {expected_path} does not '
                                   f'match path: {path}')


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>checks|unchecks) '
               '"(?P<toggle_name>.*)" toggle in modal "(?P<modal_name>.*)"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def switch_toggle_in_modal(selenium, browser_id, modals, toggle_name,
                           option, modal_name):
    driver = selenium[browser_id]
    modal = getattr(modals(driver), check_modal_name(modal_name))
    toggle = getattr(modal, transform(toggle_name))
    getattr(toggle, option[:-1])()


def go_to_path_and_return_file_name_in_modal(path, modals, driver,
                                             modal_name):
    modal = getattr(modals(driver), transform(modal_name))
    if '/' in path:
        from tests.gui.meta_steps.oneprovider.data import (
            get_item_name_and_containing_dir_path)
        file_name, path_list = get_item_name_and_containing_dir_path(path)
        for item in path_list:
            modal.files[item].click_and_enter()
        return file_name
    else:
        return path


@wt(parsers.parse('user of {browser_id} accepts terms of privacy in Space '
                  'Marketplace using checkbox in modal "Advertise space in '
                  'the marketplace"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_checkbox_in_advertise_space_modal(selenium, browser_id, modals):
    driver = selenium[browser_id]
    modal = modals(driver).advertise_space_in_the_marketplace
    modal.checkbox.click()

