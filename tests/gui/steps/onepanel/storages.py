"""This module contains gherkin steps to run acceptance tests featuring
storages management in onepanel web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import when, then, parsers

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import given
from tests.utils.utils import repeat_failed
from tests.utils.acceptance_utils import wt


@wt(parsers.parse('user of {browser_id} selects {storage_type} from storage '
                  'selector in storages page in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_select_storage_type_in_storage_page_op_panel(selenium, browser_id,
                                                    storage_type, onepanel):
    storage_selector = (
        onepanel(selenium[browser_id]).content.storages.form.storage_selector)
    storage_selector.expand()
    storage_selector.options[storage_type].click()


@wt(parsers.re('user of (?P<browser_id>.*?) types "(?P<text>.*?)" to '
               '(?P<input_box>.*?) field in (?P<form>POSIX|Local Ceph) form '
               'in storages page in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_text_to_in_box_in_storages_page_op_panel(selenium, browser_id, text,
                                                     form, onepanel, input_box):
    form = getattr(onepanel(selenium[browser_id]).content.storages.form,
                   transform(form))
    setattr(form, transform(input_box), text)


def enable_import_in_add_storage_form(selenium, browser_id, onepanel):
    form = onepanel(selenium[browser_id]).content.storages.form
    form.posix.imported_storage.check()


@wt(parsers.parse('user of {browser_id} clicks on Add button in add storage '
                  'form in storages page in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_add_btn_in_storage_add_form_in_storage_page(selenium,
                                                            browser_id,
                                                            onepanel):
    onepanel(selenium[browser_id]).content.storages.form.add()


@wt(parsers.parse('user of {browser_id} expands "{storage}" record on '
                  'storages list in storages page in Onepanel'))
@repeat_failed(timeout=WAIT_BACKEND)
def wt_expand_storage_item_in_storages_page_op_panel(selenium, browser_id,
                                                     storage, onepanel):
    onepanel(selenium[browser_id]).content.storages.storages[storage].expand()


@wt(parsers.re('user of (?P<browser_id>.*?) sees that "(?P<storage>.*?)" '
               '(?P<attr>Storage type|Mount point) is (?P<val>.*?) '
               'in storages page in Onepanel'))
@repeat_failed(timeout=WAIT_BACKEND)
def wt_assert_storage_attr_in_storages_page_op_panel(selenium, browser_id,
                                                     storage, attr, val,
                                                     onepanel):
    storages = onepanel(selenium[browser_id]).content.storages.storages
    displayed_val = getattr(storages[storage], transform(attr)).lower()
    assert displayed_val == val.lower(), (f'got {displayed_val} as storage\'s '
                                          f'{attr} instead of expected {val}')


@wt(parsers.parse('user of {browser_id} expands toolbar for "{name}" storage '
                  'record in Storages page in Onepanel'))
@repeat_failed(timeout=WAIT_BACKEND)
def wt_expands_toolbar_for_storage_in_onepanel(selenium, browser_id, name,
                                               onepanel):
    driver = selenium[browser_id]
    onepanel(driver).content.storages.storages[name].expand_menu(driver)


@wt(parsers.re(r"user of (?P<browser_id>.*?) clicks on "
               r"(?P<option>Modify storage details|Remove storage) "
               r"option in storage's toolbar in Onepanel"))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_btn_in_storage_toolbar_in_panel(selenium, browser_id, option,
                                                 popups):
    toolbar = popups(selenium[browser_id]).toolbar
    if toolbar.is_displayed():
        toolbar.options[option].click()
    else:
        raise RuntimeError('no storage toolbar found in Onepanel')


@wt(parsers.parse('user of {browser_id} types "{in_value}" into last key in '
                  'posix storage edit page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_key_in_posix_storage_edit_page(selenium, browser_id,
                                        key, onepanel):
    driver = selenium[browser_id]
    onepanel(driver).content.storages.storages['posix'].edit_form
    storage_posix = onepanel(driver).content.storages.storages['posix']
    storage_posix.edit_form.posix_editor.params.set_last_key(key)


@wt(parsers.parse('user of {browser_id} clicks value of modified record in '
                  'posix storage edit page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_value_in_posix_storage_edit_page(selenium, browser_id, onepanel):
    driver = selenium[browser_id]
    onepanel(driver).content.storages.storages['posix'].edit_form
    storage_posix = onepanel(driver).content.storages.storages['posix']
    storage_posix.edit_form.posix_editor.params.click_value_in_modified_record()


@wt(parsers.parse('user of {browser_id} deletes first additional param in posix'
                  ' storage edit page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def delete_additional_param_in_posix_storage_edit_page(selenium, browser_id,
                                                       onepanel):
    driver = selenium[browser_id]
    storage_posix = onepanel(driver).content.storages.storages['posix']
    storage_posix.edit_form.posix_editor.params.delete_first_additional_param()


@wt(parsers.parse('user of {browser_id} saves changes in posix storage edit '
                  'page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def save_changes_in_posix_storage_edit_page(selenium, browser_id, onepanel):
    driver = selenium[browser_id]
    storage = onepanel(driver).content.storages.storages['posix']
    storage.edit_form.posix_editor.save_button.click()


@wt(parsers.parse('user of {browser_id} sees that "{name}" has disappeared '
                  'from the storages list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_storage_disappeared_from_list(selenium, browser_id, name, onepanel):
    driver = selenium[browser_id]
    storages_list = onepanel(driver).content.storages.storages
    assert name not in storages_list, 'found {} on storages list'.format(name)


@wt(parsers.parse('user of {browser_id} sees that "{name}" is visible '
                  'on the storages list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_storage_on_storage_list(selenium, browser_id, name, onepanel):
    assert is_storage_on_storage_list(selenium, browser_id, name, onepanel), (
        f'{name} not visible on storages list')


def is_storage_on_storage_list(selenium, browser_id, name, onepanel):
    driver = selenium[browser_id]
    storages_list = onepanel(driver).content.storages.storages
    return name in storages_list


@wt(parsers.parse('user of {browser_id} types "{name}" to {input_box} field '
                  'in POSIX edit form for "{storage}" storage in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_name_to_form_in_storages_page(selenium, browser_id, name, input_box,
                                       onepanel, storage):
    driver = selenium[browser_id]
    form = (onepanel(driver).content.storages.storages[
                storage].edit_form.posix_editor)
    setattr(form, transform(input_box), name)


@wt(parsers.parse('user of {browser_id} clicks on {name} button in edit form '
                  'for "{storage}" storage in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_button_in_edit_form(selenium, browser_id, name, onepanel, storage):
    driver = selenium[browser_id]
    button = name.lower() + '_button'
    getattr(onepanel(driver).content.storages.storages[
                storage].edit_form.posix_editor, button)()


@wt(parsers.parse('user of {browser_id} copies id of "{storage_name}" storage '
                  'to clipboard via copy button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_storage_id_to_clipboard(selenium, browser_id, storage_name, onepanel):
    driver = selenium[browser_id]
    onepanel(driver).content.storages.storages[storage_name].copy_id_button()
