"""This module contains gherkin steps to run acceptance tests featuring
archives in oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed
from tests.gui.utils.generic import transform
import re


@wt(parsers.parse('user of {browser_id} sees that item "{name}" has {number}'
                  ' Archives'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_number_of_archives_for_item_in_dataset_browser(browser_id, name,
                                                          number, tmp_memory):
    browser = tmp_memory[browser_id]['dataset_browser']
    item_number = browser.data[name].archive
    err_msg = (f'displayed {item_number} archives for {name} does not match'
               f' expected {number}')
    assert number == item_number, err_msg


@wt(parsers.parse('user of {browser_id} clicks on {} in "{name}" Archives'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_number_in_archives(browser_id, tmp_memory, name):
    browser = tmp_memory[browser_id]['dataset_browser']
    browser.data[name].number_of_archive()


@wt(parsers.parse('user of {browser_id} writes "{text}" into description'
                  ' text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def write_description(selenium, browser_id, modals, text):
    driver = selenium[browser_id]
    modals(driver).create_archive.description = text


@wt(parsers.parse('user of {browser_id} sees "{state_status}" on first archive'
                  ' state in archive file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def see_archive_state(browser_id, tmp_memory, state_status):
    browser = tmp_memory[browser_id]['archive_file_browser']
    item_status = browser.data[0].state
    item_status = re.sub('\n', ' ', item_status)
    assert item_status == state_status, f'{item_status} state of archive does' \
                                        f' not match expected {state_status}'


@wt(parsers.parse('user of {browser_id} double clicks on {number} '
                  'archive'))
@repeat_failed(timeout=WAIT_FRONTEND)
def clicks_on_archive(browser_id, tmp_memory, number='1'):
    browser = tmp_memory[browser_id]['archive_file_browser']
    browser.data[int(number)-1].double_click()


@wt(parsers.parse('user of {browser_id} sees {tag_type} tag for latest created '
                  'archive'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_tag_for_latest_created_archive(browser_id, tag_type, tmp_memory):
    browser = tmp_memory[browser_id]['archive_file_browser']
    err_msg = f'{tag_type} tag for latest created archive is not visible'
    assert browser.data[0].is_tag_visible(tag_type), err_msg


@wt(parsers.parse('user of {browser_id} checks "{toggle_type}" toggle '
                  'in modal "Create Archive"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_toggle_in_create_archive_modal(browser_id, selenium, modals,
                                         toggle_type):
    driver = selenium[browser_id]
    getattr(modals(driver).create_archive, transform(toggle_type)).check()


@wt(parsers.parse('user of {browser_id} sees that base archive for latest '
                  'created archive is {number} archive'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_base_archive_description(browser_id, tmp_memory,
                                    number):
    browser = tmp_memory[browser_id]['archive_file_browser']
    item_base_archive = browser.data[0].base_archive
    base_archive_name = browser.data[int(number)-1].name
    err_msg = (f'Item base archive: {item_base_archive} does not'
               f' match  {base_archive_name}')
    assert item_base_archive == base_archive_name , err_msg


@wt(parsers.parse('user of {browser_id} clicks on hardlink tag for "{name}" '
                  'in archive file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_tag(browser_id, tmp_memory, name):
    browser = tmp_memory[browser_id]['archive_file_browser']
    browser.data[name].hardlink_tag.click()


@wt(parsers.parse('user of browser clicks on {button} button in '
                  'archive file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_in_archive_browser(browser_id, tmp_memory, button):
    browser = tmp_memory[browser_id]['archive_file_browser']
    getattr(browser, transform(button))()


@wt(parsers.parse('user of {browser_id} sees that base archive name in Create'
                  ' Archive modal is the same as '
                  'latest created archive name'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_name_same_as_latest_created(browser_id, tmp_memory, modals,
                                       selenium):
    driver = selenium[browser_id]
    browser = tmp_memory[browser_id]['archive_file_browser']
    latest_created_name = browser.data[0].name
    base_archive_name = modals(driver).create_archive.base_archive
    err_msg = (f'Latest created archive: {latest_created_name} is not '
               f'the same as base name: {base_archive_name}')
    assert latest_created_name == base_archive_name, err_msg


@wt(parsers.parse('user of {browser_id} copies {number} archive name in '
                  'archive file browser to clipboard'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_archive_name_to_clipboard(browser_id, tmp_memory, number, clipboard,
                                   displays):
    browser = tmp_memory[browser_id]['archive_file_browser']
    clipboard.copy(browser.data[int(number)-1].name,
                   display=displays[browser_id])


@wt(parsers.parse('user of {browser_id} clicks on menu for archive that'
                  ' name was copied to clipboard'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_menu_for_archive(browser_id, tmp_memory, clipboard, displays):
    browser = tmp_memory[browser_id]['archive_file_browser']
    item_name = clipboard.paste(display=displays[browser_id])
    browser.data[item_name].menu_button()





