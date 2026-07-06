"""This module contains meta steps for operations on automation page concerning
workflow creation in Onezone using web GUI
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
import time
from ast import literal_eval
from typing import Optional, cast

import yaml

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.meta_steps.oneprovider.automation.run_workflow import (
    choose_file_as_initial_workflow_value,
    choose_file_as_initial_workflow_value_for_store,
    choose_group_as_initial_workflow_value_for_store,
    provide_text_to_object_initial_workflow_value_store,
    provide_text_to_string_initial_workflow_value_store,
    wait_for_workflow_execution_in_atm_subpage,
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
from tests.gui.steps.onezone.automation.automation_basic import (
    assert_workflow_exists,
    get_oz_workflow_visualizer,
    go_to_inventory_subpage,
    upload_workflow_as_json,
    upload_workflow_from_repository,
    wait_for_workflow_editor_to_expand,
)
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
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils import Modals, OPLoggedIn, Popups
from tests.gui.utils.oneprovider.automation import NumberInput
from tests.type_definitions import SeleniumDrivers
from tests.utils.acceptance_utils import get_workflow_dump
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} creates workflow "{workflow_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_workflow_using_gui(
    selenium: SeleniumDrivers, browser_id: str, workflow_name: str
) -> None:
    click_add_new_button_in_menu_bar(selenium, browser_id, "Add new workflow")
    write_text_into_workflow_name_on_main_workflows_page(
        selenium, browser_id, workflow_name
    )

    confirm_workflow_creation(selenium, browser_id)


@wt(
    parsers.parse(
        'user of {browser_id} uploads "{workflow}" workflow from '
        '"{file_name}" file to "{inventory}" inventory'
    )
)
def upload_and_assert_workflow_to_inventory_using_gui(
    selenium: SeleniumDrivers,
    browser_id: str,
    inventory: str,
    workflow: str,
    file_name: str,
    tmp_memory: TmpMemory,
) -> None:
    driver = selenium[browser_id]
    click_on_automation_option_in_the_sidebar(selenium, browser_id, tmp_memory)
    go_to_inventory_subpage(selenium, browser_id, inventory, "workflows", tmp_memory)
    upload_workflow_as_json(selenium, browser_id, file_name)
    _wait_for_modal_to_appear(driver, browser_id, "Upload workflow", tmp_memory)
    click_modal_button(selenium, browser_id, "Apply", "Upload workflow")
    wait_for_workflow_editor_to_expand(driver)
    go_to_inventory_subpage(selenium, browser_id, inventory, "workflows", tmp_memory)

    assert_workflow_exists(selenium, browser_id, workflow, "sees")


@given(
    parsers.parse(
        'user of {browser_id} uploads "{workflow}" workflow from '
        'automation-examples repository to "{inventory}" inventory'
    )
)
def given_upload_workflow_from_automation_examples(
    selenium: SeleniumDrivers,
    browser_id: str,
    inventory: str,
    workflow: str,
    tmp_memory: TmpMemory,
) -> None:
    upload_workflow_from_automation_examples(
        selenium, browser_id, inventory, workflow, tmp_memory
    )


@wt(
    parsers.parse(
        'user of {browser_id} uploads "{workflow}" workflow from '
        'automation-examples repository to "{inventory}" inventory'
    )
)
def upload_workflow_from_automation_examples(
    selenium: SeleniumDrivers,
    browser_id: str,
    inventory: str,
    workflow: str,
    tmp_memory: TmpMemory,
) -> None:
    _upload_workflow_from_automation_examples(
        selenium, browser_id, inventory, workflow, tmp_memory
    )


@wt(
    parsers.parse(
        'user of {browser_id} uploads "{workflow}" workflow {method} from '
        'automation-examples repository to "{inventory}" inventory'
    )
)
def upload_workflow_from_automation_examples_with_given_method(
    selenium: SeleniumDrivers,
    browser_id: str,
    inventory: str,
    workflow: str,
    tmp_memory: TmpMemory,
    method: str,
) -> None:
    _upload_workflow_from_automation_examples(
        selenium,
        browser_id,
        inventory,
        workflow,
        tmp_memory,
        method=method,
    )


def _upload_workflow_from_automation_examples(
    selenium: SeleniumDrivers,
    browser_id: str,
    inventory: str,
    workflow: str,
    tmp_memory: TmpMemory,
    method: Optional[str] = None,
) -> None:
    subpage = "workflows"
    modal = "Upload workflow"
    button = "Apply"
    driver = selenium[browser_id]

    click_on_automation_option_in_the_sidebar(selenium, browser_id, tmp_memory)
    go_to_inventory_subpage(selenium, browser_id, inventory, subpage, tmp_memory)
    upload_workflow_from_repository(selenium, browser_id, workflow)
    _wait_for_modal_to_appear(driver, browser_id, modal, tmp_memory)
    if method == "as new workflow":
        method_button = "Persist as new workflow"
        click_modal_button(selenium, browser_id, method_button, modal)
    elif method == "and merge into existing workflow":
        method_button = "Merge into existing workflow"
        click_modal_button(selenium, browser_id, method_button, modal)
    click_modal_button(selenium, browser_id, button, modal)
    go_to_inventory_subpage(selenium, browser_id, inventory, subpage, tmp_memory)
    visible_workflow_name = change_workflow_dump_name_to_visible_name(workflow)
    assert_workflow_exists(selenium, browser_id, visible_workflow_name, "sees")


def change_workflow_dump_name_to_visible_name(workflow_name: str) -> str:
    data = get_workflow_dump(workflow_name)
    return data["name"]


@wt(
    parsers.parse(
        "user of {browser_id} executes {ordinal} revision of "
        '"{workflow}" workflow in "{space}" space with the following '
        "initial values:\n{config}"
    )
)
def execute_workflow_with_input_config(
    browser_id: str,
    selenium: SeleniumDrivers,
    space: str,
    ordinal: str,
    workflow: str,
    config: str,
) -> None:
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
        space,
        ordinal,
        workflow,
        config,
    )


def _execute_workflow_with_input_config(
    browser_id: str,
    selenium: SeleniumDrivers,
    space: str,
    ordinal: str,
    workflow: str,
    config: str,
) -> None:
    try:
        click_element_on_lists_on_left_sidebar_menu(
            selenium, browser_id, "spaces", space
        )
    except IndexError:
        pass
    click_on_option_of_space_on_left_sidebar_menu(
        selenium, browser_id, space, "Automation Workflows"
    )
    click_button_in_navigation_tab(selenium, browser_id, "Run workflow")
    choose_workflow_revision_to_run(selenium, browser_id, ordinal, workflow)

    # wait a moment for workflow revision to open
    time.sleep(1)

    data = yaml.load(config, yaml.Loader)
    for store in data:
        driver = selenium[browser_id]
        data_type = get_data_type_in_initial_value_store(driver, store)
        if data_type == "FILE":
            file_list = data[store]
            choose_file_as_initial_workflow_value_for_store(
                selenium,
                browser_id,
                file_list,
                store,
            )
        elif data_type == "ARRAY":
            item_list = data[store]
            array_store_type = get_data_type_of_array_initial_value_store(driver, store)
            if array_store_type == "group":
                choose_group_as_initial_workflow_value_for_store(
                    selenium,
                    browser_id,
                    item_list,
                    store,
                )
            elif array_store_type == "file":
                choose_file_as_initial_workflow_value_for_store(
                    selenium,
                    browser_id,
                    item_list,
                    store,
                )
            else:
                raise ValueError(f"unknown data type {array_store_type}")
        elif data_type == "OBJECT":
            text = data[store][0]
            provide_text_to_object_initial_workflow_value_store(driver, store, text)
        elif data_type == "STRING":
            text = data[store][0]
            provide_text_to_string_initial_workflow_value_store(driver, store, text)
        else:
            raise ValueError(f"unknown data type {data_type}")

    confirm_workflow_to_execute(selenium, browser_id)
    wait_for_workflow_execution_in_atm_subpage(selenium, browser_id)
    expand_first_executed_workflow_record(selenium, browser_id)


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
    browser_id: str,
    selenium: SeleniumDrivers,
    space: str,
    ordinal: str,
    workflow: str,
    item_list: str,
    data_type: str,
) -> None:

    execute_workflow(
        browser_id,
        selenium,
        space,
        ordinal,
        workflow,
        item_list,
        data_type,
    )

    wait_for_workflow_execution_in_atm_subpage(selenium, browser_id)
    expand_first_executed_workflow_record(selenium, browser_id)


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) executes (?P<ordinal>.*) revision"
        ' of "(?P<workflow>.*)", using (?P<data_type>.*) as initial '
        'value: "(?P<item_list>.*)" in "(?P<space>.*)" '
        "space"
    )
)
def execute_workflow(
    browser_id: str,
    selenium: SeleniumDrivers,
    space: str,
    ordinal: str,
    workflow: str,
    item_list: str,
    data_type: str,
) -> None:
    spaces = "spaces"
    automation_workflows = "Automation Workflows"
    tab_name = "Run workflow"
    driver = selenium[browser_id]

    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id, spaces, space)
    click_on_option_of_space_on_left_sidebar_menu(
        selenium, browser_id, space, automation_workflows
    )
    click_button_in_navigation_tab(selenium, browser_id, tab_name)
    choose_workflow_revision_to_run(selenium, browser_id, ordinal, workflow)
    # wait a moment for workflow revision to open
    time.sleep(1)
    if "range" in data_type:
        range_items = literal_eval(item_list)
        if isinstance(range_items, list):
            for item in range_items:
                choose_range_as_initial_workflow_value(
                    selenium, browser_id, cast(dict[str, object], item)
                )
        else:
            choose_range_as_initial_workflow_value(
                selenium, browser_id, cast(dict[str, object], range_items), False
            )
    elif "number" in data_type:
        items = literal_eval(item_list)
        if isinstance(items, list):
            for number in items:
                numbers = get_input_element(driver, "numbers_input")
                cast(NumberInput, numbers[len(numbers) - 1]).input = str(number)
        else:
            numbers = OPLoggedIn(driver).automation_page.numbers_input
            cast(NumberInput, numbers[len(numbers) - 1]).input = str(item_list)
    elif "string" in data_type:
        OPLoggedIn(driver).automation_page.string_input.input = item_list
    elif "boolean" in data_type:
        items = json.loads(item_list)
        if isinstance(items, list):
            for boolean in items:
                booleans = get_input_element(driver, "booleans_input")
                booleans[len(booleans) - 1].click()
                Popups(driver).boolean_values.options[str(boolean).lower()].click()
    else:
        choose_file_as_initial_workflow_value(
            selenium,
            browser_id,
            item_list,
            data_type,
        )

    confirm_workflow_to_execute(selenium, browser_id)


@wt(
    parsers.parse(
        'user of {browser_id} modifies {menu} in "{store_name}" '
        'store to be "{value}" for "{workflow_name}" workflow'
    )
)
def modify_data_type_in_store(
    selenium: SeleniumDrivers,
    browser_id: str,
    store_name: str,
    value: str,
    menu: str,
    tmp_memory: TmpMemory,
) -> None:
    driver = selenium[browser_id]
    dropdown_menu = f"{menu} dropdown menu"
    button = "OK"
    modal_name = "Modify store"
    value = value.lower()

    page = get_oz_workflow_visualizer(driver)
    page.stores_list[store_name].click()

    if "data" in menu:
        # wait a moment for modal to open
        _wait_for_modal_to_appear(driver, browser_id, modal_name, tmp_memory)
        Modals(driver).modify_store.data_type_remove()

    split_value = value.replace(")", "").split(" (")
    new_value = split_value[0] if "array" in value else value
    choose_option_in_dropdown_menu_in_modal(
        selenium,
        browser_id,
        dropdown_menu,
        new_value,
        modal_name,
    )
    if "array" in value:
        choose_option_in_dropdown_menu_in_modal(
            selenium,
            browser_id,
            dropdown_menu,
            split_value[1],
            modal_name,
        )
    click_modal_button(selenium, browser_id, button, modal_name)
