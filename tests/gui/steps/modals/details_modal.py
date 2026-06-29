"""Steps used for details modal handling in various GUI testing scenarios"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from datetime import datetime

from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.common import wait_for_sliding_panel_to_stop_moving
from tests.gui.steps.modals.modal import check_modal_name
from tests.gui.steps.oneprovider.browser import (
    click_menu_for_elem_in_browser,
    click_option_in_data_row_menu_in_browser,
)
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils import Modals, Popups
from tests.gui.utils.generic import transform
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        'user of {browser_id} sees that {which_title} is "{title}" in modal "{modal}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_chart_title_in_details_modal(
    selenium: SeleniumDrivers,
    browser_id: str,
    title: str,
    which_title: str,
    modal: str,
) -> None:
    modal_name = check_modal_name(modal)
    modal_page = getattr(Modals(selenium[browser_id]), modal_name).size_statistics
    if which_title == "charts title":
        charts_title = modal_page.charts_title
    elif which_title == "count chart title":
        charts_title = modal_page.chart[0].title
    else:
        charts_title = modal_page.chart[1].title
    assert (
        charts_title == title
    ), f"Charts title is {charts_title} not {title} as expected"


@wt(parsers.parse('user of {browser_id} clicks on chart in modal "{modal}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_chart_in_modal(
    browser_id: str, selenium: SeleniumDrivers, modal: str
) -> None:
    modal = check_modal_name(modal)
    getattr(Modals(selenium[browser_id]), modal).size_statistics.chart[0].chart.click()


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{element}" item displayed '
        'in "{modal}" modal is not active'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_button_in_modal_not_active(
    browser_id: str, modal: str, element: str, selenium: SeleniumDrivers
) -> None:
    driver = selenium[browser_id]
    modal_page = getattr(Modals(driver), check_modal_name(modal))
    err_msg = f'"{element}" button is in active state'
    assert not modal_page.is_element_active(transform(element)), err_msg


@wt(
    parsers.parse(
        "user of {browser_id} sees that tooltip with size statistics"
        ' header has date format in modal "{modal}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_tooltip_on_chart_in_modal(
    browser_id: str, selenium: SeleniumDrivers
) -> None:
    driver = selenium[browser_id]
    header = Popups(driver).chart_statistics.header
    try:
        datetime.strptime(header, "%H:%M %d/%m/%Y")
    except ValueError:
        raise ValueError(
            f"Header: {header} of tooltip does not have date format"
        ) from ValueError


@wt(
    parsers.re(
        'user of (?P<browser_id>.*) clicks on "(?P<tab_name>.*)" '
        'navigation tab in "(?P<modal>.*)" modal'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_navigation_tab_in_modal(
    selenium: SeleniumDrivers, browser_id: str, tab_name: str, modal: str
) -> None:
    modal_page = getattr(Modals(selenium[browser_id]), check_modal_name(modal))
    tab = modal_page.navigation[tab_name]
    tab.web_elem.click()


@wt(
    parsers.re(
        'user of (?P<browser_id>.*) clicks on "(?P<tab_name>.*)" '
        "navigation tab in (?P<modal>.*) panel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_navigation_tab_in_panel(
    selenium: SeleniumDrivers, browser_id: str, tab_name: str, modal: str
) -> None:
    modal_page = getattr(
        Modals(selenium[browser_id]).details_modal, check_modal_name(modal)
    )
    tab = modal_page.navigation[tab_name]
    tab.web_elem.click()


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{modal_name}" modal is opened on "{tab}" tab'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_tab_in_modal(
    selenium: SeleniumDrivers, browser_id: str, tab: str, modal_name: str
) -> None:
    # For Google Chrome run in xvfb at version >= 128.0.6613.119, tests were
    # crashing when trying to get active tab, when file details panel is being
    # animated. There are plans to add special class to the modal/panel saying that
    # the transition ended. Currently we check that rectangle position of modal stops
    # changing.
    # TODO: VFS-12424 Add class to fully-transitioned file details panel
    driver = selenium[browser_id]
    modal_name_transformed = check_modal_name(transform(modal_name))
    if modal_name_transformed == "details_modal":
        wait_for_sliding_panel_to_stop_moving(
            driver, WAIT_FRONTEND, ".modal-content .modal-body"
        )

    active_tab = getattr(Modals(driver), modal_name_transformed).active_tab
    err_msg = (
        f"Expected tab: {tab} does not match actual active tab: "
        f"{active_tab} on modal {modal_name}"
    )
    assert tab in active_tab, err_msg


@wt(
    parsers.parse(
        'user of {browser_id} sees that "Permissions" panel is opened'
        ' on "POSIX" tab in "{modal_name}" modal'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_posix_tab_in_panel(
    selenium: SeleniumDrivers, browser_id: str, modal_name: str
) -> None:
    elem_name = "posix_permission_edition"
    posix_hidden = getattr(
        Modals(selenium[browser_id]), check_modal_name(transform(modal_name))
    ).edit_permissions.is_hidden(elem_name)
    assert (
        not posix_hidden
    ), 'sees that "Permissions" panel is not opened on "POSIX" tab'


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "{context_menu_item}" in '
        'context menu for "{item_name}"'
    )
)
@wt(
    parsers.parse(
        'user of {browser_id} clicks on "{context_menu_item}" in '
        "context menu for {item_name} in file browser"
    )
)
def click_on_context_menu_item(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_name: str,
    tmp_memory: TmpMemory,
    context_menu_item: str,
) -> None:
    if item_name[0] == '"':
        item_name = item_name.replace('"', "")
    click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, context_menu_item)


@wt(
    parsers.parse(
        'user of {browser_id} clicks on button "Show more physical locations" in'
        " details modal"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_show_more_physical_locations_in_details_modal(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    details_modal = Modals(selenium[browser_id]).details_modal
    physical_locations = details_modal.physical_locations
    physical_locations.show_more_button.click()


@wt(
    parsers.parse(
        'user of {browser_id} sees "{expected_error}" as error message in physical'
        ' location section for "{provider}" provider in details modal'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_error_message_in_physical_location_in_details_modal(
    selenium: SeleniumDrivers,
    browser_id: str,
    expected_error: str,
    provider: str,
    hosts: Hosts,
) -> None:
    provider_name = hosts[provider]["name"]
    details_modal = Modals(selenium[browser_id]).details_modal
    physical_locations = details_modal.physical_locations.locations
    found_error = physical_locations[provider_name].error_message
    assert found_error == expected_error, (
        f'Error message "{found_error}" is different than expected for'
        f" {provider_name} provider"
    )


def click_copy_icon_for_browser_link_on_details_modal(
    driver: WebDriver, link_type: str
) -> None:
    copy_icon = (
        Modals(driver).details_modal.browser_links.links[link_type].clipboard_icon
    )
    copy_icon.click()
