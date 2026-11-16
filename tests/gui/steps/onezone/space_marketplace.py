"""This module contains steps for Space Marketplace management in Onezone web GUI."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from datetime import date

from selenium.webdriver.common.by import By

from tests.gui.constants import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.common.common import (
    assert_n_items_in_items_list,
    wt_assert_n_items_in_items_list,
)
from tests.gui.utils import OZLoggedIn, Popups
from tests.gui.utils.enums import ListElement
from tests.gui.utils.generic import transform
from tests.gui.utils.onezone.space_marketplace import MarketplaceSpace
from tests.gui.utils.text import parse_elements_sequence
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_FRONTEND)
def write_into_marketplace_search_input(
    selenium: SeleniumDrivers, browser_id: str, value: str
) -> None:
    page = OZLoggedIn(selenium[browser_id]).data.space_marketplace_page
    page.filter_header.search_input = value


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_marketplace_refresh_button_is_enabled(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    page = OZLoggedIn(selenium[browser_id]).data.space_marketplace_page
    assert page.refresh_button.is_enabled(), "Marketplace refresh button should be enabled"


@repeat_failed(timeout=WAIT_FRONTEND)
def scroll_to_top_of_marketplace_spaces_list(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    page = OZLoggedIn(driver).data.space_marketplace_page
    driver.execute_script("arguments[0].scrollIntoView();", page.filter_header.web_elem)


@wt(parsers.parse("user of {browser_id} sees that there is {number:d} space in the Marketplace"))
@wt(parsers.parse("user of {browser_id} sees that there are {number:d} spaces in the Marketplace"))
def assert_marketplace_spaces_count(
    selenium: SeleniumDrivers, browser_id: str, number: int
) -> None:
    """Use a concise Marketplace-specific alias for the generic list-count step."""
    wt_assert_n_items_in_items_list(
        selenium=selenium,
        browser_id=browser_id,
        number=number,
        items_type=ListElement.MARKETPLACE_SPACES,
        list_type=ListElement.MARKETPLACE_SPACES,
        unique=True,
    )


@wt(
    parsers.parse(
        "user of {browser_id} sees {number:d} Marketplace spaces and all their names "
        'contain "{subtext}"'
    )
)
@wt(
    parsers.parse(
        'user of {browser_id} sees {number:d} Marketplace space and its name contains "{subtext}"'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_marketplace_space_count_and_names_contain(
    selenium: SeleniumDrivers, browser_id: str, number: int, subtext: str
) -> None:
    scroll_to_top_of_marketplace_spaces_list(selenium, browser_id)
    page = OZLoggedIn(selenium[browser_id]).data.space_marketplace_page
    space_names = assert_n_items_in_items_list(
        page,
        selenium,
        browser_id,
        number=number,
        items_type=ListElement.MARKETPLACE_SPACES,
        main_field="name",
    )
    non_matching_names = sorted(name for name in space_names if subtext not in name)
    assert not non_matching_names, (
        f'Marketplace space names not containing "{subtext}": {non_matching_names}'
    )


@wt(
    parsers.parse(
        "user of {browser_id} sees only Marketplace spaces named {space_names:ElementsSequence}",
        extra_types={"ElementsSequence": parse_elements_sequence},
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_only_named_marketplace_spaces_are_displayed(
    selenium: SeleniumDrivers, browser_id: str, space_names: list[str]
) -> None:
    scroll_to_top_of_marketplace_spaces_list(selenium, browser_id)
    page = OZLoggedIn(selenium[browser_id]).data.space_marketplace_page
    actual_space_names = assert_n_items_in_items_list(
        page,
        selenium,
        browser_id,
        number=len(space_names),
        items_type=ListElement.MARKETPLACE_SPACES,
        main_field="name",
    )
    expected_space_names = set(space_names)
    assert actual_space_names == expected_space_names, (
        "Unexpected Marketplace spaces displayed. "
        f"Missing: {sorted(expected_space_names - actual_space_names)}; "
        f"unexpected: {sorted(actual_space_names - expected_space_names)}"
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def clear_marketplace_tags_filter(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    filter_header = OZLoggedIn(driver).data.space_marketplace_page.filter_header
    if filter_header.tags_input.tags:
        filter_header.tags_input.clear.click()


@repeat_failed(timeout=WAIT_FRONTEND)
def click_marketplace_tags_selector_trigger(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    filter_header = OZLoggedIn(driver).data.space_marketplace_page.filter_header
    filter_header.tags_input.add_tag.click()


@repeat_failed(timeout=WAIT_FRONTEND)
def select_space_tag_category(selenium: SeleniumDrivers, browser_id: str, tag_type: str) -> None:
    getattr(Popups(selenium[browser_id]).spaces_tags, tag_type).click()


@repeat_failed(timeout=WAIT_FRONTEND)
def select_space_tag(selenium: SeleniumDrivers, browser_id: str, tag: str) -> None:
    tags_popup = Popups(selenium[browser_id]).spaces_tags
    tags_popup.search_bar = tag
    tags_popup.tags_list[tag].click()


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "Advertise your space" button in Space Marketplace subpage'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_advertise_space_button_in_marketplace_subpage(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    OZLoggedIn(driver).data.space_marketplace_page.advertise_space_button.click()


@wt(
    parsers.parse(
        'user of {browser_id} sees "{space_name}" space with a "Request access" '
        "button in Space Marketplace subpage"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_space_with_request_access_in_marketplace_subpage(
    selenium: SeleniumDrivers, browser_id: str, space_name: str
) -> None:
    driver = selenium[browser_id]
    space = OZLoggedIn(driver).data.space_marketplace_page.marketplace_spaces_list[space_name]
    assert space.request_access.is_displayed(), (
        f"'Request access' button is not displayed for {space_name}"
    )


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) sees that "(?P<space_name>.*)" '
        r"space is advertised in the marketplace in space sidebar"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_marketplace_icon_in_space_sidebar(
    selenium: SeleniumDrivers, browser_id: str, space_name: str
) -> None:
    driver = selenium[browser_id]
    error_message = f"Space: {space_name} does not have marketplace indicator visible"
    assert OZLoggedIn(driver).data.spaces_list[space_name].advertised_icon, error_message


def get_space_from_marketplace_list(
    selenium: SeleniumDrivers, browser_id: str, space_name: str
) -> MarketplaceSpace:
    driver = selenium[browser_id]
    page = OZLoggedIn(driver).data.space_marketplace_page
    return page.marketplace_spaces_list[space_name]


@wt(
    parsers.parse(
        'user of {browser_id} does not see "{space_name}" space in Space Marketplace subpage'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_space_not_in_marketplace_list(
    selenium: SeleniumDrivers, browser_id: str, space_name: str
) -> None:
    driver = selenium[browser_id]
    page = OZLoggedIn(driver).data.space_marketplace_page
    assert space_name not in page.marketplace_spaces_list, (
        f'Space "{space_name}" unexpectedly found in Space Marketplace'
    )


def get_today_date() -> str:
    today = date.today()
    day = str(today.day)
    month = today.strftime("%B")[0:3]
    year = str(today.year)
    return day + " " + month + " " + year


def assert_creation_time_in_space_marketplace(
    selenium: SeleniumDrivers,
    browser_id: str,
    space_name: str,
    expected_creation_time: str,
) -> None:
    if expected_creation_time == "current":
        expected_creation_time = get_today_date()

    assert_element_in_space_marketplace(
        selenium,
        browser_id,
        space_name,
        "creation time",
        expected_creation_time,
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_element_in_space_marketplace(
    selenium: SeleniumDrivers,
    browser_id: str,
    space_name: str,
    element_type: str,
    element_data: str,
) -> None:
    space = get_space_from_marketplace_list(selenium, browser_id, space_name)
    element = getattr(space, transform(element_type))
    name_of_element = element_type.capitalize()
    error_message = (
        f"{name_of_element}: {element} displayed in advertised space:"
        f" {space_name}, does not match expected: {element_data}"
    )
    assert element_data == element, error_message


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_elements_list_in_space_marketplace(
    selenium: SeleniumDrivers,
    browser_id: str,
    space_name: str,
    element_type: str,
    elements_data_list: list[str],
) -> None:
    space = get_space_from_marketplace_list(selenium, browser_id, space_name)
    name_of_element = element_type.capitalize()
    elements_list = getattr(space, transform(element_type + "s_list"))

    for element in elements_data_list:
        assert element in elements_list, (
            f"{name_of_element}: {element} is"
            f" not displayed in {element_type}s"
            " list in advertised "
            f"space: {space_name}"
        )


@wt(
    parsers.parse(
        'user of {browser_id} sees "{space_name}" advertised space description '
        'with "{expected_header}" header and "{expected_paragraph}" paragraph'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_advertised_space_description(
    selenium: SeleniumDrivers,
    browser_id: str,
    space_name: str,
    expected_header: str,
    expected_paragraph: str,
) -> None:
    space = get_space_from_marketplace_list(selenium, browser_id, space_name)
    description = space.description_element
    header = description.find_element(By.CSS_SELECTOR, "h1")
    paragraph = description.find_element(By.CSS_SELECTOR, "p")
    assert header.is_displayed(), "Header is not displayed"
    assert header.text == expected_header, (
        f"Header should be '{expected_header}', but is '{header.text}'"
    )
    assert paragraph.is_displayed(), "Paragraph is not displayed"
    assert paragraph.text == expected_paragraph, (
        f"Paragraph should be '{expected_paragraph}', but is '{paragraph.text}'"
    )


@wt(
    parsers.parse(
        'user of {browser_id} sees "{link_name}" link for "{space_name}" '
        "space in Space Marketplace subpage"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_marketplace_space_link_visible(
    browser_id: str,
    link_name: str,
    space_name: str,
    selenium: SeleniumDrivers,
) -> None:
    space = get_space_from_marketplace_list(selenium, browser_id, space_name)
    link_attribute = {"Visit space": "visit_space", "Configure": "configure_space"}[link_name]
    link = getattr(space, link_attribute)
    assert link.is_displayed(), (
        f'"{link_name}" link is not displayed for "{space_name}" in Space Marketplace'
    )


@wt(
    parsers.parse(
        'user of {browser_id} clicks "{link_name}" link for "{space_name}" '
        "space in Space Marketplace subpage"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_marketplace_space_link(
    browser_id: str,
    link_name: str,
    space_name: str,
    selenium: SeleniumDrivers,
) -> None:
    space = get_space_from_marketplace_list(selenium, browser_id, space_name)
    link_attribute = {"Visit space": "visit_space", "Configure": "configure_space"}[link_name]
    getattr(space, link_attribute).click()
