"""This module contains meta steps for operations on automation page checking
pods activity in Oneprovider using web GUI
"""
__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import time
import yaml

from selenium.common.exceptions import StaleElementReferenceException

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import switch_to_iframe
from tests.gui.steps.modals.modal import (
    click_modal_button)
from tests.gui.steps.oneprovider.automation.automation_basic import (
    click_on_task_in_lane, click_on_link_in_task_box)
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


def change_tab_in_function_pods_activity_modal(modal, tab_name):
    tab_number = 0 if tab_name == 'Current' else 1

    time.sleep(0.25)
    modal.tabs[tab_number].click()
    time.sleep(0.25)


@wt(parsers.parse('user of {browser_id} waits for all pods to '
                  'finish execution in modal "Function pods activity"'))
@repeat_failed(interval=1, timeout=180,
               exceptions=(AssertionError, StaleElementReferenceException))
def wait_for_ongoing_pods_to_be_terminated(selenium, browser_id, modals):
    switch_to_iframe(selenium, browser_id)
    modal = modals(selenium[browser_id]).function_pods_activity
    change_tab_in_function_pods_activity_modal(modal, 'Current')

    assert len(modal.pods_list) == 0, 'Pods has not been terminated'


@wt(parsers.parse('user of {browser_id} sees that name of first pod in tab '
                  '"{tab}" in modal "Function pods activity" contains lambda '
                  'name "{lambda_name}"'))
def assert_lambda_name_in_tab_name(selenium, browser_id, modals, tab,
                                   lambda_name):
    switch_to_iframe(selenium, browser_id)
    modal = modals(selenium[browser_id]).function_pods_activity
    change_tab_in_function_pods_activity_modal(modal, tab)
    pod_name = modal.pods_list[0].pod_name
    err_msg = (f'Pod name: "{pod_name}" does not contain '
               f'lambda name: "{lambda_name}"')
    assert lambda_name in pod_name, err_msg


@wt(parsers.parse('user of {browser_id} clicks on first pod in tab "{tab}" '
                  'in modal "Function pods activity"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_first_pod(selenium, browser_id, modals, tab):
    switch_to_iframe(selenium, browser_id)
    modal = modals(selenium[browser_id]).function_pods_activity
    change_tab_in_function_pods_activity_modal(modal, tab)
    modal.pods_list[0].click()


@wt(parsers.parse('user of {browser_id} clicks on first terminated pod in '
                  'modal "Function pods activity"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_first_terminated_pod(selenium, browser_id, modals):
    switch_to_iframe(selenium, browser_id)
    modal = modals(selenium[browser_id]).function_pods_activity
    change_tab_in_function_pods_activity_modal(modal, 'All')

    modal.pods_list[0].click()


def gather_events_list(modal, driver, option):
    gathered_list = []
    number = modal.get_number_of_data_rows(driver)
    for i in reversed(range(int(number)+1)):
        elem = modal.get_elem_by_data_row_id(i, driver, option)
        gathered_list.append(elem)
    return gathered_list


@wt(parsers.re('user of (?P<browser_id>.*) sees events in modal '
               '"Function pods activity" with following '
               '(?P<option>reason|message)s:\n(?P<events>(.|\s)*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_events_in_pods_monitor(selenium, browser_id, modals, events,
                                  option):

    driver = selenium[browser_id]
    switch_to_iframe(selenium, browser_id)
    modal = modals(driver).function_pods_activity
    events_list = [event for event in yaml.load(events) if '+' not in event]
    gathered_list = gather_events_list(modal, driver, option)

    for event in events_list:
        assert event in gathered_list, f'{option}: {event} has not been found'


@wt(parsers.re('user of (?P<browser_id>.*) sees events in modal '
               '"Function pods activity" that contains lambda name '
               '"(?P<lambda_name>.*)" and following '
               '(?P<option>reason|message)s:\n(?P<events>(.|\s)*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_events_containing_lambda_name(selenium, browser_id, modals, events,
                                         option, lambda_name):
    driver = selenium[browser_id]
    switch_to_iframe(selenium, browser_id)
    modal = modals(driver).function_pods_activity
    events_list = [event.replace('"', '').split(' + ')[1] for event
                   in yaml.load(events) if '+' in event]
    if not events_list:
        events_list = yaml.load(events)
    gathered_list = gather_events_list(modal, driver, option)

    for event in events_list:
        matching = []
        for elem in gathered_list:
            if event in elem and lambda_name in elem:
                matching.append(elem)
                break

        err_msg = (f'{option}: {event} that contains {lambda_name} has not '
                   f'been found')
        assert matching != [], err_msg


def get_lambda_name(events):
    events_list = yaml.load(events)
    for event in events_list:
        if '+' in event:
            lambda_name = event.replace('message that contains: ',
                                        '').replace('"', '').split(' + ')[0]
            return lambda_name


@wt(parsers.re('user of (?P<browser_id>.*) sees following "(?P<link>.*)" '
               '(?P<option>reason|message)s for task "(?P<task>.*)" in '
               '(?P<ordinal>.*) parallel box in "(?P<lane>.*)" lane '
               '(?P<if_finished>after workflow execution is finished|during '
               'workflow execution):\n(?P<events>(.|\s)*)'))
def checks_events_for_task(selenium, browser_id, op_container, lane, task,
                           ordinal, link, modals, if_finished, option, events):
    click = 'clicks on'
    close = 'closes'
    button = 'X'
    modal =  'Function pods activity'

    click_on_task_in_lane(selenium, browser_id, op_container, lane,
                          task, ordinal, click)
    click_on_link_in_task_box(selenium, browser_id, op_container, lane, task,
                              link, ordinal)
    if 'finished' in if_finished:
        wait_for_ongoing_pods_to_be_terminated(selenium, browser_id, modals)
        click_on_first_terminated_pod(selenium, browser_id, modals)

    assert_events_in_pods_monitor(selenium, browser_id, modals, events,
                                  option)
    lambda_name =  get_lambda_name(events)

    assert_events_containing_lambda_name(selenium, browser_id, modals, events,
                                         option, lambda_name)
    click_modal_button(selenium, browser_id, button, modal, modals)
    click_on_task_in_lane(selenium, browser_id, op_container, lane, task,
                          ordinal, close)


@wt(parsers.parse('user of {browser_id} sees that name of first pod in tab'
                  ' "{tab}" for task "{task}" in {ordinal} parallel box in '
                  '"{lane}" lane contains lambda name "{lambda_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_pod_name_for_task(selenium, browser_id, op_container, lane,
                          task, ordinal, modals, tab, lambda_name):
    click = 'clicks on'
    close = 'closes'
    link = 'Pods activity'
    button = 'X'
    modal = 'Function pods activity'

    click_on_task_in_lane(selenium, browser_id, op_container, lane,
                          task, ordinal, click)
    click_on_link_in_task_box(selenium, browser_id, op_container, lane, task,
                              link, ordinal)
    assert_lambda_name_in_tab_name(selenium, browser_id, modals, tab,
                                   lambda_name)
    click_modal_button(selenium, browser_id, button, modal, modals)
    click_on_task_in_lane(selenium, browser_id, op_container, lane, task,
                          ordinal, close)


def check_number_of_events(selenium, browser_id, modals, exp_num, task):
    driver = selenium[browser_id]
    actual_num = int(modals(
        driver).function_pods_activity.get_number_of_data_rows(driver))
    exp_num = int(exp_num)
    err_msg = (f'numer of events on "Pods activity" ({actual_num}) for task '
               f'"{task}" is not about {exp_num}')
    assert abs(actual_num - exp_num) <= 3, err_msg


@wt(parsers.parse('user of {browser_id} sees that numer of events on '
                  '"Pods activity" list for task "{task}" in {ordinal}'
                  ' parallel box in "{lane}" lane is about {exp_num}'))
def assert_number_of_events_in_task(browser_id, task, lane, exp_num, ordinal,
                                    op_container, selenium, modals):
    click = 'clicks on'
    close = 'closes'
    link = 'Pods activity'
    button = 'X'
    modal = 'Function pods activity'

    click_on_task_in_lane(selenium, browser_id, op_container, lane,
                          task, ordinal, click)
    click_on_link_in_task_box(selenium, browser_id, op_container, lane, task,
                              link, ordinal)
    wait_for_ongoing_pods_to_be_terminated(selenium, browser_id, modals)
    click_on_first_terminated_pod(selenium, browser_id, modals)
    check_number_of_events(selenium, browser_id, modals, exp_num, task)
    click_modal_button(selenium, browser_id, button, modal, modals)
    click_on_task_in_lane(selenium, browser_id, op_container, lane, task,
                          ordinal, close)
