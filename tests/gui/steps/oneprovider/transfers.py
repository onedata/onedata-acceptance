"""Steps for tests of Oneprovider transfers"""

__author__ = "Michal Stanisz, Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from typing import cast

import yaml
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import (
    click_option_in_popup_labeled_menu,
    switch_to_iframe,
)
from tests.gui.steps.oneprovider.common import wait_for_item_to_appear
from tests.gui.utils import Modals, OPLoggedIn, Popups
from tests.gui.utils.generic import parse_elements_sequence, transform
from tests.gui.utils.oneprovider.transfers import (
    TransferRecord,
    TransferRecordActive,
    TransferRecordHistory,
    _TransfersTab,
)
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


def _assert_transfer(
    transfer: TransferRecord,
    item_type: str,
    desc: str,
    sufix: str,
    hosts: Hosts,
    selenium: SeleniumDrivers,
    browser_id: str,
) -> None:
    assert getattr(
        transfer, f"is_{item_type}"
    )(), f"Transferred item is not {item_type} in {sufix}"

    parsed_desc = yaml.load(desc, yaml.Loader)
    for key, val in parsed_desc.items():
        if key == "destination":
            val = hosts[val]["name"]
        transfer_val = None
        try:
            transfer_val = getattr(transfer, key.replace(" ", "_"))
        except (RuntimeError, NoSuchElementException):
            # if key differs from column name, consider creating suitable dict
            key = key.replace(" ", "_")
            if key in ["type", "destination"]:
                _select_columns_to_be_visible_in_transfers(
                    selenium, browser_id, ["type_&_destination"]
                )
            else:
                _select_columns_to_be_visible_in_transfers(selenium, browser_id, [key])
            transfer_val = getattr(transfer, key)
        try:
            assert transfer_val == str(
                val
            ), f"Transfer {key} is {transfer_val} instead of {val} in {sufix}"
        except AssertionError as e:
            if "<" in val:
                symbol = val.split(" ")[0]
                value = float(val.split(" ")[1])
                unit = val.split(" ")[2]
                val = value if unit == "MiB" else value * 1024
                transfer_val = float(transfer_val.split(" ")[0])
                if symbol == "<=":
                    assert (
                        transfer_val <= val
                    ), f"{key}: {transfer_val} MiB is greater than {val} MiB"
                else:
                    assert (
                        transfer_val < val
                    ), f"{key}: {transfer_val} MiB is no less than {val} MiB"
            else:
                raise e


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees (?P<item_type>file|directory)"
        r" in ended transfers:\n(?P<desc>(.|\s)*)"
    )
)
@repeat_failed(interval=0.5, timeout=30)
def assert_ended_transfer(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_type: str,
    desc: str,
    hosts: Hosts,
) -> None:
    transfers = _get_transfers_and_enable_initial_cols(browser_id, selenium)
    transfer = cast(TransferRecordHistory, transfers.ended[0])
    _assert_transfer(
        transfer,
        item_type,
        desc,
        "ended",
        hosts,
        selenium,
        browser_id,
    )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees (?P<item_type>file|directory)"
        r" in waiting transfers:\n(?P<desc>(.|\s)*)"
    )
)
@repeat_failed(interval=0.5, timeout=40)
def assert_waiting_transfer(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_type: str,
    desc: str,
    hosts: Hosts,
) -> None:
    transfers = _get_transfers_and_enable_initial_cols(browser_id, selenium)
    transfer = cast(TransferRecordHistory, transfers.waiting[0])
    _assert_transfer(
        transfer,
        item_type,
        desc,
        "waiting",
        hosts,
        selenium,
        browser_id,
    )


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
    transfers = _get_transfers_and_enable_initial_cols(browser_id, selenium)
    if state == "waiting":
        try:
            getattr(transfers, state)[0].menu_button()
        except RuntimeError:
            cast(TransferRecordActive, transfers.ongoing[0]).menu_button()
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
def wait_for_waiting_transfer_to_start(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    assert (
        len(OPLoggedIn(selenium[browser_id]).transfers.waiting) == 0
    ), "Waiting transfers did not start"


@wt(parsers.re(r"user of (?P<browser_id>.*) waits for all transfers to finish"))
@repeat_failed(
    interval=1,
    timeout=240,
    exceptions=(AssertionError, StaleElementReferenceException),
)
def wait_for_ongoing_tranfers_to_finish(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    assert (
        len(OPLoggedIn(selenium[browser_id]).transfers.ongoing) == 0
    ), "Ongoing transfers did not finish"


@wt(parsers.re(r"user of (?P<browser_id>.*) expands first transfer record"))
@repeat_failed(timeout=WAIT_FRONTEND)
def expand_transfer_record(selenium: SeleniumDrivers, browser_id: str) -> None:
    transfers = _get_transfers_and_enable_initial_cols(browser_id, selenium)
    cast(TransferRecordHistory, transfers.ended[0]).expand()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees that there is non-zero "
        r"throughput in transfer chart"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_non_zero_transfer_speed(selenium: SeleniumDrivers, browser_id: str) -> None:
    transfers = _get_transfers_and_enable_initial_cols(browser_id, selenium)
    chart = cast(TransferRecordHistory, transfers.ended[0]).get_chart()
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
def replicate_item(
    selenium: SeleniumDrivers, browser_id: str, provider: str, hosts: Hosts
) -> None:
    menu_option = "Replicate here"
    driver = selenium[browser_id]
    provider_name = hosts[provider]["name"]
    Modals(driver).details_modal.data_distribution.providers[
        provider_name
    ].menu_button()
    Popups(driver).data_distribution_popup.menu[menu_option]()


@repeat_failed(timeout=WAIT_FRONTEND)
def is_current_item_fully_on_provider(driver: WebDriver, provider_name: str) -> bool:
    data_distribution_modal = Modals(driver).details_modal.data_distribution
    record = data_distribution_modal.providers[provider_name]
    return record.percentage_label == "100%"


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
    Modals(driver).details_modal.data_distribution.providers[
        provider_name
    ].menu_button()


@wt(
    parsers.parse(
        'user of {browser_id} cannot click "{option}" option in data'
        ' row menu for "{provider}" provider in "Data distribution" '
        "panel"
    )
)
def fail_to_click_option_in_data_distribution_popup(
    browser_id: str, option: str, selenium: SeleniumDrivers
) -> None:
    driver = selenium[browser_id]
    try:
        Popups(driver).data_distribution_popup.menu[option]()
        raise AssertionError(
            f'User can click on "{option}" option in in data row '
            'menu in "Data distribution" panel'
        )
    except RuntimeError:
        pass


@wt(
    parsers.re(
        r'user of {browser_id} sees "see history" button in data distribution modal'
    )
)
@repeat_failed(interval=1, timeout=90)
def assert_see_history_btn_shown(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    button = getattr(Modals(driver).details_modal.data_distribution, "see_history_btn")
    assert (
        button.is_displayed()
    ), 'Button "see history" not found in data distribution modal'


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) selects "(?P<space>.*)" space in transfers tab'
    )
)
def change_transfer_space(
    selenium: SeleniumDrivers, browser_id: str, space: str
) -> None:
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
    Modals(driver).details_modal.data_distribution.providers[
        provider_name
    ].menu_button()

    menu = Popups(driver).menu_popup_with_text.menu
    assert option not in menu, f"{option} should not be in selection menu"


@repeat_failed(timeout=WAIT_FRONTEND)
def _select_columns_to_be_visible_in_transfers(
    selenium: SeleniumDrivers, browser_id: str, columns: list[str]
) -> None:
    option_select = "select"
    option_unselect = "unselect"
    columns = [column.lower().replace(" ", "_") for column in columns]
    transfer = OPLoggedIn(selenium[browser_id]).transfers
    transfer.configure_columns.click()
    columns_menu = Popups(selenium[browser_id]).configure_columns_menu.columns
    wait_for_item_to_appear(
        Popups(selenium[browser_id]).configure_columns_menu.web_elem
    )
    for column in columns_menu:
        column_name = column.name.lower().replace(" ", "_")
        if column_name in columns:
            getattr(columns_menu[column.name], option_select)()
        else:
            getattr(columns_menu[column.name], option_unselect)()
    # hide columns menu popup
    transfer.configure_columns.click()


@repeat_failed(timeout=WAIT_FRONTEND)
def _get_transfers_and_enable_initial_cols(
    browser_id: str, selenium: SeleniumDrivers
) -> _TransfersTab:
    columns = ["user", "type & destination", "status"]
    _select_columns_to_be_visible_in_transfers(selenium, browser_id, columns)
    return OPLoggedIn(selenium[browser_id]).transfers


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) enables only (?P<columns>.*) "
        r"columns in columns configuration popover in "
        r"transfers table"
    ),
    converters={
        "columns": parse_elements_sequence,
    },
)
def select_columns_to_be_visible_in_transfers(
    selenium: SeleniumDrivers, browser_id: str, columns: list[str]
) -> None:
    _select_columns_to_be_visible_in_transfers(selenium, browser_id, columns)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees only (?P<columns>.*) columns in transfers"
    ),
    converters={
        "columns": parse_elements_sequence,
    },
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_visible_columns_in_transfers(
    browser_id: str, columns: list[str], selenium: SeleniumDrivers
) -> None:
    parsed_columns = columns
    transfers = OPLoggedIn(selenium[browser_id]).transfers
    transfers_columns = transfers.column_headers
    transfers_columns = list(map(lambda x: x.name.lower(), transfers_columns))
    err_msg = (
        "there is different number of columns visible: "
        f"{len(transfers_columns)} than expected: {len(parsed_columns)}, in "
        "transfers"
    )
    assert len(parsed_columns) == len(transfers_columns), err_msg
    for column in parsed_columns:
        if column.lower() not in transfers_columns:
            raise AssertionError(f"column {column} is not visible in transfers")
