"""This module contains gherkin steps to run acceptance tests featuring
automation management in onezone web GUI"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os
from typing import Optional

from _pytest._py.path import LocalPath
from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.oneprovider.archives import from_ordinal_number_to_int
from tests.gui.types import TmpMemory
from tests.gui.utils import OZLoggedIn, Popups
from tests.gui.utils.generic import (
    parse_seq,
    transform,
    upload_file_path,
    upload_lambda_path,
    upload_workflow_path,
)
from tests.gui.utils.onezone.lambdas_subpage import Lambda
from tests.gui.utils.onezone.workflows_subpage import Workflow, WorkflowVisualiser
from tests.types import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        "user of {browser_id} clicks on Create automation inventory "
        "button in automation sidebar"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_automation_button_in_sidebar(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    OZLoggedIn(selenium[browser_id])["automation"].create_automation()


def get_oz_workflow_visualizer(driver: WebDriver) -> WorkflowVisualiser:
    page = OZLoggedIn(driver)
    if page.is_panel_clicked("automation"):
        return page["automation"].workflows_page.workflow_visualiser
    return page.get_page_and_click("automation").workflows_page.workflow_visualiser


@wt(
    parsers.parse('user of {browser_id} writes "{text}" into inventory name text field')
)
@repeat_failed(timeout=WAIT_FRONTEND)
def input_name_into_input_box_on_main_automation_page(
    selenium: SeleniumDrivers, browser_id: str, text: str
) -> None:
    OZLoggedIn(selenium[browser_id])["automation"].input_box.value = text


@wt(
    parsers.parse(
        "user of {browser_id} clicks on confirmation button on automation page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_name_input_on_main_automation_page(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    OZLoggedIn(selenium[browser_id])["automation"].input_box.confirm()


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) clicks on "
        '"(?P<option>Rename|Leave|Remove)" '
        'button in inventory "(?P<inventory>.*)" menu in the '
        "sidebar"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_inventory_menu(
    selenium: SeleniumDrivers, browser_id: str, option: str, inventory: str
) -> None:
    driver = selenium[browser_id]
    page = OZLoggedIn(driver).get_page_and_click("automation")
    page.elements_list[inventory]()
    page.elements_list[inventory].menu()
    Popups(driver).menu_popup_with_text.menu[option]()


@wt(
    parsers.parse(
        'user of {browser_id} writes "{text}" into rename inventory text field'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def input_new_inventory_name_into_rename_inventory_input_box(
    selenium: SeleniumDrivers, browser_id: str, text: str
) -> None:
    page = OZLoggedIn(selenium[browser_id])["automation"]
    page.elements_list[0].edit_box.value = text


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) confirms inventory rename with confirmation button"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_rename_the_inventory(selenium: SeleniumDrivers, browser_id: str) -> None:
    OZLoggedIn(selenium[browser_id])["automation"].automations_list[
        0
    ].edit_box.confirm()


@wt(
    parsers.re(
        "users? of (?P<browser_ids>.*) (?P<option>does not see|sees) "
        'inventory "(?P<inventory>.*)" on inventory list'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_inventory_exists(
    selenium: SeleniumDrivers, browser_ids: str, option: str, inventory: str
) -> None:
    for browser_id in parse_seq(browser_ids):
        elem_list = OZLoggedIn(selenium[browser_id])["automation"].elements_list

        if option == "does not see":
            assert inventory not in elem_list, f"inventory: {inventory} found"
        else:
            assert inventory in elem_list, f"inventory: {inventory} not found"


@wt(
    parsers.re(
        'user of (?P<browser_id>.*) opens inventory "(?P<inventory>.*)" '
        "(?P<subpage>workflows|lambdas|members|main) subpage"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def go_to_inventory_subpage(
    selenium: SeleniumDrivers,
    browser_id: str,
    inventory: str,
    subpage: str,
    tmp_memory: TmpMemory,
) -> None:
    try:
        page = tmp_memory[browser_id]["oz_page"]
    except KeyError:
        page = OZLoggedIn(selenium[browser_id]).get_page_and_click("automation")
        tmp_memory[browser_id]["oz_page"] = page
    page.elements_list[inventory]()
    if subpage != "main":
        getattr(page.elements_list[inventory], subpage)()


@wt(
    parsers.parse(
        'user of {browser_ids} sees "{text}" label in "{inventory}" main page'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_text_in_inventory_page(
    selenium: SeleniumDrivers, browser_ids: str, text: str
) -> None:
    for browser_id in parse_seq(browser_ids):
        err_msg = OZLoggedIn(selenium[browser_id])["automation"].privileges_err_msg

        assert text in err_msg, f"Error message: {text} not found"


@wt(
    parsers.parse(
        'user of {browser_id} uses "Upload (json)" button from menu '
        'bar to upload workflow "{file_name}" to current dir '
        "without waiting for upload to finish"
    )
)
@repeat_failed(timeout=2 * WAIT_BACKEND)
def upload_workflow_as_json(
    selenium: SeleniumDrivers, browser_id: str, file_name: str
) -> None:
    driver = selenium[browser_id]
    OZLoggedIn(driver)["automation"].upload_workflow(upload_file_path(file_name))


@repeat_failed(timeout=2 * WAIT_BACKEND)
def upload_workflow_from_repository(
    selenium: SeleniumDrivers, browser_id: str, workflow_name: str
) -> None:
    driver = selenium[browser_id]
    if os.path.isdir(upload_workflow_path(workflow_name)):
        dump_path = f"{upload_workflow_path(workflow_name)}/{workflow_name}.json"
    else:
        dump_path = upload_workflow_path(workflow_name + ".json")
    automation_page = OZLoggedIn(driver)["automation"]
    automation_page.upload_workflow(dump_path)


@repeat_failed(timeout=2 * WAIT_BACKEND)
def upload_lambda_from_repository(
    selenium: SeleniumDrivers, browser_id: str, lambda_name: str
) -> None:
    driver = selenium[browser_id]
    lambda_name = "".join([lambda_name, "/", lambda_name, ".json"])
    automation_page = OZLoggedIn(driver)["automation"]
    automation_page.upload_lambda(upload_lambda_path(lambda_name))


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) (?P<option>does not see|sees) "
        '"(?P<workflow>.*)" in workflows list '
        "in inventory workflows subpage"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_workflow_exists(
    selenium: SeleniumDrivers, browser_id: str, workflow: str, option: str
) -> None:
    page = OZLoggedIn(selenium[browser_id])["automation"]

    if option == "does not see":
        assert (
            workflow not in page.workflows_page.elements_list
        ), f"Workflow: {workflow} found "
    else:
        assert (
            workflow in page.workflows_page.elements_list
        ), f"Workflow: {workflow} not found "


@wt(
    parsers.parse(
        'user of {browser_id} sees "{lambda_name}" in lambdas list '
        "in inventory lambdas subpage"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_lambda_exists(
    selenium: SeleniumDrivers, browser_id: str, lambda_name: str
) -> None:
    page = OZLoggedIn(selenium[browser_id])["automation"]

    assert (
        lambda_name in page.lambdas_page.elements_list
    ), f"Lambda: {lambda_name} not found "


@wt(
    parsers.parse(
        "user of {browser_id} sees there are {number} lambdas "
        "in lambdas list in inventory lambdas subpage"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_number_of_lambdas(
    selenium: SeleniumDrivers, browser_id: str, number: str
) -> None:
    page = OZLoggedIn(selenium[browser_id])["automation"]
    lambdas_number = len(page.lambdas_page.elements_list)
    err_msg = f"number of lambdas is {lambdas_number} instead of {number}"
    assert lambdas_number == int(number), err_msg


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "Create new revision" in "{lambda_name}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_create_new_revision_button(
    selenium: SeleniumDrivers, browser_id: str, lambda_name: str
) -> None:
    page = OZLoggedIn(selenium[browser_id])["automation"]
    page.lambdas_page.elements_list[lambda_name].create_new_revision.click()


def collapse_revision_list(subpage: Lambda | Workflow) -> None:
    subpage.show_revisions_button.click()


def get_lambda_or_workflow_bracket(
    selenium: SeleniumDrivers, browser_id: str, page: str, object_name: str
) -> Lambda | Workflow:
    page_name = page + "s_page"
    subpage = getattr(OZLoggedIn(selenium[browser_id])["automation"], page_name)

    bracket = subpage.elements_list[object_name]

    try:
        collapse_revision_list(bracket)
    except (RuntimeError, AttributeError):
        pass

    return bracket


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) (?P<option>does not see|sees) that "
        "(?P<ordinal>1st|2nd|3rd|4th) revision of "
        '"(?P<object_name>.*)" (?P<page>lambda|workflow) '
        'is described "(?P<description>.*)"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_revision_description_in_object_bracket(
    selenium: SeleniumDrivers,
    browser_id: str,
    ordinal: str,
    option: str,
    object_name: str,
    page: str,
    description: str,
) -> None:
    bracket = get_lambda_or_workflow_bracket(selenium, browser_id, page, object_name)

    revision = bracket.revision_list[ordinal[:-2]]

    if option == "does not see":
        assert revision.name != description, f"Revision: {object_name} found"
    else:
        assert revision.name == description, f"Revision: {object_name} not found"


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) (?P<option>does not see|sees) "
        "(?P<ordinal>1st|2nd|3rd|4th) revision of "
        '"(?P<object_name>.*)" (?P<page>lambda|workflow)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_revision_of_object(
    selenium: SeleniumDrivers,
    browser_id: str,
    ordinal: str,
    option: str,
    object_name: str,
    page: str,
) -> None:
    bracket = get_lambda_or_workflow_bracket(selenium, browser_id, page, object_name)

    if option == "does not see":
        assert ordinal[:-2] not in bracket.revision_list, f"{ordinal} revision found"
    else:
        assert ordinal[:-2] in bracket.revision_list, f"{ordinal} revision not found"


@wt(
    parsers.re(
        'user of (?P<browser_id>.*) clicks on "(?P<option>Redesign as '
        r'new revision|Duplicate to...|Download \(json\)|Remove)" button '
        "from (?P<ordinal>1st|2nd|3rd|4th) revision of "
        '"(?P<object_name>.*)" (?P<page>lambda|workflow) menu'
    )
)
def click_option_in_revision_menu_button_ordinal(
    selenium: SeleniumDrivers,
    browser_id: str,
    option: str,
    object_name: str,
    ordinal: str,
    page: str,
) -> None:
    click_option_in_revision_menu_button(
        selenium, browser_id, option, object_name, page, ordinal
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_revision_menu_button(
    selenium: SeleniumDrivers,
    browser_id: str,
    option: str,
    object_name: str,
    page: str,
    ordinal: Optional[str] = None,
) -> None:
    item = get_lambda_or_workflow_bracket(selenium, browser_id, page, object_name)
    if ordinal is None:
        item.revision_list[0].menu_button.click()
    else:
        ordinal_parsed = str(from_ordinal_number_to_int(ordinal))
        item.revision_list[ordinal_parsed].menu_button.click()
    Popups(selenium[browser_id]).menu_popup_with_label.menu[option].click()


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "{option}" button in '
        'workflow "{workflow}" menu in workflows subpage'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_workflow_menu_button(
    selenium: SeleniumDrivers, browser_id: str, workflow: str, option: str
) -> None:
    page = OZLoggedIn(selenium[browser_id])["automation"]
    page.workflows_page.elements_list[workflow].menu_button.click()
    Popups(selenium[browser_id]).menu_popup_with_label.menu[option].click()


@wt(parsers.parse('user of {browser_id} sees that "{file_name}" has been downloaded'))
@repeat_failed(timeout=WAIT_FRONTEND)
def has_downloaded_workflow_file_content(
    browser_id: str, tmpdir: LocalPath, file_name: str
) -> None:
    downloaded_file = tmpdir.join(browser_id, "download", file_name)
    assert downloaded_file.exists(), f"file {file_name} has not been downloaded"


@wt(parsers.parse('user of {browser_id} changes workflow view to "{tab_name}" tab'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_navigation_tab_in_workflow(
    selenium: SeleniumDrivers, browser_id: str, tab_name: str
) -> None:
    page = OZLoggedIn(selenium[browser_id])["automation"]
    page.workflows_page.navigation_tab[tab_name].click()


@wt(
    parsers.parse(
        'user of {browser_id} writes "{text}" in description '
        "textfield in workflow Details tab"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def insert_text_in_description_of_revision(
    selenium: SeleniumDrivers, browser_id: str, text: str
) -> None:
    page = OZLoggedIn(selenium[browser_id])["automation"]
    page.workflows_page.revision_details.description = text


def click_on_option_of_inventory_on_left_sidebar_menu(
    selenium: SeleniumDrivers, browser_id: str, inventory_name: str, option: str
) -> None:
    driver = selenium[browser_id]
    getattr(
        OZLoggedIn(driver)["automation"].elements_list[inventory_name],
        transform(option),
    ).click()


def try_to_close_workflow_creation_popup(driver: WebDriver) -> None:
    try:
        Popups(driver).workflow_creation_alert.close()
    except Exception:  # pylint: disable=broad-exception-caught
        pass


@wt(parsers.parse("user of {browser_id} sees that workflow editor appeared"))
def wt_wait_for_workflow_editor_to_expand(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    wait_for_workflow_editor_to_expand(selenium[browser_id])


def wait_for_workflow_editor_to_expand(driver: WebDriver) -> None:
    wait_for_sliding_panel_to_stop_moving(
        driver, WAIT_FRONTEND, '[data-one-carousel-slide-id="editor"]'
    )
