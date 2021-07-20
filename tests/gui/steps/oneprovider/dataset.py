"""This module contains gherkin steps to run acceptance tests featuring
files add new data set in oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed
from tests.gui.utils.generic import transform


@wt(parsers.parse('user of {browser_id} click Dataset write protection toggle'
                  ' in Datasets modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_protection_toggle(browser_id, selenium, modals):
    driver = selenium[browser_id]
    modals(driver).file_datasets.data_protection_toggle.check()


@wt(parsers.parse('user of {browser_id} click Metadata write protection toggle'
                  ' in Datasets modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_protection_toggle(browser_id, selenium, modals):
    driver = selenium[browser_id]
    (modals(driver).file_datasets.metadata_protection_toggle
     .check())


@wt(parsers.parse('user of {browser_id} sees {text} label in Metadata modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def see_editor_disabled_label(browser_id, selenium, modals, text):
    driver = selenium[browser_id]
    item_status = modals(driver).metadata.editor_disabled
    assert item_status == text, f'{item_status} does not match expected {text}'


@wt(parsers.parse('user of {browser_id} sees {status_type} status tag with'
                  ' arrow for "{item_name}" in file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def see_tag_with_arrow(browser_id, status_type, item_name, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    data_tag = browser.data[item_name].is_tag_visible(transform(status_type))
    arrow_tag = browser.data[item_name].is_tag_visible(transform('dataset'
                                                                 ' arrow'))
    err_msg = f'{status_type} tag with arrow for {item_name} in file browser' \
              f' not visible'
    assert data_tag and arrow_tag, err_msg


@wt(parsers.parse('user of {browser_id} clicks Remove button on Remove '
                  'Selected Dataset modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_remove_button_on_remove_selected_dataset_modal(browser_id, selenium,
                                                         modals):
    driver = selenium[browser_id]
    modals(driver).remove_selected_dataset.remove_button()


@wt(parsers.parse('user of {browser_id} sees "{name}" in dataset browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def see_name_in_dataset_browser(browser_id, name, tmp_memory):
    browser = tmp_memory[browser_id]['dataset_browser']
    assert name in browser.data, f'{name} not found in dataset list'


@wt(parsers.parse('user of {browser_id} does not see "{name}" in dataset'
                  ' browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def not_see_name_in_dataset_browser(browser_id, name, tmp_memory):
    browser = tmp_memory[browser_id]['dataset_browser']
    assert name not in browser.data, f'{name} found in dataset list'


@wt(parsers.parse('user of {browser_id} double clicks on item named'
                  ' "{item_name}" in dataset browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def double_click_on_item_in_file_browser(browser_id, item_name, tmp_memory):
    browser = tmp_memory[browser_id]['dataset_browser']
    browser.data[item_name].double_click()


@wt(parsers.parse('user of {browser_id} sees that {text} write protection '
                  'toggle is checked in Ancestor Dataset menu in Datasets '
                  'modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def see_that_toggle_is_checked(browser_id, selenium, modals, text):
    driver = selenium[browser_id]
    if text == 'metadata':
        assert (modals(driver).file_datasets.ancestor_metadata_protection
                .is_checked()), f'metadata write protection toggle is ' \
                                f'unchecked in ancestor dataset menu'
    elif text == 'data':
        assert (modals(driver).file_datasets.ancestor_data_protection
                .is_checked()), f'data write protection toggle is unchecked ' \
                                f'in ancestor dataset menu'


@wt(parsers.parse('user of {browser_id} clicks on Ancestor datasets option'
                  ' in Datasets modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_in_dataset_modal(browser_id, selenium, modals):
    driver = selenium[browser_id]
    modals(driver).file_datasets.ancestor_option.click()


@wt(parsers.parse('user of {browser_id} sees that {text} write protection '
                  'toggle is checked on "{name}" in ancestors list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def see_toggle_checked_on_item_in_ancestor_list(browser_id, selenium, modals,
                                                text, name):
    driver = selenium[browser_id]
    item = modals(driver).file_datasets.ancestors[name]
    if text == 'data':
        err_msg = f'data write protection toggle is unchecked on {name}'
        assert item.data_protection_toggle.is_checked(), err_msg
    elif text == 'metadata':
        err_msg = f'metadata write protection toggle is unchecked on {name}'
        assert item.metadata_protection_toggle.is_checked(), err_msg


@wt(parsers.parse('user of {browser_id} sees that {text} write protection '
                  'toggle is unchecked on "{name}" in ancestors list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def see_toggle_checked_on_item_in_ancestor_list(browser_id, selenium, modals,
                                                text, name):
    driver = selenium[browser_id]
    item = modals(driver).file_datasets.ancestors[name]
    if text == 'data':
        err_msg = f'data write protection toggle is checked on {name}'
        assert item.data_protection_toggle.is_unchecked(), err_msg
    elif text == 'metadata':
        err_msg = f'metadata write protection toggle is checked on {name}'
        assert item.metadata_protection_toggle.is_unchecked(), err_msg


@wt(parsers.parse('user of {browser_id} sees "{text}" label in Datasets modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def see_toggle_checked_on_item_in_ancestor_list(browser_id, selenium, modals,
                                                text):
    driver = selenium[browser_id]
    assert text in modals(driver).file_datasets.protected_tag_label, \
        f'Text {text} not found in label '
