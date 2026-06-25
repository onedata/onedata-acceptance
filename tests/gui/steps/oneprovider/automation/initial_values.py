"""This module contains gherkin steps to run acceptance tests featuring
workflows initial values in oneprovider web GUI"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time
from typing import Optional, Protocol, cast

from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils import Modals, OPLoggedIn, Popups
from tests.gui.utils.core.web_objects import PageObjectsSequence
from tests.gui.utils.oneprovider.automation import InitialValueStore
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


class InitialValueOption(Protocol):
    name: str

    def click(self) -> None: ...


@repeat_failed(timeout=WAIT_FRONTEND)
def choose_range_as_initial_workflow_value(
    selenium: SeleniumDrivers,
    browser_id: str,
    item: dict[str, object],
    add_new: bool = True,
) -> None:
    driver = selenium[browser_id]
    if add_new:
        OPLoggedIn(driver).automation_page.input_link.click()
    ranges = OPLoggedIn(driver).automation_page.ranges_input

    last_index = len(ranges) - 1
    for key, val in item.items():
        setattr(ranges[last_index], key, str(val))


@repeat_failed(timeout=WAIT_FRONTEND)
def check_if_select_files_modal_disappeared(
    driver: WebDriver, files: str | list[str]
) -> None:
    try:
        Modals(driver).select_files  # pylint: disable=expression-not-assigned
        raise AssertionError(
            f"Files: {files} as initial value for workflow was not selected"
        )
    except RuntimeError:
        pass


@repeat_failed(timeout=WAIT_FRONTEND)
def open_select_initial_files_modal(
    driver: WebDriver, store_name: Optional[str] = None
) -> None:
    option = "Select/upload file"

    click_input_link_in_automation_page(driver, store_name)
    time.sleep(1)
    menu_option = get_select_option_from_initial_value_popup(
        option, Popups(driver).workflow_initial_values.menu
    )
    menu_option.click()
    time.sleep(1)
    # check if modal opened
    Modals(driver).select_files  # pylint: disable=expression-not-assigned


@wt(
    parsers.parse(
        'user of {browser_id} clicks "Add groups..." link in "{store_name}" store'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def open_select_initial_groups_modal(
    selenium: SeleniumDrivers, browser_id: str, store_name: str
) -> None:
    option = "Select groups"
    driver = selenium[browser_id]

    click_input_link_in_automation_page(driver, store_name)
    time.sleep(1)
    menu_option = get_select_option_from_initial_value_popup(
        option, Popups(driver).workflow_group_initial_value.menu
    )
    menu_option.click()
    time.sleep(1)
    # check if modal opened
    Modals(driver).select_groups  # pylint: disable=expression-not-assigned


@repeat_failed(timeout=WAIT_FRONTEND)
def open_select_initial_datasets_modal(driver: WebDriver) -> None:
    option = "Select datasets"
    OPLoggedIn(driver).automation_page.input_link()
    time.sleep(1)
    Popups(driver).workflow_dataset_initial_value.menu[option].click()
    time.sleep(1)
    # check if modal opened
    Modals(driver).select_dataset  # pylint: disable=expression-not-assigned


def get_select_option_from_initial_value_popup(
    option: str, popup_menu: PageObjectsSequence
) -> InitialValueOption:
    for elem in popup_menu:
        option_elem = cast(InitialValueOption, elem)
        if option in option_elem.name:
            return option_elem
    raise ValueError(f"{option} not found in popup menu")


def get_initial_value_store(driver: WebDriver, store_name: str) -> InitialValueStore:
    initial_value_stores = OPLoggedIn(driver).automation_page.initial_value_store
    if store_name + ":" in initial_value_stores:
        return initial_value_stores[store_name + ":"]
    if store_name + ": " in initial_value_stores:
        return initial_value_stores[store_name + ": "]
    raise ValueError()


def click_input_link_in_automation_page(
    driver: WebDriver, store_name: Optional[str]
) -> None:
    if store_name:
        store = get_initial_value_store(driver, store_name)
        store.input_link.click()
    else:
        try:
            # for input store type Single Value this Button does not work
            OPLoggedIn(driver).automation_page.files_input_link.click()
        except RuntimeError:
            # for adding another files to input store (type List) this Button
            # does not work because it finds two links (one for changing file,
            # another for adding)
            # this button is used for input store type Single Value
            OPLoggedIn(driver).automation_page.single_file_input_link.click()


def get_data_type_in_initial_value_store(driver: WebDriver, store_name: str) -> str:
    store = get_initial_value_store(driver, store_name)
    return store.data_type


def get_data_type_of_array_initial_value_store(
    driver: WebDriver, store_name: str
) -> str:
    store = get_initial_value_store(driver, store_name)
    link_name = store.input_link.web_elem.text

    if "group" in link_name:
        return "group"
    if "file" in link_name:
        return "file"
    raise ValueError(f"unknown type for link {link_name}")


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) (?P<option>sees|does not see) "
        '"(?P<group>.*)" group in "Select groups" modal'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_group_in_select_initial_groups_modal(
    selenium: SeleniumDrivers, browser_id: str, option: str, group: str
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).select_groups
    err_msg = "there {} visible {} in select groups modal, but should {}"
    if option == "sees":
        assert group in modal.groups, err_msg.format("is not", group, "be")
    else:
        assert group not in modal.groups, err_msg.format("is", group, "not be")
