"""Steps for tests of Oneprovider transfers"""

__author__ = "Michal Stanisz, Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from typing import Any

import pytest
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from tests.gui.constants import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import (
    click_option_in_popup_labeled_menu,
    switch_to_iframe,
)
from tests.gui.utils import Modals, OPLoggedIn, Popups
from tests.gui.utils.core.web_objects import PageObjectNotFoundError
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    TransferState,
    parse_elements_sequence,
    transform,
)
from tests.gui.utils.oneprovider.transfers import (
    TransferItemType,
    TransferRecord,
    TransferRecordActive,
    TransferRecordHistory,
    _TransfersTab,
)
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


def get_transfer_record(
    selenium: SeleniumDrivers,
    browser_id: str,
    transfer_id: str | int,
) -> TransferRecord:
    transfers = OPLoggedIn(selenium[browser_id]).transfers
    active_tab: TransferState = transfers.get_active_tab()
    return getattr(transfers, active_tab.value)[transfer_id]


@repeat_failed(timeout=WAIT_FRONTEND)
def select_transfer_state_tab(
    selenium: SeleniumDrivers,
    browser_id: str,
    transfer_state: TransferState,
) -> None:
    transfers = OPLoggedIn(selenium[browser_id]).transfers
    transfers[transfer_state.value].click()


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_transfer_item_type(
    selenium: SeleniumDrivers,
    browser_id: str,
    transfer_id: str | int,
    transfer_state: TransferState,
    expected_item_type: TransferItemType,
) -> None:
    transfer = get_transfer_record(selenium, browser_id, transfer_id)
    match expected_item_type:
        case TransferItemType.FILE:
            is_expected_item_type = transfer.is_file()
        case TransferItemType.DIRECTORY:
            is_expected_item_type = transfer.is_directory()

    assert is_expected_item_type, (
        f"Transferred item is not {expected_item_type.value} in {transfer_state.value}"
    )


def assert_transfer_status(
    selenium: SeleniumDrivers,
    browser_id: str,
    transfer_id: str | int,
    transfer_state: TransferState,
    expected_status: str,
) -> None:
    def has_expected_status(_: WebDriver) -> bool:
        transfer = get_transfer_record(selenium, browser_id, transfer_id)
        return transfer.status == expected_status

    WebDriverWait(
        selenium[browser_id],
        timeout=90,
        poll_frequency=0.5,
        ignored_exceptions=(
            NoSuchElementException,
            PageObjectNotFoundError,
            StaleElementReferenceException,
        ),
    ).until(
        has_expected_status,
        message=(
            f'Transfer "{transfer_id}" in {transfer_state.value} '
            f'did not reach status "{expected_status}"'
        ),
    )


def get_transfer_column_value(
    selenium: SeleniumDrivers,
    browser_id: str,
    transfer_id: str | int,
    column: str,
) -> Any:
    def get_column_value(_: WebDriver) -> Any:
        transfer = get_transfer_record(selenium, browser_id, transfer_id)
        return getattr(transfer, column)

    return WebDriverWait(
        selenium[browser_id],
        timeout=WAIT_FRONTEND,
        poll_frequency=0.1,
        ignored_exceptions=(
            NoSuchElementException,
            PageObjectNotFoundError,
            StaleElementReferenceException,
            ValueError,
        ),
    ).until(
        get_column_value,
        message=(f'Column "{column}" for transfer "{transfer_id}" was not readable'),
    )


def assert_transfer_column_value(
    column_name: str,
    actual: Any,
    expected: Any,
) -> None:
    if actual == str(expected):
        return

    error_message = f"Transfer {column_name} is {actual} instead of {expected}"
    if not isinstance(expected, str) or not expected.startswith("<"):
        raise AssertionError(error_message)

    operator, value, unit = expected.split()
    limit_mib = float(value) if unit == "MiB" else float(value) * 1024
    actual_mib = float(actual.split()[0])
    is_within_limit = actual_mib <= limit_mib if operator == "<=" else actual_mib < limit_mib
    assert is_within_limit, error_message


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) (?P<option>cancels|reruns) transfer "
        r"in transfers tab for (?P<state>certain file)"
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) (?P<option>cancels|reruns) transfer "
        r"in (?P<state>waiting|ended) transfers"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def cancel_or_rerun_transfer(
    selenium: SeleniumDrivers, browser_id: str, option: str, state: str
) -> None:
    transfers = get_transfers(selenium[browser_id])
    if state == "waiting":
        try:
            getattr(transfers, state)[0].menu_button()
        except (
            ElementNotInteractableException,
            NoSuchElementException,
            PageObjectNotFoundError,
        ):
            ongoing_transfer: TransferRecordActive = transfers.ongoing[0]
            ongoing_transfer.menu_button()
    else:
        getattr(transfers, transform(state))[0].menu_button()

    option = "Cancel transfer" if option == "cancels" else "Rerun transfer"
    click_option_in_popup_labeled_menu(selenium, browser_id, option)


@wt(parsers.re(r"user of (?P<browser_id>.*) waits for all transfers to start"))
@repeat_failed(
    interval=1,
    timeout=420,
    exceptions=(AssertionError, StaleElementReferenceException),
)
def wait_for_waiting_transfer_to_start(selenium: SeleniumDrivers, browser_id: str) -> None:
    assert len(OPLoggedIn(selenium[browser_id]).transfers.waiting) == 0, (
        "Waiting transfers did not start"
    )


@wt(parsers.re(r"user of (?P<browser_id>.*) waits for all transfers to finish"))
@repeat_failed(
    interval=1,
    timeout=240,
    exceptions=(AssertionError, StaleElementReferenceException),
)
def wait_for_ongoing_tranfers_to_finish(selenium: SeleniumDrivers, browser_id: str) -> None:
    assert len(OPLoggedIn(selenium[browser_id]).transfers.ongoing) == 0, (
        "Ongoing transfers did not finish"
    )


@wt(parsers.re(r"user of (?P<browser_id>.*) expands first transfer record"))
@repeat_failed(timeout=WAIT_FRONTEND)
def expand_transfer_record(selenium: SeleniumDrivers, browser_id: str) -> None:
    transfers = get_transfers(selenium[browser_id])
    ended_transfer: TransferRecordHistory = transfers.ended[0]
    ended_transfer.expand()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees that there is non-zero "
        r"throughput in transfer chart"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_non_zero_transfer_speed(selenium: SeleniumDrivers, browser_id: str) -> None:
    transfers = get_transfers(selenium[browser_id])
    ended_transfer: TransferRecordHistory = transfers.ended[0]
    chart = ended_transfer.get_chart()
    assert chart.get_speed() != "0", "Transfer throughput is 0"


@repeat_failed(timeout=WAIT_BACKEND)
def _expand_dropdown_in_migrate_record(driver: WebDriver) -> None:
    data_distribution_modal = Modals(driver).details_modal.data_distribution
    data_distribution_modal.migrate.expand_dropdown()
    assert len(Popups(driver).migrate_dropdown.providers_list) > 0


def check_provider_in_migrate_dropdown(driver: WebDriver, provider_name: str) -> bool:
    data_distribution_modal = Modals(driver).details_modal.data_distribution
    return provider_name == data_distribution_modal.migrate.target_provider


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) migrates selected item from "
        r'provider "(?P<source>.*)" to provider "(?P<target>.*)"'
    )
)
def migrate_item(
    selenium: SeleniumDrivers,
    browser_id: str,
    source: str,
    target: str,
    hosts: Hosts,
) -> None:
    menu_option = "Migrate..."

    driver = selenium[browser_id]
    source_name = hosts[source]["name"]
    target_name = hosts[target]["name"]

    data_distribution_modal = Modals(driver).details_modal.data_distribution
    data_distribution_modal.providers[source_name].menu_button()
    Popups(driver).data_distribution_popup.menu[menu_option]()

    if not check_provider_in_migrate_dropdown(driver, target_name):
        _expand_dropdown_in_migrate_record(driver)
        Popups(driver).migrate_dropdown.providers_list[target_name].click()

    data_distribution_modal.migrate.migrate_button()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) replicates selected item"
        r' to provider "(?P<provider>.*)"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def replicate_item(selenium: SeleniumDrivers, browser_id: str, provider: str, hosts: Hosts) -> None:
    menu_option = "Replicate here"
    driver = selenium[browser_id]
    provider_name = hosts[provider]["name"]
    Modals(driver).details_modal.data_distribution.providers[provider_name].menu_button()
    Popups(driver).data_distribution_popup.menu[menu_option]()


@repeat_failed(timeout=WAIT_FRONTEND)
def is_current_item_fully_on_provider(driver: WebDriver, provider_name: str) -> bool:
    data_distribution_modal = Modals(driver).details_modal.data_distribution
    record = data_distribution_modal.providers[provider_name]
    return record.percentage_label == "100%"


@repeat_failed(timeout=WAIT_FRONTEND)
def click_link_in_data_distribution_panel(
    selenium: SeleniumDrivers, browser_id: str, link: str
) -> None:
    getattr(
        Modals(selenium[browser_id]).details_modal.data_distribution,
        transform(link),
    ).click()


@wt(
    parsers.parse(
        "user of {browser_id} clicks on menu button for "
        '"{provider}" provider in "Data distribution" panel'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_menu_button_in_data_distribution_panel(
    selenium: SeleniumDrivers, browser_id: str, provider: str, hosts: Hosts
) -> None:
    driver = selenium[browser_id]
    provider_name = hosts[provider]["name"]
    Modals(driver).details_modal.data_distribution.providers[provider_name].menu_button()


@wt(
    parsers.parse(
        'user of {browser_id} cannot click "{option}" option in data'
        ' row menu for "{provider}" provider in "Data distribution" panel'
    )
)
def fail_to_click_option_in_data_distribution_popup(
    browser_id: str, option: str, selenium: SeleniumDrivers
) -> None:
    driver = selenium[browser_id]
    menu = Popups(driver).data_distribution_popup.menu
    if option not in menu:
        return

    with pytest.raises(ElementNotInteractableException):
        menu[option]()


@wt(parsers.re(r'user of {browser_id} sees "see history" button in data distribution modal'))
@repeat_failed(interval=1, timeout=90)
def assert_see_history_btn_shown(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    button = Modals(driver).details_modal.data_distribution.see_history
    assert button.is_displayed(), 'Button "see history" not found in data distribution modal'


@wt(parsers.re(r'user of (?P<browser_id>.*) selects "(?P<space>.*)" space in transfers tab'))
def change_transfer_space(selenium: SeleniumDrivers, browser_id: str, space: str) -> None:
    OPLoggedIn(selenium[browser_id]).transfers.spaces[space].select()


@wt(parsers.re(r"user of (?P<browser_id>.*) waits for Transfers page to load"))
@repeat_failed(timeout=WAIT_BACKEND)
def wait_for_transfers_page_to_load(selenium: SeleniumDrivers, browser_id: str) -> None:
    switch_to_iframe(selenium, browser_id)

    assert OPLoggedIn(selenium[browser_id]).transfers.providers_table.is_displayed()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) does not see "(?P<option>Replicate '
        r'here|Migrate...|Evict)" options when clicking on provider "('
        r'?P<provider>.*)" menu button'
    ),
)
def assert_option_in_provider_popup_menu(
    selenium: SeleniumDrivers,
    browser_id: str,
    provider: str,
    hosts: Hosts,
    option: str,
) -> None:
    driver = selenium[browser_id]
    provider_name = hosts[provider]["name"]
    Modals(driver).details_modal.data_distribution.providers[provider_name].menu_button()

    menu = Popups(driver).menu_popup_with_text.menu
    assert option not in menu, f"{option} should not be in selection menu"


def get_transfers(driver: WebDriver) -> _TransfersTab:
    return OPLoggedIn(driver).transfers


@wt(
    parsers.re(
        rf"user of (?P<browser_id>.*) sees only "
        rf"(?P<columns>{ELEMENTS_SEQUENCE_PATTERN}) columns in transfers"
    ),
    converters={
        "columns": parse_elements_sequence,
    },
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_visible_columns_in_transfers(
    browser_id: str, columns: list[str], selenium: SeleniumDrivers
) -> None:
    transfers = get_transfers(selenium[browser_id])
    transfers_columns = transfers.column_headers
    transfers_columns = [x.name.lower() for x in transfers_columns]
    error_message = (
        "there is different number of columns visible: "
        f"{len(transfers_columns)} than expected: {len(columns)}, in "
        "transfers"
    )
    assert len(columns) == len(transfers_columns), error_message
    for column in columns:
        if column.lower() not in transfers_columns:
            raise AssertionError(f"column {column} is not visible in transfers")
