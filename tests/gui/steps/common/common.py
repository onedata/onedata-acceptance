"""This module contains gherkin steps to run acceptance tests in web GUI."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import re
import time
from collections.abc import Callable, Sequence
from contextlib import suppress
from typing import Any

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import invisibility_of_element
from selenium.webdriver.support.ui import WebDriverWait

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.type_definitions import (
    Clickable,
    VisibilityCondition,
    WebElementOrCssLocator,
    WebElementOrSelector,
)
from tests.gui.utils import OZLoggedIn, Popups
from tests.gui.utils.common.modals import Modals
from tests.gui.utils.common.modals.archives_modals.archive_audit_log import (
    ArchiveAuditLog,
)
from tests.gui.utils.common.modals.archives_modals.archive_recall_information import (
    ArchiveRecallInformation,
)
from tests.gui.utils.common.popups.generic import AlertPopupType
from tests.gui.utils.core.base import NamedElement
from tests.gui.utils.generic import (
    ListElement,
    ListItemMainField,
    get_visibility_condition,
    get_web_elem_or_locator,
    transform,
)
from tests.gui.utils.oneprovider.browser import Browser
from tests.gui.utils.onezone.generic_page import ListPage, get_visible_elements_list
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


def assert_n_items_in_items_list(
    page: ListPage | Browser,
    selenium: dict[str, WebDriver],
    browser_id: str,
    number: int,
    items_type: ListElement,
    main_field: ListItemMainField,
) -> None:
    driver = selenium[browser_id]
    seen_items = set()
    stop_scrolling_flag = False

    WebDriverWait(driver, WAIT_FRONTEND).until(
        lambda _: len(get_visible_items_list(page, items_type, main_field)) > 0,
        message=f"Waiting for initial {items_type.value} to appear failed",
    )

    while not stop_scrolling_flag:
        new_items = get_visible_items_list(page, items_type, main_field)
        new_items_fields = [getattr(el, main_field) for el in new_items]

        stop_scrolling_flag = not any(el not in seen_items for el in new_items_fields)
        seen_items.update(new_items_fields)
        driver.execute_script("arguments[0].scrollIntoView();", new_items[-1].web_elem)

    assert len(seen_items) == number, (
        f"There are {len(seen_items)} items, but should be: {number}. All found"
        f" items:\n {seen_items}"
    )


# there is a small chance that not all item will be loaded at time,
# so there is a need to add repeats
@repeat_failed(timeout=WAIT_BACKEND)
def get_visible_items_list(
    page: ListPage | Browser,
    items_type: ListElement,
    main_field: ListItemMainField = "name",
) -> Sequence[NamedElement]:
    items_type_str = transform(items_type.value)
    elements_list = getattr(page, f"{items_type_str}_list")
    if isinstance(page, Browser):
        return page.get_visible_file_rows(elements_list, main_field)
    return get_visible_elements_list(elements_list, main_field)


@repeat_failed(timeout=WAIT_BACKEND)
def wait_for_checking_toggle(toggle: Any, toggle_name: str = "") -> None:
    assert toggle.is_checked(), f"did not manage to check a toggle {toggle_name}"


def get_page_for_list(
    list_element: ListElement,
    driver: WebDriver,
) -> ListPage:
    oz = OZLoggedIn(driver)

    match list_element:
        case ListElement.SPACES | ListElement.SPACES_HEADERS:
            return oz.data
        case ListElement.GROUPS_HEADERS:
            return oz.groups
        case ListElement.SHARES_SIDEBAR:
            return oz.shares
        case ListElement.WORKFLOWS:
            return oz.automation.workflows_page
        case ListElement.LAMBDAS:
            return oz.automation.lambdas_page
        case _:
            return getattr(oz, list_element.value)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) can see there are (?P<number>\d+)"
        r" (?P<items_type>.*) on the (?P<list_type>.*) list in the sidebar",
    ),
    converters={
        "number": int,
        "items_type": ListElement,
        "list_type": ListElement,
    },
)
def wt_assert_n_items_in_items_list(
    selenium: dict[str, WebDriver],
    browser_id: str,
    number: int,
    items_type: ListElement,
    list_type: ListElement,
) -> None:
    driver = selenium[browser_id]
    page = get_page_for_list(list_type, driver)
    assert_n_items_in_items_list(page, selenium, browser_id, number, items_type, "name")


def get_last_item_number_in_table(driver: WebDriver) -> int:
    last_item = get_last_item_in_table(driver)
    if last_item is None:
        return 0
    return int(last_item.get_attribute("data-row-id")) + 1


def get_last_item_in_table(driver: WebDriver) -> WebElement | None:
    entries = driver.find_elements(By.CSS_SELECTOR, "tbody.table-body tr.table-entry")
    return entries[-1] if len(entries) > 0 else None


def scroll_to_bottom_of_the_table(driver: WebDriver) -> int:
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
    logs_expected: list[dict[str, str]], logs_actual: list[str]
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


def scroll_and_get_columns(
    modal: ArchiveRecallInformation | ArchiveAuditLog,
    columns: list[str],
    main_column: str = "file",
) -> list[str]:
    # The modal has to be a class that implements get_visible_rows_of_columns
    checked_names = set()
    columns = [transform(column) for column in columns]
    stop_scrolling_flag = False
    while not stop_scrolling_flag:
        visible_elems = modal.get_visible_rows_of_columns(columns)
        visible_names = visible_elems[main_column]

        modal.scroll_by_press_space()
        stop_scrolling_flag = not any(
            name not in checked_names for name in visible_names
        )
        checked_names.update(visible_names)
    return list(checked_names)


def element_rect_stable(
    css_selector: str, checks: int = 5, interval: float = 0.1
) -> Callable[[WebDriver], bool]:
    def _predicate(driver: WebDriver) -> bool:
        web_element = driver.find_element(By.CSS_SELECTOR, css_selector)

        last_rect = web_element.rect
        for _ in range(checks):
            time.sleep(interval)
            current_rect = web_element.rect
            if current_rect != last_rect:
                return False
            last_rect = current_rect

        return True

    return _predicate


# TODO: VFS-12424 Add class to fully-transitioned file details panel
def wait_for_sliding_panel_to_stop_moving(
    driver: WebDriver, timeout: int, css_selector: str
) -> None:
    WebDriverWait(driver=driver, timeout=timeout).until(
        element_rect_stable(css_selector=css_selector)
    )


def wait_for_error_modal_to_disappear(driver: WebDriver) -> bool:
    """Close the error modal and return whether it appeared."""

    def get_error_modal_close_button(current_driver: WebDriver) -> Clickable:
        return Modals(current_driver).error.close

    return wait_till_error_modal_disappear(
        driver,
        ".alert-global.modal.in .modal-dialog",
        get_error_modal_close_button,
    )


def try_click_without_throwing_error(
    action: Callable[[], object], timeout: float = WAIT_FRONTEND // 2
) -> None:

    @repeat_failed(timeout=timeout)
    def perform(_action: Callable[[], object]) -> None:
        _action()

    with suppress(Exception):
        perform(action)


def wait_for_element_to_appear(
    driver: WebDriver,
    web_elem_or_selector: WebElementOrSelector,
    timeout: float = WAIT_FRONTEND,
) -> bool:
    """Return whether the element appeared before the timeout."""
    web_elem_or_locator: WebElementOrCssLocator = get_web_elem_or_locator(
        web_elem_or_selector
    )
    visibility_condition: VisibilityCondition = get_visibility_condition(
        web_elem_or_locator
    )
    try:
        # selenium function visibility_of does not ignore StaleElementReferenceException
        WebDriverWait(
            driver, timeout, ignored_exceptions=[StaleElementReferenceException]
        ).until(visibility_condition)
    except TimeoutException:
        return False
    return True


def wait_for_error_modal_to_appear(driver: WebDriver, timeout: float) -> bool:
    """Return whether the error modal appeared before the timeout."""
    return wait_for_element_to_appear(
        driver,
        ".alert-global.modal.in .modal-dialog",
        timeout,
    )


def click_close_button_and_wait_to_disappear(
    driver: WebDriver,
    web_elem_or_locator: WebElementOrCssLocator,
    get_close_button: Callable[[WebDriver], Clickable],
) -> bool:
    try_click_without_throwing_error(
        lambda: get_close_button(driver).click()  # pylint: disable=unnecessary-lambda
    )
    WebDriverWait(driver, WAIT_FRONTEND).until(
        invisibility_of_element(web_elem_or_locator),
        message="Popup or modal is still visible",
    )
    return True


def wait_till_error_modal_disappear(
    driver: WebDriver,
    web_elem_or_selector: WebElementOrSelector,
    get_close_button: Callable[[WebDriver], Clickable],
) -> bool:
    if not wait_for_element_to_appear(driver, web_elem_or_selector, WAIT_FRONTEND // 4):
        return False
    web_elem_or_locator = get_web_elem_or_locator(web_elem_or_selector)

    click_close_button_and_wait_to_disappear(
        driver,
        web_elem_or_locator,
        get_close_button,
    )
    return True


def close_alert_popup_if_present(
    driver: WebDriver,
    popup: AlertPopupType,
) -> bool:
    # Close an alert identified by its enum value.
    # If popup doesn't appear, don't throw an error.
    # If it appeared and was not closed, raise.
    alert_popup = Popups(driver).alert_popups.get_alert_popup(popup)
    if alert_popup is None:
        return False

    def close_matching_popup() -> None:
        current_popup = Popups(driver).alert_popups.find_alert_popup(popup)
        if current_popup is not None:
            current_popup.close.click()

    try_click_without_throwing_error(close_matching_popup)

    def is_popup_closed(driver: WebDriver) -> bool:
        return Popups(driver).alert_popups.find_alert_popup(popup) is None

    WebDriverWait(driver, WAIT_FRONTEND).until(
        is_popup_closed,
        message=f'Alert popup matching "{popup.message}" is still visible',
    )
    return True


def parse_size(size: str) -> float:
    units = ["B", "KiB", "MiB", "GiB"]
    units_reg = "|".join(units)

    match = re.fullmatch(
        rf"\s*(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>{units_reg})\s*",
        size,
    )

    if match is None:
        raise ValueError(f"Unsupported size format: {size!r}")

    value = float(match.group("value"))
    unit = match.group("unit")
    return value * 1024 ** (units.index(unit))
