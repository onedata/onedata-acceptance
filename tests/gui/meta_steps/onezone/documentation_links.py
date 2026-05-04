"""This module contains gherkin steps to run acceptance tests featuring
operations on links to documentation and checking documentation site content.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.steps.common.miscellaneous import switch_to_iframe, title_contains
from tests.gui.utils import DocsWebsite, EndpointInfo, Modals, Popups
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed

# The docs timeout needs to be higher than the standard WAIT_FRONTEND,
# because opening the docs page is a resource-consuming operation.
# Additionally, waiting for the headers to expand or for the desired section
# to become active also takes some time.
DEFAULT_DOCS_TIMEOUT = 30


SPACE_ENDPOINTS = {
    "Get space details": EndpointInfo("GET", "Get space details"),
    "List all space privileges": EndpointInfo("GET", "List all space privileges"),
    "List direct space users": EndpointInfo("GET", "List space users"),
    "List effective space users": EndpointInfo("GET", "List effective space users"),
    "Get effective space user details": EndpointInfo(
        "GET", "Get effective space user details"
    ),
    "List user's direct space privileges": EndpointInfo(
        "GET", "List user's space privileges"
    ),
    "List user's effective space privileges": EndpointInfo(
        "GET", "List effective user's space privileges"
    ),
    "Update user's space privileges": EndpointInfo(
        "PATCH", "Update user's space privileges"
    ),
    "List direct space groups": EndpointInfo("GET", "List space groups"),
    "List effective space groups": EndpointInfo("GET", "List effective space groups"),
    "Get effective space group details": EndpointInfo(
        "GET", "Get effective space group details"
    ),
    "List group's direct space privileges": EndpointInfo(
        "GET", "List group's space privileges"
    ),
    "List group's effective space privileges": EndpointInfo(
        "GET", "List effective group's space privileges"
    ),
    "Update group's space privileges": EndpointInfo(
        "PATCH", "Update group privileges to space"
    ),
    "List space shares": EndpointInfo("GET", "List space shares"),
}


FILE_DETAILS_ENDPOINTS = {
    "Download directory (tar)": EndpointInfo("GET", "Download file content"),
    "List directory files and subdirectories": EndpointInfo(
        "GET", "List directory files and subdirectories"
    ),
    "Create file in directory": EndpointInfo("POST", "Create file in directory"),
    "Remove file": EndpointInfo("DEL", "Remove file"),
    "Get attributes": EndpointInfo("GET", "Get file attributes"),
    "Get JSON metadata": EndpointInfo("GET", "Get file JSON metadata"),
    "Set JSON metadata": EndpointInfo("PUT", "Set file JSON metadata"),
    "Remove JSON metadata": EndpointInfo("DEL", "Remove file JSON metadata"),
    "Get RDF metadata": EndpointInfo("GET", "Get file RDF metadata"),
    "Set RDF metadata": EndpointInfo("PUT", "Set file RDF metadata"),
    "Remove RDF metadata": EndpointInfo("DEL", "Remove file RDF metadata"),
    "Get extended attributes (xattrs)": EndpointInfo(
        "GET", "Get file extended attributes"
    ),
    "Set extended attribute (xattr)": EndpointInfo(
        "PUT", "Set file extended attribute"
    ),
    "Remove extended attributes (xattrs)": EndpointInfo(
        "DEL", "Remove file extended attributes"
    ),
}


@repeat_failed(timeout=DEFAULT_DOCS_TIMEOUT)
def assert_active_section_in_docs_page(selenium, browser_id, link, page):
    driver = selenium[browser_id]
    active_links = DocsWebsite(driver)[page].sidebar.find_active_rows_names()
    assert (
        len(active_links) == 1
    ), f"Expected only one active link, but found {len(active_links)}"
    active_link = active_links[0]
    assert (
        active_link == link
    ), f"Expected active link to be {link}, but found {active_link}"


@repeat_failed(timeout=DEFAULT_DOCS_TIMEOUT)
def assert_user_sees_docs_page_header(selenium, browser_id, header):
    driver = selenium[browser_id]
    found_header = DocsWebsite(driver)["docs"].current_header
    assert (
        found_header == header
    ), f"expected header: {header}, found header: {found_header}"


@repeat_failed(timeout=DEFAULT_DOCS_TIMEOUT)
def assert_user_sees_api_endpoint_name(selenium, browser_id, endpoint):
    driver = selenium[browser_id]
    found_endpoint = DocsWebsite(driver)["api"].current_endpoint
    assert (
        found_endpoint == endpoint
    ), f"expected header: {endpoint}, found header: {found_endpoint}"


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
        command_name = FILE_DETAILS_ENDPOINTS[command].name
        title_contains(selenium, browser_id, f"{command_name} | API Reference")
        assert_user_sees_api_endpoint_name(selenium, browser_id, command_name)
        # TODO: VFS-13504, uncomment after fix
        # assert_active_section_in_docs_page(selenium, browser_id, command, "api")
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
        command_name = SPACE_ENDPOINTS[command].name
        title_contains(selenium, browser_id, f"{command_name} | API Reference")
        assert_user_sees_api_endpoint_name(selenium, browser_id, command_name)
        # TODO: VFS-13504, uncomment after fix
        # assert_active_section_in_docs_page(selenium, browser_id, command, "api")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        modal.operations.click()


@wt(parsers.parse('user of {browser_id} sees "{page_name}" docs page in documentation'))
def assert_user_sees_docs_page(selenium, browser_id, page_name):
    assert_user_sees_docs_page_header(selenium, browser_id, page_name)
    assert_active_section_in_docs_page(selenium, browser_id, page_name, "docs")
    title_contains(selenium, browser_id, f"{page_name} | Onedata Docs")
