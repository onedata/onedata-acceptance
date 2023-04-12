"""This module contains meta steps for operations on automation page concerning
 workflow creation in Onezone using web GUI
"""
__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import time


from tests.gui.meta_steps.oneprovider.automation.run_workflow import (
    choose_file_as_initial_workflow_value,
    wait_for_workflows_in_automation_subpage,
    choose_range_as_initial_workflow_value)
from tests.gui.steps.modals.modal import (
    _wait_for_modal_to_appear, click_modal_button,
    choose_option_in_dropdown_menu_in_modal)
from tests.gui.steps.oneprovider.archives import from_ordinal_number_to_int
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


@wt(parsers.re('user of (?P<browser_id>.*) clicks on (?P<ordinal>|1st |2nd '
               '|3rd |4th )revision of "(?P<workflow>.*)" in workflows list '
               'in inventory workflows subpage'))
def click_on_workflow_in_inventory_subpage(oz_page, selenium, browser_id,
                                           ordinal, workflow):
    page = oz_page(selenium[browser_id])['automation']
    number = from_ordinal_number_to_int(ordinal)
    page.workflows_page.elements_list[workflow].revision_list[
        str(number)].click()


@wt(parsers.parse('user of {browser_id} executes {ordinal} revision of '
                  '"{workflow}", using "{item_list}" {data_type}as initial '
                  'value, in "{space}" space'))
def execute_workflow(browser_id, selenium, oz_page, space, op_container,
                     ordinal, workflow, modals, item_list, popups, data_type):
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

    if 'start' in item_list:
        item_list = eval(item_list)
        if type(item_list) == list:
            for item in item_list:
                choose_range_as_initial_workflow_value(selenium, browser_id,
                                                       op_container, item)
    elif 'numbers' in data_type:
        # wait a moment for workflow revision to open
        time.sleep(1)
        items = eval(item_list)
        driver = selenium[browser_id]
        for number in items:
            op_container(driver).automation_page.input_link.click()
            numbers = op_container(driver).automation_page.numbers
            numbers[len(numbers)-1].input = str(number)

    else:
        choose_file_as_initial_workflow_value(selenium, browser_id, item_list,
                                              modals, op_container, popups,
                                              data_type)

    confirm_workflow_to_execute(selenium, browser_id, op_container)


@wt(parsers.re('user of (?P<browser_id>.*) executes (?P<ordinal>.*) revision'
               ' of "(?P<workflow>.*)", using "(?P<item>.*)" '
               '(?P<data_type>.*)as initial value, in "(?P<space>.*)" '
               'space and waits extended time for workflow to finish'))
def execute_workflow_and_wait(browser_id, selenium, oz_page, space,
                              op_container, ordinal, workflow, modals, item,
                              popups, data_type):
    start = 'start'
    finish = 'finish'
    execute_workflow(browser_id, selenium, oz_page, space, op_container,
                     ordinal, workflow, modals, item, popups, data_type)
    wait_for_workflows_in_automation_subpage(selenium, browser_id, op_container,
                                             start)
    wait_for_workflows_in_automation_subpage(selenium, browser_id, op_container,
                                             finish)
    expand_first_executed_workflow_record(selenium, browser_id, op_container)


@wt(parsers.parse('user of {browser_id} modifies {menu} in "{store_name}" '
                  'store to be "{value}" for "{workflow_name}" workflow'))
def modify_data_type_in_store(selenium, browser_id, oz_page, store_name, modals,
                              popups, value, menu):
    driver = selenium[browser_id]
    page = oz_page(driver)['automation']
    dropdown_menu = f'{menu} dropdown menu'
    button = 'OK'
    modal_name = 'Modify store'

    page.workflows_page.workflow_visualiser.stores_list[store_name].click()

    if 'data' in menu:
        # wait a moment for modal to open
        time.sleep(0.5)
        modals(driver).modify_store.data_type_remove()

    choose_option_in_dropdown_menu_in_modal(selenium, browser_id, modals,
                                            dropdown_menu, popups,
                                            value, modal_name)
    click_modal_button(selenium, browser_id, button, modal_name, modals)
