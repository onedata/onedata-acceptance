"""This module contains meta steps for operations on automation page in
Oneprovider using web GUI
"""
__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import time

from selenium.common.exceptions import StaleElementReferenceException

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.steps.common.miscellaneous import switch_to_iframe
from tests.gui.steps.modals.modal import (
    click_modal_button, go_to_path_and_return_file_name_in_modal)
from tests.gui.steps.oneprovider.automation.workflow_results_modals import (
    assert_processing_chart, choose_time_resolution)
from tests.gui.steps.oneprovider.automation.automation_statuses import (
    await_for_task_status_in_parallel_box, assert_task_status_in_parallel_box)
from tests.gui.steps.oneprovider.browser import (
    click_and_press_enter_on_item_in_browser)
from tests.gui.steps.oneprovider.file_browser import (
    click_on_status_tag_for_file_in_file_browser)
from tests.gui.steps.oneprovider.automation.automation_basic import (
    switch_to_automation_page, click_on_task_in_lane,
    click_on_link_in_task_box, change_tab_in_automation_subpage)
from tests.utils.bdd_utils import wt, parsers
from tests.gui.utils.generic import parse_seq
from tests.utils.utils import repeat_failed
from tests.gui.utils.common.count_checksums import *


@repeat_failed(timeout=WAIT_FRONTEND)
def check_if_files_were_selected(modals, driver, files):
    try:
        modals(driver).select_files
        raise Exception(f'Files: {files} as initial value for workflow was '
                        f'not selected')
    except RuntimeError:
        pass


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


def open_initial_modal(data_type,op_container, driver, popups, modals):
    if 'dataset' in data_type:
        open_select_initial_datasets_modal(op_container, driver, popups, modals)
    else:
        open_select_initial_files_modal(op_container, driver, popups, modals)


@wt(parsers.re('user of (?P<browser_id>.*) chooses (?P<file_list>.*) '
               '(?P<data_type>file|files|datasets) as initial value for '
               'workflow in "Select files" modal'))
@repeat_failed(timeout=WAIT_BACKEND)
def choose_file_as_initial_workflow_value(selenium, browser_id, file_list,
                                          modals, op_container, popups,
                                          data_type):
    files = parse_seq(file_list)
    switch_to_iframe(selenium, browser_id)
    driver = selenium[browser_id]
    open_initial_modal(data_type,op_container, driver, popups, modals)

    for path in files:
        modal_name = 'select files'
        file_name = go_to_path_and_return_file_name_in_modal(path, modals,
                                                             driver, modal_name)
        select_files_modal = modals(driver).select_files

        for file in select_files_modal.files:
            if file.name == file_name:
                file.clickable_field.click()
                select_files_modal.confirm_button.click()
                # wait a moment for modal to close
                time.sleep(0.25)
                if file_name != files[-1].split('/')[-1]:
                    open_initial_modal(data_type,op_container, driver, popups,
                                       modals)
                    # wait a moment for modal to open
                    time.sleep(0.25)
                break

    check_if_files_were_selected(modals, driver, files)


@repeat_failed(timeout=WAIT_FRONTEND)
def choose_range_as_initial_workflow_value(selenium, browser_id, op_container,
                                           item, add_new=True):
    driver = selenium[browser_id]
    if add_new:
        op_container(driver).automation_page.input_link.click()
    ranges = op_container(driver).automation_page.ranges

    i = len(ranges)-1
    for key, val in item.items():
        setattr(ranges[i], key, str(val))


@wt(parsers.re('user of (?P<browser_id>.*) waits for all workflows to '
               '(?P<option>start|finish)'))
@repeat_failed(interval=1, timeout=180,
               exceptions=(AssertionError, StaleElementReferenceException))
def wait_for_workflows_in_automation_subpage(selenium, browser_id, op_container,
                                             option):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    if option == 'start':
        change_tab_in_automation_subpage(selenium, browser_id,
                                         op_container, 'Waiting')
        err = 'Waiting workflows did not start'
    else:
        change_tab_in_automation_subpage(selenium, browser_id,
                                         op_container, 'Ongoing')
        err = 'Ongoing workflows did not finish their run'

    assert len(page.workflow_executions_list) == 0, err


def get_store_content(browser_id, driver, page, modals, clipboard,
                      displays, store_name, store_type, index=0):
    page.stores_list[store_name].click()
    modal = modals(driver).store_details
    time.sleep(0.25)
    store_content_type = 'store_content_' + store_type
    store_content_list = getattr(modal, store_content_type)
    store_content_list[index].click()
    modal.copy_button()
    store_value = clipboard.paste(display=displays[browser_id])
    modal.close()

    return store_value


@wt(parsers.parse('user of {browser_id} sees that content of "{store1}" store '
                  'is the same as content of "{store2}" store'))
def compare_store_contents(selenium, browser_id, op_container, store1,
                           store2, modals, clipboard, displays):
    switch_to_iframe(selenium, browser_id)
    driver = selenium[browser_id]

    page = op_container(driver).automation_page.workflow_visualiser

    store1_value = get_store_content(browser_id, driver, page, modals,
                                     clipboard, displays, store1, 'list')
    store2_value = get_store_content(browser_id, driver, page, modals,
                                     clipboard, displays, store2, 'object')

    assert store1_value == store2_value, (f'Value of {store1} '
                                          f'store:{store1_value} \n is not '
                                          f'equal to value of {store2} '
                                          f'store:{store2_value}')


@wt(parsers.parse('user of {browser_id} counts checksums {checksum_list} for '
                  '"{file_name}" in "{space}" space'))
@repeat_failed(timeout=WAIT_FRONTEND)
def count_checksums_for_file(browser_id, tmp_memory, file_name, tmpdir,
                             checksum_list, selenium, op_container):

    click_and_press_enter_on_item_in_browser(selenium, browser_id, file_name,
                                             tmp_memory, op_container)
    downloaded_file = tmpdir.join(browser_id, 'download', file_name)
    checksums = parse_seq(checksum_list)
    results = {}

    for checksum in checksums:
        sum_name = checksum + '_sum'
        results[checksum] = globals()[sum_name](downloaded_file)

    tmp_memory["checksums_" + file_name] = results


def checksums_counted_in_workflow(metadata_modal):
    result = {}
    for item in metadata_modal.basic.entries:
        result[item.key.replace('_key', '')] = item.value
    return result


@wt(parsers.parse('user of {browser_id} sees that checksums {checksum_list} for'
                  ' "{file_name}" counted in workflow are alike to '
                  'those counted earlier by user'))
def assert_checksums_are_the_same(browser_id, checksum_list, file_name,
                                  tmp_memory, modals, selenium):

    status_type = 'Metadata'
    modal_name = 'Details modal'
    button = 'X'
    checksums = parse_seq(checksum_list)

    # checksums needs to be counted in advance using
    # count_checksums_for_file function
    counted_checksum = tmp_memory["checksums_" + file_name]
    click_on_status_tag_for_file_in_file_browser(browser_id, status_type,
                                                 file_name, tmp_memory)
    metadata_modal = modals(selenium[browser_id]).details_modal.metadata
    workflow_checksum = checksums_counted_in_workflow(metadata_modal)

    for key in checksums:
        err_msg = (f'{key} checksum counted by user is {counted_checksum[key]},'
                   f' and is different from checksum counted in workflow: '
                   f'{workflow_checksum[key]}')
        assert workflow_checksum[key] == counted_checksum[key], err_msg

    click_modal_button(selenium, browser_id, button, modal_name, modals)


@wt(parsers.parse('user of {browser_id} sees that counted checksums'
                  ' {checksum_list} for "{file_name}" are alike to those'
                  ' counted in workflow'))
def count_checksums_and_compare_them(browser_id, tmp_memory, file_name, tmpdir,
                                     checksum_list, selenium, op_container,
                                     modals):
    count_checksums_for_file(browser_id, tmp_memory, file_name, tmpdir,
                             checksum_list, selenium, op_container)
    assert_checksums_are_the_same(browser_id, checksum_list, file_name,
                                  tmp_memory, modals, selenium)


@wt(parsers.parse('user of {browser_id} sees that status of task "{task}" in '
                  '{ordinal} parallel box in "{lane}" lane is one of '
                  '"{status1}" or "{status2}"'))
def assert_status_of_task_is_one_of_two(selenium, browser_id, op_container,
                                        lane, task, ordinal, status1, status2):
    click = 'clicks on'
    close = 'closes'
    click_on_task_in_lane(selenium, browser_id, op_container, lane,
                          task, ordinal, click)
    try:
        assert_task_status_in_parallel_box(selenium, browser_id,
                                           op_container, ordinal, lane,
                                           task, status1)
    except AssertionError:
        assert_task_status_in_parallel_box(selenium, browser_id,
                                           op_container, ordinal, lane,
                                           task, status2)
    click_on_task_in_lane(selenium, browser_id, op_container, lane, task,
                          ordinal, close)


@wt(parsers.parse('user of {browser_id} sees that status of task "{task}" in '
                  '{ordinal} parallel box in "{lane}" lane is '
                  '"{expected_status}"'))
def assert_status_of_task(selenium, browser_id, op_container, lane,
                          task, ordinal, expected_status):

    click = 'clicks on'
    close = 'closes'

    click_on_task_in_lane(selenium, browser_id, op_container, lane,
                          task, ordinal, click)
    assert_task_status_in_parallel_box(selenium, browser_id, op_container,
                                       ordinal, lane, task, expected_status)
    click_on_task_in_lane(selenium, browser_id, op_container, lane, task,
                          ordinal, close)


@wt(parsers.parse('user of {browser_id} awaits for status of task "{task}" in '
                  '{ordinal} parallel box in "{lane}" lane to be '
                  '"{expected_status}" maximum of {seconds} seconds'))
def await_for_task_status(selenium, browser_id, op_container, lane,
                          task, ordinal, expected_status, seconds):
    click = 'clicks on'
    close = 'closes'

    click_on_task_in_lane(selenium, browser_id, op_container, lane,
                          task, ordinal, click)
    await_for_task_status_in_parallel_box(selenium, browser_id, op_container,
                                          lane, task, ordinal, expected_status,
                                          seconds)
    click_on_task_in_lane(selenium, browser_id, op_container, lane, task,
                          ordinal, close)


@wt(parsers.parse('user of {browser_id} changes time resolution to'
                  ' "{resolution}" in modal "{modal}"'))
def change_time_resolution_in_modal(selenium, browser_id, modals, popups,
                                    resolution):
    button = "Time resolution"
    modal_name = "Task time series"
    click_modal_button(selenium, browser_id, button, modal_name, modals)
    choose_time_resolution(selenium, browser_id, popups, resolution, modal_name)


@wt(parsers.parse('user of {browser_id} sees chart with processing stats after'
                  ' opening "{link}" link for task "{task}" in {ordinal}'
                  ' parallel box in "{lane}" lane'))
def open_link_and_assert_processing_stats_chart(selenium, browser_id,
                                                op_container, lane, task,
                                                ordinal, link, modals):
    click = 'clicks on'
    click_on_task_in_lane(selenium, browser_id, op_container, lane,
                          task, ordinal, click)
    click_on_link_in_task_box(selenium, browser_id, op_container, lane, task,
                              link, ordinal)
    assert_processing_chart(browser_id, selenium, modals)

