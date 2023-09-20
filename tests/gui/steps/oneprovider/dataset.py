"""This module contains gherkin steps to run acceptance tests featuring
datasets in oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.modals.modal import click_modal_button
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed

DATASET_BROWSER = 'dataset browser'


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


@wt(parsers.parse('user of {browser_id} checks {toggle_type} write protection'
                  ' toggle in {modal_name} modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_protection_toggle(browser_id, selenium, modals, toggle_type,
                            modal_name):
    driver = selenium[browser_id]
    toggle = getattr(getattr(modals(driver), transform(modal_name)),
                     f'{toggle_type}_protection_toggle')
    toggle.check()
    if toggle.is_unchecked():
        raise Exception(f'Cannot check {toggle_type} write protection toggle')


@wt(parsers.parse('user of {browser_id} cannot click {toggle_type} write '
                  'protection toggle in {modal_name} modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def can_not_click_protection_toggle(browser_id, selenium, modals, toggle_type,
                                    modal_name):
    driver = selenium[browser_id]
    try:
        getattr(getattr(modals(driver), transform(modal_name)),
                f'{toggle_type}_protection_toggle').check()
        raise Exception(f'{toggle_type}_protection_toggle is clickable')
    except RuntimeError:
        pass



@wt(parsers.parse('user of {browser_id} sees "{text}" label in Datasets modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def see_protected_tag_label_in_dataset_modal(browser_id, selenium, modals,
                                             text):
    driver = selenium[browser_id]
    error = f'Text: {text} not found in label '

    if 'metadata' in text:
        assert text in modals(driver).datasets.metadata_protected_label, error
    else:
        assert text in modals(driver).datasets.data_protected_label, error


@wt(parsers.parse('user of {browser_id} clicks on dataset for'
                  ' "{name}" in dataset browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_dataset(browser_id, tmp_memory, name):
    browser = tmp_memory[browser_id][transform(DATASET_BROWSER)]
    browser.click_on_background()
    browser.data[name].click()


@wt(parsers.parse('user of {browser_id} sees path to root file: "{path}" '
                  'for "{name}" dataset in dataset browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_path_to_root_file(browser_id, tmp_memory, path, name):
    browser = tmp_memory[browser_id][transform(DATASET_BROWSER)]
    path_to_root = browser.data[name].path_to_root_file
    err_msg = (f'Path to root: "{path_to_root} does not match expected'
               f' path: "{path}"')
    assert path == path_to_root, err_msg


@wt(parsers.parse('user of {browser_id} sees that one of two listed datasets'
                  ' "{name}" has got root file deleted'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_one_of_two_dataset_has_deleted_root(browser_id, tmp_memory, name):
    browser = tmp_memory[browser_id][transform(DATASET_BROWSER)]
    number_of_deleted_icon = 0
    for dataset in browser.data:
        if dataset.name == name:
            try:
                dataset.deleted_root_file_icon
                number_of_deleted_icon += 1
            except RuntimeError:
                pass
    err_msg = (f'Number of deleted icon in detached dataset list '
               f'is {number_of_deleted_icon}, but should be 1')
    assert number_of_deleted_icon == 1, err_msg


@wt(parsers.parse('user of {browser_id} sees two same root file paths '
                  '"{path}" for datasets named "{name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_two_identical_root_file_paths(browser_id, tmp_memory, name, path):
    browser = tmp_memory[browser_id][transform(DATASET_BROWSER)]
    paths = []
    for dataset in browser.data:
        if dataset.name == name:
            paths.append(dataset.path_to_root_file)

    assert len(paths) == 2 and paths[0] == paths[1], (
        f'"{paths[0]}" and "{paths[1]}" should be identical')
    assert paths[0] == path, (
        f'"{paths[0]}" match "{path[1]}" but does not match expected "{path}"')


@wt(parsers.parse('user of {browser_id} fails to click on "{button}" button'
                  ' in modal "{modal}"'))
def fail_to_click_button_in_modal(browser_id, button, modal, selenium, modals):
    try:
        click_modal_button(selenium, browser_id, button, modal, modals)
        raise Exception(f'User can click on "{button}" in modal "{modal}"')
    except RuntimeError:
        pass



