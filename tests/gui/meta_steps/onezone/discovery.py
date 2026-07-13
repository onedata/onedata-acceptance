"""This module contains gherkin meta steps to run acceptance tests featuring
harvester management in onezone web GUI.
"""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.steps.onezone.harvesters.data_discovery import (
    assert_data_discovery_page,
)
from tests.gui.steps.onezone.harvesters.discovery import (
    click_on_option_of_harvester_on_left_sidebar_menu,
)
from tests.gui.steps.onezone.spaces import (
    click_element_on_lists_on_left_sidebar_menu,
    click_on_option_in_the_sidebar,
)
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt


@wt(
    parsers.re(
        r"user of (?P<browser_id>\w+) opens (?P<subpage>Data Discovery"
        '|Spaces|Indices) page of "(?P<harvester_name>[^"]+)" harvester'
    )
)
def open_discovery_subpage_of_harvester(
    selenium: SeleniumDrivers, browser_id: str, harvester_name: str, subpage: str
) -> None:
    panel_name = "Discovery"
    list_name = "harvesters"
    subpage = subpage.lower()

    click_on_option_in_the_sidebar(selenium, browser_id, panel_name)
    click_element_on_lists_on_left_sidebar_menu(
        selenium, browser_id, list_name, harvester_name
    )
    click_on_option_of_harvester_on_left_sidebar_menu(
        selenium, browser_id, harvester_name, subpage
    )
    if subpage == "data discovery":
        assert_data_discovery_page(selenium, browser_id)
