"""This module contains gherkin steps to run acceptance tests featuring
wokrflows statuses in oneprovider web GUI """

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.steps.oneprovider.archives import from_ordinal_number_to_int
from tests.gui.steps.oneprovider.automation.automation_basic import switch_to_automation_page
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


def get_parallel_box(selenium, browser_id, op_container, ordinal, lane):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    workflow_visualiser = page.workflow_visualiser
    number = from_ordinal_number_to_int(ordinal) - 1
    workflow_visualiser.workflow_lanes[
        lane].scroll_to_first_task_in_parallel_box(number)
    return workflow_visualiser.workflow_lanes[lane].parallel_box[number]


@wt(parsers.parse('user of {browser_id} sees "{status}" status in status '
                  'bar in workflow visualizer'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_status_in_workflow_visualizer(selenium, browser_id, op_container,
                                         status):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    assert status in page.workflow_visualiser.status, (f'Workflow status is not'
                                                       f' equal to {status}')


@repeat_failed(timeout=WAIT_BACKEND)
def assert_task_status_in_parallel_box(selenium, browser_id, op_container,
                                       ordinal, lane, task, expected_status):
    box = get_parallel_box(selenium, browser_id, op_container, ordinal, lane)
    actual_status = box.task_list[task].status
    assert_status(task, actual_status, expected_status)


def await_for_task_status_in_parallel_box(selenium, browser_id, op_container,
                                          lane, task, ordinal, expected_status,
                                          seconds):
    box = get_parallel_box(selenium, browser_id, op_container, ordinal, lane)
    t_end = time.time() + int(seconds)
    while time.time() < t_end:
        actual_status = box.task_list[task].status
        if actual_status.lower() == expected_status.lower():
            break
    else:
        raise Exception(f'After awaiting for task "{task}" for {seconds} '
                        f'seconds its status ({actual_status}) is not '
                        f'{expected_status} as expected')


@wt(parsers.parse('user of {browser_id} sees that status of "{lane}" lane in'
                  ' "{workflow}" is "{expected_status}"'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_status_of_lane(selenium, browser_id, op_container, lane,
                          expected_status):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    workflow_visualiser = page.workflow_visualiser
    actual_status = workflow_visualiser.workflow_lanes[lane].status
    assert_status(lane, actual_status, expected_status)


@repeat_failed(timeout=WAIT_FRONTEND)
def get_status(page, option, name):
    if option == 'lane':
        return page.workflow_visualiser.workflow_lanes[name].status
    elif option == 'workflow':
        return page.workflow_visualiser.status


@wt(parsers.re('user of (?P<browser_id>.*) awaits for status of "(?P<name>.*)"'
               ' (?P<option>lane|workflow) to be "(?P<expected_status>.*)"'
               ' maximum of (?P<seconds>.*) seconds'))
def await_for_lane_workflow_status(selenium, browser_id, op_container,
                                   expected_status, name, seconds, option):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    t_end = time.time() + int(seconds)
    while time.time() < t_end:
        actual_status = get_status(page, option, name)
        if actual_status.lower() == expected_status.lower():
            break
    else:
        raise Exception(f'After awaiting for {option} "{name}" for'
                        f' {seconds} seconds its status is not '
                        f'{expected_status} as expected')


@wt(parsers.parse('user of {browser_id} sees that status of "{workflow}"'
                  ' workflow is "{expected_status}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_status_of_workflow_if_needed_wait_for_stopping_status(
        selenium, browser_id, op_container, expected_status, workflow):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    time.sleep(0.5)
    actual_status = page.workflow_visualiser.status
    if expected_status == 'Stopping' and  actual_status == 'Active':
        seconds = 20
        option = 'workflow'
        actual_status = await_for_lane_workflow_status(
            selenium, browser_id, op_container, expected_status, workflow,
            seconds, option)

    assert_status(workflow, actual_status, expected_status)


def assert_status(name, actual_status, expected_status):
    err_msg = (f'Actual "{name}" status: "{actual_status}" does not '
               f'match expected: "{expected_status}"')
    assert actual_status.lower() == expected_status.lower(), err_msg


@wt(parsers.parse('user of {browser_id} clicks "{button}" button on '
                  '"{workflow}" workflow status bar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_on_status_bar(selenium, browser_id, op_container, button):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    getattr(page.workflow_visualiser, transform(button))()


@wt(parsers.re('user of (?P<browser_id>.*) waits for workflow '
               '"(?P<workflow>.*)" to be (paused|cancelled|stopped)'))
def wait_for_workflow_to_be_stopped(selenium, browser_id, op_container):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    status =  page.workflow_visualiser.status
    while status == 'Stopping':
        time.sleep(1)
        status = page.workflow_visualiser.status
