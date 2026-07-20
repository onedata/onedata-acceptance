"""This module contains gherkin steps to run acceptance tests featuring
workflows statuses in oneprovider web GUI"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.oneprovider.archives import from_ordinal_number_to_int
from tests.gui.steps.oneprovider.automation.automation_basic import (
    search_for_lane_status,
    search_for_task_in_parallel_box,
    switch_to_automation_page,
)
from tests.gui.utils.oneprovider.automation import ParallelBox, WorkflowExecutionPage
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_FRONTEND)
def get_status_from_workflow_visualizer(page: WorkflowExecutionPage) -> str:
    return page.workflow_visualiser.status


def get_parallel_box(
    selenium: SeleniumDrivers, browser_id: str, ordinal: str, lane: str
) -> ParallelBox:
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
    selenium: SeleniumDrivers, browser_id: str, status: str
) -> None:
    page = switch_to_automation_page(selenium, browser_id)
    actual_status = page.workflow_visualiser.status
    assert (
        status in actual_status
    ), f"Workflow status {actual_status} is not equal to {status}"


@repeat_failed(timeout=2 * WAIT_BACKEND)
def assert_task_status_in_parallel_box(
    selenium: SeleniumDrivers,
    browser_id: str,
    ordinal: str,
    lane: str,
    task: str,
    expected_status: str,
) -> None:
    driver = selenium[browser_id]
    box = get_parallel_box(selenium, browser_id, ordinal, lane)
    task_page, task_id = search_for_task_in_parallel_box(driver, box, task)
    try:
        actual_status = driver.find_element(
            By.CSS_SELECTOR, f"#{task_id} .status-detail .detail-value"
        ).text
    except NoSuchElementException:
        actual_status = task_page.status

    assert_status(task_page, actual_status, expected_status)


@repeat_failed(interval=1, timeout=90)
def await_for_task_status_in_parallel_box(
    selenium: SeleniumDrivers,
    browser_id: str,
    lane: str,
    task: str,
    ordinal: str,
    expected_status: str,
) -> None:
    box = get_parallel_box(selenium, browser_id, ordinal, lane)
    actual_status = box.task_list[task].status
    error_message = (
        f'After awaiting for task "{task}" its status ({actual_status})'
        f" is not {expected_status} as expected"
    )
    assert actual_status.lower() == expected_status.lower(), error_message


@wt(
    parsers.parse(
        'user of {browser_id} sees that status of "{lane}" lane in'
        ' "{workflow}" is "{expected_status}"'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_status_of_lane(
    selenium: SeleniumDrivers, browser_id: str, lane: str, expected_status: str
) -> None:
    page = switch_to_automation_page(selenium, browser_id)
    driver = selenium[browser_id]
    actual_status = search_for_lane_status(driver, page, lane)
    assert_status(lane, actual_status, expected_status)


@repeat_failed(timeout=WAIT_FRONTEND)
def get_status(page: WorkflowExecutionPage, option: str, name: str) -> str:
    if option == "lane":
        return page.workflow_visualiser.workflow_lanes[name].status
    if option == "workflow":
        return page.workflow_visualiser.status
    raise ValueError(f"unknown option {option}")


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) awaits for status of "(?P<name>.*)"'
        r' (?P<option>lane|workflow) to be "(?P<expected_status>.*)"'
    )
)
@repeat_failed(interval=1, timeout=120)
def await_for_lane_or_workflow_status(
    selenium: SeleniumDrivers,
    browser_id: str,
    expected_status: str,
    name: str,
    option: str,
) -> None:
    page = switch_to_automation_page(selenium, browser_id)
    actual_status = get_status(page, option, name)
    error_message = (
        f'After awaiting for {option} "{name}" its'
        f" status is not {expected_status} as expected"
    )
    assert actual_status.lower() == expected_status.lower(), error_message


@wt(
    parsers.parse(
        'user of {browser_id} sees that status of "{workflow}"'
        ' workflow is "{expected_status}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_status_of_workflow(
    selenium: SeleniumDrivers,
    browser_id: str,
    expected_status: str,
    workflow: str,
) -> None:
    option = "workflow"
    page = switch_to_automation_page(selenium, browser_id)
    actual_status = get_status(page, option, workflow)
    assert_status(workflow, actual_status, expected_status)


def assert_status(name: object, actual_status: str, expected_status: str) -> None:
    error_message = (
        f'Actual "{name}" status: "{actual_status}" does not '
        f'match expected: "{expected_status}"'
    )
    assert actual_status.lower() == expected_status.lower(), error_message


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) waits for workflow "
        r'"(?P<workflow>.*)" to be (?P<option>paused|cancelled|stopped)'
    )
)
@repeat_failed(
    interval=1,
    timeout=360,
)
def wait_for_workflow_to_be_stopped(
    selenium: SeleniumDrivers, browser_id: str, option: str
) -> None:
    page = switch_to_automation_page(selenium, browser_id)
    status = page.workflow_visualiser.status
    assert status != "Stopping", f"workflow is not in {option} state"
