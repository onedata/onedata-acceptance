"""This module contains gherkin steps to run acceptance tests featuring
wokrflows and their execution in onezone web GUI """

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.oneprovider.archives import from_ordinal_number_to_int
from tests.utils.bdd_utils import wt, parsers
from tests.gui.utils.generic import transform
from tests.utils.utils import repeat_failed
from tests.gui.steps.common.miscellaneous import switch_to_iframe


def switch_to_automation_page(selenium, browser_id, op_container):
    switch_to_iframe(selenium, browser_id)
    return op_container(selenium[browser_id]).automation_page


@wt(parsers.parse('user of {browser_id} clicks "{tab_name}" '
                  'in the automation tab bar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_in_navigation_tab(selenium, browser_id, op_container,
                                   tab_name):
    switch_to_iframe(selenium, browser_id)
    driver = selenium[browser_id]
    op_container(driver).automation_page.navigation_tab[tab_name].click()


@wt(parsers.re('user of (?P<browser_id>.*?) chooses to run '
               '(?P<ordinal>1st|2nd|3rd|4th) revision of '
               '"(?P<workflow>.*?)" workflow'))
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_workflow_revision_to_run(selenium, browser_id, op_container,
                                    ordinal, workflow):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    page.available_workflow_list[workflow].revision_list[ordinal[:-2]].click()


@wt(parsers.parse('user of {browser_id} confirms workflow execution '
                  'by clicking "Run workflow" button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_workflow_to_execute(selenium, browser_id, op_container):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    page.run_workflow_button.click()


@wt(parsers.parse('user of {browser_id} sees "{status}" status in status '
                  'bar in workflow visualizer'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_status_in_workflow_visualizer(selenium, browser_id, op_container,
                                         status):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    assert status in page.workflow_visualiser.status_bar, \
        f'Workflow status is not equal to {status}'


def check_if_task_is_opened(task):
    if task.instance_id == '':
        return False
    else:
        return True


@wt(parsers.re('user of (?P<browser_id>.*?) (?P<option>clicks on|closes) task '
               '"(?P<task_name>.*?)" in (?P<ordinal>.*?) parallel box in '
               '"(?P<lane_name>.*?)" lane in workflow visualizer'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_task_in_lane(selenium, browser_id, op_container, lane_name,
                          task_name, ordinal, option):
    number = from_ordinal_number_to_int(ordinal) - 1
    page = switch_to_automation_page(selenium, browser_id, op_container)
    workflow_visualiser = page.workflow_visualiser
    box = workflow_visualiser.workflow_lanes[lane_name].parallel_box[number]
    task = box.task_list[task_name]
    if option == 'closes':
        if check_if_task_is_opened(task):
            task.drag_handle.click()
        # wait for task to be closed
        time.sleep(2)
        assert not check_if_task_is_opened(task), (
                f'Failed to close {task_name} task in parallel box')
    else:
        task.drag_handle.click()


@wt(parsers.parse('user of {browser_id} clicks on link "{option}" in '
                  '"{task_name}" task in {ordinal} parallel box in '
                  '"{lane_name}" lane in workflow visualizer'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_link_in_task_box(selenium, browser_id, op_container, lane_name,
                              task_name, option, ordinal):
    number = from_ordinal_number_to_int(ordinal) - 1
    page = switch_to_automation_page(selenium, browser_id, op_container)
    workflow_visualiser = page.workflow_visualiser
    box = workflow_visualiser.workflow_lanes[lane_name].parallel_box[number]
    getattr(box.task_list[task_name], transform(option)).click()



@wt(parsers.parse('user of {browser_id} closes modal "Function pods activity"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def close_pods_activity_modal(selenium, browser_id, op_container):
    # In modal "Function pods activity" there is no 'X' button (this will be
    # resolved in VFS-10324) so closing modal is handled by clicking in
    # the background.
    page = switch_to_automation_page(selenium, browser_id, op_container)
    page.click_on_background_in_workflow_visualiser()


def assert_task_status_in_parallel_box(selenium, browser_id, op_container,
                                       ordinal, lane, task, expected_status):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    workflow_visualiser = page.workflow_visualiser
    number = from_ordinal_number_to_int(ordinal) - 1
    box = workflow_visualiser.workflow_lanes[lane].parallel_box[number]
    actual_status = box.task_list[task].status
    assert_status(task, actual_status, expected_status)



@wt(parsers.parse('user of {browser_id} sees that status of "{lane}" lane in'
                  ' "{workflow}" is "{expected_status}"'))
def assert_status_of_lane(selenium, browser_id, op_container, lane,
                          expected_status):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    workflow_visualiser = page.workflow_visualiser
    actual_status = workflow_visualiser.workflow_lanes[lane].status
    assert_status(lane, actual_status, expected_status)


@wt(parsers.parse('user of {browser_id} sees that status of "{workflow}"'
                  ' workflow is "{expected_status}"'))
def assert_status_of_workflow(selenium, browser_id, op_container,
                              expected_status, workflow):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    actual_status = page.workflow_visualiser.status_bar
    assert_status(workflow, actual_status, expected_status)


def assert_status(name, actual_status, expected_status):
    err_msg = (f'Actual "{name}" status: "{actual_status}" does not '
               f'match expected: "{expected_status}"')
    assert actual_status == expected_status, err_msg
