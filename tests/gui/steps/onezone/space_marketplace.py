"""This module contains steps for Space Marketplace management in Onezone web GUI."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from datetime import date

from selenium.webdriver.common.by import By

from tests.gui.constants import WAIT_FRONTEND
from tests.gui.utils import OZLoggedIn
from tests.gui.utils.generic import transform
from tests.gui.utils.onezone.space_marketplace import MarketplaceSpace
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


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
    space = OZLoggedIn(driver).data.space_marketplace_page.spaces_marketplace_list[space_name]
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
    return page.spaces_marketplace_list[space_name]


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
    assert space_name not in page.spaces_marketplace_list, (
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
