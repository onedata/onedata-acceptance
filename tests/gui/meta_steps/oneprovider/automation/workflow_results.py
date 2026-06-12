"""This module contains meta steps for operations on automation page
concerning workflow results in Oneprovider using web GUI
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
import time

from _pytest._py.path import LocalPath
from selenium.webdriver.remote.webdriver import WebDriver

from tests.conftest import SeleniumDrivers
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import switch_to_iframe
from tests.gui.steps.modals.modal import click_modal_button
from tests.gui.steps.oneprovider.automation.automation_basic import (
    click_on_link_in_task_box,
    click_on_task_in_lane,
    get_op_workflow_visualizer_page,
)
from tests.gui.steps.oneprovider.automation.automation_statuses import (
    assert_task_status_in_parallel_box,
)
from tests.gui.steps.oneprovider.automation.workflow_results_modals import (
    assert_processing_chart,
    get_store_content,
)
from tests.gui.steps.oneprovider.browser import click_and_press_enter_on_item_in_browser
from tests.gui.steps.oneprovider.file_browser import (
    click_on_status_tag_for_file_in_file_browser,
)
from tests.gui.types import Clipboard, DisplayMap, TmpMemory
from tests.gui.utils import Modals
from tests.gui.utils.common.count_checksums import (
    adler32_sum,
    md5_sum,
    sha256_sum,
    sha512_sum,
)
from tests.gui.utils.common.modals.files_modals.tabs_in_details_modal.metadata_tab import (
    MetadataTab,
)
from tests.gui.utils.generic import parse_seq
from tests.gui.utils.oneprovider.automation import WorkflowVisualiser
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


def get_store_details_json(
    driver: WebDriver,
    browser_id: str,
    clipboard: Clipboard,
    displays: DisplayMap,
    store_name: str,
    store_type: str,
) -> dict[str, object]:
    page = get_op_workflow_visualizer_page(driver)
    store_details = json.loads(
        open_modal_and_get_store_content(
            browser_id,
            driver,
            page,
            clipboard,
            displays,
            store_name,
            store_type,
        )
    )

    return store_details


def open_modal_and_get_store_content(
    browser_id: str,
    driver: WebDriver,
    page: WorkflowVisualiser,
    clipboard: Clipboard,
    displays: DisplayMap,
    store_name: str,
    store_type: str,
    index: int = 0,
) -> str:
    page.stores_list[store_name].click()
    modal = Modals(driver).store_details
    store_value = get_store_content(
        modal, store_type, index, clipboard, displays, browser_id
    )
    modal.close()

    return store_value


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{option}" in "{store2}" '
        'store is the same as in "{store1}" store'
    )
)
def compare_store_contents(
    selenium: SeleniumDrivers,
    browser_id: str,
    store1: str,
    store2: str,
    clipboard: Clipboard,
    displays: DisplayMap,
    option: str,
) -> None:
    switch_to_iframe(selenium, browser_id)
    driver = selenium[browser_id]

    page = get_op_workflow_visualizer_page(driver)

    store1_value = json.loads(
        open_modal_and_get_store_content(
            browser_id,
            driver,
            page,
            clipboard,
            displays,
            store1,
            "list",
        )
    )
    store2_value = json.loads(
        open_modal_and_get_store_content(
            browser_id,
            driver,
            page,
            clipboard,
            displays,
            store2,
            "object",
        )
    )

    assert store1_value[option] == store2_value[option], (
        f'"{option}" in {store2} store:{store2_value[option]} \n is not '
        f'equal to "{option}" {store1} store:{store1_value[option]}'
    )


@wt(
    parsers.parse(
        "user of {browser_id} counts checksums {checksum_list} for "
        '"{file_name}" in "{space}" space'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def count_checksums_for_file(
    browser_id: str,
    tmp_memory: TmpMemory,
    file_name: str,
    tmpdir: LocalPath,
    checksum_list: str,
    selenium: SeleniumDrivers,
) -> None:

    click_and_press_enter_on_item_in_browser(
        selenium, browser_id, file_name, tmp_memory, "file browser"
    )
    downloaded_file = tmpdir.join(browser_id, "download", file_name)
    checksums = parse_seq(checksum_list)
    results = {}
    checksum_functions = {
        "adler32_sum": adler32_sum,
        "md5_sum": md5_sum,
        "sha256_sum": sha256_sum,
        "sha512_sum": sha512_sum,
    }

    for checksum in checksums:
        sum_name = checksum + "_sum"
        results[checksum] = checksum_functions[sum_name](downloaded_file)

    tmp_memory["checksums_" + file_name] = results


def checksums_counted_in_workflow(metadata_modal: MetadataTab) -> dict[str, str]:
    result: dict[str, str] = {}
    # wait for modal to load
    time.sleep(0.5)
    for item in metadata_modal.xattrs.entries:
        result[item.key.replace("_key", "")] = item.value
    return result


@wt(
    parsers.parse(
        "user of {browser_id} sees that checksums {checksum_list} for"
        ' "{file_name}" counted in workflow are alike to '
        "those counted earlier by user"
    )
)
def assert_checksums_are_the_same(
    browser_id: str,
    checksum_list: str,
    file_name: str,
    tmp_memory: TmpMemory,
    selenium: SeleniumDrivers,
) -> None:

    status_type = "Metadata"
    modal_name = "Details modal"
    button = "X"
    checksums = parse_seq(checksum_list)

    # checksums needs to be counted in advance using
    # count_checksums_for_file function
    counted_checksum = tmp_memory["checksums_" + file_name]
    click_on_status_tag_for_file_in_file_browser(
        browser_id, status_type, file_name, tmp_memory
    )
    metadata_modal = Modals(selenium[browser_id]).details_modal.metadata
    workflow_checksum = checksums_counted_in_workflow(metadata_modal)

    for key in checksums:
        err_msg = (
            f"{key} checksum counted by user is {counted_checksum[key]},"
            " and is different from checksum counted in workflow: "
            f"{workflow_checksum[key]}"
        )
        assert workflow_checksum[key] == counted_checksum[key], err_msg

    click_modal_button(selenium, browser_id, button, modal_name)


@wt(
    parsers.parse(
        "user of {browser_id} sees that counted checksums"
        ' {checksum_list} for "{file_name}" are alike to those'
        " counted in workflow"
    )
)
def count_checksums_and_compare_them(
    browser_id: str,
    tmp_memory: TmpMemory,
    file_name: str,
    tmpdir: LocalPath,
    checksum_list: str,
    selenium: SeleniumDrivers,
) -> None:
    count_checksums_for_file(
        browser_id,
        tmp_memory,
        file_name,
        tmpdir,
        checksum_list,
        selenium,
    )
    assert_checksums_are_the_same(
        browser_id, checksum_list, file_name, tmp_memory, selenium
    )


@wt(
    parsers.parse(
        'user of {browser_id} sees that status of task "{task}" in '
        '{ordinal} parallel box in "{lane}" lane is one of '
        '"{status1}" or "{status2}"'
    )
)
def assert_status_of_task_is_one_of_two(
    selenium: SeleniumDrivers,
    browser_id: str,
    lane: str,
    task: str,
    ordinal: str,
    status1: str,
    status2: str,
) -> None:
    click = "clicks on"
    close = "closes"
    click_on_task_in_lane(selenium, browser_id, lane, task, ordinal, click)
    try:
        assert_task_status_in_parallel_box(
            selenium, browser_id, ordinal, lane, task, status1
        )
    except AssertionError:
        assert_task_status_in_parallel_box(
            selenium, browser_id, ordinal, lane, task, status2
        )
    click_on_task_in_lane(selenium, browser_id, lane, task, ordinal, close)


@wt(
    parsers.parse(
        'user of {browser_id} sees that status of task "{task}" in '
        '{ordinal} parallel box in "{lane}" lane is '
        '"{expected_status}"'
    )
)
def assert_status_of_task(
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
    assert_task_status_in_parallel_box(
        selenium, browser_id, ordinal, lane, task, expected_status
    )
    click_on_task_in_lane(selenium, browser_id, lane, task, ordinal, close)


@wt(
    parsers.parse(
        "user of {browser_id} sees chart with processing stats after"
        ' opening "{link}" link for task "{task}" in {ordinal}'
        ' parallel box in "{lane}" lane'
    )
)
def open_link_and_assert_processing_stats_chart(
    selenium: SeleniumDrivers,
    browser_id: str,
    lane: str,
    task: str,
    ordinal: str,
    link: str,
) -> None:
    click = "clicks on"
    click_on_task_in_lane(selenium, browser_id, lane, task, ordinal, click)
    click_on_link_in_task_box(selenium, browser_id, lane, task, link, ordinal)
    assert_processing_chart(browser_id, selenium)
