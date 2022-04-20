"""This module contains meta steps for operations on automation page in
Oneprovider using web GUI
"""
__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import time

import yaml
from selenium.common.exceptions import StaleElementReferenceException

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import switch_to_iframe
from tests.gui.steps.modal import wt_wait_for_modal_to_appear
from tests.gui.steps.oneprovider.file_browser import _select_files
from tests.utils.bdd_utils import wt, parsers
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} chooses "{item_list}" file '
                  'as initial value for workflow in modal "Select files"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_file_as_initial_workflow_value(selenium, browser_id, item_list,
                                          modals, op_container):
    switch_to_iframe(selenium, browser_id)
    driver = selenium[browser_id]
    op_container(driver).automation_page.input_icon.click()

    modal = modals(selenium[browser_id]).select_files
    browser = modal.file_browser

    with browser.select_files() as selector:
        _select_files(browser, selector, item_list)

    modal.confirm_button.click()


@wt(parsers.re('user of (?P<browser_id>.*) waits for all workflows to start'))
@repeat_failed(interval=1, timeout=90,
               exceptions=(AssertionError, StaleElementReferenceException))
def wait_for_workflows_to_start(selenium, browser_id, op_container):
    switch_to_iframe(selenium, browser_id)
    page = op_container(selenium[browser_id]).automation_page
    page.navigation_tab['Waiting'].click()
    time.sleep(0.25)
    assert len(page.workflow_list_row) == 0, 'Waiting workflows did not start'


@wt(parsers.re('user of (?P<browser_id>.*) waits for all workflows to finish'))
@repeat_failed(interval=1, timeout=180,
               exceptions=(AssertionError, StaleElementReferenceException))
def wait_for_ongoing_workflows_to_finish(selenium, browser_id, op_container):
    switch_to_iframe(selenium, browser_id)
    page = op_container(selenium[browser_id]).automation_page
    page.navigation_tab['Ongoing'].click()
    time.sleep(0.25)
    assert len(page.workflow_list_row) == 0, 'Ongoing workflows did not finish'


@wt(parsers.re('user of (?P<browser_id>.*) clicks on first executed workflow'))
@repeat_failed(timeout=WAIT_FRONTEND)
def expand_workflow_record(selenium, browser_id, op_container):
    switch_to_iframe(selenium, browser_id)
    page = op_container(selenium[browser_id]).automation_page
    page.navigation_tab['Ended'].click()
    time.sleep(0.25)
    page.workflow_list_row[0].click()


@wt(parsers.parse('user of {browser_id} compares content of "{store1}" store '
                  'and "{store2}" store'))
def compare_store_contents(selenium, browser_id, op_container, store1,
                           store2, modals, clipboard, displays, tmp_memory):
    switch_to_iframe(selenium, browser_id)
    driver = selenium[browser_id]

    page = op_container(driver).automation_page.workflow_visualiser

    page.stores_list[store1].click()
    modal = modals(driver).store_details
    time.sleep(0.25)
    modal.details_list[0].expander.click()
    modal.copy_button.click()
    store1_value = clipboard.paste(display=displays[browser_id])
    modal.close.click()

    page.stores_list[store2].click()
    modal = modals(driver).store_details
    time.sleep(0.25)
    modal.details_list[0].expander.click()
    modal.copy_button.click()
    store2_value = clipboard.paste(display=displays[browser_id])

    assert store1_value == store2_value, (f'Value of {store1} store is not '
                                          f'equal to value of {store2} store')


@wt(parsers.parse('user of {browser_id} waits for all pods to '
                  'finish execution in modal "Function pods activity"'))
@repeat_failed(interval=1, timeout=180,
               exceptions=(AssertionError, StaleElementReferenceException))
def wait_for_ongoing_pods_to_be_terminated(selenium, browser_id, modals):
    modal = modals(selenium[browser_id]).function_pods_activity
    time.sleep(0.25)
    modal.tabs['Current'].click()
    assert len(modal.pods_list) == 0, 'Pods has not been terminated'


@wt(parsers.parse('user of {browser_id} clicks on first terminated pod in '
                  'modal "Function pods activity"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_first_terminated_pod(selenium, browser_id, modals):
    modal = modals(selenium[browser_id]).function_pods_activity
    time.sleep(0.25)
    modal.tabs['All'].click()
    modal.pods_list[0].click()


@wt(parsers.parse('user of {browser_id} sees event with following reason: '
                  '{event} in modal "Function pods activity"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_events_in_pods_monitor(selenium, browser_id, modals, event):
    modal = modals(selenium[browser_id]).function_pods_activity
    time.sleep(0.25)
    assert event in modal.events_list


def _assert_event(pod, desc):
    desc = yaml.load(desc)
    for key, val in desc.items():
        pod_value = getattr(pod, key.replace(' ', '_'))
        assert pod_value == str(val), \
            'Pod {} is {} instead of {} in list'.format(key, pod_value, val)


@wt(parsers.re('user of (?P<browser_id>.*) sees pod in all pods '
               'in modal "Function pods activity":\n(?P<desc>(.|\s)*)'))
@repeat_failed(interval=0.5, timeout=90)
def assert_event_of_pod(selenium, browser_id, desc, modals):
    pod = modals(selenium[browser_id]).function_pods_activity.pods_list[0]
    _assert_event(pod, desc)
