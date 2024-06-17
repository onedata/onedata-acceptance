"""This module contains gherkin steps to run acceptance tests featuring
workflows initial values in oneprovider web GUI """

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time

from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_FRONTEND)
def choose_range_as_initial_workflow_value(selenium, browser_id, op_container,
                                           item, add_new=True):
    driver = selenium[browser_id]
    if add_new:
        op_container(driver).automation_page.input_link.click()
    ranges = op_container(driver).automation_page.ranges_input

    last_index = len(ranges)-1
    for key, val in item.items():
        setattr(ranges[last_index], key, str(val))


@repeat_failed(timeout=WAIT_FRONTEND)
def check_if_select_files_modal_disappeared(modals, driver, files):
    try:
        modals(driver).select_files
        raise Exception(f'Files: {files} as initial value for workflow was '
                        f'not selected')
    except RuntimeError:
        pass


@repeat_failed(timeout=WAIT_FRONTEND)
def open_select_initial_files_modal(op_container, driver, popups, modals,
                                    store_name=False):
    option = "Select/upload file"

    click_input_link_in_automation_page(op_container, driver, store_name)
    time.sleep(1)
    menu_option = get_select_option_from_initial_value_popup(
        option, popups(driver).workflow_initial_values.menu)
    menu_option.click()
    time.sleep(1)
    # check if modal opened
    modals(driver).select_files


@wt(parsers.parse('user of {browser_id} clicks "Add groups..." link in '
                  '"{store_name}" store'))
@repeat_failed(timeout=WAIT_FRONTEND)
def open_select_initial_groups_modal(op_container, selenium, browser_id,
                                     popups, modals, store_name=False):
    option = "Select groups"
    driver = selenium[browser_id]

    click_input_link_in_automation_page(op_container, driver, store_name)
    time.sleep(1)
    menu_option = get_select_option_from_initial_value_popup(
        option, popups(driver).workflow_group_initial_value.menu)
    menu_option.click()
    time.sleep(1)
    # check if modal opened
    modals(driver).select_groups


@repeat_failed(timeout=WAIT_FRONTEND)
def open_select_initial_datasets_modal(op_container, driver, popups, modals):
    option = "Select datasets"
    op_container(driver).automation_page.input_link()
    time.sleep(1)
    popups(driver).workflow_dataset_initial_value.menu[option].click()
    time.sleep(1)
    # check if modal opened
    modals(driver).select_dataset


def get_select_option_from_initial_value_popup(option, popup_menu):
    for elem in popup_menu:
        if option in elem.name:
            return elem


def get_initial_value_store(driver, op_container, store_name):
    initial_value_stores = op_container(driver).automation_page.initial_value_store
    if store_name + ':' in initial_value_stores:
        return initial_value_stores[store_name + ':']
    if store_name + ': ' in initial_value_stores:
        return initial_value_stores[store_name + ': ']


def click_input_link_in_automation_page(op_container, driver, store_name):
    if store_name:
        store = get_initial_value_store(driver, op_container, store_name)
        store.input_link.click()
    else:
        try:
            # for input store type Single Value this Button does not work
            op_container(driver).automation_page.files_input_link.click()
        except RuntimeError:
            # for adding another files to input store (type List) this Button
            # does not work because it finds two links (one for changing file,
            # another for adding)
            # this button is used for input store type Single Value
            op_container(driver).automation_page.single_file_input_link.click()


def get_data_type_in_initial_value_store(driver, op_container, store_name):
    store = get_initial_value_store(driver, op_container, store_name)
    return store.data_type


def get_data_type_of_array_initial_value_store(driver, op_container, store_name):
    store = get_initial_value_store(driver, op_container, store_name)
    link_name = store.input_link.web_elem.text

    if 'group' in link_name:
        return 'group'
    if 'file' in link_name:
        return 'file'
    raise ValueError(f'unknown type for link {link_name}')


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>sees|does not see) '
               '"(?P<group>.*)" group in "Select groups" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_group_in_select_initial_groups_modal(
        selenium, browser_id, option, modals, group):
    driver = selenium[browser_id]
    modal = modals(driver).select_groups
    err_msg = 'there {} visible {} in select groups modal, but should {}'
    if option == 'sees':
        assert group in modal.groups, err_msg.format('is not', group, 'be')
    else:
        assert group not in modal.groups, err_msg.format('is', group, 'not be')

