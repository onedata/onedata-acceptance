"""This module contains meta steps for operations on automation page in
Oneprovider using web GUI
"""
__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import time

from selenium.common.exceptions import StaleElementReferenceException

from tests.gui.steps.common.miscellaneous import switch_to_iframe
from tests.gui.steps.modals.modal import (
    click_modal_button, go_to_path_and_return_file_name_in_modal)
from tests.gui.steps.oneprovider.automation.initial_values import (
    check_if_files_were_selected, open_select_initial_datasets_modal,
    open_select_initial_files_modal)
from tests.gui.steps.oneprovider.automation.workflow_results_modals import (
    choose_time_resolution)
from tests.gui.steps.oneprovider.automation.automation_statuses import (
    await_for_task_status_in_parallel_box)
from tests.gui.steps.oneprovider.automation.automation_basic import (
    switch_to_automation_page, click_on_task_in_lane,
    change_tab_in_automation_subpage)
from tests.utils.bdd_utils import wt, parsers
from tests.gui.utils.generic import parse_seq
from tests.utils.utils import repeat_failed


def open_initial_modal(data_type, op_container, driver, popups, modals):
    if 'dataset' in data_type:
        open_select_initial_datasets_modal(op_container, driver, popups, modals)
    else:
        open_select_initial_files_modal(op_container, driver, popups, modals)


@wt(parsers.re('user of (?P<browser_id>.*) chooses (?P<file_list>.*) '
               '(?P<data_type>file|files|datasets) as initial value for '
               'workflow in "Select files" modal'))
def choose_file_as_initial_workflow_value(selenium, browser_id, file_list,
                                          modals, op_container, popups,
                                          data_type):
    files = parse_seq(file_list)
    switch_to_iframe(selenium, browser_id)
    driver = selenium[browser_id]
    open_initial_modal(data_type, op_container, driver, popups, modals)

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
                    open_initial_modal(data_type, op_container, driver, popups,
                                       modals)
                    # wait a moment for modal to open
                    time.sleep(0.25)
                break

    check_if_files_were_selected(modals, driver, files)


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

