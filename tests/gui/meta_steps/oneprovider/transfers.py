"""This module contains meta steps for operations on transfers
using web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from typing import cast

import yaml
from selenium.common.exceptions import NoSuchElementException

from tests.gui.meta_steps.oneprovider.browser_columns_configuration import (
    select_columns_to_be_visible_in_transfers,
)
from tests.gui.meta_steps.oneprovider.common import replicate_files_to_providers
from tests.gui.steps.modals.details_modal import assert_tab_in_modal
from tests.gui.steps.modals.modal import click_modal_button
from tests.gui.steps.oneprovider.browser import (
    click_menu_for_elem_in_browser,
    click_option_in_data_row_menu_in_browser,
)
from tests.gui.steps.oneprovider.data_tab import (
    check_current_provider_in_space,
    choose_provider_in_selected_page,
    click_choose_other_oneprovider_on_file_browser,
)
from tests.gui.steps.oneprovider.transfers import (
    click_link_in_data_distribution_panel,
    get_transfers,
    wait_for_ongoing_tranfers_to_finish,
    wait_for_transfers_page_to_load,
    wait_for_waiting_transfer_to_start,
)
from tests.gui.steps.onezone.spaces import click_on_option_of_space_on_left_sidebar_menu
from tests.gui.type_definitions import TmpMemory, VisibleColumns
from tests.gui.utils import Modals, Popups
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    parse_elements_sequence,
)
from tests.gui.utils.oneprovider.transfers import TransferRecord, TransferRecordHistory
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


def assert_transfer(
    transfer: TransferRecord,
    item_type: str,
    desc: str,
    sufix: str,
    hosts: Hosts,
    selenium: SeleniumDrivers,
    browser_id: str,
    visible_columns: VisibleColumns,
) -> None:
    assert getattr(transfer, f"is_{item_type}")(), f"Transferred item is not {item_type} in {sufix}"

    parsed_desc = yaml.load(desc, yaml.Loader)
    for field_name, configured_value in parsed_desc.items():
        expected_value = (
            hosts[configured_value]["name"] if field_name == "destination" else configured_value
        )
        attribute_name = field_name.replace(" ", "_")
        transfer_val = None
        try:
            transfer_val = getattr(transfer, attribute_name)
        except NoSuchElementException:
            # if key differs from column name, consider creating suitable dict
            if attribute_name in ["type", "destination"]:
                select_columns_to_be_visible_in_transfers(
                    selenium, browser_id, ["type_&_destination"], visible_columns
                )
            else:
                select_columns_to_be_visible_in_transfers(
                    selenium, browser_id, [attribute_name], visible_columns
                )
            transfer_val = getattr(transfer, attribute_name)
        try:
            assert transfer_val == str(expected_value), (
                f"Transfer {field_name} is {transfer_val} instead of {expected_value} in {sufix}"
            )
        except AssertionError as e:
            if "<" in expected_value:
                symbol = expected_value.split(" ")[0]
                size_value = float(expected_value.split(" ")[1])
                unit = expected_value.split(" ")[2]
                expected_size_mib = size_value if unit == "MiB" else size_value * 1024
                actual_size_mib = float(transfer_val.split(" ")[0])
                if symbol == "<=":
                    assert actual_size_mib <= expected_size_mib, (
                        f"{field_name}: {actual_size_mib} MiB is greater than "
                        f"{expected_size_mib} MiB"
                    )
                else:
                    assert actual_size_mib < expected_size_mib, (
                        f"{field_name}: {actual_size_mib} MiB is no less than "
                        f"{expected_size_mib} MiB"
                    )
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
    visible_columns: VisibleColumns,
) -> None:
    transfers = get_transfers(selenium[browser_id])
    transfer = cast(TransferRecordHistory, transfers.ended[0])
    assert_transfer(
        transfer,
        item_type,
        desc,
        "ended",
        hosts,
        selenium,
        browser_id,
        visible_columns,
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
    visible_columns: VisibleColumns,
) -> None:
    transfers = get_transfers(selenium[browser_id])
    transfer = cast(TransferRecordHistory, transfers.waiting[0])
    assert_transfer(
        transfer,
        item_type,
        desc,
        "waiting",
        hosts,
        selenium,
        browser_id,
        visible_columns,
    )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) opens (?P<provider>.*) "
        r'Oneprovider transfers for "(?P<space>.*)" space'
    )
)
def open_transfers_page(
    selenium: SeleniumDrivers, browser_id: str, provider: str, space: str, hosts: Hosts
) -> None:
    option = "Transfers"
    provider_name = hosts[provider]["name"]

    click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id, space, option)
    if provider_name != check_current_provider_in_space(selenium, browser_id):
        click_choose_other_oneprovider_on_file_browser(selenium, browser_id)
        choose_provider_in_selected_page(selenium, browser_id, provider, hosts)

    wait_for_transfers_page_to_load(selenium, browser_id)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) opens transfer page using "
        r'"(?P<link>see ongoing transfers|see history)" link on "Distribution" tab for "(?P<file>.*)" file'
    )
)
def open_transfer_page_by_clicking_on_link(
    browser_id: str,
    file: str,
    tmp_memory: TmpMemory,
    selenium: SeleniumDrivers,
    link: str,
) -> None:
    click_menu_for_elem_in_browser(browser_id, file, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, "Data distribution")
    click_link_in_data_distribution_panel(selenium, browser_id, link)
    wait_for_transfers_page_to_load(selenium, browser_id)


@wt(parsers.parse('user of {browser_id} evicts file "{file_name}" from provider {provider}'))
def evict_file(
    selenium: SeleniumDrivers,
    browser_id: str,
    provider: str,
    file_name: str,
    tmp_memory: TmpMemory,
    hosts: Hosts,
) -> None:
    option = "Data distribution"
    tab = "Distribution"
    menu_option = "Evict"
    driver = selenium[browser_id]
    provider_name = hosts[provider]["name"]
    details_modal = "Details modal"
    close_button = "X"

    click_menu_for_elem_in_browser(browser_id, file_name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option)
    assert_tab_in_modal(selenium, browser_id, tab, details_modal)
    data_distribution_modal = Modals(driver).details_modal.data_distribution
    data_distribution_modal.providers[provider_name].menu_button()
    Popups(driver).data_distribution_popup.menu[menu_option]()
    click_modal_button(selenium, browser_id, close_button, details_modal)


@wt(
    parsers.re(
        r'user of (?P<browser_id>.+) waits until "(?P<provider>.+)" transfers complete'
        r' for "(?P<space>.+)" space'
    )
)
def wait_for_all_transfers_to_start_and_finish(
    selenium: SeleniumDrivers, browser_id: str, provider: str, space: str, hosts: Hosts
) -> None:
    open_transfers_page(selenium, browser_id, provider, space, hosts)
    wait_for_waiting_transfer_to_start(selenium, browser_id)
    wait_for_ongoing_tranfers_to_finish(selenium, browser_id)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+) "
        rf'replicates (?P<names>{ELEMENTS_SEQUENCE_PATTERN}) in space "(?P<space>.+)"'
        r' to provider "(?P<provider>.+)"'
        r" and waits for all transfers to complete"
    ),
    converters={"names": parse_elements_sequence},
)
def replicate_and_wait_to_complete(
    selenium: SeleniumDrivers,
    browser_id: str,
    names: list[str],
    space: str,
    provider: str,
    tmp_memory: TmpMemory,
    hosts: Hosts,
) -> None:
    replicate_files_to_providers(
        selenium, browser_id, names, tmp_memory, [provider], hosts, "replicates"
    )
    wait_for_all_transfers_to_start_and_finish(selenium, browser_id, provider, space, hosts)
