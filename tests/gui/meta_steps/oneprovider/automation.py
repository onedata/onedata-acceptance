"""This module contains meta steps for operations on automation page in
Oneprovider using web GUI
"""
__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import time

from selenium.common.exceptions import StaleElementReferenceException

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import switch_to_iframe
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


@wt(parsers.parse('user of {browser_id} waits for all pods to '
                  'finish execution in modal "Function pods activity"'))
@repeat_failed(interval=1, timeout=180,
               exceptions=(AssertionError, StaleElementReferenceException))
def wait_for_ongoing_pods_to_be_terminated(selenium, browser_id, modals):
    modal = modals(selenium[browser_id]).function_pods_activity
    time.sleep(0.25)
    assert len(modal.pods_list) == 0, 'Pods has not been terminated'


@wt(parsers.parse('user of {browser_id} compares content of "{store1}" store '
                  'and "{store2}" store'))
@repeat_failed(timeout=WAIT_FRONTEND)
def compare_store_contents(selenium, browser_id, op_container, store1,
                           store2, modals):

    switch_to_iframe(selenium, browser_id)
    driver = selenium[browser_id]

    page = op_container(driver).automation_page.workflow_visualiser
    modal = modals(driver).store_details

    page.stores_list[store1].click()
    store1_value = modal.details_list_row[0].get_content()
    modal.close.click()

    page.stores_list[store2].click()
    store2_value = modal.details_list_row[0].get_content()

    assert store1_value == store2_value, (f'Value of {store1} store is not '
                                          f'equal to value of {store2} store')
