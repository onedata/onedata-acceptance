"""This module contains gherkin steps to run acceptance tests featuring
files create dataset in oneprovider web GUI.
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
def assert_item_in_dataset_browser_has_number_archives(browser_id, name,
                                                       number, tmp_memory):
    browser = tmp_memory[browser_id]['dataset_browser']
    item_number = browser.data[name].archive
    err_msg = f'displayed {item_number} archives for {name} does not match' \
              f' expected {number}'
    assert number == item_number, err_msg


@wt(parsers.parse('user of {browser_id} clicks on menu '
                  'for "{item_name}" dataset in dataset browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_menu_for_elem_in_dataset_browser(browser_id, item_name, tmp_memory):
    browser = tmp_memory[browser_id]['dataset_browser']
    browser.data[item_name].menu_button()


@wt(parsers.parse('user of {browser_id} clicks "{option}" option '
                  'in data row menu in dataset browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_data_row_menu_in_datasets_browser(selenium, browser_id,
                                                      option, modals):
    driver = selenium[browser_id]
    modals(driver).data_row_menu.options[option].click()


@wt(parsers.parse('user of {browser_id} clicks Create button in Create'
                  ' Archive modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_in_create_archive_modal(selenium, browser_id, modals):
    driver = selenium[browser_id]
    modals(driver).datasets_archive.create_button()


@wt(parsers.parse('user of {browser_id} clicks on {} in "{name}" Archives'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_number_in_archives(browser_id, tmp_memory, name):
    browser = tmp_memory[browser_id]['dataset_browser']
    browser.data[name].number_of_archive()


@wt(parsers.parse('user of {browser_id} sees "{status}" Archived: {number} {}, '
                  '{size} {unit} on first archive state in archive'
                  ' browser'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_archive_status(browser_id, tmp_memory, status, number, size, unit):
    browser = tmp_memory[browser_id]['dataset_browser']
    item_status = browser.archives[0].state
    item_status = re.sub('\n', ' ', item_status)
    state_status = f'{status} Archived: {number} files, {size} {unit}'
    assert item_status == state_status, f'{item_status} state of archive does' \
                                        f' not match expected {state_status}'
