"""This module contains gherkin steps to run acceptance tests featuring
wokrflows and their execution in onezone web GUI """

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time
from datetime import datetime

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
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
@repeat_failed(timeout=WAIT_BACKEND)
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
    assert status in page.workflow_visualiser.status, (f'Workflow status is not'
                                                       f' equal to {status}')


def check_if_task_is_opened(task):
    if task.status == '':
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


def get_parallel_box(selenium, browser_id, op_container, ordinal, lane):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    workflow_visualiser = page.workflow_visualiser
    number = from_ordinal_number_to_int(ordinal) - 1
    workflow_visualiser.workflow_lanes[
        lane].scroll_to_first_task_in_parallel_box(number)
    return workflow_visualiser.workflow_lanes[lane].parallel_box[number]


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
                        f'seconds its status is not {expected_status} as '
                        f'expected')


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


@wt(parsers.parse('user of {browser_id} clicks on "{tab_name}" tab in '
                  'automation subpage'))
def change_tab_in_automation_subpage(selenium, browser_id, op_container,
                                     tab_name):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    page.navigation_tab[tab_name].click()
    time.sleep(0.25)


@wt(parsers.re('user of (?P<browser_id>.*) clicks on first executed workflow'))
@repeat_failed(timeout=WAIT_FRONTEND)
def expand_first_executed_workflow_record(selenium, browser_id, op_container):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    change_tab_in_automation_subpage(selenium, browser_id, op_container,
                                     'Ended')
    page.workflow_executions_list[0].click()


@wt(parsers.re('user of (?P<browser_id>.*) clicks on "(?P<workflow>.*)" menu '
               'on workflow executions list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_workflow_menu(selenium, browser_id, op_container, workflow):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    page.workflow_executions_list[workflow].menu_button()


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>does not see|sees)'
               ' "(?P<workflow>.*)" on workflow executions list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_workflow_on_executed_workflows_list(selenium, browser_id,
                                               op_container, workflow, option):

    page = switch_to_automation_page(selenium, browser_id, op_container)

    workflow_executions_list = page.workflow_executions_list
    if option == 'does not see':
        err_msg = f'Workflow: {workflow} is on workflow executions list'
        assert not workflow in workflow_executions_list, err_msg
    else:
        err_msg = f'Workflow: {workflow} is not on workflow executions list'
        assert workflow in workflow_executions_list, err_msg


@wt(parsers.parse('user of {browser_id} sees that "{option}" option in '
                  'data row menu in automation workflows page is disabled'))
def assert_option_disabled_in_automation_page(selenium, browser_id, option, popups):
    err_msg = (f'Option {option} is not disabled in data row menu'
               f' in automation workflows page')
    disabled_options =  popups(selenium[browser_id]
                               ).workflow_menu.disabled_options
    assert option in disabled_options, err_msg


@wt(parsers.parse('user of {browser_id} sees that chart with processing '
                  'stats exist'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_processing_chart(browser_id, selenium, modals):
    switch_to_iframe(selenium, browser_id)
    modal = modals(selenium[browser_id]).task_time_series
    assert modal.chart, 'chart with processing stats is not visible'


@wt(parsers.parse('user of {browser_id} sees that time in right corner of chart'
                  ' with processing stats is around actual time'))
def assert_time_on_lower_right_corner_of_chart_is_around_actual_time(
        browser_id, selenium, modals):
    switch_to_iframe(selenium, browser_id)
    modal = modals(selenium[browser_id]).task_time_series
    chart_time_in_right_corner = modal.get_time_from_chart()[-1]
    now = datetime.now()
    ts = datetime.timestamp(now)
    assert abs(chart_time_in_right_corner - ts) < 120, (
        'Difference between actual time and time on chart is bigger than 120s')


@wt(parsers.parse('user of {browser_id} sees that value of last column on chart'
                  ' with processing stats is bigger than zero'))
def asser_value_of_last_column_is_bigger_than_zero(browser_id, selenium,
                                                   modals):
    switch_to_iframe(selenium, browser_id)
    modal = modals(selenium[browser_id]).task_time_series
    values = modal.get_last_column_value()
    err_msg = (f'Last column {values[0][1]} is {values[0][0]} and'
               f' {values[1][1]} is {values[1][0]} when one of them should be '
               f'bigger than zero')
    assert (values[0][0] > 0 or values[1][0] > 0), err_msg


@wt(parsers.parse('user of {browser_id} chooses "{resolution}" resolution from'
                  ' time resolution list in modal "{modal}"'))
def choose_time_resolution(selenium, browser_id, popups, resolution, modal):
    driver = selenium[browser_id]
    for option in popups(driver).time_resolutions_list:
        if option.text == resolution:
            option.click()
            break
    else:
        raise Exception(f'There is no {resolution} in time resolution'
                        f' list in modal "{modal}".')


@wt(parsers.parse('user of {browser_id} sees that {option} processing speed'
                  ' is not bigger than {number} per second on chart with'
                  ' processing stats'))
def assert_number_of_proceeded_files(browser_id, selenium, modals, option,
                                     number):
    switch_to_iframe(selenium, browser_id)
    modal = modals(selenium[browser_id]).task_time_series
    values = modal.get_last_column_value()
    for value in values:
        if option in value[1].lower():
            err_msg = (f'Processing speed is {value[0]} {option} per second '
                       f'and is bigger than expected {number} per second.')
            assert value[0] <= int(number), err_msg
            break
    else:
        raise Exception(f'There is no {option} processing speed on chart with'
                        f' processing stat.')
