"""This module contains meta steps for operations on automation page in Onezone
using web GUI
"""
__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.steps.modal import _wait_for_modal_to_appear, click_modal_button
from tests.gui.steps.onezone.automation import assert_workflow_exists, \
    go_to_inventory_subpage, upload_workflow_as_json, confirm_workflow_creation, \
    write_text_into_workflow_name_on_main_workflows_page, \
    click_add_new_button_in_menu_bar, write_text_into_lambda_form, \
    assert_lambda_exists, confirm_lambda_creation_or_edition
from tests.gui.steps.onezone.spaces import click_on_option_in_the_sidebar
from tests.gui.utils.generic import transform, upload_file_path
from tests.utils.bdd_utils import wt, parsers
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} creates workflow "{workflow_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_workflow_using_gui(selenium, browser_id, oz_page, workflow_name):
    click_add_new_button_in_menu_bar(selenium, browser_id,
                                     oz_page, 'Add new workflow')
    write_text_into_workflow_name_on_main_workflows_page(selenium, browser_id,
                                                         oz_page, workflow_name)

    confirm_workflow_creation(selenium, browser_id, oz_page)


@wt(parsers.parse('user of {browser_id} uploads "{workflow}" workflow from '
                  '"{file_name}" file to "{inventory}" inventory'))
def upload_and_assert_workflow_to_inventory_using_gui(selenium, browser_id,
                                                      oz_page, modals,
                                                      inventory, workflow,
                                                      file_name, tmp_memory):
    driver = selenium[browser_id]
    click_on_option_in_the_sidebar(selenium, browser_id, 'Automation', oz_page)
    go_to_inventory_subpage(selenium, browser_id, inventory,
                            'workflows', oz_page)
    upload_workflow_as_json(selenium, browser_id, file_name, oz_page)
    _wait_for_modal_to_appear(driver, browser_id, 'Upload workflow', tmp_memory)
    click_modal_button(selenium, browser_id, 'Apply', 'Upload workflow', modals)
    go_to_inventory_subpage(selenium, browser_id, inventory,
                            'workflows', oz_page)

    assert_workflow_exists(selenium, browser_id, oz_page, workflow, 'sees')


@wt(parsers.parse('user of {browser_id} creates "{lambda_name}" lambda from '
                  '"{docker_image}" docker image in "{inventory}" inventory'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_lambda_using_gui(selenium, browser_id, oz_page, lambda_name,
                            docker_image, inventory):
    click_on_option_in_the_sidebar(selenium, browser_id, 'Automation', oz_page)
    go_to_inventory_subpage(selenium, browser_id, inventory,
                            'lambdas', oz_page)
    click_add_new_button_in_menu_bar(selenium, browser_id, oz_page,
                                     'Add new lambda')
    write_text_into_lambda_form(selenium, browser_id, oz_page,
                                lambda_name, 'lambda name')
    write_text_into_lambda_form(selenium, browser_id, oz_page,
                                docker_image, 'docker image')

    confirm_lambda_creation_or_edition(selenium, browser_id, oz_page, 'lambda')

    go_to_inventory_subpage(selenium, browser_id, inventory,
                            'lambdas', oz_page)

    assert_lambda_exists(selenium, browser_id, oz_page, lambda_name)


@wt(parsers.parse(
    'user of {browser_id} chooses "{item_list}" file as initial value '
    'for workflow in modal "Select files"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_file_as_initial_workflow_value(selenium, browser_id, item_list,
                                          modals,op_container):

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
def wait_for_waiting_workflows_to_start(selenium, browser_id, op_container):
    assert len(op_container(selenium[browser_id]).automation_page.waiting) == 0, \
        'Waiting workflows did not start'


@wt(parsers.re('user of (?P<browser_id>.*) waits for all workflows to finish'))
@repeat_failed(interval=1, timeout=180,
               exceptions=(AssertionError, StaleElementReferenceException))
def wait_for_ongoing_workflows_to_finish(selenium, browser_id, op_container):
    assert len(op_container(selenium[browser_id]).automation_page.ongoing) == 0, \
        'Ongoing workflows did not finish'


@wt(parsers.re('user of (?P<browser_id>.*) clicks on first executed workflow'))
def expand_workflow_record(selenium, browser_id, op_container):
    op_container(selenium[browser_id]).automation_page.ended[0].expand()


@wt(parsers.parse('user of browser waits for all pods to finish execution in '
                  'in modal "Function pods activity"'))
@repeat_failed(interval=1, timeout=180,
               exceptions=(AssertionError, StaleElementReferenceException))
def assert_status_in_events_monitor(selenium, browser_id, modals):
    modal = modals(selenium[browser_id]).pods_activity
    assert len(modal.pods_list) == 0, 'Pods has not been terminated'
