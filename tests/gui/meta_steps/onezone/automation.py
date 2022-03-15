"""This module contains meta steps for operations on automation page in Onezone
using web GUI
"""
__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.steps.modal import _wait_for_modal_to_appear
from tests.gui.steps.onezone.automation import assert_workflow_exists
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


@wt(parsers.parse('user of {browser_id} uploads workflow "{file_name}" '
                  'to "{inventory}" inventory and then sees "{workflow}"'
                  ' in workflows list in inventory'))
def upload_and_assert_workflow_to_inventory_using_gui(selenium, browser_id,
                                                      oz_page, modals,
                                                      inventory, workflow,
                                                      file_name, tmp_memory):

    driver = selenium[browser_id]
    oz_page(driver)['automation'].upload_workflow(upload_file_path(file_name))
    _wait_for_modal_to_appear(driver, browser_id, 'Upload workflow', tmp_memory)
    modals(driver).upload_workflow.apply.click()
    page = oz_page(driver)['automation']
    page.elements_list[inventory].workflows()

    assert_workflow_exists(selenium, browser_id, oz_page, workflow, 'sees')




