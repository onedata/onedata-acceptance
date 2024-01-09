"""This module contains gherkin steps to run acceptance tests featuring
workflows and their execution in oneprovider web GUI """

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.steps.oneprovider.archives import from_ordinal_number_to_int
from tests.gui.utils.core import scroll_to_css_selector
from tests.utils.bdd_utils import wt, parsers
from tests.gui.utils.generic import transform
from tests.utils.utils import repeat_failed
from tests.gui.steps.common.miscellaneous import (
    switch_to_iframe, click_option_in_popup_labeled_menu)


# this step is created to avoid using repeat_failed in metasteps
@repeat_failed(timeout=WAIT_FRONTEND)
def get_op_workflow_visualizer_page(op_container, driver):
    return op_container(driver).automation_page.workflow_visualiser


def switch_to_automation_page(selenium, browser_id, op_container):
    switch_to_iframe(selenium, browser_id)
    return op_container(selenium[browser_id]).automation_page


@repeat_failed(timeout=WAIT_FRONTEND)
def get_input_element(op_container, driver, input_type):
    op_container(driver).automation_page.input_link.click()
    return getattr(op_container(driver).automation_page, input_type)


@wt(parsers.parse('user of {browser_id} clicks "{tab_name}" '
                  'in the automation tab bar'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_button_in_navigation_tab(selenium, browser_id, op_container,
                                   tab_name):
    switch_to_iframe(selenium, browser_id)
    driver = selenium[browser_id]
    try:
        op_container(driver).automation_page.navigation_tab[tab_name].click()
    except RuntimeError:
        driver.refresh()
        # wait for page to refresh
        time.sleep(5)
        switch_to_iframe(selenium, browser_id)
        op_container(driver).automation_page.navigation_tab[tab_name].click()


@wt(parsers.re('user of (?P<browser_id>.*?) chooses to run '
               '(?P<ordinal>1st|2nd|3rd|4th|5th|6th) revision of '
               '"(?P<workflow>.*?)" workflow'))
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_workflow_revision_to_run(selenium, browser_id, op_container,
                                    ordinal, workflow):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    revision = int(ordinal[:-2]) - 1
    page.available_workflow_list[workflow].revision_list[revision].click()


@wt(parsers.parse('user of {browser_id} confirms workflow execution '
                  'by clicking "Run workflow" button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_workflow_to_execute(selenium, browser_id, op_container):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    page.run_workflow_button.click()


def check_if_task_is_opened(task):
    return task.status != ''


def search_for_lane_status(driver, page, lane_name, box_number=None):
    workflow_visualiser = page.workflow_visualiser
    number_of_lanes = len(workflow_visualiser.workflow_lanes)

    for i in range(number_of_lanes):
        lane_id = workflow_visualiser.workflow_lanes[
            i].lane_web_elem.get_attribute('id')
        scroll_to_css_selector(driver, f'#{lane_id}')
        found_lane = driver.find_element_by_css_selector(
            f'#{lane_id} .lane-name').text
        if found_lane == lane_name:
            if box_number is not None:
                return workflow_visualiser.workflow_lanes[i].parallel_boxes[
                    box_number]
            status = driver.find_element_by_css_selector(
                f'#{lane_id} .visible-run-status-label').text
            return status
        else:
            try:
                page.workflow_visualiser.right_arrow_scroll.click()
            except RuntimeError:
                pass


def search_for_task_in_parallel_box(driver, parallel_box, task_name):
    number_of_tasks = len(parallel_box.task_list)
    for j in range(number_of_tasks):
        task_id = parallel_box.task_list[j].name_web_elem.get_attribute('id')
        scroll_to_css_selector(driver, f'#{task_id}')
        found_task = driver.find_element_by_css_selector(f'#{task_id}').text

        if found_task == task_name:
            return parallel_box.task_list[j], task_id


@wt(parsers.re('user of (?P<browser_id>.*?) (?P<option>clicks on|closes) task '
               '"(?P<task_name>.*?)" in (?P<ordinal>.*?) parallel box in '
               '"(?P<lane_name>.*?)" lane in workflow visualizer'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_task_in_lane(selenium, browser_id, op_container, lane_name,
                          task_name, ordinal, option):
    number = from_ordinal_number_to_int(ordinal) - 1
    page = switch_to_automation_page(selenium, browser_id, op_container)
    driver = selenium[browser_id]

    parallel_box = search_for_lane_status(driver, page, lane_name, number)
    time.sleep(1)
    if len(parallel_box.task_list) == 1:
        task = parallel_box.task_list[0]
    else:
        task, task_id = search_for_task_in_parallel_box(driver, parallel_box,
                                                        task_name)
    # wait a moment to find parallel box
    time.sleep(1)
    if option == 'closes':
        if check_if_task_is_opened(task):
            if len(parallel_box.task_list) > 1:
                scroll_to_css_selector(driver, f'.task-drag-handle')
            # wait a moment for scroll
            time.sleep(1)
            task.click_on_drag_handle()
        # wait for task to be closed
        time.sleep(2)
        assert not check_if_task_is_opened(task), (
            f'Failed to close {task_name} task in parallel box')
    else:
        if not check_if_task_is_opened(task):
            if len(parallel_box.task_list) > 1:
                scroll_to_css_selector(driver, f'#{task_id}')
            # wait a moment for scroll
            time.sleep(1)
            task.click_on_drag_handle()


@wt(parsers.parse('user of {browser_id} clicks on link "{option}" in '
                  '"{task_name}" task in {ordinal} parallel box in '
                  '"{lane_name}" lane in workflow visualizer'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_link_in_task_box(selenium, browser_id, op_container, lane_name,
                              task_name, option, ordinal):
    number = from_ordinal_number_to_int(ordinal) - 1
    page = switch_to_automation_page(selenium, browser_id, op_container)
    driver = selenium[browser_id]

    parallel_box = search_for_lane_status(driver, page, lane_name, number)
    task, task_id = search_for_task_in_parallel_box(driver, parallel_box,
                                                    task_name)

    scroll_to_css_selector(driver, f'#{task_id}')
    parallel_box.scroll_to_bottom_of_task_in_parallel_box(task_id)
    time.sleep(0.5)

    task.click_on_option_in_task(option)


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


@wt(parsers.re('user of (?P<browser_id>.*) clicks on "(?P<workflow>.*)" '
               'on workflow executions list'))
def click_and_enter_workflow(selenium, browser_id, op_container, workflow):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    page.workflow_executions_list[workflow].click()


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>does not see|sees)'
               ' "(?P<workflow>.*)" on workflow executions list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_workflow_on_executed_workflows_list(selenium, browser_id,
                                               op_container, workflow, option):
    page = switch_to_automation_page(selenium, browser_id, op_container)

    workflow_executions_list = page.workflow_executions_list
    if option == 'does not see':
        err_msg = f'Workflow: {workflow} is on workflow executions list'
        assert workflow not in workflow_executions_list, err_msg
    else:
        err_msg = f'Workflow: {workflow} is not on workflow executions list'
        assert workflow in workflow_executions_list, err_msg


@wt(parsers.parse('user of {browser_id} sees that "{option}" option in '
                  'data row menu in automation workflows page is disabled'))
def assert_option_disabled_in_automation_page(selenium, browser_id, option,
                                              popups):
    err_msg = (f'Option {option} is not disabled in data row menu'
               f' in automation workflows page')
    disabled_options = popups(selenium[browser_id]
                              ).workflow_menu.disabled_options
    assert option in disabled_options, err_msg


@wt(parsers.parse('user of {browser_id} clicks "{option}" option in run menu '
                  'for "{lane_name}" lane'))
def click_option_for_lane(selenium, browser_id, op_container, lane_name,
                          option, popups):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    workflow_visualiser = page.workflow_visualiser
    lane = workflow_visualiser.workflow_lanes[lane_name]
    lane.latest_run_menu()
    click_option_in_popup_labeled_menu(selenium, browser_id, option, popups)


@wt(parsers.parse('user of {browser_id} clicks "{button}" button on '
                  '"{workflow}" workflow status bar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_on_status_bar(selenium, browser_id, op_container, button):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    time.sleep(1)
    getattr(page.workflow_visualiser, transform(button))()


@wt(parsers.re('user of (?P<browser_id>.*) clicks on (?P<ordinal>|1st|2nd'
               '|3rd|4th) revision of "(?P<workflow>.*)" in workflows list '
               'in inventory workflows subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_workflow_in_inventory_subpage(oz_page, selenium, browser_id,
                                           ordinal, workflow):
    page = oz_page(selenium[browser_id])['automation']
    revision = int(ordinal[:-2]) - 1
    page.workflows_page.elements_list[workflow].revision_list[revision].click()
