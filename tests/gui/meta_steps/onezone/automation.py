"""This module contains meta steps for operations on automation page in Onezone
using web GUI
"""
__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from selenium.common.exceptions import StaleElementReferenceException

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.steps.common.miscellaneous import switch_to_iframe
from tests.gui.utils.generic import transform, upload_file_path
from tests.utils.bdd_utils import wt, parsers
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} creates workflow "{workflow_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_workflow_using_gui(selenium, browser_id, oz_page, workflow_name):
    page = oz_page(selenium[browser_id])['automation']
    page.main_page.add_new_workflow.click()
    page.workflows_page.workflow_name.value = workflow_name
    page.workflows_page.create_button.click()


@wt(parsers.parse('user of {browser_id} confirm workflow upload to '
                  '"{inventory}" inventory and then sees "{workflow}" '
                  'in workflows list in inventory'))
@repeat_failed(timeout=WAIT_FRONTEND)
def upload_and_assert_workflow_to_inventory_using_gui(selenium, browser_id,
                                                      oz_page, modals,
                                                      inventory, workflow):
    driver = selenium[browser_id]
    modals(driver).upload_workflow.apply.click()
    page = oz_page(driver)['automation']
    page.elements_list[inventory].workflows()

    assert workflow in page.workflows_page.elements_list, \
        f'Workflow: {workflow} not found '


@wt(parsers.parse('user of {browser_id} chooses "{file_path}" file as initial value '
                  'for workflow'))
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_file_as_initial_workflow_value(selenium, browser_id, op_container, file_path):
    switch_to_iframe(selenium, browser_id)
    page = op_container(selenium[browser_id]).automation_page
    # page.input_icon.click()
    #
    # #choose_file


@wt(parsers.re('user of (?P<browser_id>.*) waits for all workflows to start'))
@repeat_failed(interval=1, timeout=90,
               exceptions=(AssertionError, StaleElementReferenceException))
def wait_for_waiting_workflows_to_start(selenium, browser_id, op_container):
    assert len(op_container(selenium[browser_id]).automation_page.waiting) == 0, \
        'Waiting workflows did not start'


@wt(parsers.re('user of (?P<browser_id>.*) waits for all workflows to finish'))
@repeat_failed(interval=1, timeout=90,
               exceptions=(AssertionError, StaleElementReferenceException))
def wait_for_ongoing_workflows_to_finish(selenium, browser_id, op_container):
    assert len(op_container(selenium[browser_id]).automation_page.ongoing) == 0, \
        'Ongoing workflows did not finish'


@wt(parsers.re('user of (?P<browser_id>.*) clicks on first executed workflow'))
def expand_workflow_record(selenium, browser_id, op_container):
    op_container(selenium[browser_id]).automation_page.ended[0].expand()



