"""This module contains meta steps for operations on automation page in
Oneprovider using web GUI
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.constants import (
    WAIT_EXTENDED_WORKFLOW_EXECUTION,
    WAIT_NORMAL_WORKFLOW_EXECUTION,
)
from tests.gui.meta_steps.oneprovider.data import get_item_name_and_containing_dir_path
from tests.gui.steps.common.miscellaneous import switch_to_iframe
from tests.gui.steps.modals.modal import click_modal_button
from tests.gui.steps.oneprovider.automation.automation_basic import (
    change_tab_in_automation_subpage,
    click_on_task_in_lane,
    switch_to_automation_page,
    wait_until_workflow_executions_list_is_empty,
)
from tests.gui.steps.oneprovider.automation.automation_statuses import (
    await_for_task_status_in_parallel_box,
)
from tests.gui.steps.oneprovider.automation.initial_values import (
    check_if_select_files_modal_disappeared,
    get_initial_value_store,
    open_select_initial_datasets_modal,
    open_select_initial_files_modal,
    open_select_initial_groups_modal,
    select_groups_from_select_groups_modal,
)
from tests.gui.steps.oneprovider.automation.workflow_results_modals import (
    choose_time_resolution,
)
from tests.gui.utils import Modals, Popups
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    parse_elements_sequence,
    parse_seq,
    transform,
)
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt


def open_initial_modal(data_type: str, driver: WebDriver) -> None:
    if "dataset" in data_type:
        open_select_initial_datasets_modal(driver)
    else:
        open_select_initial_files_modal(driver)


def go_to_path_and_return_file_name_in_modal(
    path: str, driver: WebDriver, modal_name: str
) -> str:
    if "/" in path:
        modal = getattr(Modals(driver), transform(modal_name))
        file_name, path_list = get_item_name_and_containing_dir_path(path)
        for item in path_list:
            modal.files[item].click_and_enter()
        return file_name
    return path


def select_initial_items_for_workflow_in_modal(
    files: str | list[str], driver: WebDriver, data_type: str
) -> None:
    if isinstance(files, str):
        parsed_files = parse_seq(files)
    else:
        parsed_files = files
    last_file_name = parsed_files[-1].split("/")[-1]

    for path in parsed_files:
        modal_name = "select files"
        file_name = go_to_path_and_return_file_name_in_modal(path, driver, modal_name)
        select_files_modal = Modals(driver).select_files

        for file in select_files_modal.files:
            if file.name == file_name:
                file.clickable_field.click()
                if Popups(driver).is_upload_presenter():
                    Popups(driver).upload_presenter[0].cancel_button.click()
                select_files_modal.confirm_button.click()
                # wait a moment for modal to close
                time.sleep(0.25)
                if file_name != last_file_name:
                    open_initial_modal(data_type, driver)
                    # wait a moment for modal to open
                    time.sleep(0.25)
                break

    check_if_select_files_modal_disappeared(driver, files)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) chooses"
        rf" (?P<file_list>{ELEMENTS_SEQUENCE_PATTERN}) file as "
        r'initial value of "(?P<store_name>.*)" store for workflow '
        r'in "Select files" modal'
    ),
    converters={"file_list": parse_elements_sequence},
)
def choose_file_as_initial_workflow_value_for_store(
    selenium: SeleniumDrivers,
    browser_id: str,
    file_list: str | list[str],
    store_name: str,
) -> None:
    data_type = "file"

    switch_to_iframe(selenium, browser_id)
    driver = selenium[browser_id]
    open_select_initial_files_modal(driver, store_name)
    select_initial_items_for_workflow_in_modal(file_list, driver, data_type)


def choose_group_as_initial_workflow_value_for_store(
    selenium: SeleniumDrivers,
    browser_id: str,
    group_list: str | list[str],
    store_name: str,
) -> None:
    switch_to_iframe(selenium, browser_id)
    driver = selenium[browser_id]
    open_select_initial_groups_modal(selenium, browser_id, store_name)
    # Modal can be opened but groups might not be loaded yet
    select_groups_from_select_groups_modal(driver, group_list)


def provide_text_to_object_initial_workflow_value_store(
    driver: WebDriver, store_name: str, text: str
) -> None:
    store = get_initial_value_store(driver, store_name)
    store.content.send_keys([Keys.CONTROL, "a", Keys.BACKSPACE])
    text = str(text).replace("'", '"')
    store.content.send_keys(text)


def provide_text_to_string_initial_workflow_value_store(
    driver: WebDriver, store_name: str, text: str
) -> None:
    store = get_initial_value_store(driver, store_name)
    store.input = text


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) sees "(?P<expected_error_message>.*)" '
        r'message while choosing "(?P<dir_name>.*)" directory as initial '
        r'value for workflow in "Select files" modal'
    )
)
def fails_to_choose_directory_as_initial_workflow_value(
    selenium: SeleniumDrivers,
    browser_id: str,
    dir_name: str,
    expected_error_message: str,
) -> None:
    data_type = "directory"
    switch_to_iframe(selenium, browser_id)
    driver = selenium[browser_id]
    open_initial_modal(data_type, driver)
    Modals(driver).select_files.files[dir_name].click()
    actual_error_message = Modals(driver).select_files.error_msg
    assert actual_error_message == expected_error_message, (
        f'User does not see expected error: "{expected_error_message}" while trying'
        f' to set "{dir_name}" as initial value for workflow'
    )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) chooses"
        rf" (?P<file_list>{ELEMENTS_SEQUENCE_PATTERN}) "
        r"(?P<data_type>file|files|datasets) as initial value for "
        r'workflow in "Select files" modal'
    ),
    converters={"file_list": parse_elements_sequence},
)
def choose_file_as_initial_workflow_value(
    selenium: SeleniumDrivers,
    browser_id: str,
    file_list: str | list[str],
    data_type: str,
) -> None:
    switch_to_iframe(selenium, browser_id)
    driver = selenium[browser_id]
    open_initial_modal(data_type, driver)

    select_initial_items_for_workflow_in_modal(file_list, driver, data_type)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) waits for all workflows to"
        r" (?P<option>start|finish)"
    )
)
def wait_for_workflows_in_automation_subpage(
    selenium: SeleniumDrivers, browser_id: str, option: str
) -> None:
    _wait_for_workflows_in_automation_subpage(selenium, browser_id, option)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) waits extended time for "
        r"all workflows to (?P<option>start|finish)"
    )
)
def wait_for_workflows_in_automation_subpage_extended_time(
    selenium: SeleniumDrivers, browser_id: str, option: str
) -> None:
    _wait_for_workflows_in_automation_subpage(
        selenium,
        browser_id,
        option,
        timeout=WAIT_EXTENDED_WORKFLOW_EXECUTION,
    )


def wait_for_workflow_execution_in_atm_subpage(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    wait_for_workflows_in_automation_subpage(selenium, browser_id, "start")
    wait_for_workflows_in_automation_subpage(selenium, browser_id, "finish")
    assert_no_suspended_workflows_in_atm_subpage(selenium, browser_id)


def _wait_for_workflows_in_automation_subpage(
    selenium: SeleniumDrivers,
    browser_id: str,
    option: str,
    *,
    timeout: float = WAIT_NORMAL_WORKFLOW_EXECUTION,
) -> None:
    page = switch_to_automation_page(selenium, browser_id)
    if option == "start":
        change_tab_in_automation_subpage(selenium, browser_id, "Waiting")
        err = "Waiting workflows did not start"
    else:
        change_tab_in_automation_subpage(selenium, browser_id, "Ongoing")
        err = "Ongoing workflows did not finish their run"

    wait_until_workflow_executions_list_is_empty(
        page,
        err,
        timeout=timeout,
    )


def assert_no_suspended_workflows_in_atm_subpage(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    page = switch_to_automation_page(selenium, browser_id)
    change_tab_in_automation_subpage(selenium, browser_id, "Suspended")
    error_message = (
        "Workflow did not finished successfully and it is in suspended state."
    )
    wait_until_workflow_executions_list_is_empty(page, error_message)


@wt(
    parsers.parse(
        'user of {browser_id} awaits for status of task "{task}" in '
        '{ordinal} parallel box in "{lane}" lane to be "{expected_status}"'
    )
)
def await_for_task_status(
    selenium: SeleniumDrivers,
    browser_id: str,
    lane: str,
    task: str,
    ordinal: str,
    expected_status: str,
) -> None:
    click = "clicks on"
    close = "closes"

    click_on_task_in_lane(selenium, browser_id, lane, task, ordinal, click)
    await_for_task_status_in_parallel_box(
        selenium, browser_id, lane, task, ordinal, expected_status
    )
    click_on_task_in_lane(selenium, browser_id, lane, task, ordinal, close)


@wt(
    parsers.parse(
        "user of {browser_id} changes time resolution to"
        ' "{resolution}" in modal "{modal}"'
    )
)
def change_time_resolution_in_modal(
    selenium: SeleniumDrivers, browser_id: str, resolution: str
) -> None:
    button = "Time resolution"
    modal_name = "Task time series"
    click_modal_button(selenium, browser_id, button, modal_name)
    choose_time_resolution(selenium, browser_id, resolution, modal_name)
