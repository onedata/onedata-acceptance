"""This module contains gherkin steps to run acceptance tests featuring
Space Marketplace management in onezone web GUI.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from datetime import date

from tests.gui.constants import WAIT_FRONTEND
from tests.gui.utils import OZLoggedIn
from tests.gui.utils.generic import transform
from tests.gui.utils.onezone.space_marketplace import MarketplaceSpace
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) clicks on "Advertise your space" '
        r"button in Space Marketplace subpage"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_in_marketplace_subpage(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    OZLoggedIn(driver).data.space_marketplace_page.advertise_space_button()


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

    assert (
        OZLoggedIn(driver).data.spaces_list[space_name].advertised_icon
    ), error_message


def get_space_from_marketplace_list(
    selenium: SeleniumDrivers, browser_id: str, space_name: str
) -> MarketplaceSpace:
    driver = selenium[browser_id]
    page = OZLoggedIn(driver).data.space_marketplace_page
    return page.spaces_marketplace_list[space_name]


def get_today_date() -> str:
    today = date.today()
    day = str(today.day)
    month = today.strftime("%B")[0:3]
    year = str(today.year)
    return day + " " + month + " " + year


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

    if element_type == "creation time" and element_data == "current":
        element_data = get_today_date()

    assert element_data in element, error_message


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
