"""This module contains gherkin steps to run acceptance tests featuring
workflow creation in onezone web GUI"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
import time

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.common import wait_for_sliding_panel_to_stop_moving
from tests.gui.steps.common.miscellaneous import press_backspace_on_active_element
from tests.gui.steps.modals.modal import wt_wait_for_modal_to_appear
from tests.gui.steps.onezone.automation.automation_basic import collapse_revision_list
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils import OZLoggedIn, Popups
from tests.gui.utils.generic import transform
from tests.gui.utils.onezone.automation_page import AutomationPage
from tests.gui.utils.onezone.workflows_subpage import JSONWorkflowsPanel
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) uses "
        r'"(?P<option>Add new lambda|Add new workflow)" button from '
        r"menu bar in (lambdas|workflows) subpage"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_add_new_button_in_menu_bar(
    selenium: SeleniumDrivers, browser_id: str, option: str
) -> None:
    driver = selenium[browser_id]
    getattr(OZLoggedIn(driver).automation.main_page, transform(option)).click()
    wait_for_sliding_panel_to_stop_moving(
        driver, WAIT_FRONTEND, '[data-one-carousel-slide-id="editor"]'
    )


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) writes "(?P<text>.*)" into ('
        r"?P<text_field>lambda name|docker image) text field"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def write_text_into_lambda_form(
    selenium: SeleniumDrivers, browser_id: str, text: str, text_field: str
) -> None:
    page = OZLoggedIn(selenium[browser_id]).automation
    label = getattr(page.lambdas_page.form, transform(text_field))
    setattr(label, "value", text)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) (?P<option>checks|unchecks) "
        r'lambdas "(?P<toggle>Mount space|Read only)" toggle'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def switch_toggle_in_lambda_form(
    selenium: SeleniumDrivers, browser_id: str, option: str, toggle: str
) -> None:
    subpage = OZLoggedIn(selenium[browser_id]).automation.lambdas_page.form
    toggle = transform(toggle) + "_toggle"
    getattr(getattr(subpage, toggle), option[:-1])()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) confirms (creating new|edition of) "
        r"(?P<option>lambda|revision|task) using "
        r'"(Create|Modify)" button'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_lambda_creation_or_edition(
    selenium: SeleniumDrivers, browser_id: str, option: str
) -> None:
    page = OZLoggedIn(selenium[browser_id]).automation

    if option == "task":
        page.workflows_page.task_form.create_button.click()
    else:
        page.lambdas_page.form.create_button.click()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) chooses "(?P<option>.*)" in '
        r'(?P<dropdown_name>.*) in "(?P<object_name>.*)" '
        r"(?P<object_type>result|argument|configuration parameters)"
        r" in task creation page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_option_in_dropdown_menu_in_task_page(
    selenium: SeleniumDrivers,
    browser_id: str,
    option: str,
    object_name: str,
    object_type: str,
) -> None:
    driver = selenium[browser_id]
    page = OZLoggedIn(driver).automation.workflows_page.task_form
    if object_type == "result":
        page.results[object_name + ":"].add_mapping()
        page.results[object_name + ":"].target_store_dropdown[-1].click()
    elif object_type == "argument":
        page.arguments[object_name + ":"].value_builder_dropdown.click()
    elif object_type == "configuration parameters":
        page.conf_parameters[object_name + ":"].value_builder_dropdown.click()

    Popups(driver).power_select.choose_item(option)


def clean_tab_textarea_in_json_argument_editor(
    tab: JSONWorkflowsPanel, selenium: SeleniumDrivers, browser_id: str
) -> None:
    tab.click()
    while tab.text_area:
        press_backspace_on_active_element(selenium, browser_id)
    time.sleep(0.5)


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) writes "(?P<input_value>.*)" into'
        r' json editor bracket in "(?P<object_name>.*)" '
        r"(?P<object_type>result|argument) in task creation page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def write_text_into_editor_bracket(
    selenium: SeleniumDrivers,
    browser_id: str,
    input_value: str,
    object_name: str,
    object_type: str,
) -> None:
    driver = selenium[browser_id]
    page = OZLoggedIn(driver).automation.workflows_page.task_form
    if object_type == "result":
        page.results[object_name + ":"].json_editor = input_value
    elif object_type == "argument":
        tab = page.arguments[object_name + ":"]
        if tab.data_type == "STRING":
            tab.string_editor = input_value
        elif tab.data_type == "OBJECT":
            clean_tab_textarea_in_json_argument_editor(tab.json, selenium, browser_id)
            tab.json.text_area = json.dumps(input_value)
    elif object_type == "configuration parameters":
        page.conf_parameters[object_name + ":"].value_editor = str(input_value)


@wt(parsers.parse('user of {browser_id} writes "{text}" into workflow name text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def write_text_into_workflow_name_on_main_workflows_page(
    selenium: SeleniumDrivers, browser_id: str, text: str
) -> None:
    page = OZLoggedIn(selenium[browser_id]).automation
    page.workflows_page.workflow_creator.workflow_name.value = text


@wt(
    parsers.parse(
        'user of {browser_id} confirms creating new workflow using "Create" button'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_workflow_creation(selenium: SeleniumDrivers, browser_id: str) -> None:
    page = OZLoggedIn(selenium[browser_id]).automation
    page.workflows_page.workflow_creator.create_button.click()


@wt(
    parsers.parse(
        'user of {browser_id} clicks "Add store" button in workflow visualizer'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_add_store_button(selenium: SeleniumDrivers, browser_id: str) -> None:
    page = OZLoggedIn(selenium[browser_id]).automation
    page.workflows_page.workflow_visualiser.add_store_button.click()


@wt(
    parsers.parse(
        'user of {browser_id} sees "{store_name}" in the stores '
        "list in workflow visualizer"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_store_in_store_list(
    selenium: SeleniumDrivers, browser_id: str, store_name: str
) -> None:
    page = OZLoggedIn(selenium[browser_id]).automation
    stores_list = page.workflows_page.workflow_visualiser.stores_list

    assert store_name in stores_list, f"Store: {store_name} not found"


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) clicks on create lane button "
        r"(?P<option>in the middle|on the right side of latest created"
        r" lane) of workflow visualizer"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_add_lane_button_in_workflow_visualizer(
    selenium: SeleniumDrivers, browser_id: str, option: str, tmp_memory: TmpMemory
) -> None:
    page = OZLoggedIn(selenium[browser_id]).automation
    modal_name = "create new lane"
    if "right" in option:
        page.workflows_page.workflow_visualiser.create_lane_button[-1].click()
    else:
        page.workflows_page.workflow_visualiser.create_lane_button[0].click()
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)


@wt(
    parsers.parse('user of {browser_id} sees "{lane_name}" lane in workflow visualizer')
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_lane_in_workflow_visualizer(
    selenium: SeleniumDrivers, browser_id: str, lane_name: str
) -> None:
    page = OZLoggedIn(selenium[browser_id]).automation
    workflow_visualizer = page.workflows_page.workflow_visualiser.workflow_lanes

    assert lane_name in workflow_visualizer, f"Lane: {lane_name} not found"


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "Add parallel box" button in '
        'the middle of "{lane_name}" lane'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def add_parallel_box_to_lane(
    selenium: SeleniumDrivers, browser_id: str, lane_name: str
) -> None:
    page = OZLoggedIn(selenium[browser_id]).automation
    workflow_visualiser = page.workflows_page.workflow_visualiser
    workflow_visualiser.workflow_lanes[lane_name].add_parallel_box_button.click()


@wt(
    parsers.parse(
        'user of {browser_id} clicks "Create task" button in empty '
        'parallel box in "{lane_name}" lane'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def add_task_to_empty_parallel_box(
    selenium: SeleniumDrivers, browser_id: str, lane_name: str
) -> None:
    page = OZLoggedIn(selenium[browser_id]).automation
    lane = page.workflows_page.workflow_visualiser.workflow_lanes[lane_name]
    lane.empty_parallel_box.add_task_button.click()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) (?P<option>does not see|sees) task "
        r'named "(?P<task_name>.*)" in "(?P<lane_name>.*)" lane'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_task_in_lane_in_workflow(
    selenium: SeleniumDrivers,
    browser_id: str,
    lane_name: str,
    task_name: str,
    option: str,
) -> None:
    page = OZLoggedIn(selenium[browser_id]).automation
    workflow_visualiser = page.workflows_page.workflow_visualiser
    task = workflow_visualiser.workflow_lanes[lane_name].parallel_box.task_list

    if option == "does not see":
        assert task_name not in task, f"Task: {task_name} found"
    else:
        assert task_name in task, f"Task: {task_name} not found"


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) writes "(?P<task_name>.*)" '
        r"into name text field in task (creation|edition) subpage"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def write_task_name_in_task_edition_text_field(
    selenium: SeleniumDrivers, browser_id: str, task_name: str
) -> None:
    page = OZLoggedIn(selenium[browser_id]).automation
    page.workflows_page.task_form.task_name.value = task_name


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "{option}" button in task '
        '"{task_name}" menu in "{lane_name}" lane in workflow visualizer'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_task_menu_button(
    selenium: SeleniumDrivers,
    browser_id: str,
    lane_name: str,
    task_name: str,
    option: str,
) -> None:
    driver = selenium[browser_id]
    oz_page = OZLoggedIn(driver)
    oz_page.open_panel(AutomationPage)
    page = oz_page.automation
    workflow_visualiser = page.workflows_page.workflow_visualiser
    box = workflow_visualiser.workflow_lanes[lane_name].parallel_box
    box.task_list[task_name].menu_button.click()

    Popups(driver).menu_popup_with_label.menu[option].click()


@wt(
    parsers.parse(
        'user of {browser_id} writes "{text}" in name textfield of selected workflow'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def insert_text_in_textfield_of_workflow(
    selenium: SeleniumDrivers, browser_id: str, text: str
) -> None:
    page = OZLoggedIn(selenium[browser_id]).automation
    page.workflows_page.workflow_name_input.value = text


@wt(
    parsers.parse(
        "user of {browser_id} confirms edition of selected workflow "
        'details using "Save" button'
    )
)
@wt(
    parsers.parse(
        "user of {browser_id} saves workflow edition by clicking "
        '"Save" button from menu bar'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_in_workflow(selenium: SeleniumDrivers, browser_id: str) -> None:
    page = OZLoggedIn(selenium[browser_id]).automation
    page.workflows_page.workflow_save_button.click()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) chooses "
        r"(?P<ordinal>1st|2nd|3rd|4th) revision of "
        r'"(?P<lambda_name>.*?)" lambda to add to workflow'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def add_lambda_revision_to_workflow(
    selenium: SeleniumDrivers, browser_id: str, lambda_name: str, ordinal: str
) -> None:
    subpage = OZLoggedIn(selenium[browser_id]).automation.lambdas_page
    lambda_object = subpage.lambdas_list[lambda_name]
    revision = lambda_object.revision_list[ordinal[:-2]]

    try:
        collapse_revision_list(lambda_object)
    except (RuntimeError, AttributeError):
        pass

    revision.add_to_workflow.click()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) clicks on "Add parallel box" button'
        r" (?P<position>below|above) Parallel box"
        r' in "(?P<lane_name>.*?)" lane'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def add_another_parallel_box_to_lane(
    selenium: SeleniumDrivers, browser_id: str, lane_name: str, position: str
) -> None:
    page = OZLoggedIn(selenium[browser_id]).automation
    workflow_visualiser = page.workflows_page.workflow_visualiser
    lane = workflow_visualiser.workflow_lanes[lane_name]

    if position == "below":
        lane.add_parallel_box_below.click()
    else:
        lane.add_parallel_box_above.click()
