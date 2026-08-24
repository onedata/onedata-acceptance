"""This module contains gherkin meta steps to run acceptance tests featuring
operations on links to documentation and checking documentation site content.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.steps.common.miscellaneous import assert_title_contains, switch_to_iframe
from tests.gui.steps.common.url import (
    close_current_tab,
    switch_to_first_tab,
    switch_to_last_tab,
)
from tests.gui.steps.onezone.documentation import (
    assert_active_chapter_tab_in_docs_subpage,
    assert_expanded_folders_in_sidebar_in_docs_subpage,
    assert_sidebar_link_is_active_in_documentation_subpage,
    assert_user_sees_name_in_header_in_docs_subpage,
    choose_rest_api_command_from_dropdown,
    click_operations_dropdown_in_api_modal,
    click_rest_api_documentation_link,
    get_rest_api_commands_from_dropdown,
)
from tests.gui.utils.homepage.documentation import EndpointInfo
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt

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


@wt(
    parsers.parse(
        "user of {browser_id} sees that all links to REST API documentation works"
        " correctly for each selected operation in file details API section"
    )
)
def assert_all_links_to_rest_api_docs_works_in_file_details(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    modal_name = "details_modal"
    click_operations_dropdown_in_api_modal(selenium, browser_id, modal_name)
    commands = get_rest_api_commands_from_dropdown(selenium, browser_id)
    for command in commands:
        choose_rest_api_command_from_dropdown(selenium, browser_id, command)
        click_rest_api_documentation_link(selenium, browser_id, modal_name)
        switch_to_last_tab(selenium, browser_id)
        endpoint = FILE_DETAILS_ENDPOINTS[command]
        assert_title_contains(selenium, browser_id, f"{endpoint.name} | API Reference")
        assert_active_chapter_tab_in_docs_subpage(
            selenium, browser_id, "API", endpoint.chapter
        )
        assert_user_sees_name_in_header_in_docs_subpage(
            selenium, browser_id, "API", endpoint.name
        )
        assert_sidebar_link_is_active_in_documentation_subpage(
            selenium, browser_id, "API", endpoint.label
        )
        assert_expanded_folders_in_sidebar_in_docs_subpage(
            selenium,
            browser_id,
            "API",
            [endpoint.category],
        )
        close_current_tab(selenium, browser_id)
        switch_to_first_tab(selenium, browser_id)
        switch_to_iframe(selenium, browser_id)
        click_operations_dropdown_in_api_modal(selenium, browser_id, modal_name)


@wt(
    parsers.parse(
        "user of {browser_id} sees that all links to REST API documentation works"
        " correctly for each selected operation in space menu API section"
    )
)
def assert_all_links_to_rest_api_docs_works_in_space_menu(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    modal_name = "rest_api"
    click_operations_dropdown_in_api_modal(selenium, browser_id, modal_name)
    commands = get_rest_api_commands_from_dropdown(selenium, browser_id)
    for command in commands:
        choose_rest_api_command_from_dropdown(selenium, browser_id, command)
        click_rest_api_documentation_link(selenium, browser_id, modal_name)
        switch_to_last_tab(selenium, browser_id)
        endpoint = SPACE_ENDPOINTS[command]
        assert_title_contains(selenium, browser_id, f"{endpoint.name} | API Reference")
        assert_active_chapter_tab_in_docs_subpage(
            selenium, browser_id, "API", endpoint.chapter
        )
        assert_user_sees_name_in_header_in_docs_subpage(
            selenium, browser_id, "API", endpoint.name
        )
        assert_sidebar_link_is_active_in_documentation_subpage(
            selenium, browser_id, "API", endpoint.label
        )
        assert_expanded_folders_in_sidebar_in_docs_subpage(
            selenium, browser_id, "API", [endpoint.category]
        )
        close_current_tab(selenium, browser_id)
        switch_to_first_tab(selenium, browser_id)
        click_operations_dropdown_in_api_modal(selenium, browser_id, modal_name)


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
    assert_sidebar_link_is_active_in_documentation_subpage(
        selenium, browser_id, subpage, name
    )
    assert_title_contains(selenium, browser_id, f"{name} | Onedata Docs")
