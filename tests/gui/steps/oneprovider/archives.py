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


@wt(parsers.parse('user of {browser_id} double clicks on latest created '
                  'archive'))
@repeat_failed(timeout=WAIT_FRONTEND)
def clicks_latest_created_archive(browser_id, tmp_memory):
    browser = tmp_memory[browser_id]['archive_file_browser']
    browser.data[0].double_click()


@wt(parsers.parse('user of {browser_id} sees {tag_type} tag for latest created '
                  'archive'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_tag_for_latest_created_archive(browser_id, tag_type, tmp_memory):
    browser = tmp_memory[browser_id]['archive_file_browser']
    err_msg = f'{tag_type} tag for latest created archive is not visible'
    assert browser.data[0].is_tag_visible(tag_type), err_msg
