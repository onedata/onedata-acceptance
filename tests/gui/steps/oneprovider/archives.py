"""This module contains gherkin steps to run acceptance tests featuring
archives in oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.steps.oneprovider.data_tab import assert_browser_in_tab_in_op
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed
from tests.gui.utils.generic import transform
import re


@wt(parsers.re(r'user of (?P<browser_id>.*?) sees that item "(?P<name>.*?)"'
               r' has (?P<number>.*?) archives?'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_number_of_archives_for_item_in_dataset_browser(browser_id, name,
                                                          number, tmp_memory):
    browser = tmp_memory[browser_id]['dataset_browser']
    item_number = browser.data[name].number_of_archives.text
    err_msg = (f'displayed {item_number} archives for {name} does not match'
               f' expected {number}')
    assert number == item_number, err_msg


@wt(parsers.parse('user of {browser_id} writes "{text}" into description'
                  ' text field in create archive modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def write_description_in_create_archive_modal(selenium, browser_id, modals,
                                              text):
    driver = selenium[browser_id]
    modals(driver).create_archive.description = text


def get_archive_with_description(browser, description):
    for archive in browser.data:
        try:
            if description == archive.description:
                return archive
        except RuntimeError:
            pass
    else:
        raise Exception('failed to load archive from description')


@wt(parsers.parse('user of {browser_id} saves time of creation archive with'
                  ' description: "{description}" for "{file_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def save_date_of_archive_creation(browser_id, tmp_memory, description):
    browser = tmp_memory[browser_id]['archive_browser']
    archive = get_archive_with_description(browser, description)
    name = archive.name.split(' —')[0]
    tmp_memory['created_at'] = name


@wt(parsers.re('user of (?P<browser_id>.*?) sees that archive with '
               'description: "(?P<description>.*?)" in archive browser '
               'has status: "(?P<status>.*?)", number of files: '
               '(?P<files_count>\d+), size: "(?P<size>.*?)"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_archive_full_state_status(browser_id, tmp_memory, status,
                                     files_count, size, description):
    browser = tmp_memory[browser_id]['archive_browser']
    archive = get_archive_with_description(browser, description)
    state_name = archive.state.get_state_name()
    archive_files_count = archive.state.get_files_count()
    archive_size = archive.state.get_size()
    assert_archive_partial_state_status(state_name, status)
    assert_archive_partial_state_status(archive_files_count, int(files_count))
    assert_archive_partial_state_status(archive_size, size)


def assert_archive_partial_state_status(item_status, expected_status):
    assert expected_status == item_status, (
        f'{expected_status} does not match {item_status}')


@wt(parsers.re('user of (?P<browser_id>.*?) clicks and presses enter on '
               'archive with description: "(?P<description>.*?)" on '
               'archives list in archive browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_and_press_enter_on_archive(browser_id, tmp_memory, description):
    browser = tmp_memory[browser_id]['archive_browser']
    archive = get_archive_with_description(browser, description)
    # clicking on the background of browser to ensure correct
    # working of click_and enter
    browser.click_on_background()
    archive.click_and_enter()


@wt(parsers.re(r'user of (?P<browser_id>.*?) sees (?P<tag_type>.*?) tag for '
               r'archive with description: "(?P<description>.*?)" on archives'
               r' list in archive browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_tag_for_archive_in_archive_browser(browser_id, tag_type, tmp_memory,
                                              description):
    browser = tmp_memory[browser_id]['archive_browser']
    err_msg = f'{tag_type} tag for archive with description is not visible'
    archive = get_archive_with_description(browser, description)
    assert archive.is_tag_visible(tag_type), err_msg


def from_ordinal_number_to_int(ordinal_number):
    return int(re.findall(r'\d+', ordinal_number)[0])


@wt(parsers.parse('user of {browser_id} checks "{toggle_type}" toggle '
                  'in modal "Create Archive"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_toggle_in_create_archive_modal(browser_id, selenium, modals,
                                         toggle_type):
    driver = selenium[browser_id]
    getattr(modals(driver).create_archive, transform(toggle_type)).check()


def compare_base_archive_name_with_archive_with_description(browser,
                                                            base_description,
                                                            item_base_archive):
    base_archive_name = get_archive_with_description(browser,
                                                     base_description).name
    err_msg = (f'Item base archive: {item_base_archive} does not'
               f' match  {base_archive_name}')
    assert item_base_archive == base_archive_name, err_msg


@wt(parsers.re(r'user of (?P<browser_id>.*?) sees that base archive for '
               r'latest created archive is archive with description:'
               r' "(?P<base_description>.*?)" on archives list'
               r' in archive browser'))
def assert_base_archive_description_for_latest_created_archive(
        browser_id, tmp_memory, base_description):
    browser = tmp_memory[browser_id]['archive_browser']
    item_base_archive = browser.data[0].base_archive
    compare_base_archive_name_with_archive_with_description(browser,
                                                            base_description,
                                                            item_base_archive)


@wt(parsers.re(r'user of (?P<browser_id>.*?) sees that base archive for '
               r'archive with description: "(?P<description>.*?)" is archive '
               r'with description: "(?P<base_description>.*?)" on archives list'
               r' in archive browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_base_archive_description(browser_id, tmp_memory, base_description,
                                    description):
    browser = tmp_memory[browser_id]['archive_browser']
    item_base_archive = get_archive_with_description(browser,
                                                     description).base_archive
    compare_base_archive_name_with_archive_with_description(browser,
                                                            base_description,
                                                            item_base_archive)


@wt(parsers.parse('user of browser clicks on {button} button in '
                  'archive browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_in_archive_browser(browser_id, tmp_memory, button):
    browser = tmp_memory[browser_id]['archive_browser']
    getattr(browser, transform(button))()


@wt(parsers.parse('user of {browser_id} sees that base archive name in Create'
                  ' Archive modal is the same as latest created archive name'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_name_same_as_latest_created(browser_id, tmp_memory, modals,
                                       selenium):
    driver = selenium[browser_id]
    browser = tmp_memory[browser_id]['archive_browser']
    latest_created_name = browser.data[0].name
    base_archive_name = modals(driver).create_archive.base_archive
    err_msg = (f'Latest created archive: {latest_created_name} is not '
               f'the same as base name: {base_archive_name}')
    assert latest_created_name == base_archive_name, err_msg


@wt(parsers.re(r'user of (?P<browser_id>.*?) copies archive with'
               r' description: "(?P<description>.*?)" name in archive browser '
               r'to clipboard'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_archive_name_to_clipboard(browser_id, tmp_memory, description,
                                   clipboard, displays):
    browser = tmp_memory[browser_id]['archive_browser']
    archive = get_archive_with_description(browser, description)
    clipboard.copy(archive.name, display=displays[browser_id])


@wt(parsers.parse('user of {browser_id} clicks on menu for archive that'
                  ' name was copied to clipboard'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_menu_for_named_archive(browser_id, tmp_memory, clipboard, displays):
    browser = tmp_memory[browser_id]['archive_browser']
    item_name = clipboard.paste(display=displays[browser_id])
    browser.data[item_name].menu_button()


@wt(parsers.re('user of (?P<browser_id>.*?) clicks on menu for archive '
               'with description: "(?P<description>.*?)" in archive browser'))
def click_menu_for_archive(browser_id, tmp_memory, description):
    browser = tmp_memory[browser_id]['archive_browser']
    archive = get_archive_with_description(browser, description)
    archive.menu_button()


@wt(parsers.parse('user of {browser_id} writes "{text}" into confirmation '
                  'input in Purge Archive modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def write_in_confirmation_input(browser_id, modals, text, selenium):
    driver = selenium[browser_id]
    modals(driver).purge_archive.confirmation_input = text


@wt(parsers.re(r'user of (?P<browser_id>.*?) sees that (?P<ordinal>1st|2nd|3rd|'
               r'\d*?[4567890]th|\d*?11th|\d*?12th|\d*?13th|\d*?[^1]1st|'
               r'\d*?[^1]2nd|\d*?[^1]3rd) archive in archive browser '
               r'has description: "(?P<description>.*?)"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_description_for_archive(browser_id, tmp_memory, description,
                                   ordinal):
    browser = tmp_memory[browser_id]['archive_browser']
    number = from_ordinal_number_to_int(ordinal)
    archive_description = browser.data[number - 1].description
    err_msg = (f'Archive description {archive_description} does not match'
               f' expected description: {description}')
    assert archive_description == description, err_msg


@wt(parsers.parse('user of {browser_id} sees that page with text '
                  '"{text}" appeared in archive browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_page_with_text_appeared(browser_id, text, tmp_memory):
    browser = tmp_memory[browser_id]['archive_browser']
    assert browser.empty_dir_msg == text, f'page with text "{text}" not found'


@wt(parsers.parse('user of {browser_id} goes back to dataset browser from '
                  'archive browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def go_back_to_dataset_page_from_archive_browser(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    oz_page(driver)['data'].archive_header.back_to_dataset_page()


def assert_not_archive_with_description(tmp_memory, browser_id, description):
    browser = tmp_memory[browser_id]['archive_browser']
    archives = browser.data
    for item in archives:
        if description in item.name:
            raise Exception(f'Archive with description: "{description}" found')
    else:
        pass


@wt(parsers.parse('user of {browser_id} sees message "{text}" in place of '
                  'archive browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_page_with_error_appeared(browser_id, text, tmp_memory, selenium,
                                    op_container):
    which_browser = 'archive container'
    assert_browser_in_tab_in_op(selenium, browser_id, op_container, tmp_memory,
                                item_browser=which_browser)
    browser = tmp_memory[browser_id][transform(which_browser)]
    assert browser.message == text, f'page with text "{text}" not  found'

