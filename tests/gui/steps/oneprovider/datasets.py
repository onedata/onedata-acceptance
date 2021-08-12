"""This module contains gherkin steps to run acceptance tests featuring
datasets in oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} clicks Mark this file as dataset toggle'
                  ' in Datasets modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_mark_file_as_dataset_toggle(browser_id, selenium, modals):
    driver = selenium[browser_id]
    modals(driver).datasets.dataset_toggle.check()


@wt(parsers.parse('user of {browser_id} fails to click Mark this file as '
                  'dataset toggle in Datasets modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_mark_file_as_dataset_toggle(browser_id, selenium, modals):
    driver = selenium[browser_id]
    err_msg = 'user does not fail to create dataset'
    assert not modals(driver).datasets.dataset_toggle.check(), err_msg


@wt(parsers.parse('user of {browser_id} clicks on menu '
                  'for "{item_name}" dataset in dataset browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_menu_for_elem_in_dataset_browser(browser_id, item_name, tmp_memory):
    browser = tmp_memory[browser_id]['dataset_browser']
    browser.data[item_name].menu_button()


@wt(parsers.parse('user of {browser_id} cannot click "{option}" option'
                  ' in data row menu in dataset browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def cannot_click_option_in_dataset_browser(selenium, browser_id, option,
                                           modals):
    driver = selenium[browser_id]
    err_msg = f'{option} is clickable'
    assert not modals(driver).data_row_menu.options[option].click(), err_msg


