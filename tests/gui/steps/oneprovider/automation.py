"""This module contains gherkin steps to run acceptance tests featuring
wokrflows and their execution in onezone web GUI """

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time
from datetime import datetime

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
