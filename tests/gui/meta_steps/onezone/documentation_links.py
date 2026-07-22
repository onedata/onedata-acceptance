"""This module contains gherkin steps to run acceptance tests featuring
operations on links to documentation and checking documentation site content.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.steps.common.miscellaneous import assert_title_contains, switch_to_iframe
from tests.gui.utils import Homepage, Modals, Popups
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    parse_elements_sequence,
    transform,
)
from tests.gui.utils.homepage.documentation import DocumentationPage, EndpointInfo
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed

# The docs timeout needs to be higher than the standard WAIT_FRONTEND,
# because opening the docs page is a resource-consuming operation.
# Additionally, waiting for the headers to expand or for the desired section
# to become active also takes some time.
DEFAULT_DOCS_TIMEOUT = 30


SPACE_ENDPOINTS = {
    "Get space details": EndpointInfo.space("GET", "Get space details"),
    "List all space privileges": EndpointInfo.space("GET", "List all space privileges"),
    "List direct space users": EndpointInfo.space("GET", "List space users"),
    "List effective space users": EndpointInfo.space(
        "GET", "List effective space users"
    ),
    "Get effective space user details": EndpointInfo.space(
        "GET", "Get effective space user details"
    ),
    "List user's direct space privileges": EndpointInfo.space(
        "GET", "List user's space privileges"
    ),
    "List user's effective space privileges": EndpointInfo.space(
        "GET", "List effective user's space privileges"
    ),
    "Update user's space privileges": EndpointInfo.space(
        "PATCH", "Update user's space privileges"
    ),
    "List direct space groups": EndpointInfo.space("GET", "List space groups"),
    "List effective space groups": EndpointInfo.space(
        "GET", "List effective space groups"
    ),
    "Get effective space group details": EndpointInfo.space(
        "GET", "Get effective space group details"
    ),
    "List group's direct space privileges": EndpointInfo.space(
        "GET", "List group's space privileges"
    ),
    "List group's effective space privileges": EndpointInfo.space(
        "GET", "List effective group's space privileges"
    ),
    "Update group's space privileges": EndpointInfo.space(
        "PATCH",
        "Update group privileges to space",
    ),
    "List space shares": EndpointInfo.space("GET", "List space shares"),
}

FILE_DETAILS_ENDPOINTS = {
    "Download directory (tar)": EndpointInfo.file_details(
        "GET", "Download file content", "Basic File Operations"
    ),
    "List directory files and subdirectories": EndpointInfo.file_details(
        "GET", "List directory files and subdirectories", "Basic File Operations"
    ),
    "Create file in directory": EndpointInfo.file_details(
        "POST", "Create file in directory", "Basic File Operations"
    ),
    "Remove file": EndpointInfo.file_details(
        "DELETE", "Remove file", "Basic File Operations"
    ),
    "Get attributes": EndpointInfo.file_details(
        "GET", "Get file attributes", "Basic File Operations"
    ),
    "Get JSON metadata": EndpointInfo.file_details(
        "GET", "Get file JSON metadata", "Custom File Metadata"
    ),
    "Set JSON metadata": EndpointInfo.file_details(
        "PUT", "Set file JSON metadata", "Custom File Metadata"
    ),
    "Remove JSON metadata": EndpointInfo.file_details(
        "DELETE", "Remove file JSON metadata", "Custom File Metadata"
    ),
    "Get RDF metadata": EndpointInfo.file_details(
        "GET", "Get file RDF metadata", "Custom File Metadata"
    ),
    "Set RDF metadata": EndpointInfo.file_details(
        "PUT", "Set file RDF metadata", "Custom File Metadata"
    ),
    "Remove RDF metadata": EndpointInfo.file_details(
        "DELETE", "Remove file RDF metadata", "Custom File Metadata"
    ),
    "Get extended attributes (xattrs)": EndpointInfo.file_details(
        "GET", "Get file extended attributes", "Custom File Metadata"
    ),
    "Set extended attribute (xattr)": EndpointInfo.file_details(
        "PUT", "Set file extended attribute", "Custom File Metadata"
    ),
    "Remove extended attributes (xattrs)": EndpointInfo.file_details(
        "DELETE", "Remove file extended attributes", "Custom File Metadata"
    ),
    "Get data distribution": EndpointInfo.file_details(
        "GET", "Get data distribution", "Data Distribution"
    ),
}


@repeat_failed(timeout=DEFAULT_DOCS_TIMEOUT)
def assert_active_sidebar_link_in_docs_subpage(
    selenium: SeleniumDrivers, browser_id: str, subpage: str, link: str
) -> None:
    driver = selenium[browser_id]
    # inherits from DocumentationPage
    subpage = transform(subpage)
    page: DocumentationPage = getattr(Homepage(driver), subpage)
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
    driver = selenium[browser_id]
    subpage = transform(subpage)
    page: DocumentationPage = getattr(Homepage(driver), subpage)
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
    driver = selenium[browser_id]
    subpage = transform(subpage)
    page: DocumentationPage = getattr(Homepage(driver), subpage)
    assert (
        page.current_header == name
    ), f"Expected header: {name}, but found header: {page.current_header}"


@repeat_failed(timeout=DEFAULT_DOCS_TIMEOUT)
def assert_docs_title_contains(
    selenium: SeleniumDrivers, browser_id: str, text: str
) -> None:
    assert_title_contains(selenium, browser_id, text)


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
    driver = selenium[browser_id]
    expected_folders = set(folders)
    subpage = transform(subpage)
    page: DocumentationPage = getattr(Homepage(driver), subpage)
    found_folders = set(page.sidebar.get_expanded_folders_names())
    assert (
        found_folders == expected_folders
    ), f"Expected folders: {expected_folders}, but found folders {found_folders}"


@wt(
    parsers.parse(
        "user of {browser_id} sees that all links to REST API documentation works"
        " correctly for each selected operation in file details API section"
    )
)
def assert_all_links_to_rest_api_docs_works_in_file_details(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).details_modal.api
    modal.operations.click()
    popup = Popups(driver).power_select
    commands = [item.text.split("\n")[0] for item in popup.items]
    for command in commands:
        modal = Modals(driver).details_modal.api
        Popups(driver).power_select.choose_item(f"{command}\nREST")
        modal.rest_api_documentation.click()
        driver.switch_to.window(driver.window_handles[-1])
        endpoint = FILE_DETAILS_ENDPOINTS[command]
        assert_docs_title_contains(
            selenium, browser_id, f"{endpoint.name} | API Reference"
        )
        assert_active_chapter_tab_in_docs_subpage(
            selenium, browser_id, "API", endpoint.chapter
        )
        assert_user_sees_name_in_header_in_docs_subpage(
            selenium, browser_id, "API", endpoint.name
        )
        assert_active_sidebar_link_in_docs_subpage(
            selenium, browser_id, "API", endpoint.label
        )
        assert_expanded_folders_in_sidebar_in_docs_subpage(
            selenium,
            browser_id,
            "API",
            [endpoint.category],
        )
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        switch_to_iframe(selenium, browser_id)
        modal.operations.click()


@wt(
    parsers.parse(
        "user of {browser_id} sees that all links to REST API documentation works"
        " correctly for each selected operation in space menu API section"
    )
)
def assert_all_links_to_rest_api_docs_works_in_space_menu(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).rest_api.api
    modal.operations.click()
    popup = Popups(driver).power_select
    commands = [item.text.split("\n")[0] for item in popup.items]
    for command in commands:
        modal = Modals(driver).rest_api.api
        Popups(driver).power_select.choose_item(f"{command}\nREST")
        modal.rest_api_documentation.click()
        driver.switch_to.window(driver.window_handles[-1])
        endpoint = SPACE_ENDPOINTS[command]
        assert_docs_title_contains(
            selenium, browser_id, f"{endpoint.name} | API Reference"
        )
        assert_active_chapter_tab_in_docs_subpage(
            selenium, browser_id, "API", endpoint.chapter
        )
        assert_user_sees_name_in_header_in_docs_subpage(
            selenium, browser_id, "API", endpoint.name
        )
        assert_active_sidebar_link_in_docs_subpage(
            selenium, browser_id, "API", endpoint.label
        )
        assert_expanded_folders_in_sidebar_in_docs_subpage(
            selenium, browser_id, "API", [endpoint.category]
        )
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        modal.operations.click()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) sees that page title, header and"
        r' active sidebar link contain "(?P<name>.*?)" name in "(?P<subpage>Docs|API)"'
        r" subpage in documentation"
    )
)
def assert_user_sees_name_in_docs_subpage(
    selenium: SeleniumDrivers, browser_id: str, name: str, subpage: str
) -> None:
    assert_user_sees_name_in_header_in_docs_subpage(selenium, browser_id, subpage, name)
    assert_active_sidebar_link_in_docs_subpage(selenium, browser_id, subpage, name)
    assert_docs_title_contains(selenium, browser_id, f"{name} | Onedata Docs")
