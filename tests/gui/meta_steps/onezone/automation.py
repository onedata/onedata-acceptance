"""This module contains meta steps for operations on automation page in Onezone
using web GUI
"""
__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
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




