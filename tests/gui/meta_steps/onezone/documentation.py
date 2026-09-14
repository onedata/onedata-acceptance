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
    assert_active_chapter_tab_in_documentation_subpage,
    assert_active_sidebar_endpoint_in_api_subpage,
    assert_active_sidebar_link_in_docs_subpage,
    assert_expanded_folders_in_sidebar_in_documentation_subpage,
    assert_user_sees_name_in_header_in_documentation_subpage,
    choose_rest_api_command_from_dropdown,
    click_operations_dropdown_in_api_modal,
    click_rest_api_documentation_link,
    get_rest_api_commands_from_dropdown,
)
from tests.gui.utils.homepage.api import EndpointInfo
from tests.gui.utils.homepage.generic import FILE_DETAILS_ENDPOINTS, SPACE_ENDPOINTS
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt


def _assert_endpoint_details_in_api_subpage(
    selenium: SeleniumDrivers, browser_id: str, endpoint: EndpointInfo
) -> None:
    assert_title_contains(
        selenium, browser_id, f"{endpoint.name} | {endpoint.reference_title}"
    )
    assert_active_chapter_tab_in_documentation_subpage(
        selenium, browser_id, "API", endpoint.chapter
    )
    assert_user_sees_name_in_header_in_documentation_subpage(
        selenium, browser_id, "API", endpoint.name
    )
    assert_active_sidebar_endpoint_in_api_subpage(
        selenium, browser_id, endpoint.name, endpoint.method
    )
    assert_expanded_folders_in_sidebar_in_documentation_subpage(
        selenium, browser_id, "API", [endpoint.category]
    )


@wt(
    parsers.parse(
        "user of {browser_id} sees that all links to REST API documentation works"
        " correctly for each selected operation in file details API section"
    )
)
def assert_all_links_to_rest_api_documentation_work_in_file_details(
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
        _assert_endpoint_details_in_api_subpage(selenium, browser_id, endpoint)
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
def assert_all_links_to_rest_api_documentation_work_in_space_menu(
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
        _assert_endpoint_details_in_api_subpage(selenium, browser_id, endpoint)
        close_current_tab(selenium, browser_id)
        switch_to_first_tab(selenium, browser_id)
        click_operations_dropdown_in_api_modal(selenium, browser_id, modal_name)


@wt(
    parsers.parse(
        "user of {browser_id} sees that page title, header and active sidebar link "
        'contain "{name}" name in "Docs" subpage in documentation'
    )
)
def assert_user_sees_name_in_docs_subpage(
    selenium: SeleniumDrivers, browser_id: str, name: str
) -> None:
    assert_user_sees_name_in_header_in_documentation_subpage(
        selenium, browser_id, "Docs", name
    )
    assert_active_sidebar_link_in_docs_subpage(selenium, browser_id, name)
    assert_title_contains(selenium, browser_id, f"{name} | Onedata Docs")
