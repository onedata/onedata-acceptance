"""This module contains gherkin steps to run acceptance tests featuring
workflows initial values in oneprovider web GUI """

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time

from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_FRONTEND)
def choose_range_as_initial_workflow_value(selenium, browser_id, op_container,
                                           item, add_new=True):
    driver = selenium[browser_id]
    if add_new:
        op_container(driver).automation_page.input_link.click()
    ranges = op_container(driver).automation_page.ranges_input

    i = len(ranges)-1
    for key, val in item.items():
        setattr(ranges[i], key, str(val))


@repeat_failed(timeout=WAIT_FRONTEND)
def check_if_files_were_selected(modals, driver, files):
    try:
        modals(driver).select_files
        raise Exception(f'Files: {files} as initial value for workflow was '
                        f'not selected')
    except RuntimeError:
        pass


@repeat_failed(timeout=WAIT_FRONTEND)
def open_select_initial_files_modal(op_container, driver, popups, modals):
    option = f"Select/upload file"

    click_file_input_link_in_automation_page(op_container, driver)
    time.sleep(1)
    menu_option = get_select_option_from_initial_value_popup(
        option, popups(driver).workflow_initial_values.menu)
    menu_option.click()
    time.sleep(1)
    # check if modal opened
    select_files_modal = modals(driver).select_files


@repeat_failed(timeout=WAIT_FRONTEND)
def open_select_initial_datasets_modal(op_container, driver, popups, modals):
    option = "Select datasets"
    op_container(driver).automation_page.input_link()
    time.sleep(1)
    popups(driver).workflow_dataset_initial_value.menu[option].click()
    time.sleep(1)
    # check if modal opened
    select_dataset_modal = modals(driver).select_dataset


def get_select_option_from_initial_value_popup(option, popup_menu):
    for elem in popup_menu:
        if option in elem.name:
            return elem


def click_file_input_link_in_automation_page(op_container, driver):
    try:
        # for input store type Single Value this Button does not work
        op_container(driver).automation_page.files_input_link.click()
    except RuntimeError:
        # for adding another files to input store (type List) this Button
        # does not work because it finds two links (one for changing file,
        # another for adding)
        # this button is used for input store type Single Value
        op_container(driver).automation_page.single_file_input_link.click()

