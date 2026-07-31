"""This module contains meta steps for operations on automation page checking
audit logs in Oneprovider using web GUI
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
import os
import time
from ast import literal_eval
from collections.abc import Mapping
from datetime import date
from typing import TypedDict, cast

import yaml
from _pytest._py.path import LocalPath
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver

from tests import GUI_LOGDIR
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.meta_steps.oneprovider.automation.workflow_results import (
    get_store_details_json,
    open_modal_and_get_store_content,
)
from tests.gui.meta_steps.oneprovider.data import get_file_id_from_details_modal
from tests.gui.steps.common.url import switch_to_last_tab
from tests.gui.steps.modals.modal import click_modal_button, wt_wait_for_modal_to_appear
from tests.gui.steps.oneprovider.archives import from_ordinal_number_to_int
from tests.gui.steps.oneprovider.automation.automation_basic import (
    check_if_task_is_opened,
    click_on_elem_in_store_details_modal,
    click_on_link_in_task_box,
    click_on_task_in_lane,
    get_op_workflow_visualizer_page,
    switch_to_automation_page,
)
from tests.gui.steps.oneprovider.automation.automation_statuses import (
    get_status_from_workflow_visualizer,
)
from tests.gui.steps.oneprovider.automation.workflow_results_modals import (
    check_number_of_elements_in_store_details_modal,
    click_on_task_audit_log,
    close_modal_and_task,
    compare_array_in_store_details_modal,
    compare_booleans_in_store_details_modal,
    compare_datasets_in_store_details_modal,
    compare_string_in_store_details_modal,
    get_audit_log_json_and_write_to_file,
    get_modal_and_logs_for_task,
    get_store_content,
    open_store_details_modal,
)
from tests.gui.steps.oneprovider.common import (
    wait_for_file_with_unknown_name_to_download,
)
from tests.gui.steps.oneprovider.data_tab import assert_browser_in_tab_in_op
from tests.gui.type_definitions import (
    AuditLogContent,
    AuditLogValue,
    Clipboard,
    TmpMemory,
)
from tests.gui.utils import Modals
from tests.gui.utils.common.modals.workflows_modals.audit_log import LogsEntry
from tests.gui.utils.common.modals.workflows_modals.store_details import StoreDetails
from tests.gui.utils.core.web_objects import PageObjectsSequence
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    parse_elements_sequence,
    parse_seq,
    transform,
)
from tests.gui.utils.oneprovider.automation import Task, WorkflowLane
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.path_utils import append_log_to_file
from tests.utils.utils import repeat_failed


class AuditLogDebugContent(TypedDict):
    description: str


class AuditLogDebugEntry(TypedDict):
    content: AuditLogDebugContent
    severity: str


def write_audit_logs_for_task_to_file(
    task: Task,
    driver: WebDriver,
    clipboard: Clipboard,
    path: str,
    displays: dict[str, str],
    browser_id: str,
    exp_status: str,
) -> None:
    task.drag_handle.click()
    # wait for task to open
    time.sleep(1)
    if not check_if_task_is_opened(task):
        task.drag_handle.click()
    if task.status == exp_status:
        modal, logs = get_modal_and_logs_for_task(path, task, driver)
        for log in logs:
            log = cast(LogsEntry, log)
            if log.severity != "Info":
                get_audit_log_json_and_write_to_file(
                    log, modal, clipboard, displays, browser_id, path
                )
                modal.close_details()
                append_log_to_file(path, "\n")

        close_modal_and_task(modal, task)


def get_audit_logs_from_every_task_in_workflow(
    lanes: PageObjectsSequence,
    driver: WebDriver,
    clipboard: Clipboard,
    path: str,
    displays: dict[str, str],
    browser_id: str,
    exp_status: str,
) -> None:
    for lane in lanes:
        lane = cast(WorkflowLane, lane)
        for parallel_box in lane.parallel_boxes:
            for task in parallel_box.task_list:
                write_audit_logs_for_task_to_file(
                    task,
                    driver,
                    clipboard,
                    path,
                    displays,
                    browser_id,
                    exp_status,
                )


@wt(
    parsers.parse(
        'if workflow status is "{exp_status}" {user} of {browser_id}'
        " saves audit logs for all tasks to logs"
    )
)
def save_audit_logs_to_logs(
    selenium: SeleniumDrivers,
    browser_id: str,
    exp_status: str,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
    page = switch_to_automation_page(selenium, browser_id)
    act_status = get_status_from_workflow_visualizer(page)
    driver = selenium[browser_id]
    if act_status == exp_status:
        lanes = page.workflow_visualiser.workflow_lanes
        path = GUI_LOGDIR + "/audit_logs.txt"
        get_audit_logs_from_every_task_in_workflow(
            lanes,
            driver,
            clipboard,
            path,
            displays,
            browser_id,
            exp_status,
        )


@wt(
    parsers.parse(
        "user of {browser_id} sees file_id, checksum and algorithm "
        'information in audit log in "{store_name}" store details'
    )
)
def assert_audit_log_in_store(
    browser_id: str,
    selenium: SeleniumDrivers,
    store_name: str,
    clipboard: Clipboard,
    displays: dict[str, str],
    tmp_memory: TmpMemory,
) -> None:

    driver = selenium[browser_id]
    store_type = "object"
    store_details = get_store_details_json(
        driver,
        browser_id,
        clipboard,
        displays,
        store_name,
        store_type,
    )

    error_message = (
        "There is no information about algorithm, checksum or file id "
        f"in audit log in {store_name} store details"
    )
    assert (
        store_details["algorithm"]
        and store_details["checksum"]
        and store_details["fileId"]
    ), error_message

    tmp_memory[f"{store_name}_store_log"] = store_details


@wt(
    parsers.parse(
        "user of {browser_id} sees destination path, size and "
        'source URL information in audit log in "{store_name}" store'
        " details and they are as follow:\n{content}"
    )
)
def assert_content_in_audit_log_in_store(
    browser_id: str,
    selenium: SeleniumDrivers,
    store_name: str,
    clipboard: Clipboard,
    displays: dict[str, str],
    content: str,
) -> None:
    driver = selenium[browser_id]
    store_type = "object"
    expected_data = yaml.load(content, yaml.Loader)
    store_details = get_store_details_json(
        driver,
        browser_id,
        clipboard,
        displays,
        store_name,
        store_type,
    )

    error_message1 = (
        "There is no information about destination path, size or "
        f"source URL in audit log in {store_name} store details"
    )
    assert (
        store_details["destinationPath"]
        and store_details["sourceUrl"]
        and store_details["size"]
    ), error_message1

    actual_expected = {
        "sourceUrl": "source URL",
        "size": "size",
        "destinationPath": "destination path",
    }

    for actual, expected in actual_expected.items():
        actual_elem = (
            cast(str, store_details[actual]).split("/")[-1]
            if actual == "destinationPath"
            else store_details[actual]
        )
        expected_elem = expected_data[expected]
        error_message2 = (
            f"Actual {actual} {actual_elem} is not the same as expected {expected_elem}"
        )
        assert actual_elem == expected_elem, error_message2


def get_store_audit_log(
    browser_id: str,
    selenium: SeleniumDrivers,
    store_name: str,
    clipboard: Clipboard,
    displays: dict[str, str],
    tmp_memory: TmpMemory,
    store_key: str,
) -> AuditLogContent:
    if store_key not in tmp_memory.keys():
        assert_audit_log_in_store(
            browser_id,
            selenium,
            store_name,
            clipboard,
            displays,
            tmp_memory,
        )

    return cast(AuditLogContent, tmp_memory[store_key])


def compare_audit_log_to_store_log(
    clipboard: Clipboard,
    displays: dict[str, str],
    browser_id: str,
    elem_name: str,
    elem_type: str,
    store_name: str,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
) -> None:
    store_key = f"{store_name}_store_log"
    store_audit_log = get_store_audit_log(
        browser_id,
        selenium,
        store_name,
        clipboard,
        displays,
        tmp_memory,
        store_key,
    )

    click_modal_button(selenium, browser_id, "user_log", "audit_log")
    click_modal_button(selenium, browser_id, "copy_json", "audit_log")

    audit_log = json.loads(clipboard.paste(display=displays[browser_id]))

    error_message = (
        f'Audit logs for {elem_type} "{elem_name}" does not contain '
        f"audit log for {store_name} store"
    )
    assert store_audit_log == audit_log["content"], error_message


@wt(
    parsers.parse(
        "user of {browser_id} sees that audit log in task "
        '"{task_name}" in {ordinal} parallel box in lane '
        '"{lane_name}" contains same entries like audit log in'
        ' "{store_name}" store details'
    )
)
def assert_task_audit_log_is_like_store_audit_log(
    selenium: SeleniumDrivers,
    browser_id: str,
    lane_name: str,
    task_name: str,
    ordinal: str,
    clipboard: Clipboard,
    displays: dict[str, str],
    tmp_memory: TmpMemory,
    store_name: str,
) -> None:
    elem_type = "task"
    driver = selenium[browser_id]
    number = from_ordinal_number_to_int(ordinal) - 1
    page = switch_to_automation_page(selenium, browser_id)

    task = (
        page.workflow_visualiser.workflow_lanes[lane_name]
        .parallel_boxes[number]
        .task_list[task_name]
    )

    click_on_task_audit_log(task)
    # wait a moment for audit log modal to appear
    time.sleep(1)

    compare_audit_log_to_store_log(
        clipboard,
        displays,
        browser_id,
        task_name,
        elem_type,
        store_name,
        selenium,
        tmp_memory,
    )
    modal = Modals(driver).audit_log
    close_modal_and_task(modal, task)


@wt(
    parsers.parse(
        'user of {browser_id} sees that audit log for "{workflow}"'
        " workflow contains the same entries like audit log in"
        ' "{store_name}" store details'
    )
)
def assert_workflow_audit_log_contains_store_audit_log_info(
    selenium: SeleniumDrivers,
    browser_id: str,
    store_name: str,
    clipboard: Clipboard,
    displays: dict[str, str],
    tmp_memory: TmpMemory,
    workflow: str,
) -> None:
    elem_type = "workflow"
    page = switch_to_automation_page(selenium, browser_id)
    page.workflow_visualiser.audit_log()
    driver = selenium[browser_id]

    compare_audit_log_to_store_log(
        clipboard,
        displays,
        browser_id,
        workflow,
        elem_type,
        store_name,
        selenium,
        tmp_memory,
    )
    Modals(driver).audit_log.x()


@wt(
    parsers.parse(
        "user of {browser_id} sees that number of elements in the "
        'content of the "{store_name}" store details modal is {number}'
    )
)
def assert_number_of_elements_in_store_details(
    selenium: SeleniumDrivers, browser_id: str, store_name: str, number: str
) -> None:
    _ = open_store_details_modal(selenium, browser_id, store_name)
    check_number_of_elements_in_store_details_modal(
        selenium, browser_id, int(number), store_name
    )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) sees that each element from list "
        rf'"(?P<file_list>{ELEMENTS_SEQUENCE_PATTERN})" in "(?P<space_name>.*?)" '
        r"(?P<option>corresponds to two) instances of the element with "
        r'"file_id" in "(?P<store_name>.*?)" store'
    ),
    converters={
        "file_list": parse_elements_sequence,
    },
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) sees that (each element with |)"
        r'"file_id" in "(?P<store_name>.*?)" store details modal '
        r"(?P<option>corresponds to id of file from|is id of) "
        rf'"(?P<file_list>{ELEMENTS_SEQUENCE_PATTERN})" in "(?P<space_name>.*?)" space'
    ),
    converters={
        "file_list": parse_elements_sequence,
    },
)
def assert_file_id_in_store_details(
    browser_id: str,
    selenium: SeleniumDrivers,
    store_name: str,
    clipboard: Clipboard,
    displays: dict[str, str],
    tmp_memory: TmpMemory,
    file_list: list[str],
    space_name: str,
    option: str,
) -> None:
    driver = selenium[browser_id]

    page = get_op_workflow_visualizer_page(driver)
    store_type = "object"

    element_count = len(Modals(driver).store_details.store_content_object)
    storage_file_ids = [
        json.loads(
            open_modal_and_get_store_content(
                browser_id,
                driver,
                page,
                clipboard,
                displays,
                store_name,
                store_type,
                i,
            )
        )["fileId"]
        for i in range(element_count)
    ]

    file_ids = [
        get_file_id_from_details_modal(
            selenium,
            browser_id,
            space_name,
            tmp_memory,
            file,
            clipboard,
            displays,
        )
        for file in file_list
    ]

    for storage_file_id in storage_file_ids:
        error_message = (
            f'"file_id" in "{store_name}" store details modal is not '
            f'id of "{file_list}" from "{space_name}" space'
        )

        assert storage_file_id in file_ids, error_message

    if "two" in option:
        assert len(storage_file_ids) == 2 * len(file_ids), (
            f'Number of elements in "{store_name}" store details modal does not'
            " match twice number of files given to check id"
        )
    else:
        assert len(storage_file_ids) == len(file_ids), (
            f'Number of elements in "{store_name}" store details modal does not'
            " match number of files given to check id"
        )


@wt(
    parsers.parse(
        "user of {browser_id} sees that element in the content of the"
        ' "{store_name}" store details modal contains following {option}:\n{content}'
    )
)
@wt(
    parsers.parse(
        "user of {browser_id} sees that each element in the content "
        'of the "{store_name}" store details modal contains one of '
        "following {option}:\n{content}"
    )
)
def assert_each_element_contains_some_information(
    browser_id: str,
    selenium: SeleniumDrivers,
    store_name: str,
    content: str,
    clipboard: Clipboard,
    displays: dict[str, str],
    option: str,
) -> None:
    driver = selenium[browser_id]
    store_type = "object"
    expected_data = yaml.load(content, yaml.Loader)
    actual_data = []
    get_op_workflow_visualizer_page(driver)
    modal = Modals(driver).store_details
    element_count = len(modal.store_content_object)
    for i in range(element_count):
        store_content = json.loads(
            get_store_content(modal, store_type, i, clipboard, displays, browser_id)
        )
        modal.close_details()
        file_path = (
            store_content
            if option == "file names"
            else store_content[
                option.split(" ")[0] + option.split(" ")[-1].capitalize()
            ]
        )
        actual_data.append(file_path.split("/")[-1])
    assert len(actual_data) == len(
        expected_data
    ), f"Actual and expected number of elements in {store_name} differ"
    for elem in actual_data:
        assert elem in expected_data, (
            f"Expected data does not contain {elem} file name in"
            f" {store_name} store details modal"
        )


@wt(
    parsers.parse(
        "user of {browser_id} sees that each element in the "
        'content of the "{store_name}" store details modal contains '
        "following information:\n{content}"
    )
)
def assert_each_element_checksum_content_in_store(
    browser_id: str,
    selenium: SeleniumDrivers,
    store_name: str,
    content: str,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
    driver = selenium[browser_id]
    store_type = "object"
    expected_data = yaml.load(content, yaml.Loader)
    get_op_workflow_visualizer_page(driver)
    modal = Modals(driver).store_details
    element_count = len(modal.store_content_object)
    for i in range(element_count):
        store_content = json.loads(
            get_store_content(modal, store_type, i, clipboard, displays, browser_id)
        )
        modal.close_details()
        expected_sha256 = expected_data["checksums"]["sha256"]["status"]
        actual_sha256 = store_content["checksums"]["sha256"]["status"]
        error_message = (
            f"expected sha256 status {expected_sha256} does not match "
            f"actual {actual_sha256} for {i} element in {store_name}"
            " details modal"
        )
        assert expected_sha256 == actual_sha256, error_message
        expected_md5 = expected_data["checksums"]["md5"]["status"]
        actual_md5 = store_content["checksums"]["md5"]["status"]
        error_message = (
            f"expected md5 status {expected_md5} does not match "
            f"actual {actual_md5} for {i} element in {store_name}"
            " details modal"
        )
        assert expected_md5 == actual_md5, error_message


def check_visual_in_store_details_modal(
    modal: StoreDetails,
    variable_type: str,
    serialized_items: str,
    store_name: str,
) -> None:
    if variable_type == "booleans":
        boolean_items = cast(list[bool], json.loads(serialized_items))
        compare_booleans_in_store_details_modal(boolean_items, modal)
    elif variable_type == "boolean":
        error_message = (
            f"{modal.raw_view} in store details modal does not match"
            f" expected {serialized_items}"
        )
        assert modal.raw_view == serialized_items, error_message
    else:
        parsed_items = cast(
            list[AuditLogValue] | AuditLogContent,
            (
                literal_eval(serialized_items)
                if variable_type != "files"
                else parse_seq(serialized_items)
            ),
        )
        for elem in modal.store_content_list:
            if variable_type == "ranges":
                expected = {
                    "start": int(elem.range_start),
                    "end": int(elem.range_end),
                    "step": int(elem.range_step),
                }
            elif variable_type == "range_objects":
                expected = {
                    "start": int(elem.objects_sequence[1].text),
                    "end": int(elem.objects_sequence[0].text),
                    "step": int(elem.objects_sequence[2].text),
                }
            elif variable_type == "files":
                expected = elem.path
            elif variable_type in ["strings", "numbers"]:
                expected = literal_eval(elem.value)
            else:
                raise ValueError(
                    f"this {variable_type} is not handled in this function"
                )

            error_message = (
                f"expected {variable_type} {parsed_items} does not "
                f"contain {expected} in {store_name} store details"
                " modal"
            )
            assert expected in parsed_items, error_message


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) sees following "
        r'(?P<variable_type>.*?) represented by "(?P<serialized_items>.*?)" in '
        r'content in "(?P<store_name>.*?)" store details modal'
    )
)
def assert_elements_in_store_details_modal(
    browser_id: str,
    selenium: SeleniumDrivers,
    serialized_items: str,
    store_name: str,
    variable_type: str,
) -> None:
    modal = open_store_details_modal(selenium, browser_id, store_name)

    if variable_type == "string":
        compare_string_in_store_details_modal(
            serialized_items, modal, variable_type, store_name
        )
    elif variable_type == "array":
        compare_array_in_store_details_modal(modal, serialized_items)

    else:
        check_visual_in_store_details_modal(
            modal, variable_type, serialized_items, store_name
        )


@wt(
    parsers.parse(
        "user of {browser_id} sees {item_list:ElementsSequence} datasets in "
        'Store details modal for "{store_name}" store',
        extra_types={"ElementsSequence": parse_elements_sequence},
    ),
)
def assert_datasets_in_store_details(
    selenium: SeleniumDrivers,
    browser_id: str,
    store_name: str,
    item_list: list[str],
) -> None:
    modal = open_store_details_modal(selenium, browser_id, store_name)
    compare_datasets_in_store_details_modal(item_list, modal, store_name)
    modal.close()


@wt(
    parsers.parse(
        'user of {browser_id} sees "{file}" file in '
        'Store details modal for "{store_name}" store'
    )
)
def assert_file_in_store_details(
    selenium: SeleniumDrivers, browser_id: str, store_name: str, file: str
) -> None:
    modal = open_store_details_modal(selenium, browser_id, store_name)
    actual_file = modal.single_file_container.name

    error_message = f"{file} is not in Store details modal for {store_name} store"
    assert file == actual_file, error_message
    modal.close()


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "{name}" {option} link in '
        'Store details modal for "{store_name}" store'
    )
)
def wt_click_on_elem_in_store_details_modal(
    browser_id: str, selenium: SeleniumDrivers, name: str, store_name: str, option: str
) -> None:
    modal = open_store_details_modal(selenium, browser_id, store_name)
    click_on_elem_in_store_details_modal(
        modal,
        name,
        option=option,
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def check_if_element_is_selected(
    tmp_memory: TmpMemory, browser_id: str, name: str, which_browser: str
) -> None:
    error_message = f"Element {name} is not selected in {which_browser}"
    browser = tmp_memory[browser_id][transform(which_browser)]
    if_selected = browser.data[name].is_selected()
    assert if_selected, error_message


@wt(
    parsers.parse(
        'user of {browser_id} sees "{name}" item selected in the'
        " {which_browser} opened in new web browser tab"
    )
)
def assert_element_selected_in_new_browser_tab(
    browser_id: str,
    selenium: SeleniumDrivers,
    name: str,
    tmp_memory: TmpMemory,
    which_browser: str,
) -> None:
    switch_to_last_tab(selenium, browser_id)
    assert_browser_in_tab_in_op(selenium, browser_id, tmp_memory, which_browser)
    check_if_element_is_selected(tmp_memory, browser_id, name, which_browser)


def compare_to_expected_if_element_exist_for_store(
    elem: AuditLogValue,
    items: AuditLogContent,
    option: str,
    store_name: str,
    selenium: SeleniumDrivers,
    browser_id: str,
    tmp_memory: TmpMemory,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
    if elem:
        if option == "fileId":
            file_info = cast(str, elem).split(" ")[1].replace(")", "").split("/")
            elem = get_file_id_from_details_modal(
                selenium,
                browser_id,
                file_info[0],
                tmp_memory,
                file_info[1],
                clipboard,
                displays,
            )

        assert elem == items[option], (
            f"{option}: {items[option]} in store {store_name} does not"
            f" match expected {elem}"
        )


@wt(
    parsers.parse(
        'user of {browser_id} sees that content of "{store_name}" store is:\n{config}'
    )
)
def assert_content_of_store(
    selenium: SeleniumDrivers,
    browser_id: str,
    store_name: str,
    config: str,
    clipboard: Clipboard,
    displays: dict[str, str],
    tmp_memory: TmpMemory,
) -> None:

    options_to_check = [
        "mimeType",
        "formatName",
        "isExtensionMatchingFormat",
        "fileName",
        "extensions",
        "sourceUrl",
        "fileId",
    ]
    data = yaml.load(config, yaml.Loader)
    modal = open_store_details_modal(selenium, browser_id, store_name)

    if len(modal.store_content_list) == 0:
        modal.copy_button()
        item = json.loads(clipboard.paste(display=displays[browser_id]))
        error_message = "expected value: {} differs from actual one: {}"
        assert data[0] == item, error_message.format(data[0], item)
    else:
        modal.store_content_list[0].click()
        modal.copy_button()
        items = json.loads(clipboard.paste(display=displays[browser_id]))

        for option in options_to_check:
            elem = data.get(option, False)
            compare_to_expected_if_element_exist_for_store(
                elem,
                items,
                option,
                store_name,
                selenium,
                browser_id,
                tmp_memory,
                clipboard,
                displays,
            )
    try:
        modal.close()
    except (StaleElementReferenceException, RuntimeError):
        pass


def compare_to_expected_if_elem_exist_audit_log(
    data: Mapping[str, AuditLogValue],
    label: str,
    actual_items: Mapping[str, AuditLogValue],
    task_name: str,
) -> None:
    expected = data.get(label, False)
    if expected:
        comparable_expected: AuditLogValue | date = expected
        comparable_actual: AuditLogValue | date = actual_items[label]
        if label == "timestamp":
            comparable_expected = date.today()
            comparable_actual = date.fromtimestamp(
                cast(float, actual_items["timestamp"]) / 1000
            )
        elif label == "severity":
            comparable_expected = cast(str, expected).lower()
        assert_elements_of_task_audit_log_are_the_same(
            comparable_expected, comparable_actual, label, task_name
        )


def assert_elements_of_task_audit_log_are_the_same(
    expected: AuditLogValue | date,
    actual: AuditLogValue | date,
    label: str,
    task_name: str,
) -> None:
    assert expected == actual, (
        f'{label} "{actual}" in audit log for "{task_name}" task is '
        f'not "{expected}" as expected'
    )


def compare_content_reason_of_task_audit_log(
    reason: AuditLogValue,
    actual_reason: AuditLogValue,
    selenium: SeleniumDrivers,
    browser_id: str,
    tmp_memory: TmpMemory,
    clipboard: Clipboard,
    displays: dict[str, str],
    task_name: str,
) -> None:
    error_message = (
        f'Reason: "{reason}" in audit log for "{task_name}" '
        f'task does not contain "{actual_reason}" as expected'
    )
    if isinstance(reason, str) and "contains" in reason:
        reason_data = yaml.load(
            reason.split("contains ")[1].replace("])", "]"), yaml.Loader
        )
        actual_reason_text = cast(str, actual_reason)
        for reason_elem in reason_data:
            assert reason_elem in actual_reason_text, error_message
    elif isinstance(reason, str) and "file checksum" in reason:
        assert reason == cast(str, actual_reason).replace(":", ""), error_message
    else:
        if isinstance(reason, dict):
            reason_details = cast(AuditLogContent, reason["details"])
            specific_error = cast(AuditLogContent, reason_details["specificError"])
            specific_details = cast(AuditLogContent, specific_error["details"])
            value = cast(AuditLogContent, specific_details["value"])
            placeholder_file_id = cast(str, value["fileId"])
            placeholder_file_path = (
                placeholder_file_id.split(" ")[1].replace(")", "").split("/")
            )
            value["fileId"] = get_file_id_from_details_modal(
                selenium,
                browser_id,
                placeholder_file_path[0],
                tmp_memory,
                placeholder_file_path[1],
                clipboard,
                displays,
            )
        assert_elements_of_task_audit_log_are_the_same(
            reason, actual_reason, "Reason", task_name
        )


def compare_content_of_task_audit_log(
    content: AuditLogContent,
    actual_content: AuditLogContent,
    task_name: str,
    selenium: SeleniumDrivers,
    browser_id: str,
    tmp_memory: TmpMemory,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
    expected_identical = ["status", "fetchFileName", "description"]
    actual_details = cast(AuditLogContent, actual_content.get("details", {}))
    details = cast(AuditLogContent, content.get("details", {}))
    reason = details.get("reason", False) if details else False
    item = cast(AuditLogContent, details.get("item", {})) if details else {}

    for label in expected_identical:
        compare_to_expected_if_elem_exist_audit_log(
            content, label, actual_content, task_name
        )
    if reason:
        compare_content_reason_of_task_audit_log(
            reason,
            actual_details["reason"],
            selenium,
            browser_id,
            tmp_memory,
            clipboard,
            displays,
            task_name,
        )
    if item:
        file_id = cast(str, item["fileId"]).split(" ")[1].replace(")", "").split("/")
        item["fileId"] = get_file_id_from_details_modal(
            selenium,
            browser_id,
            file_id[0],
            tmp_memory,
            file_id[1],
            clipboard,
            displays,
        )
        assert_elements_of_task_audit_log_are_the_same(
            item,
            cast(AuditLogContent, actual_details["item"])["value"],
            "Item",
            task_name,
        )


@wt(
    parsers.parse(
        "user of {browser_id} sees that audit log in task "
        '"{task_name}" in {ordinal} parallel box in lane '
        "\"{lane_name}\" doesn't contain user's entry"
    )
)
def assert_content_of_user_task_audit_log(
    selenium: SeleniumDrivers,
    browser_id: str,
    lane_name: str,
    task_name: str,
    ordinal: str,
) -> None:
    click = "click"
    close = "closes"
    link = "Audit log"
    driver = selenium[browser_id]

    click_on_task_in_lane(selenium, browser_id, lane_name, task_name, ordinal, click)
    click_on_link_in_task_box(selenium, browser_id, lane_name, task_name, link, ordinal)
    # wait a moment for modal to open
    time.sleep(1)
    modal = Modals(driver).audit_log
    try:
        modal.user_log  # pylint: disable=pointless-statement
        raise AssertionError(
            f'Audit log in task "{task_name}" in lane'
            f' "{lane_name}" contains user\'s entry'
        )
    except RuntimeError:
        pass
    modal.x()
    click_on_task_in_lane(selenium, browser_id, lane_name, task_name, ordinal, close)


@wt(
    parsers.parse(
        "user of {browser_id} sees expected exception for "
        '{file_name} in "{element}" content of audit log in task '
        '"{task_name}" in {ordinal} parallel box in lane "{lane_name}"'
    )
)
def assert_exception_in_element_content_in_task_audit_log(
    file_name: str,
    element: str,
    selenium: SeleniumDrivers,
    browser_id: str,
    lane_name: str,
    task_name: str,
    ordinal: str,
    clipboard: Clipboard,
    displays: dict[str, str],
    tmp_memory: TmpMemory,
) -> None:
    file_name = file_name.replace('"', "")
    expected_data = tmp_memory["exceptions"][file_name]
    expected_data = list(map(lambda x: x.lower(), expected_data))
    assert_element_content_in_task_audit_log(
        expected_data,
        element,
        selenium,
        browser_id,
        lane_name,
        task_name,
        ordinal,
        clipboard,
        displays,
    )


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{element}" content of audit'
        ' log in task "{task_name}" in {ordinal} parallel box in lane'
        ' "{lane_name}" is {expected_data}'
    )
)
def assert_element_content_in_task_audit_log(
    expected_data: str | list[str],
    element: str,
    selenium: SeleniumDrivers,
    browser_id: str,
    lane_name: str,
    task_name: str,
    ordinal: str,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
    click = "click"
    link = "Audit log"
    close = "closes"
    if isinstance(expected_data, list):
        expected_data = list(map(lambda x: x.replace('"', ""), expected_data))
        expected_data = list(map(lambda x: x.replace("\\n", "\n"), expected_data))
    else:
        expected_data = expected_data.replace('"', "")
        expected_data = expected_data.replace("\\n", "\n")
    driver = selenium[browser_id]
    click_on_task_in_lane(selenium, browser_id, lane_name, task_name, ordinal, click)
    click_on_link_in_task_box(selenium, browser_id, lane_name, task_name, link, ordinal)
    # wait a moment for modal to open
    time.sleep(1)
    modal = Modals(driver).audit_log
    modal.user_log.click()
    modal.copy_json()
    actual_items = json.loads(clipboard.paste(display=displays[browser_id]))
    actual_data = actual_items["content"][element]
    # this is done because of very specific problem with passing (data/)
    # as expected_data
    actual_data = actual_data.replace("(data/) ", "")
    actual_data = actual_data.lower()
    if isinstance(expected_data, list):
        error_message = (
            f'actual {element} content for task:\n "{actual_data}"\n is not '
            f'in expected cases:\n "{expected_data}"'
        )
        assert actual_data in expected_data, error_message
    else:
        error_message = (
            f'actual {element} content for task:\n "{actual_data}"\n is not '
            f'as expected:\n "{expected_data}"'
        )
        assert actual_data == expected_data, error_message
    modal.x()
    click_on_task_in_lane(selenium, browser_id, lane_name, task_name, ordinal, close)


@wt(
    parsers.parse(
        "user of {browser_id} sees that audit log in task"
        ' "{task_name}" in {ordinal} parallel box in lane '
        '"{lane_name}" contains following entry:\n{config}'
    )
)
def assert_content_of_task_audit_log(
    config: str,
    selenium: SeleniumDrivers,
    browser_id: str,
    lane_name: str,
    task_name: str,
    ordinal: str,
    clipboard: Clipboard,
    displays: dict[str, str],
    tmp_memory: TmpMemory,
) -> None:
    expected_identical = ["source", "severity", "timestamp"]
    click = "click"
    link = "Audit log"
    driver = selenium[browser_id]
    data = yaml.load(config, yaml.Loader)
    content = data.get("content", False)
    severity = data.get("severity", False)
    source = data.get("source", False)
    close = "closes"
    # wait a second for workflow to open
    time.sleep(1)
    click_on_task_in_lane(selenium, browser_id, lane_name, task_name, ordinal, click)
    click_on_link_in_task_box(selenium, browser_id, lane_name, task_name, link, ordinal)
    # wait a moment for modal to open
    time.sleep(1)
    modal = Modals(driver).audit_log
    click_on_log_in_workflow_audit_log(driver, severity, source)
    modal.copy_json()
    actual_items = json.loads(clipboard.paste(display=displays[browser_id]))

    for label in expected_identical:
        compare_to_expected_if_elem_exist_audit_log(
            data, label, actual_items, task_name
        )

    if content:
        compare_content_of_task_audit_log(
            content,
            actual_items["content"],
            task_name,
            selenium,
            browser_id,
            tmp_memory,
            clipboard,
            displays,
        )

    try:
        modal.x()
        click_on_task_in_lane(
            selenium,
            browser_id,
            lane_name,
            task_name,
            ordinal,
            close,
        )
    except StaleElementReferenceException:
        pass


@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_log_in_workflow_audit_log(
    driver: WebDriver, severity: str, source: str
) -> None:
    modal = Modals(driver).audit_log
    if severity in ["Error", "Debug"]:
        modal.logs_entry[severity].click()
    elif source == "user":
        modal.user_log.click()
    else:
        modal.logs_entry[0].click()


@wt(
    parsers.parse(
        "user of {browser_id} sees that recent downloaded json "
        "file contains audit log which has the same entries as the "
        "workflow audit log in GUI"
    )
)
def assert_log_entries_in_json_same_as_visible_in_workflow_audit_log(
    browser_id: str,
    tmpdir: LocalPath,
    selenium: SeleniumDrivers,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).audit_log
    path = tmpdir.join(browser_id, "download")
    file_name = os.listdir(path)[-1]
    file_path = tmpdir.join(browser_id, "download", file_name)
    if file_path.isfile():
        with open(file_path) as f:
            data = json.load(f)
            log_entries = len(modal.logs_entry)
            error_message = (
                "there is different number of log entries in file "
                f"{len(data)} and visible {log_entries}"
            )
            assert len(data) == log_entries, error_message
            for i in range(log_entries):
                file_log = data[i]
                idx = log_entries - i - 1
                modal.logs_entry[idx].click()
                modal.copy_json()
                visible_log = json.loads(clipboard.paste(display=displays[browser_id]))
                # remove 'source' from dict
                visible_log.pop("source")
                error_message = (
                    f"logs in file: {file_log} and visible {visible_log}are different"
                )
                assert file_log == visible_log, error_message
                modal.close_details.click()
    else:
        raise AssertionError(f"file {file_name} has not been downloaded")


@wt(
    parsers.parse(
        "user of {browser_id} sees that workflow audit log contains "
        "following system debug entries with description:\n{config}"
    )
)
def assert_workflow_audit_log_contains_entries(
    selenium: SeleniumDrivers,
    browser_id: str,
    tmpdir: LocalPath,
    tmp_memory: TmpMemory,
    config: str,
) -> None:
    _assert_workflow_audit_log_contains_entries(
        selenium, browser_id, tmpdir, tmp_memory, config
    )


def _assert_workflow_audit_log_contains_entries(
    selenium: SeleniumDrivers,
    browser_id: str,
    tmpdir: LocalPath,
    tmp_memory: TmpMemory,
    config: str,
) -> None:
    data = yaml.load(config, yaml.Loader)
    driver = selenium[browser_id]
    modal = Modals(driver).audit_log
    file_path = _get_workflow_audit_log(browser_id, selenium, tmp_memory, tmpdir)

    with open(file_path) as f:
        data_file = json.load(f)
    for expected_entry in data:
        if assert_expected_in_entries(expected_entry, data_file):
            continue
        error_message = f"there is no entry {expected_entry} in workflow audit log"
        raise AssertionError(error_message)
    modal.x()


def assert_expected_in_entries(
    expected_entry: str, entries: list[AuditLogDebugEntry]
) -> bool:
    for actual_entry in entries:
        if compare_audit_log_debug_entries(actual_entry, expected_entry):
            return True
    return False


def compare_audit_log_debug_entries(
    actual_entry: AuditLogDebugEntry, expected_entry: str
) -> bool:
    return expected_entry in actual_entry["content"]["description"] and (
        actual_entry["severity"] == "debug"
    )


@wt(
    parsers.parse(
        "user of {browser_id} sees that workflow audit log contains "
        "entry with info only about file attributes {item_list:ElementsSequence}",
        extra_types={"ElementsSequence": parse_elements_sequence},
    ),
)
def assert_workflow_audit_log_contains_entry(
    selenium: SeleniumDrivers,
    browser_id: str,
    tmpdir: LocalPath,
    tmp_memory: TmpMemory,
    item_list: list[str],
) -> bool:
    file_path = _get_workflow_audit_log(browser_id, selenium, tmp_memory, tmpdir)
    with open(file_path) as f:
        data_file = json.load(f)
    for entry in data_file:
        try:
            content = entry["content"]
            if _assert_all_items_in_json(item_list, content) and (
                len(item_list) == len(content)
            ):
                return True
        except KeyError:
            pass
    error_message = (
        f"there is no entry containing data about {item_list} in workflow audit log"
    )
    raise AssertionError(error_message)


def _assert_all_items_in_json(item_list: list[str], data: AuditLogContent) -> bool:
    for item in item_list:
        if not data.get(item, False):
            return False
    return True


@wt(
    parsers.parse(
        "user of {browser_id} sees that workflow audit log does "
        "not contain any system debug entry"
    )
)
def assert_no_debug_entry_in_workflow_audit_log(
    browser_id: str, selenium: SeleniumDrivers, tmp_memory: TmpMemory, tmpdir: LocalPath
) -> None:
    file_path = _get_workflow_audit_log(browser_id, selenium, tmp_memory, tmpdir)
    with open(file_path) as f:
        data_file: list[AuditLogContent] = json.load(f)
        error_message = "workflow audit log contains debug entry"
        assert not any(
            entry.get("severity", "") == "debug" for entry in data_file
        ), error_message


def _get_workflow_audit_log(
    browser_id: str, selenium: SeleniumDrivers, tmp_memory: TmpMemory, tmpdir: LocalPath
) -> LocalPath:
    driver = selenium[browser_id]
    modal_name = "Workflow audit log"
    path = tmpdir.join(browser_id, "download")
    n_files_before_download = len(os.listdir(path))
    # wait for modal to appear
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    modal = Modals(driver).audit_log
    modal.download_as_json()
    wait_for_file_with_unknown_name_to_download(n_files_before_download, path)
    file_name = os.listdir(path)[-1]
    file_path = tmpdir.join(browser_id, "download", file_name)
    return file_path
