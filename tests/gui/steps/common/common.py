"""This module contains gherkin steps to run acceptance tests in web GUI."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.steps.common.miscellaneous import switch_to_iframe
from tests.utils.bdd_utils import parsers, wt


def assert_n_items_in_items_list(page, selenium, browser_id, number: int, items_names):
    driver = selenium[browser_id]
    seen_items = set()
    stop_scrolling_flag = False
    while not stop_scrolling_flag:
        new_items = getattr(page, f"get_visible_{items_names}_list")()
        new_items_names = [el.text.split("\n")[0] for el in new_items]

        # if there are at least 1 new item keep scrolling
        stop_scrolling_flag = not any(el not in seen_items for el in new_items_names)
        seen_items.update(new_items_names)
        driver.execute_script("arguments[0].scrollIntoView();", new_items[-1])
    assert (
        len(seen_items) == number
    ), f"There are {len(seen_items)} items, but should be: {number}."


def _get_page(page, op_container, oz_page, driver):
    if page == "shares view":
        return op_container(driver).shares_page
    if page == "shares list":
        return oz_page(driver)["shares"]
    if page == "groups list":
        return oz_page(driver)["shares"]
    if page == "spaces list":
        return oz_page(driver)["data"]
    raise AssertionError(f"page {page} not found")


@wt(parsers.parse("user of {browser_id} can see there are {number} {items} in {where}"))
@wt(
    parsers.parse(
        "user of {browser_id} can see there are {number} {items} on the {where} in"
        " the sidebar"
    )
)
def wt_assert_n_items_in_items_list(
    selenium, browser_id, number: int, oz_page, op_container, items, where
):
    driver = selenium[browser_id]
    switch_to_iframe(selenium, browser_id)
    page = _get_page(where, op_container, oz_page, driver)
    assert_n_items_in_items_list(page, selenium, browser_id, number, items)
