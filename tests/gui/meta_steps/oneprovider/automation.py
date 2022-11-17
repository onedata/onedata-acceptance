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
from tests.gui.steps.oneprovider.automation import switch_to_automation_page
from tests.gui.steps.oneprovider.file_browser import _select_files
from tests.gui.utils.core import scroll_to_css_selector
from tests.utils.bdd_utils import wt, parsers
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} chooses "{file_name}" file '
                  'as initial value for workflow in "Select files" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_file_as_initial_workflow_value(selenium, browser_id, file_name,
                                          modals, op_container):
    switch_to_iframe(selenium, browser_id)
    driver = selenium[browser_id]
    op_container(driver).automation_page.input_icon.click()

    select_files_modal = modals(driver).select_files

    for file in select_files_modal.files:
        if file.name == file_name:
            file.clickable_field.click()

    select_files_modal.confirm_button.click()


def change_tab_in_automation_subpage(page, tab_name):
    page.navigation_tab[tab_name].click()
    time.sleep(0.25)


@wt(parsers.re('user of (?P<browser_id>.*) waits for all workflows to '
               '(?P<option>start|finish)'))
@repeat_failed(interval=1, timeout=180,
               exceptions=(AssertionError, StaleElementReferenceException))
def wait_for_workflows_in_automation_subpage(selenium, browser_id, op_container,
                                             option):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    if option == 'start':
        change_tab_in_automation_subpage(page, 'Waiting')
        err = 'Waiting workflows did not start'
    else:
        change_tab_in_automation_subpage(page, 'Ongoing')
        err = 'Ongoing workflows did not finish their run'

    assert len(page.executed_workflow_list) == 0, err


@wt(parsers.re('user of (?P<browser_id>.*) clicks on first executed workflow'))
@repeat_failed(timeout=WAIT_FRONTEND)
def expand_workflow_record(selenium, browser_id, op_container):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    change_tab_in_automation_subpage(page, 'Ended')
    page.executed_workflow_list[0].click()


def get_store_content(browser_id, driver, page, modals, clipboard,
                       displays, store_name, store_type):
    page.stores_list[store_name].click()
    modal = modals(driver).store_details
    time.sleep(0.25)
    store_content_type = 'store_content_' + store_type
    store_content_list = getattr(modal, store_content_type)
    modal.store_content_list[0].click()
    modal.copy_button()
    store_value = clipboard.paste(display=displays[browser_id])
    modal.close()

    return store_value


@wt(parsers.parse('user of {browser_id} sees that content of "{store1}" store '
                  'is the same as content of "{store2}" store'))
def compare_store_contents(selenium, browser_id, op_container, store1,
                           store2, modals, clipboard, displays):
    switch_to_iframe(selenium, browser_id)
    driver = selenium[browser_id]

    page = op_container(driver).automation_page.workflow_visualiser

    store1_value = get_store_content(browser_id, driver, page, modals,
                                      clipboard, displays, store1, 'list')
    store2_value = get_store_content(browser_id, driver, page, modals,
                                      clipboard, displays, store2, 'object')

    assert store1_value == store2_value, (f'Value of {store1} '
                                          f'store:{store1_value} \n is not '
                                          f'equal to value of {store2} '
                                          f'store:{store2_value}')


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


@wt(parsers.parse('user of {browser_id} clicks on first terminated pod in '
                  'modal "Function pods activity"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_first_terminated_pod(selenium, browser_id, modals):
    switch_to_iframe(selenium, browser_id)
    modal = modals(selenium[browser_id]).function_pods_activity
    change_tab_in_function_pods_activity_modal(modal, 'All')

    modal.pods_list[0].click()


@wt(parsers.parse('user of {browser_id} sees events with following reasons: '
                  '{reasons} in modal "Function pods activity"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_events_in_pods_monitor(selenium, browser_id, modals, reasons):
    driver = selenium[browser_id]
    switch_to_iframe(selenium, browser_id)
    modal = modals(driver).function_pods_activity

    events_list = modal.events_list
    reasons_list = parse_seq(reasons)
    gathered_reasons_list = []

    # Loop below creates list of reasons from all the events that happened in
    # a selected pod
    for i in range(1, len(events_list) + 1):
        reason = modal.get_event_reason(driver, i, len(events_list))
        gathered_reasons_list.append(reason)

    for reason in reasons_list:
        assert reason in gathered_reasons_list, \
            f'Reason: {reason} has not been found'
