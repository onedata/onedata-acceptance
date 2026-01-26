"""This module contains gherkin steps to run acceptance tests featuring
operations on links to documentation and checking documentation site content.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from selenium.webdriver.common.by import By

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import title_contains
from tests.gui.utils import Modals, Popups
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{link}" sidebar link is active in'
        " documentation page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND * 4)
def assert_active_section_in_docks(selenium, browser_id, link):
    driver = selenium[browser_id]
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    if len(iframes) > 0:
        driver.switch_to.frame(iframes[-1])
    sidebar_links = driver.find_elements(By.CSS_SELECTOR, ".sidebar-link.active")
    for sidebar_link in sidebar_links:
        if sidebar_link.text.lower() == link.lower():
            return
    raise AssertionError(f"sidebar link {link} not found")


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{heading}" sidebar heading is expanded in'
        " documentation page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND * 4)
def assert_expanded_heading_in_docks(selenium, browser_id, heading):
    driver = selenium[browser_id]
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    if len(iframes) > 0:
        driver.switch_to.frame(iframes[-1])
    sidebar_links = driver.find_elements(By.CSS_SELECTOR, ".sidebar-heading.open")
    for sidebar_link in sidebar_links:
        if sidebar_link.text.lower() == heading.lower():
            return
    raise AssertionError(f"sidebar link {heading} not found")


@repeat_failed(timeout=WAIT_FRONTEND * 6)
def assert_active_section_in_api_docks(selenium, browser_id, label):
    driver = selenium[browser_id]
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    if len(iframes) > 0:
        driver.switch_to.frame(iframes[-1])
    sidebar_labels = driver.find_elements(
        By.CSS_SELECTOR, 'label[role="menuitem"].active'
    )
    for sidebar_label in sidebar_labels:
        if (
            sidebar_label.text.replace("\n", " ").lower()
            == label.replace("\n", " ").lower()
        ):
            return
    raise ValueError(f"sidebar label {label} not found")


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
    commands = [item.text for item in popup.items]
    s = {
        "Download directory (tar)\nREST": "GET Download file content",
        "List directory files and subdirectories\nREST": (
            "GET List directory files and subdirectories"
        ),
        "Create file in directory\nREST": "POST Create file in directory",
        # "Get data distribution\nREST": "",
        "Remove file\nREST": "DEL Remove file",
        "Get attributes\nREST": "GET Get file attributes",
        "Get JSON metadata\nREST": "GET Get file json metadata",
        "Set JSON metadata\nREST": "PUT Set file json metadata",
        "Remove JSON metadata\nREST": "DEL Remove file json metadata",
        "Get RDF metadata\nREST": "GET Get file rdf metadata",
        "Set RDF metadata\nREST": "PUT Set file rdf metadata",
        "Remove RDF metadata\nREST": "DEL Remove file rdf metadata",
        "Get extended attributes (xattrs)\nREST": "GET Get file extended attributes",
        "Set extended attribute (xattr)\nREST": "PUT Set file extended attribute",
        "Remove extended attributes (xattrs)\nREST": (
            "DEL Remove file extended attributes"
        ),
    }
    for command in commands:
        # TODO: VFS-12753, remove after fix
        if command == "Get data distribution\nREST":
            continue
        modal = Modals(driver).details_modal.api
        Popups(driver).power_select.choose_item(command)
        modal.rest_api_documentation.click()
        driver.switch_to.window(driver.window_handles[-1])
        title_contains(selenium, browser_id, "Onedata | API")
        assert_active_section_in_api_docks(selenium, browser_id, s[command])

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframes[-1])
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
    commands = [item.text for item in popup.items]
    s = {
        "Get space details\nREST": "GET Get space details",
        "List all space privileges\nREST": "GET List all space privileges",
        "List direct space users\nREST": "GET List space users",
        "List effective space users\nREST": "GET List effective space users",
        "Get effective space user details\nREST": (
            "GET Get effective space user details"
        ),
        "List user's direct space privileges\nREST": "GET List user's space privileges",
        "List user's effective space privileges\nREST": (
            "GET List effective user's space privileges"
        ),
        "Update user's space privileges\nREST": "PATCH Update user's space privileges",
        "List direct space groups\nREST": "GET List space groups",
        "List effective space groups\nREST": "GET List effective space groups",
        "Get effective space group details\nREST": (
            "GET Get effective space group details"
        ),
        "List group's direct space privileges\nREST": (
            "GET List group's space privileges"
        ),
        "List group's effective space privileges\nREST": (
            "GET List effective group's space privileges"
        ),
        "Update group's space privileges\nREST": (
            "PATCH Update group privileges to space"
        ),
        "List space shares\nREST": "GET List space shares",
    }

    for command in commands:
        modal = Modals(driver).rest_api.api
        Popups(driver).power_select.choose_item(command)
        modal.rest_api_documentation.click()
        driver.switch_to.window(driver.window_handles[-1])
        title_contains(selenium, browser_id, "Onedata | API")
        assert_active_section_in_api_docks(selenium, browser_id, s[command])

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        modal.operations.click()
