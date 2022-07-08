"""This module contains meta steps for operations on automation page in Onezone
using web GUI
"""
__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.modals.modal import (_wait_for_modal_to_appear,
                                          click_modal_button)
from tests.gui.steps.onezone.automation import (
    assert_workflow_exists, go_to_inventory_subpage, upload_workflow_as_json,
    confirm_workflow_creation,
    write_text_into_workflow_name_on_main_workflows_page,
    click_add_new_button_in_menu_bar, write_text_into_lambda_form,
    assert_lambda_exists, confirm_lambda_creation_or_edition)
from tests.gui.steps.onezone.spaces import click_on_option_in_the_sidebar
from tests.utils.bdd_utils import wt, parsers
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
