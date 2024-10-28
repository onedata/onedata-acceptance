"""This module contains meta steps for operations on automation page concerning
workflow creation in Onezone using web GUI
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
import time

import yaml
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.meta_steps.oneprovider.automation.run_workflow import (
    choose_file_as_initial_workflow_value,
    choose_file_as_initial_workflow_value_for_store,
    choose_group_as_initial_workflow_value_for_store,
    provide_text_to_object_initial_workflow_value_store,
    provide_text_to_string_initial_workflow_value_store,
    wait_for_workflows_in_automation_subpage,
)
from tests.gui.steps.modals.modal import (
    _wait_for_modal_to_appear,
    choose_option_in_dropdown_menu_in_modal,
    click_modal_button,
)
from tests.gui.steps.oneprovider.automation.automation_basic import (
    choose_workflow_revision_to_run,
    click_button_in_navigation_tab,
    confirm_workflow_to_execute,
    expand_first_executed_workflow_record,
    get_input_element,
)
from tests.gui.steps.oneprovider.automation.initial_values import (
    choose_range_as_initial_workflow_value,
    get_data_type_in_initial_value_store,
    get_data_type_of_array_initial_value_store,
)
from tests.gui.steps.onezone.automation.automation_basic import *
from tests.gui.steps.onezone.automation.workflow_creation import (
    click_add_new_button_in_menu_bar,
    confirm_workflow_creation,
    write_text_into_workflow_name_on_main_workflows_page,
)
from tests.gui.steps.onezone.spaces import (
    click_element_on_lists_on_left_sidebar_menu,
    click_on_automation_option_in_the_sidebar,
    click_on_option_of_space_on_left_sidebar_menu,
)
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} creates workflow "{workflow_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_workflow_using_gui(selenium, browser_id, oz_page, workflow_name):
    click_add_new_button_in_menu_bar(selenium, browser_id, oz_page, "Add new workflow")
    write_text_into_workflow_name_on_main_workflows_page(
        selenium, browser_id, oz_page, workflow_name
    )

    confirm_workflow_creation(selenium, browser_id, oz_page)


@wt(
    parsers.parse(
        'user of {browser_id} uploads "{workflow}" workflow from '
        '"{file_name}" file to "{inventory}" inventory'
    )
)
def upload_and_assert_workflow_to_inventory_using_gui(
    selenium,
    browser_id,
    oz_page,
    modals,
    inventory,
    workflow,
    file_name,
    tmp_memory,
):
    driver = selenium[browser_id]
    click_on_automation_option_in_the_sidebar(selenium, browser_id, oz_page, tmp_memory)
    go_to_inventory_subpage(
        selenium, browser_id, inventory, "workflows", oz_page, tmp_memory
    )
    upload_workflow_as_json(selenium, browser_id, file_name, oz_page)
    _wait_for_modal_to_appear(driver, browser_id, "Upload workflow", tmp_memory)
    click_modal_button(selenium, browser_id, "Apply", "Upload workflow", modals)
    go_to_inventory_subpage(
        selenium, browser_id, inventory, "workflows", oz_page, tmp_memory
    )

    assert_workflow_exists(selenium, browser_id, oz_page, workflow, "sees")


@given(
    parsers.parse(
        'user of {browser_id} uploads "{workflow}" workflow from '
        'automation-examples repository to "{inventory}" inventory'
    )
)
def given_upload_workflow_from_automation_examples(
    selenium, browser_id, oz_page, modals, inventory, workflow, tmp_memory
):
    upload_workflow_from_automation_examples(
        selenium, browser_id, oz_page, modals, inventory, workflow, tmp_memory
    )


@wt(
    parsers.parse(
        'user of {browser_id} uploads "{workflow}" workflow from '
        'automation-examples repository to "{inventory}" inventory'
    )
)
def upload_workflow_from_automation_examples(
    selenium, browser_id, oz_page, modals, inventory, workflow, tmp_memory
):
    _upload_workflow_from_automation_examples(
        selenium, browser_id, oz_page, modals, inventory, workflow, tmp_memory
    )


@wt(
    parsers.parse(
        'user of {browser_id} uploads "{workflow}" workflow {method} from '
        'automation-examples repository to "{inventory}" inventory'
    )
)
def upload_workflow_from_automation_examples_with_given_method(
    selenium,
    browser_id,
    oz_page,
    modals,
    inventory,
    workflow,
    tmp_memory,
    method,
):
    _upload_workflow_from_automation_examples(
        selenium,
        browser_id,
        oz_page,
        modals,
        inventory,
        workflow,
        tmp_memory,
        method=method,
    )


def _upload_workflow_from_automation_examples(
    selenium,
    browser_id,
    oz_page,
    modals,
    inventory,
    workflow,
    tmp_memory,
    method=None,
):
    subpage = "workflows"
    modal = "Upload workflow"
    button = "Apply"
    driver = selenium[browser_id]

    click_on_automation_option_in_the_sidebar(selenium, browser_id, oz_page, tmp_memory)
    go_to_inventory_subpage(
        selenium, browser_id, inventory, subpage, oz_page, tmp_memory
    )
    upload_workflow_from_repository(selenium, browser_id, workflow, oz_page)
    _wait_for_modal_to_appear(driver, browser_id, modal, tmp_memory)
    if method == "as new workflow":
        method_button = "Persist as new workflow"
        click_modal_button(selenium, browser_id, method_button, modal, modals)
    elif method == "and merge into existing workflow":
        method_button = "Merge into existing workflow"
        click_modal_button(selenium, browser_id, method_button, modal, modals)
    click_modal_button(selenium, browser_id, button, modal, modals)
    go_to_inventory_subpage(
        selenium, browser_id, inventory, subpage, oz_page, tmp_memory
    )
    if workflow == "initialize-eureka3D-project":
        workflow = "Initialize Eureka3D project"
    assert_workflow_exists(selenium, browser_id, oz_page, workflow, "sees")


@wt(
    parsers.parse(
        "user of {browser_id} executes {ordinal} revision of "
        '"{workflow}" workflow in "{space}" space with the following '
        "initial values:\n{config}"
    )
)
def execute_workflow_with_input_config(
    browser_id,
    selenium,
    oz_page,
    space,
    op_container,
    ordinal,
    workflow,
    modals,
    popups,
    config,
):
    """Adjust configuration of input values for stores according to given config.

    Config format given in yaml is as follows:
        store name: store_name
            - file1
            - file2

    Example configuration:
        fetch-files:
            - fetch.txt
            - fetch_xrootd.txt
        destination:
            - result_directory

    """

    _execute_workflow_with_input_config(
        browser_id,
        selenium,
        oz_page,
        space,
        op_container,
        ordinal,
        workflow,
        modals,
        popups,
        config,
    )


def _execute_workflow_with_input_config(
    browser_id,
    selenium,
    oz_page,
    space,
    op_container,
    ordinal,
    workflow,
    modals,
    popups,
    config,
):
    spaces = "spaces"
    automation_workflows = "Automation Workflows"
    tab_name = "Run workflow"

    start = "start"
    finish = "finish"

    try:
        click_element_on_lists_on_left_sidebar_menu(
            selenium, browser_id, spaces, space, oz_page
        )
    except IndexError:
        pass
    click_on_option_of_space_on_left_sidebar_menu(
        selenium, browser_id, space, automation_workflows, oz_page
    )
    click_button_in_navigation_tab(selenium, browser_id, op_container, tab_name)
    choose_workflow_revision_to_run(
        selenium, browser_id, op_container, ordinal, workflow
    )

    # wait a moment for workflow revision to open
    time.sleep(1)

    data = yaml.load(config, yaml.Loader)
    for store in data:
        driver = selenium[browser_id]
        data_type = get_data_type_in_initial_value_store(driver, op_container, store)
        if data_type == "FILE":
            file_list = data[store]
            choose_file_as_initial_workflow_value_for_store(
                selenium,
                browser_id,
                file_list,
                modals,
                op_container,
                popups,
                store,
            )
        elif data_type == "ARRAY":
            item_list = data[store]
            array_store_type = get_data_type_of_array_initial_value_store(
                driver, op_container, store
            )
            if array_store_type == "group":
                choose_group_as_initial_workflow_value_for_store(
                    selenium,
                    browser_id,
                    item_list,
                    modals,
                    op_container,
                    popups,
                    store,
                )
            elif array_store_type == "file":
                choose_file_as_initial_workflow_value_for_store(
                    selenium,
                    browser_id,
                    item_list,
                    modals,
                    op_container,
                    popups,
                    store,
                )
            else:
                raise ValueError(f"unknown data type {array_store_type}")
        elif data_type == "OBJECT":
            text = data[store][0]
            provide_text_to_object_initial_workflow_value_store(
                driver, op_container, store, text
            )
        elif data_type == "STRING":
            text = data[store][0]
            provide_text_to_string_initial_workflow_value_store(
                driver, op_container, store, text
            )
        else:
            raise ValueError(f"unknown data type {data_type}")

    confirm_workflow_to_execute(selenium, browser_id, op_container)
    wait_for_workflows_in_automation_subpage(selenium, browser_id, op_container, start)
    wait_for_workflows_in_automation_subpage(selenium, browser_id, op_container, finish)
    expand_first_executed_workflow_record(selenium, browser_id, op_container)


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) executes (?P<ordinal>.*) revision"
        ' of "(?P<workflow>.*)" and waits extended time for workflow '
        "to finish, using (?P<data_type>.*) as initial "
        'value: "(?P<item_list>.*)" in "(?P<space>.*)" '
        "space"
    )
)
def execute_workflow_and_wait(
    browser_id,
    selenium,
    oz_page,
    space,
    op_container,
    ordinal,
    workflow,
    modals,
    item_list,
    popups,
    data_type,
):
    start = "start"
    finish = "finish"

    execute_workflow(
        browser_id,
        selenium,
        oz_page,
        space,
        op_container,
        ordinal,
        workflow,
        modals,
        item_list,
        popups,
        data_type,
    )

    wait_for_workflows_in_automation_subpage(selenium, browser_id, op_container, start)
    wait_for_workflows_in_automation_subpage(selenium, browser_id, op_container, finish)
    expand_first_executed_workflow_record(selenium, browser_id, op_container)


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) executes (?P<ordinal>.*) revision"
        ' of "(?P<workflow>.*)", using (?P<data_type>.*) as initial '
        'value: "(?P<item_list>.*)" in "(?P<space>.*)" '
        "space"
    )
)
def execute_workflow(
    browser_id,
    selenium,
    oz_page,
    space,
    op_container,
    ordinal,
    workflow,
    modals,
    item_list,
    popups,
    data_type,
):
    spaces = "spaces"
    automation_workflows = "Automation Workflows"
    tab_name = "Run workflow"
    driver = selenium[browser_id]

    click_element_on_lists_on_left_sidebar_menu(
        selenium, browser_id, spaces, space, oz_page
    )
    click_on_option_of_space_on_left_sidebar_menu(
        selenium, browser_id, space, automation_workflows, oz_page
    )
    click_button_in_navigation_tab(selenium, browser_id, op_container, tab_name)
    choose_workflow_revision_to_run(
        selenium, browser_id, op_container, ordinal, workflow
    )
    # wait a moment for workflow revision to open
    time.sleep(1)
    if "range" in data_type:
        item_list = eval(item_list)
        if type(item_list) is list:
            for item in item_list:
                choose_range_as_initial_workflow_value(
                    selenium, browser_id, op_container, item
                )
        else:
            choose_range_as_initial_workflow_value(
                selenium, browser_id, op_container, item_list, False
            )
    elif "number" in data_type:
        items = eval(item_list)
        if type(items) is list:
            for number in items:
                numbers = get_input_element(op_container, driver, "numbers_input")
                numbers[len(numbers) - 1].input = str(number)
        else:
            numbers = op_container(driver).automation_page.numbers_input
            numbers[len(numbers) - 1].input = str(item_list)
    elif "string" in data_type:
        op_container(driver).automation_page.string_input.input = item_list
    elif "boolean" in data_type:
        items = json.loads(item_list)
        if type(items) is list:
            for boolean in items:
                booleans = get_input_element(op_container, driver, "booleans_input")
                booleans[len(booleans) - 1].click()
                popups(driver).boolean_values.options[str(boolean).lower()].click()
    else:
        choose_file_as_initial_workflow_value(
            selenium,
            browser_id,
            item_list,
            modals,
            op_container,
            popups,
            data_type,
        )

    confirm_workflow_to_execute(selenium, browser_id, op_container)


@wt(
    parsers.parse(
        'user of {browser_id} modifies {menu} in "{store_name}" '
        'store to be "{value}" for "{workflow_name}" workflow'
    )
)
def modify_data_type_in_store(
    selenium,
    browser_id,
    oz_page,
    store_name,
    modals,
    popups,
    value,
    menu,
    tmp_memory,
):
    driver = selenium[browser_id]
    dropdown_menu = f"{menu} dropdown menu"
    button = "OK"
    modal_name = "Modify store"
    value = value.lower()

    page = get_oz_workflow_visualizer(oz_page, driver)
    page.stores_list[store_name].click()

    if "data" in menu:
        # wait a moment for modal to open
        _wait_for_modal_to_appear(driver, browser_id, modal_name, tmp_memory)
        modals(driver).modify_store.data_type_remove()

    split_value = value.replace(")", "").split(" (")
    new_value = split_value[0] if "array" in value else value
    choose_option_in_dropdown_menu_in_modal(
        selenium,
        browser_id,
        modals,
        dropdown_menu,
        popups,
        new_value,
        modal_name,
    )
    if "array" in value:
        choose_option_in_dropdown_menu_in_modal(
            selenium,
            browser_id,
            modals,
            dropdown_menu,
            popups,
            split_value[1],
            modal_name,
        )
    click_modal_button(selenium, browser_id, button, modal_name, modals)
