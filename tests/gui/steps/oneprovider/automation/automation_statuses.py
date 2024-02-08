"""This module contains gherkin steps to run acceptance tests featuring
workflows statuses in oneprovider web GUI """

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time

from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException)
from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.steps.oneprovider.archives import from_ordinal_number_to_int
from tests.gui.steps.oneprovider.automation.automation_basic import (
    switch_to_automation_page, search_for_lane_status,
    search_for_task_in_parallel_box)
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_FRONTEND)
def get_status_from_workflow_visualizer(page):
    return page.workflow_visualiser.status


def get_parallel_box(selenium, browser_id, op_container, ordinal, lane):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    number = from_ordinal_number_to_int(ordinal) - 1
    return search_for_lane_status(
        selenium[browser_id], page, lane, number)


@wt(parsers.parse('user of {browser_id} sees "{status}" status in status '
                  'bar in workflow visualizer'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_status_in_workflow_visualizer(selenium, browser_id, op_container,
                                         status):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    assert status in page.workflow_visualiser.status, (f'Workflow status is not'
                                                       f' equal to {status}')


@repeat_failed(timeout=2*WAIT_BACKEND)
def assert_task_status_in_parallel_box(selenium, browser_id, op_container,
                                       ordinal, lane, task, expected_status):
    driver = selenium[browser_id]
    box = get_parallel_box(selenium, browser_id, op_container, ordinal, lane)
    task, task_id = search_for_task_in_parallel_box(driver, box, task)
    try:
        actual_status = driver.find_element_by_css_selector(
            f'#{task_id} .status-detail .detail-value')
    except NoSuchElementException:
        actual_status = task.status

    assert_status(task, actual_status, expected_status)


@repeat_failed(interval=1, timeout=90, exceptions=AssertionError)
def await_for_task_status_in_parallel_box(selenium, browser_id, op_container,
                                          lane, task, ordinal, expected_status):
    box = get_parallel_box(selenium, browser_id, op_container, ordinal, lane)
    actual_status = box.task_list[task].status
    err_msg = (f'After awaiting for task "{task}" its status ({actual_status})'
               f' is not {expected_status} as expected')
    assert actual_status.lower() == expected_status.lower(), err_msg


@wt(parsers.parse('user of {browser_id} sees that status of "{lane}" lane in'
                  ' "{workflow}" is "{expected_status}"'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_status_of_lane(selenium, browser_id, op_container, lane,
                          expected_status):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    driver = selenium[browser_id]
    actual_status = search_for_lane_status(driver, page, lane)
    assert_status(lane, actual_status, expected_status)


@repeat_failed(timeout=WAIT_FRONTEND)
def get_status(page, option, name):
    if option == 'lane':
        return page.workflow_visualiser.workflow_lanes[name].status
    elif option == 'workflow':
        return page.workflow_visualiser.status


@wt(parsers.re('user of (?P<browser_id>.*) awaits for status of "(?P<name>.*)"'
               ' (?P<option>lane|workflow) to be "(?P<expected_status>.*)"'))
@repeat_failed(interval=1, timeout=120, exceptions=AssertionError)
def await_for_lane_workflow_status(selenium, browser_id, op_container,
                                   expected_status, name, option):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    actual_status = get_status(page, option, name)
    err_msg = (f'After awaiting for {option} "{name}" its'
               f' status is not {expected_status} as expected')
    assert actual_status.lower() == expected_status.lower(), err_msg


@wt(parsers.parse('user of {browser_id} sees that status of "{workflow}"'
                  ' workflow is "{expected_status}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_status_of_workflow_if_needed_wait_for_stopping_status(
        selenium, browser_id, op_container, expected_status, workflow):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    time.sleep(0.5)
    actual_status = page.workflow_visualiser.status
    if expected_status == 'Stopping' and actual_status == 'Active':
        option = 'workflow'
        actual_status = await_for_lane_workflow_status(
            selenium, browser_id, op_container, expected_status, workflow,
            option)

    assert_status(workflow, actual_status, expected_status)


def assert_status(name, actual_status, expected_status):
    err_msg = (f'Actual "{name}" status: "{actual_status}" does not '
               f'match expected: "{expected_status}"')
    assert actual_status.lower() == expected_status.lower(), err_msg


@wt(parsers.re('user of (?P<browser_id>.*) waits for workflow '
               '"(?P<workflow>.*)" to be (?P<option>paused|cancelled|stopped)'))
@repeat_failed(interval=1, timeout=360,
               exceptions=(AssertionError, StaleElementReferenceException))
def wait_for_workflow_to_be_stopped(selenium, browser_id, op_container, option):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    status = page.workflow_visualiser.status
    assert status != 'Stopping', f'workflow have not {option}'
