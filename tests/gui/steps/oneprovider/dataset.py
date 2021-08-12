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


@wt(parsers.parse('user of {browser_id} click {kind} write protection toggle'
                  ' in Datasets modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_protection_toggle(browser_id, selenium, modals, kind):
    driver = selenium[browser_id]
    protection_kind = f'{kind}_protection_toggle'
    getattr(modals(driver).datasets, protection_kind).check()


@wt(parsers.parse('user of {browser_id} sees that {kind} write protection '
                  'toggle is checked in Ancestor Datasets row in Datasets '
                  'modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_general_toggle_checked_for_ancestors(browser_id, selenium, modals,
                                                kind):
    driver = selenium[browser_id]
    protection_kind = f'ancestor_{kind}_protection'
    toggle = getattr(modals(driver).datasets, protection_kind)
    assert toggle.is_checked(), (f'{kind} write protection toggle is unchecked'
                                 f' in ancestor dataset menu')


@wt(parsers.parse('user of {browser_id} expands Ancestor datasets row '
                  'in Datasets modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_in_dataset_modal(browser_id, selenium, modals):
    driver = selenium[browser_id]
    modals(driver).datasets.ancestor_option.click()


@wt(parsers.parse('user of {browser_id} sees that {kind} write protection '
                  'toggle is checked on "{name}" in ancestors list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_toggle_checked_on_item_in_ancestor_list(browser_id, selenium, modals,
                                                   kind, name):
    driver = selenium[browser_id]
    protection_kind = f'{kind}_protection_toggle'
    item = modals(driver).datasets.ancestors[name]
    err_msg = f'{kind} write protection toggle is unchecked on {name}'
    assert getattr(item, protection_kind).is_checked(), err_msg


@wt(parsers.parse('user of {browser_id} sees that {kind} write protection '
                  'toggle is unchecked on "{name}" in ancestors list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_toggle_unchecked_on_item_in_ancestor_list(browser_id, selenium,
                                                     modals, kind, name):
    driver = selenium[browser_id]
    protection_kind = f'{kind}_protection_toggle'
    item = modals(driver).datasets.ancestors[name]
    err_msg = f'{kind} write protection toggle is checked on {name}'
    assert getattr(item, protection_kind).is_unchecked(), err_msg


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

