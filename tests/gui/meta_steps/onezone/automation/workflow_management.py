"""This module contains meta steps for operations on automation page concerning
 workflow creation in Onezone using web GUI
"""
__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import yaml

from tests.gui.meta_steps.oneprovider.automation.run_workflow import (
    choose_file_as_initial_workflow_value,
    wait_for_workflows_in_automation_subpage)
from tests.gui.steps.modals.modal import (
    _wait_for_modal_to_appear, click_modal_button)
from tests.gui.steps.oneprovider.automation.automation_basic import (
    click_button_in_navigation_tab, choose_workflow_revision_to_run,
    confirm_workflow_to_execute, expand_first_executed_workflow_record)
from tests.gui.steps.onezone.automation.automation_basic import *
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.onezone.automation.workflow_creation import (
    click_add_new_button_in_menu_bar,
    write_text_into_workflow_name_on_main_workflows_page,
    confirm_workflow_creation)
from tests.gui.steps.onezone.spaces import (
    click_on_option_in_the_sidebar, click_element_on_lists_on_left_sidebar_menu,
    click_on_option_of_space_on_left_sidebar_menu)
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


@wt(parsers.parse('user of {browser_id} uploads "{workflow}" workflow from '
                  'automation-examples repository to "{inventory}" inventory'))
def upload_workflow_from_automation_examples(selenium, browser_id,
                                             oz_page, modals,
                                             inventory, workflow, tmp_memory):
    driver = selenium[browser_id]
    click_on_option_in_the_sidebar(selenium, browser_id, 'Automation', oz_page)
    go_to_inventory_subpage(selenium, browser_id, inventory,
                            'workflows', oz_page)
    upload_workflow_from_repository(selenium, browser_id, workflow, oz_page)
    _wait_for_modal_to_appear(driver, browser_id, 'Upload workflow', tmp_memory)
    click_modal_button(selenium, browser_id, 'Apply', 'Upload workflow', modals)
    go_to_inventory_subpage(selenium, browser_id, inventory,
                            'workflows', oz_page)

    assert_workflow_exists(selenium, browser_id, oz_page, workflow, 'sees')


@wt(parsers.parse('user of {browser_id} executes {ordinal} revision of '
                  '"{workflow}", using "{item_list}" as initial value, in '
                  '"{space}" space'))
def execute_workflow(browser_id, selenium, oz_page, space, op_container,
                     ordinal, workflow, modals, item_list, popups):
    spaces = 'spaces'
    automation_workflows = 'Automation Workflows'
    tab_name = 'Run workflow'

    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id, spaces,
                                                space, oz_page)
    click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id, space,
                                                  automation_workflows, oz_page)
    click_button_in_navigation_tab(selenium, browser_id, op_container,
                                   tab_name)
    choose_workflow_revision_to_run(selenium, browser_id, op_container,
                                    ordinal, workflow)
    choose_file_as_initial_workflow_value(selenium, browser_id, item_list, modals,
                                          op_container, popups)
    confirm_workflow_to_execute(selenium, browser_id, op_container)


@wt(parsers.parse('user of {browser_id} executes {ordinal} revision of '
                  '"{workflow}", using "{item}" as initial value, in '
                  '"{space}" space and waits extended time for workflow to '
                  'finish'))
def execute_workflow_and_wait(browser_id, selenium, oz_page, space,
                              op_container, ordinal, workflow, modals, item,
                              popups):
    start = 'start'
    finish = 'finish'
    execute_workflow(browser_id, selenium, oz_page, space, op_container,
                     ordinal, workflow, modals, item, popups)
    wait_for_workflows_in_automation_subpage(selenium, browser_id, op_container,
                                             start)
    wait_for_workflows_in_automation_subpage(selenium, browser_id, op_container,
                                             finish)
    expand_first_executed_workflow_record(selenium, browser_id, op_container)


