"""This module contains gherkin steps to run acceptance tests featuring
operations on links to documentation and checking documentation site content.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.steps.common.miscellaneous import assert_title_contains, switch_to_iframe
from tests.gui.utils import Homepage, Modals, Popups
from tests.gui.utils.generic import parse_seq
from tests.gui.utils.homepage.documentation import DocumentationPage, EndpointInfo
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed

# The docs timeout needs to be higher than the standard WAIT_FRONTEND,
# because opening the docs page is a resource-consuming operation.
# Additionally, waiting for the headers to expand or for the desired section
# to become active also takes some time.
DEFAULT_DOCS_TIMEOUT = 30


SPACE_ENDPOINTS = {
    "Get space details": EndpointInfo("GET", "Get space details", "Space"),
    "List all space privileges": EndpointInfo(
        "GET", "List all space privileges", "Space"
    ),
    "List direct space users": EndpointInfo("GET", "List space users", "Space"),
    "List effective space users": EndpointInfo(
        "GET", "List effective space users", "Space"
    ),
    "Get effective space user details": EndpointInfo(
        "GET", "Get effective space user details", "Space"
    ),
    "List user's direct space privileges": EndpointInfo(
        "GET", "List user's space privileges", "Space"
    ),
    "List user's effective space privileges": EndpointInfo(
        "GET", "List effective user's space privileges", "Space"
    ),
    "Update user's space privileges": EndpointInfo(
        "PATCH", "Update user's space privileges", "Space"
    ),
    "List direct space groups": EndpointInfo("GET", "List space groups", "Space"),
    "List effective space groups": EndpointInfo(
        "GET", "List effective space groups", "Space"
    ),
    "Get effective space group details": EndpointInfo(
        "GET", "Get effective space group details", "Space"
    ),
    "List group's direct space privileges": EndpointInfo(
        "GET", "List group's space privileges", "Space"
    ),
    "List group's effective space privileges": EndpointInfo(
        "GET", "List effective group's space privileges", "Space"
    ),
    "Update group's space privileges": EndpointInfo(
        "PATCH", "Update group privileges to space", "Space"
    ),
    "List space shares": EndpointInfo("GET", "List space shares", "Space"),
}

FILE_DETAILS_ENDPOINTS = {
    "Download directory (tar)": EndpointInfo(
        "GET", "Download file content", "Basic File Operations"
    ),
    "List directory files and subdirectories": EndpointInfo(
        "GET", "List directory files and subdirectories", "Basic File Operations"
    ),
    "Create file in directory": EndpointInfo(
        "POST", "Create file in directory", "Basic File Operations"
    ),
    "Remove file": EndpointInfo("DELETE", "Remove file", "Basic File Operations"),
    "Get attributes": EndpointInfo(
        "GET", "Get file attributes", "Basic File Operations"
    ),
    "Get JSON metadata": EndpointInfo(
        "GET", "Get file JSON metadata", "Custom File Metadata"
    ),
    "Set JSON metadata": EndpointInfo(
        "PUT", "Set file JSON metadata", "Custom File Metadata"
    ),
    "Remove JSON metadata": EndpointInfo(
        "DELETE", "Remove file JSON metadata", "Custom File Metadata"
    ),
    "Get RDF metadata": EndpointInfo(
        "GET", "Get file RDF metadata", "Custom File Metadata"
    ),
    "Set RDF metadata": EndpointInfo(
        "PUT", "Set file RDF metadata", "Custom File Metadata"
    ),
    "Remove RDF metadata": EndpointInfo(
        "DELETE", "Remove file RDF metadata", "Custom File Metadata"
    ),
    "Get extended attributes (xattrs)": EndpointInfo(
        "GET", "Get file extended attributes", "Custom File Metadata"
    ),
    "Set extended attribute (xattr)": EndpointInfo(
        "PUT", "Set file extended attribute", "Custom File Metadata"
    ),
    "Remove extended attributes (xattrs)": EndpointInfo(
        "DELETE", "Remove file extended attributes", "Custom File Metadata"
    ),
}


@repeat_failed(timeout=DEFAULT_DOCS_TIMEOUT)
def assert_active_sidebar_link_in_docs_subpage(selenium, browser_id, subpage, link):
    driver = selenium[browser_id]
    # inherits from DocumentationPage
    page:DocumentationPage = Homepage(driver)[subpage]
    active_links = page.sidebar.get_active_rows_names()
    assert (
        len(active_links) == 1
    ), f"Expected only one active link, but found {len(active_links)}"
    active_link = active_links[0]
    assert (
        active_link == link
    ), f"Expected active link: {link}, but found: {active_link}"


@repeat_failed(timeout=DEFAULT_DOCS_TIMEOUT)
def assert_user_sees_name_in_header_in_docs_subpage(selenium, browser_id, subpage, name):
    driver = selenium[browser_id]
    page:DocumentationPage = Homepage(driver)[subpage]
    assert (
        page.current_header == name
    ), f"Expected header: {name}, but found header: {page.current_header}"


@repeat_failed(timeout=DEFAULT_DOCS_TIMEOUT)
def assert_docs_title_contains(selenium, browser_id, text):
    assert_title_contains(selenium, browser_id, text)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) sees that (?P<folders>.*?) sidebar folder(s are|"
        r' is) expanded on "(?P<subpage>Docs|API)" page in documentation'
    )
)
@repeat_failed(timeout=DEFAULT_DOCS_TIMEOUT)
def assert_expanded_folders_in_sidebar_in_docs_subpage(selenium, browser_id, subpage, folders):
    driver = selenium[browser_id]
    expected_folders = set(parse_seq(folders))
    page:DocumentationPage = Homepage(driver)[subpage]
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
def assert_all_links_to_rest_api_docs_works_in_file_details(selenium, browser_id):
    driver = selenium[browser_id]
    modal = Modals(driver).details_modal.api
    modal.operations.click()
    popup = Popups(driver).power_select
    commands = [item.text.split("\n")[0] for item in popup.items]
    for command in commands:
        # TODO: VFS-12753, remove after fix
        if command == "Get data distribution":
            continue
        modal = Modals(driver).details_modal.api
        Popups(driver).power_select.choose_item(f"{command}\nREST")
        modal.rest_api_documentation.click()
        driver.switch_to.window(driver.window_handles[-1])
        endpoint = FILE_DETAILS_ENDPOINTS[command]
        assert_docs_title_contains(
            selenium, browser_id, f"{endpoint.name} | API Reference"
        )
        assert_user_sees_name_in_header_in_docs_subpage(selenium, browser_id, "API", endpoint.name)
        assert_active_sidebar_link_in_docs_subpage(selenium, browser_id, "API", endpoint.label)
        assert_expanded_folders_in_sidebar_in_docs_subpage(
            selenium, browser_id, "API", endpoint.category,
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
def assert_all_links_to_rest_api_docs_works_in_space_menu(selenium, browser_id):
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
        assert_user_sees_name_in_header_in_docs_subpage(selenium, browser_id, "API", endpoint.name)
        assert_active_sidebar_link_in_docs_subpage(selenium, browser_id, "API", endpoint.label)
        assert_expanded_folders_in_sidebar_in_docs_subpage(
            selenium, browser_id, "API", endpoint.category
        )
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        modal.operations.click()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) sees "(?P<name>.*?)" name in title, header and'
        r' active sidebar section in "(?P<subpage>Docs|API)" subpage of documentation'
    )
)
def assert_user_sees_docs_page(selenium, browser_id, subpage, name):
    assert_user_sees_name_in_header_in_docs_subpage(selenium, browser_id, subpage, name)
    assert_active_sidebar_link_in_docs_subpage(selenium, browser_id, subpage, name)
    assert_docs_title_contains(selenium, browser_id, f"{name} | Onedata Docs")
