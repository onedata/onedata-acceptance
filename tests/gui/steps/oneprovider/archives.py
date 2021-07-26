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
