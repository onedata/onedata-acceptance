"""This module contains gherkin steps to run acceptance tests featuring
workflows and their execution in oneprovider web GUI"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time
from typing import Any

from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import (
    click_option_in_popup_labeled_menu,
    switch_to_iframe,
)
from tests.gui.steps.oneprovider.archives import from_ordinal_number_to_int
from tests.gui.utils import OPLoggedIn, OZLoggedIn, Popups
from tests.gui.utils.core import scroll_to_css_selector
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed
from tests.conftest import SeleniumDrivers


# this step is created to avoid using repeat_failed in metasteps
@repeat_failed(timeout=WAIT_FRONTEND)
def get_op_workflow_visualizer_page(driver: Any) -> Any:
    return OPLoggedIn(driver).automation_page.workflow_visualiser


def switch_to_automation_page(selenium: SeleniumDrivers, browser_id: Any) -> Any:
    switch_to_iframe(selenium, browser_id)
    return OPLoggedIn(selenium[browser_id]).automation_page


@repeat_failed(timeout=WAIT_FRONTEND)
def get_input_element(driver: Any, input_type: Any) -> Any:
    OPLoggedIn(driver).automation_page.input_link.click()
    return getattr(OPLoggedIn(driver).automation_page, input_type)


@wt(parsers.parse('user of {browser_id} clicks "{tab_name}" in the automation tab bar'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_button_in_navigation_tab(
    selenium: SeleniumDrivers, browser_id: Any, tab_name: Any
) -> Any:
    switch_to_iframe(selenium, browser_id)
    driver = selenium[browser_id]
    try:
        OPLoggedIn(driver).automation_page.navigation_tab[tab_name].click()
    except RuntimeError:
        driver.refresh()
        # wait for page to refresh
        time.sleep(5)
        switch_to_iframe(selenium, browser_id)
        OPLoggedIn(driver).automation_page.navigation_tab[tab_name].click()


@wt(
    parsers.re(
        "user of (?P<browser_id>.*?) chooses to run "
        "(?P<ordinal>1st|2nd|3rd|4th|5th|6th) revision of "
        '"(?P<workflow>.*?)" workflow'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_workflow_revision_to_run(
    selenium: SeleniumDrivers, browser_id: Any, ordinal: Any, workflow: Any
) -> Any:
    page = switch_to_automation_page(selenium, browser_id)
    revision = int(ordinal[:-2]) - 1
    page.available_workflow_list[workflow].revision_list[revision].click()


@wt(
    parsers.parse(
        "user of {browser_id} confirms workflow execution "
        'by clicking "Run workflow" button'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_workflow_to_execute(selenium: SeleniumDrivers, browser_id: Any) -> Any:
    page = switch_to_automation_page(selenium, browser_id)
    page.run_workflow_button.click()


def check_if_task_is_opened(task: Any) -> Any:
    return task.status != ""


def search_for_lane_status(
    driver: Any, page: Any, lane_name: Any, box_number: Any = None
) -> Any:
    workflow_visualiser = page.workflow_visualiser
    number_of_lanes = len(workflow_visualiser.workflow_lanes)

    for i in range(number_of_lanes):
        lane_id = workflow_visualiser.workflow_lanes[i].lane_web_elem.get_attribute(
            "id"
        )
        scroll_to_css_selector(driver, f"#{lane_id}")
        found_lane = driver.find_element(By.CSS_SELECTOR, f"#{lane_id} .lane-name").text
        if found_lane == lane_name:
            if box_number is not None:
                return workflow_visualiser.workflow_lanes[i].parallel_boxes[box_number]
            status = driver.find_element(
                By.CSS_SELECTOR, f"#{lane_id} .visible-run-status-label"
            ).text
            return status
        try:
            page.workflow_visualiser.right_arrow_scroll.click()
        except RuntimeError:
            pass
    raise ValueError(f"lane {lane_name} found")


def search_for_task_in_parallel_box(
    driver: Any, parallel_box: Any, task_name: Any
) -> Any:
    number_of_tasks = len(parallel_box.task_list)
    for j in range(number_of_tasks):
        task_id = parallel_box.task_list[j].name_web_elem.get_attribute("id")
        scroll_to_css_selector(driver, f"#{task_id}")
        found_task = driver.find_element(By.CSS_SELECTOR, f"#{task_id}").text

        if found_task == task_name:
            return parallel_box.task_list[j], task_id
    raise ValueError(f"task {task_name} not found")


@wt(
    parsers.re(
        "user of (?P<browser_id>.*?) (?P<option>clicks on|closes) task "
        '"(?P<task_name>.*?)" in (?P<ordinal>.*?) parallel box in '
        '"(?P<lane_name>.*?)" lane in workflow visualizer'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_task_in_lane(
    selenium: SeleniumDrivers,
    browser_id: Any,
    lane_name: Any,
    task_name: Any,
    ordinal: Any,
    option: Any,
) -> Any:
    number = from_ordinal_number_to_int(ordinal) - 1
    page = switch_to_automation_page(selenium, browser_id)
    driver = selenium[browser_id]

    parallel_box = search_for_lane_status(driver, page, lane_name, number)
    time.sleep(1)
    if len(parallel_box.task_list) == 1:
        task = parallel_box.task_list[0]
    else:
        task, task_id = search_for_task_in_parallel_box(driver, parallel_box, task_name)
    # wait a moment to find parallel box
    time.sleep(1)
    if option == "closes":
        if check_if_task_is_opened(task):
            try:
                task.click_on_drag_handle()
            except ElementNotInteractableException:
                scroll_to_css_selector(driver, ".task-drag-handle")
                time.sleep(1)
                task.click_on_drag_handle()
        # wait for task to be closed
        time.sleep(2)
        assert not check_if_task_is_opened(
            task
        ), f"Failed to close {task_name} task in parallel box"
    else:
        if not check_if_task_is_opened(task):
            if len(parallel_box.task_list) > 1:
                scroll_to_css_selector(driver, f"#{task_id}")
            # wait a moment for scroll
            time.sleep(1)
            task.click_on_drag_handle()


@wt(
    parsers.parse(
        'user of {browser_id} clicks on link "{option}" in '
        '"{task_name}" task in {ordinal} parallel box in '
        '"{lane_name}" lane in workflow visualizer'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_link_in_task_box(
    selenium: SeleniumDrivers,
    browser_id: Any,
    lane_name: Any,
    task_name: Any,
    option: Any,
    ordinal: Any,
) -> Any:
    number = from_ordinal_number_to_int(ordinal) - 1
    page = switch_to_automation_page(selenium, browser_id)
    driver = selenium[browser_id]

    parallel_box = search_for_lane_status(driver, page, lane_name, number)
    task, task_id = search_for_task_in_parallel_box(driver, parallel_box, task_name)

    scroll_to_css_selector(driver, f"#{task_id}")
    parallel_box.scroll_to_bottom_of_task_in_parallel_box(task_id)
    time.sleep(0.5)

    task.click_on_option_in_task(option)


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "{tab_name}" tab in automation subpage'
    )
)
def change_tab_in_automation_subpage(
    selenium: SeleniumDrivers, browser_id: Any, tab_name: Any
) -> Any:
    page = switch_to_automation_page(selenium, browser_id)
    page.navigation_tab[tab_name].click()
    time.sleep(0.25)


@wt(parsers.re("user of (?P<browser_id>.*) clicks on first executed workflow"))
@repeat_failed(timeout=WAIT_FRONTEND)
def expand_first_executed_workflow_record(selenium: SeleniumDrivers, browser_id: Any) -> Any:
    page = switch_to_automation_page(selenium, browser_id)
    change_tab_in_automation_subpage(selenium, browser_id, "Ended")
    page.workflow_executions_list[0].click()


@wt(
    parsers.re(
        'user of (?P<browser_id>.*) clicks on "(?P<workflow>.*)" menu '
        "on workflow executions list"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_workflow_menu(selenium: SeleniumDrivers, browser_id: Any, workflow: Any) -> Any:
    page = switch_to_automation_page(selenium, browser_id)
    page.workflow_executions_list[workflow].menu_button()


@wt(
    parsers.re(
        'user of (?P<browser_id>.*) clicks on "(?P<workflow>.*)" '
        "on workflow executions list"
    )
)
def click_and_enter_workflow(selenium: SeleniumDrivers, browser_id: Any, workflow: Any) -> Any:
    page = switch_to_automation_page(selenium, browser_id)
    page.workflow_executions_list[workflow].click()


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) (?P<option>does not see|sees)"
        ' "(?P<workflow>.*)" on workflow executions list'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_workflow_on_executed_workflows_list(
    selenium: SeleniumDrivers, browser_id: Any, workflow: Any, option: Any
) -> Any:
    page = switch_to_automation_page(selenium, browser_id)

    workflow_executions_list = page.workflow_executions_list
    if option == "does not see":
        err_msg = f"Workflow: {workflow} is on workflow executions list"
        assert workflow not in workflow_executions_list, err_msg
    else:
        err_msg = f"Workflow: {workflow} is not on workflow executions list"
        assert workflow in workflow_executions_list, err_msg


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{option}" option in '
        "data row menu in automation workflows page is disabled"
    )
)
def assert_option_disabled_in_automation_page(
    selenium: SeleniumDrivers, browser_id: Any, option: Any
) -> Any:
    err_msg = (
        f"Option {option} is not disabled in data row menu in automation workflows page"
    )
    disabled_options = Popups(selenium[browser_id]).workflow_menu.disabled_options
    assert option in disabled_options, err_msg


@wt(
    parsers.parse(
        'user of {browser_id} clicks "{option}" option in run menu '
        'for "{lane_name}" lane'
    )
)
def click_option_for_lane(
    selenium: SeleniumDrivers, browser_id: Any, lane_name: Any, option: Any
) -> Any:
    page = switch_to_automation_page(selenium, browser_id)
    workflow_visualiser = page.workflow_visualiser
    lane = workflow_visualiser.workflow_lanes[lane_name]
    lane.latest_run_menu()
    click_option_in_popup_labeled_menu(selenium, browser_id, option)


@wt(
    parsers.parse(
        'user of {browser_id} clicks "{button}" button on '
        '"{workflow}" workflow status bar'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_on_status_bar(selenium: SeleniumDrivers, browser_id: Any, button: Any) -> Any:
    page = switch_to_automation_page(selenium, browser_id)
    time.sleep(1)
    getattr(page.workflow_visualiser, transform(button))()


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) clicks on (?P<ordinal>|1st|2nd"
        '|3rd|4th) revision of "(?P<workflow>.*)" in workflows list '
        "in inventory workflows subpage"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_workflow_in_inventory_subpage(
    selenium: SeleniumDrivers, browser_id: Any, ordinal: Any, workflow: Any
) -> Any:
    driver = selenium[browser_id]
    page = OZLoggedIn(driver)["automation"]
    revision = int(ordinal[:-2]) - 1
    page.workflows_page.elements_list[workflow].revision_list[revision].click()
    # wait for page to open
    time.sleep(1)


@wt(parsers.parse('user of {browser_id} chooses "{level}" logging level'))
def select_logging_level_in_automation_subpage(
    browser_id: Any, selenium: SeleniumDrivers, level: Any
) -> Any:
    driver = selenium[browser_id]
    OPLoggedIn(driver).automation_page.logging_level()
    options = Popups(driver).logging_level
    options.choose_item(level)


@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_elem_in_store_details_modal(
    modal: Any, name: Any, option: Any = ""
) -> Any:
    if option == "archive":
        modal.store_content_list[name].file_name.click()
    elif option == "dataset":
        modal.store_content_list[name].dataset_name.click()
    else:
        modal.single_file_container.clickable_name()

    # wait a moment to open a tab
    time.sleep(1)
