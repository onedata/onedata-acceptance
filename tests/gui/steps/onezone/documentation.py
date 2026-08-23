"""Steps for interacting with Onedata documentation pages."""

__author__ = "Mateusz Zajac, Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.utils import Homepage, Modals, Popups
from tests.gui.utils.common.modals.files_modals.details_modal import ApiTab
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    parse_elements_sequence,
    transform,
)
from tests.gui.utils.homepage import RestApiCommand
from tests.gui.utils.homepage.documentation import DocumentationPage
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed

DEFAULT_DOCS_TIMEOUT = 30


@repeat_failed(timeout=DEFAULT_DOCS_TIMEOUT)
def _get_api_tab(driver: WebDriver, modal_name: str) -> ApiTab:
    return getattr(Modals(driver), modal_name).api


def click_operations_dropdown_in_api_modal(
    selenium: SeleniumDrivers, browser_id: str, modal_name: str
) -> None:
    _get_api_tab(selenium[browser_id], modal_name).operations.click()


@repeat_failed(timeout=DEFAULT_DOCS_TIMEOUT)
def get_rest_api_commands_from_dropdown(
    selenium: SeleniumDrivers, browser_id: str
) -> list[str]:
    command_items = Popups(selenium[browser_id]).power_select.items_as(RestApiCommand)
    commands = [
        item.command_title for item in command_items if item.command_type == "REST"
    ]
    assert commands, "No REST API commands found in operations dropdown"
    return commands


@repeat_failed(timeout=DEFAULT_DOCS_TIMEOUT)
def choose_rest_api_command_from_dropdown(
    selenium: SeleniumDrivers, browser_id: str, command: str
) -> None:
    command_items = Popups(selenium[browser_id]).power_select.items_as(RestApiCommand)
    for item in command_items:
        if item.command_title == command and item.command_type == "REST":
            item.click()
            return
    raise AssertionError(f'REST API command "{command}" not found')


def click_rest_api_documentation_link(
    selenium: SeleniumDrivers, browser_id: str, modal_name: str
) -> None:
    _get_api_tab(selenium[browser_id], modal_name).rest_api_documentation.click()


@repeat_failed(timeout=DEFAULT_DOCS_TIMEOUT)
def get_documentation_page(
    selenium: SeleniumDrivers, browser_id: str, subpage: str
) -> DocumentationPage:
    return getattr(Homepage(selenium[browser_id]), transform(subpage))


def assert_active_sidebar_link_in_docs_subpage(
    selenium: SeleniumDrivers, browser_id: str, subpage: str, link: str
) -> None:
    page = get_documentation_page(selenium, browser_id, subpage)
    assert_active_sidebar_link(page, link)


@repeat_failed(timeout=DEFAULT_DOCS_TIMEOUT)
def assert_active_sidebar_link(page: DocumentationPage, link: str) -> None:
    active_links = page.sidebar.get_active_rows_names()
    assert (
        len(active_links) == 1
    ), f"Expected only one active link, but found {len(active_links)}"
    active_link = active_links[0]
    assert (
        active_link == link
    ), f"Expected active link: {link}, but found: {active_link}"


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) sees "(?P<chapter>.*?)" active chapter'
        r' in "(?P<subpage>Docs|API)" subpage in documentation'
    )
)
@repeat_failed(timeout=DEFAULT_DOCS_TIMEOUT)
def assert_active_chapter_tab_in_docs_subpage(
    selenium: SeleniumDrivers, browser_id: str, subpage: str, chapter: str
) -> None:
    page = get_documentation_page(selenium, browser_id, subpage)
    active_tabs = page.chapters.get_active_chapter_tabs_names()
    assert (
        len(active_tabs) == 1
    ), f"Expected only one active chapter tab, but found {len(active_tabs)}"
    active_tab = active_tabs[0]
    assert (
        active_tab == chapter
    ), f"Expected active chapter tab: {chapter}, but found: {active_tab}"


@repeat_failed(timeout=DEFAULT_DOCS_TIMEOUT)
def assert_user_sees_name_in_header_in_docs_subpage(
    selenium: SeleniumDrivers, browser_id: str, subpage: str, name: str
) -> None:
    page = get_documentation_page(selenium, browser_id, subpage)
    current_header = page.current_header
    assert (
        current_header == name
    ), f"Expected header: {name}, but found header: {current_header}"


@wt(
    parsers.re(
        rf"user of (?P<browser_id>.*?) sees that "
        rf"(?P<folders>{ELEMENTS_SEQUENCE_PATTERN}) sidebar folder(s are|"
        r' is) expanded in "(?P<subpage>Docs|API)" subpage in documentation'
    ),
    converters={
        "folders": parse_elements_sequence,
    },
)
@repeat_failed(timeout=DEFAULT_DOCS_TIMEOUT)
def assert_expanded_folders_in_sidebar_in_docs_subpage(
    selenium: SeleniumDrivers, browser_id: str, subpage: str, folders: list[str]
) -> None:
    page = get_documentation_page(selenium, browser_id, subpage)
    expected_folders = set(folders)
    found_folders = set(page.sidebar.get_expanded_folders_names())
    assert (
        found_folders == expected_folders
    ), f"Expected folders: {expected_folders}, but found folders {found_folders}"
