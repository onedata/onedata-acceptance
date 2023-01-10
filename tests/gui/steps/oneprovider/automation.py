"""This module contains gherkin steps to run acceptance tests featuring
wokrflows and their execution in onezone web GUI """

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time
import yaml

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.utils.generic import transform, upload_file_path
from tests.utils.bdd_utils import wt, parsers
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.utils import repeat_failed
from tests.gui.steps.common.miscellaneous import press_enter_on_active_element, \
    switch_to_iframe


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


@wt(parsers.parse('user of {browser_id} clicks on "{task_name}" task in '
                  '"{lane_name}" lane in workflow visualizer'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_task_in_lane(selenium, browser_id, op_container, lane_name,
                          task_name):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    workflow_visualiser = page.workflow_visualiser
    box = workflow_visualiser.workflow_lanes[lane_name].parallel_box
    box.task_list[task_name].click()


@wt(parsers.parse('user of {browser_id} clicks on "{option}" link in '
                  '"{task_name}" task in "{lane_name}" lane '
                  'in workflow visualizer'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_link_in_task_box(selenium, browser_id, op_container, lane_name,
                              task_name, option):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    workflow_visualiser = page.workflow_visualiser
    box = workflow_visualiser.workflow_lanes[lane_name].parallel_box
    getattr(box.task_list[task_name], transform(option)).click()


@wt(parsers.parse('user of {browser_id} sees that chart with processing stats exist'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_elem_on_processing_chart(browser_id, selenium, modals):
    switch_to_iframe(selenium, browser_id)
    modal = modals(selenium[browser_id]).task_time_series
    assert modal.chart, 'chart with processing stats is not visible'
