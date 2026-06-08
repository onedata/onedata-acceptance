"""This module contains gherkin steps to run acceptance tests featuring
workflows statuses in oneprovider web GUI"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from typing import Any

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.oneprovider.archives import from_ordinal_number_to_int
from tests.gui.steps.oneprovider.automation.automation_basic import (
    search_for_lane_status,
    search_for_task_in_parallel_box,
    switch_to_automation_page,
)
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_FRONTEND)
def get_status_from_workflow_visualizer(page: Any) -> Any:
    return page.workflow_visualiser.status


def get_parallel_box(selenium: Any, browser_id: Any, ordinal: Any, lane: Any) -> Any:
    page = switch_to_automation_page(selenium, browser_id)
    number = from_ordinal_number_to_int(ordinal) - 1
    return search_for_lane_status(selenium[browser_id], page, lane, number)


@wt(
    parsers.parse(
        'user of {browser_id} sees "{status}" status in status '
        "bar in workflow visualizer"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_status_in_workflow_visualizer(
    selenium: Any, browser_id: Any, status: Any
) -> Any:
    page = switch_to_automation_page(selenium, browser_id)
    actual_status = page.workflow_visualiser.status
    assert (
        status in actual_status
    ), f"Workflow status {actual_status} is not equal to {status}"


@repeat_failed(timeout=2 * WAIT_BACKEND)
def assert_task_status_in_parallel_box(
    selenium: Any,
    browser_id: Any,
    ordinal: Any,
    lane: Any,
    task: Any,
    expected_status: Any,
) -> Any:
    driver = selenium[browser_id]
    box = get_parallel_box(selenium, browser_id, ordinal, lane)
    task, task_id = search_for_task_in_parallel_box(driver, box, task)
    try:
        actual_status = driver.find_element(
            By.CSS_SELECTOR, f"#{task_id} .status-detail .detail-value"
        )
    except NoSuchElementException:
        actual_status = task.status

    assert_status(task, actual_status, expected_status)


@repeat_failed(interval=1, timeout=90)
def await_for_task_status_in_parallel_box(
    selenium: Any,
    browser_id: Any,
    lane: Any,
    task: Any,
    ordinal: Any,
    expected_status: Any,
) -> Any:
    box = get_parallel_box(selenium, browser_id, ordinal, lane)
    actual_status = box.task_list[task].status
    err_msg = (
        f'After awaiting for task "{task}" its status ({actual_status})'
        f" is not {expected_status} as expected"
    )
    assert actual_status.lower() == expected_status.lower(), err_msg


@wt(
    parsers.parse(
        'user of {browser_id} sees that status of "{lane}" lane in'
        ' "{workflow}" is "{expected_status}"'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_status_of_lane(
    selenium: Any, browser_id: Any, lane: Any, expected_status: Any
) -> Any:
    page = switch_to_automation_page(selenium, browser_id)
    driver = selenium[browser_id]
    actual_status = search_for_lane_status(driver, page, lane)
    assert_status(lane, actual_status, expected_status)


@repeat_failed(timeout=WAIT_FRONTEND)
def get_status(page: Any, option: Any, name: Any) -> Any:
    if option == "lane":
        return page.workflow_visualiser.workflow_lanes[name].status
    if option == "workflow":
        return page.workflow_visualiser.status
    raise ValueError(f"unknown option {option}")


@wt(
    parsers.re(
        'user of (?P<browser_id>.*) awaits for status of "(?P<name>.*)"'
        ' (?P<option>lane|workflow) to be "(?P<expected_status>.*)"'
    )
)
@repeat_failed(interval=1, timeout=120)
def await_for_lane_or_workflow_status(
    selenium: Any, browser_id: Any, expected_status: Any, name: Any, option: Any
) -> Any:
    page = switch_to_automation_page(selenium, browser_id)
    actual_status = get_status(page, option, name)
    err_msg = (
        f'After awaiting for {option} "{name}" its'
        f" status is not {expected_status} as expected"
    )
    assert actual_status.lower() == expected_status.lower(), err_msg


@wt(
    parsers.parse(
        'user of {browser_id} sees that status of "{workflow}"'
        ' workflow is "{expected_status}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_status_of_workflow(
    selenium: Any, browser_id: Any, expected_status: Any, workflow: Any
) -> Any:
    option = "workflow"
    page = switch_to_automation_page(selenium, browser_id)
    actual_status = get_status(page, option, workflow)
    assert_status(workflow, actual_status, expected_status)


def assert_status(name: Any, actual_status: Any, expected_status: Any) -> Any:
    err_msg = (
        f'Actual "{name}" status: "{actual_status}" does not '
        f'match expected: "{expected_status}"'
    )
    assert actual_status.lower() == expected_status.lower(), err_msg


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) waits for workflow "
        '"(?P<workflow>.*)" to be (?P<option>paused|cancelled|stopped)'
    )
)
@repeat_failed(
    interval=1,
    timeout=360,
)
def wait_for_workflow_to_be_stopped(selenium: Any, browser_id: Any, option: Any) -> Any:
    page = switch_to_automation_page(selenium, browser_id)
    status = page.workflow_visualiser.status
    assert status != "Stopping", f"workflow is not in {option} state"
