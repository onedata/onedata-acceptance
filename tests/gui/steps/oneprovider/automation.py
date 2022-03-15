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


def _assert_workflow(transfer, desc, sufix, hosts):
    assert getattr(transfer, 'is_workflow')(), \
        'Transferred item is not workflow in {}'.format(sufix)

    desc = yaml.load(desc)
    for key, val in desc.items():
        transfer_val = getattr(transfer, key.replace(' ', '_'))
        assert transfer_val == str(val), \
            'Transfer {} is {} instead of {} in {}'.format(key, transfer_val,
                                                           val, sufix)


@wt(parsers.parse(
    'user of {browser_id} clicks {tab_name} in the navigation bar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_tab_in_automation_subpage(selenium, browser_id, op_container,
                                     tab_name):
    switch_to_iframe(selenium, browser_id)
    driver = selenium[browser_id]
    op_container(driver).automation_page.navigation_tab[tab_name].click()


@wt(parsers.parse('user of {browser_id} chooses to run "{revision}" '
                  'revision of "{workflow}" workflow'))
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_workflow_revision_to_run(selenium, browser_id, op_container,
                                    revision, workflow):
    switch_to_iframe(selenium, browser_id)
    page = op_container(selenium[browser_id]).automation_page
    page.workflow_list[workflow].revision_list[revision].click()


@wt(parsers.parse('user of {browser_id} confirms Workflow deployment '
                  'by clicking Run workflow button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_workflow_revision_to_run(selenium, browser_id, op_container,
                                    revision, workflow):
    switch_to_iframe(selenium, browser_id)
    page = op_container(selenium[browser_id]).automation_page
    page.run_workflow_button.click()


@wt(parsers.re('user of (?P<browser_id>.*) sees workflow'
               ' in ended workflows:\n(?P<desc>(.|\s)*)'))
@repeat_failed(interval=0.5, timeout=90)
def assert_ended_transfer(selenium, browser_id, desc, hosts,
                          op_container):
    transfer = op_container(selenium[browser_id]).automation_page.ended[0]
    _assert_workflow(transfer, desc, 'ended', hosts)


@wt(parsers.re('user of {browser_id} sees {status} status in status '
               'bar in workflow visualizer'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_status_in_workflow_visualizer(selenium, browser_id, op_container,
                                         status):
    switch_to_iframe(selenium, browser_id)
    page = op_container(selenium[browser_id]).automation_page
    assert status in page.workflow_visualiser.status_bar, \
        f'Workflow status is not equal to {status}'


@wt(parsers.parse('user of {browser_id} clicks on "{task_name}" task in "{'
                  'lane_name}" lane in workflow visualizer'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_task_in_lane(selenium, browser_id, op_container, lane_name,
                                     task_name):
    switch_to_iframe(selenium, browser_id)
    page = op_container(selenium[browser_id]).automation_page
    workflow_visualiser = page.workflows_page.workflow_visualiser
    box = workflow_visualiser.workflow_lanes[lane_name].parallel_box
    box.task_list[task_name].click()


@wt(parsers.parse('user of {browser_id} clicks on "{option}" link in '
                  '"{task_name}" task in "{lane_name}" lane '
                  'in workflow visualizer'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_link_in_task_box(selenium, browser_id, op_container, lane_name,
                              task_name):
    switch_to_iframe(selenium, browser_id)
    page = op_container(selenium[browser_id]).automation_page
    workflow_visualiser = page.workflows_page.workflow_visualiser
    box = workflow_visualiser.workflow_lanes[lane_name].parallel_box
    box.task_list[task_name].pods_activity.click()

