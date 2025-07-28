"""This module contains gherkin steps to run acceptance tests in web GUI."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Dict, List

from tests.gui.conftest import WAIT_BACKEND
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


def assert_n_items_in_items_list(page, selenium, browser_id, number: int, items_names):
    driver = selenium[browser_id]
    seen_items = set()
    stop_scrolling_flag = False
    while not stop_scrolling_flag:
        new_items = _get_visible_items_list(page, items_names)
        new_items_names = [el.text.split("\n")[0] for el in new_items]

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
def _get_visible_items_list(page, items_names):
    return getattr(page, f"get_visible_{items_names}_list")()


def _get_page(where, oz_page, driver):
    if where == "shares":
        return oz_page(driver)["shares"]
    if where == "groups":
        return oz_page(driver)["groups"]
    if where == "spaces":
        return oz_page(driver)["data"]
    raise AssertionError(f"page {where} not found")


@wt(
    parsers.parse(
        "user of {browser_id} can see there are {number} {items} on the {where} list in"
        " the sidebar"
    )
)
def wt_assert_n_items_in_items_list(
    selenium, browser_id, number: int, oz_page, items, where
):
    driver = selenium[browser_id]
    page = _get_page(where, oz_page, driver)
    assert_n_items_in_items_list(page, selenium, browser_id, number, items)


def assert_logs_order_with_optional_logs(
    logs_expected: List[Dict[str, str]], logs_actual: List[str]
):
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

    logs_to_severity = {}
    logs_expected_list = []

    for logs_expected_dict in logs_expected:
        for k, v in logs_expected_dict.items():
            logs_to_severity[v] = k
            logs_expected_list.append(v)

    index, n = 0, len(logs_expected_list)

    for act_log in logs_actual:
        if logs_to_severity[act_log] == "Required":

            while (
                index < n and logs_to_severity[logs_expected_list[index]] == "Optional"
            ):
                index += 1

            assert index < n and act_log == logs_expected_list[index]
            index += 1
        else:
            if logs_to_severity[logs_expected_list[index]] == "Required":
                assert False
            else:
                found = False
                while (
                    index < n
                    and logs_to_severity[logs_expected_list[index]] == "Optional"
                ):
                    if logs_expected_list[index] == act_log:
                        found = True
                        break
                    index += 1

                assert found
                index += 1
