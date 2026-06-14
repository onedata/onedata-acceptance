"""This module contains gherkin steps to run acceptance tests featuring
harvester indices management in onezone web GUI.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time
from collections.abc import Iterable
from datetime import datetime

from selenium.webdriver.remote.webelement import WebElement

from tests.conftest import SeleniumDrivers
from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.onezone.harvesters.data_discovery import (
    click_button_on_data_disc_page,
)
from tests.gui.types import Clipboard, DisplayMap, TmpMemory
from tests.gui.utils import DataDiscoveryPage as DataDiscovery
from tests.gui.utils import OZLoggedIn, Popups
from tests.gui.utils.generic import parse_seq
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed

CREATE_INDEX_TOGGLES = {
    "include_metadata": ["xattrs", "json", "rdf"],
    "include_file_details": [
        "file_name",
        "file_type",
        "space_id",
        "dataset_info",
        "metadata_existence_flags",
        "archive_info",
    ],
    "rejection_toggles": ["include_rejection_reason", "retry_on_rejection"],
}


@wt(
    parsers.parse('user of {browser_id} clicks "{text}" in harvester indices page menu')
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_member_menu_option_in_harvester_indices_page(
    selenium: SeleniumDrivers, browser_id: str, text: str
) -> None:
    driver = selenium[browser_id]
    OZLoggedIn(driver)["discovery"].indices_page.menu_button.click()
    Popups(driver).menu_popup_with_text.menu[text]()


@wt(
    parsers.parse(
        'user of {browser_id} types "{index_name}" to name input field in indices page'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def type_index_name_to_input_field_in_indices_page(
    selenium: SeleniumDrivers, browser_id: str, index_name: str
) -> None:
    driver = selenium[browser_id]
    OZLoggedIn(driver)["discovery"].indices_page.name_input = index_name


@wt(parsers.parse("user of {browser_id} clicks on Create button in indices page"))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_button_in_indices_page(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    OZLoggedIn(driver)["discovery"].indices_page.create_button()


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{index_name}" has appeared on the indices list'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_index_has_appeared_in_indices_page(
    selenium: SeleniumDrivers, browser_id: str, index_name: str
) -> None:
    driver = selenium[browser_id]
    indices_list = OZLoggedIn(driver)["discovery"].indices_page.indices_list
    assert index_name in indices_list, f'index "{index_name}" not found'


@wt(
    parsers.parse(
        'user of {browser_id} expands "{index_name}" index record in indices page'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def expand_index_record_in_indices_page(
    selenium: SeleniumDrivers, browser_id: str, index_name: str | int
) -> None:
    driver = selenium[browser_id]
    indices_list = OZLoggedIn(driver)["discovery"].indices_page.indices_list
    indices_list[index_name].click()


@wt(
    parsers.parse(
        'user of {browser_id} sees "Used by GUI" tag on '
        '"{index}" index record in indices page'
    )
)
def assert_used_by_gui_tag_on_indices_page(
    selenium: SeleniumDrivers, browser_id: str, index: int
) -> None:
    driver = selenium[browser_id]
    indices_list = OZLoggedIn(driver)["discovery"].indices_page.indices_list
    assert indices_list[
        index
    ].is_used_by_gui_tag_visible(), f"Used by GUI tag is not visible for {index}"


@wt(
    parsers.parse(
        "user of {browser_id} sees 100% progress for "
        'all spaces in "{index_name}" index harvesting'
    )
)
@repeat_failed(timeout=WAIT_BACKEND * 4)
def assert_progress_in_harvesting(
    selenium: SeleniumDrivers, browser_id: str, index_name: str | int
) -> None:
    driver = selenium[browser_id]
    value = "100%"
    indices_list = OZLoggedIn(driver)["discovery"].indices_page.indices_list
    progress_values = indices_list[index_name].progress_values

    for progress in progress_values:
        assert (
            progress.progress_value == value
        ), f'Harvesting process did not finished for "{progress.space}"'


@wt(
    parsers.parse(
        "user of {browser_id} unchecks all toggles apart from "
        "{stay_checked} in indices page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def uncheck_toggles_on_create_index_page(
    selenium: SeleniumDrivers, browser_id: str, stay_checked: str
) -> None:
    driver = selenium[browser_id]
    toggles_to_keep = parse_seq(stay_checked)
    indices_page = OZLoggedIn(driver)["discovery"].indices_page
    for toggles_group, toggle_group_types in CREATE_INDEX_TOGGLES.items():
        for toggle in toggle_group_types:
            if toggle not in toggles_to_keep:
                if toggles_group == "rejection_toggles":
                    getattr(indices_page, toggle).click()
                else:
                    toggles = getattr(indices_page, toggles_group)
                    getattr(toggles, toggle).click()


@wt(
    parsers.parse(
        'user of {browser_id} changes indices to "{index_name}" '
        "on GUI plugin tab on harvester configuration page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def change_indices_on_gui_plugin_tab(
    selenium: SeleniumDrivers, browser_id: str, index_name: str
) -> None:
    driver = selenium[browser_id]
    gui_plugin_tab = OZLoggedIn(driver)["discovery"].configuration_page.gui_plugin_tab
    gui_plugin_tab.indices_edit()
    gui_plugin_tab.choose_indices_expand()
    Popups(driver).power_select.choose_item(index_name)
    gui_plugin_tab.indices_save()


@wt(
    parsers.parse(
        'user of {browser_id} does not see "{name}" in'
        " results list on data discovery page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_not_text_on_data_discovery_page(
    selenium: SeleniumDrivers, browser_id: str, name: str
) -> None:
    driver = selenium[browser_id]
    results_list = DataDiscovery(driver).results_list
    for item in results_list:
        assert name not in item.text, f"{name} in result list"


def results_list_to_list_with_dictionaries(
    results_list: Iterable[WebElement],
) -> list[dict[str, str]]:
    results = []
    for item in results_list:
        text = item.text.split("__onedata: ")[1]
        text = text.replace("{", "")
        text = text.replace("}", "")
        result_dict = {}
        for i in text.split(", "):
            result_dict[i.split(": ")[0]] = i.split(": ")[1]
        results.append(result_dict)

    return results


def text_in_result_list(
    key: str, value: str, results_list: Iterable[WebElement]
) -> None:
    results = results_list_to_list_with_dictionaries(results_list)
    for item in results:
        if value == item.get(key):
            break
    else:
        raise AssertionError(f"{key}: {value} not in results list")


@wt(
    parsers.parse(
        "user of {browser_id} sees that rejection is caused by field "
        "{field_name} of type {field_type} with ID from clipboard"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_rejection_reason_on_data_discovery_page(
    selenium: SeleniumDrivers,
    browser_id: str,
    field_name: str,
    field_type: str,
    clipboard: Clipboard,
    displays: DisplayMap,
) -> None:
    driver = selenium[browser_id]
    file_id = clipboard.paste(display=displays[browser_id])
    key = "__rejectionReason"
    info = (
        f'"failed to parse field {field_name} of type'
        f" {field_type} in document with id '{file_id}'. Preview of "
        "field's value"
    )
    results_list = DataDiscovery(driver).results_list
    text_in_result_list(key, info, results_list)


@wt(
    parsers.parse(
        "user of {browser_id} sees archives ID in results list on data discovery page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_id_on_data_discovery_page(
    selenium: SeleniumDrivers,
    browser_id: str,
    clipboard: Clipboard,
    displays: DisplayMap,
) -> None:
    driver = selenium[browser_id]
    archive_id = f'"{clipboard.paste(display=displays[browser_id])}"'
    key = "archiveId"
    results_list = DataDiscovery(driver).results_list
    text_in_result_list(key, archive_id, results_list)


@wt(
    parsers.parse(
        "user of {browser_id} sees that archives creation time in"
        " results list on data discovery page is the same as on "
        "the archives page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_creation_time_on_data_discovery_page(
    selenium: SeleniumDrivers, browser_id: str, tmp_memory: TmpMemory
) -> None:
    created_at = tmp_memory["created_at"]
    created_at = datetime.strptime(created_at, "%d %b %Y %H:%M").timestamp()
    driver = selenium[browser_id]
    timestamp = float(
        DataDiscovery(driver).results_list[2].text.split(",")[0].split(": ")[2]
    )
    err_msg = (
        "archive creation time is not compatible with creation time on archives page"
    )
    assert (created_at - 60) < timestamp < (created_at + 60), err_msg


@wt(
    parsers.parse(
        "user of {browser_id} sees {text}: {info}"
        " in results list on data discovery page"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_info_on_data_discovery_page(
    selenium: SeleniumDrivers, browser_id: str, info: str, text: str
) -> None:
    driver = selenium[browser_id]
    key = set_key(text)
    try:
        results_list = DataDiscovery(driver).results_list
        text_in_result_list(key, info, results_list)
    except AssertionError:
        button_name = "Query"
        click_button_on_data_disc_page(selenium, browser_id, button_name)
        time.sleep(1)
        results_list = DataDiscovery(driver).results_list
        text_in_result_list(key, info, results_list)


def set_key(text: str) -> str:
    if text == "rejected":
        return "__rejected"
    if text == "archives description":
        return "archiveDescription"
    return "fileName"
