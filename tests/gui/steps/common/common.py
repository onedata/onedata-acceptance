"""This module contains gherkin steps to run acceptance tests in web GUI."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Dict, List, Optional

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from tests.conftest import SeleniumDrivers
from tests.gui.conftest import WAIT_BACKEND
from tests.gui.types import GuiObject
from tests.gui.utils import OZLoggedIn
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


def assert_n_items_in_items_list(
    page: GuiObject,
    selenium: SeleniumDrivers,
    browser_id: str,
    number: int,
    items_names: str,
    transform_fun: Optional[GuiObject] = None,
) -> None:
    driver = selenium[browser_id]
    seen_items = set()
    stop_scrolling_flag = False
    if not transform_fun:
        transform_fun = lambda item: item.text.split("\n")[0]
    while not stop_scrolling_flag:
        new_items = _get_visible_items_list(page, items_names)
        new_items_names = [
            transform_fun(el) for el in new_items if transform_fun(el) != ""
        ]

        # if there are at least 1 new item keep scrolling
        stop_scrolling_flag = not any(el not in seen_items for el in new_items_names)
        seen_items.update(new_items_names)
        driver.execute_script("arguments[0].scrollIntoView();", new_items[-1])
    assert len(seen_items) == number, (
        f"There are {len(seen_items)} items, but should be: {number}. All found"
        f" items:\n {seen_items}"
    )


# there is a small chance that not all item will be loaded at time,
# so there is a need to add repeats
@repeat_failed(timeout=WAIT_BACKEND)
def _get_visible_items_list(page: GuiObject, items_names: GuiObject) -> GuiObject:
    return getattr(page, f"get_visible_{items_names}_list")()


@repeat_failed(timeout=WAIT_BACKEND)
def wait_for_checking_toggle(toggle: GuiObject, toggle_name: str = "") -> None:
    assert toggle.is_checked(), f"did not manage to check a toggle {toggle_name}"


def _get_page(where: str, driver: WebDriver) -> GuiObject:
    if where == "shares":
        return OZLoggedIn(driver)["shares"]
    if where == "groups":
        return OZLoggedIn(driver)["groups"]
    if where == "spaces":
        return OZLoggedIn(driver)["data"]
    raise AssertionError(f"page {where} not found")


@wt(
    parsers.parse(
        "user of {browser_id} can see there are {number} {items} on the {where} list in"
        " the sidebar"
    )
)
def wt_assert_n_items_in_items_list(
    selenium: SeleniumDrivers,
    browser_id: str,
    number: int,
    items: str,
    where: str,
) -> None:
    driver = selenium[browser_id]
    page = _get_page(where, driver)
    assert_n_items_in_items_list(page, selenium, browser_id, number, items)


def get_last_item_number_in_table(driver: WebDriver) -> int:
    last_item = get_last_item_in_table(driver)
    if last_item is None:
        return 0
    return int(last_item.get_attribute("data-row-id")) + 1


def get_last_item_in_table(driver: WebDriver) -> GuiObject:
    entries = driver.find_elements(By.CSS_SELECTOR, "tbody.table-body tr.table-entry")
    return entries[-1] if len(entries) > 0 else None


def scroll_to_bottom_of_the_table(driver: WebDriver) -> GuiObject:
    while True:
        count = get_last_item_number_in_table(driver)
        if count == 0:
            return count
        # Scroll to last
        driver.execute_script(
            "arguments[0].scrollIntoView();", get_last_item_in_table(driver)
        )
        try:
            WebDriverWait(driver, 2).until(
                lambda d: get_last_item_number_in_table(d) > count
            )
        except TimeoutException:
            break
    return count


def assert_logs_order_with_optional_logs(
    logs_expected: List[Dict[str, str]], logs_actual: List[str]
) -> None:
    """

    This function takes as a first argument list of dictionaries as in example below:
    [
        {
            "Required": "Example log 1"
        },
        {
            "Optional": "Example log 2"
        },
        {
            "Required": "Example log 3"
        }
    ]

    As a second argument it takes list of strings.

    Function checks that expected entries exist with maintained order.
    Function can skip checking optional entries, if they are also skipped in Logs Actual,
    but if they are not, it checks whether thay are placed in allowed place.

    """

    severity = {}
    logs_expected_list = []

    for logs_expected_dict in logs_expected:
        for k, v in logs_expected_dict.items():
            severity[v] = k
            logs_expected_list.append(v)

    idx, n = 0, len(logs_expected_list)
    for expected_log in logs_expected_list:
        if severity[expected_log] == "Required":
            assert idx < n and expected_log == logs_actual[idx], (
                f"expected logs: {logs_expected_list}\n"
                f"do not match actual logs: {logs_actual}"
            )
            idx += 1
        if severity[expected_log] == "Optional":
            if idx < n and expected_log == logs_actual[idx]:
                idx += 1


def scroll_and_get_columns(modal: GuiObject, columns: list[str]) -> GuiObject:
    # The modal has to be a class that implements get_rows_of_columns
    checked_names = set()
    columns = [transform(column) for column in columns]
    stop_scrolling_flag = False
    while not stop_scrolling_flag:
        visible_elems: Dict[str, List[str]] = modal.get_rows_of_columns(columns)
        visible_names = visible_elems["file"]
        modal.scroll_by_press_space()
        stop_scrolling_flag = not any(
            name not in checked_names for name in visible_names
        )
        checked_names.update(visible_names)
    return list(checked_names)
