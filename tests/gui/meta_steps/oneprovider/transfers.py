"""This module contains meta steps for operations on transfers
using web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from typing import Any

import yaml

from tests.gui.meta_steps.oneprovider.browser_columns_configuration import (
    ADDITIONAL_TRANSFER_COLUMNS_USED_IN_TESTS,
    ALWAYS_VISIBLE_TRANSFER_COLUMNS,
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
    assert_transfer_column_value,
    assert_transfer_item_type,
    assert_transfer_status,
    click_link_in_data_distribution_panel,
    get_transfer_column_value,
    select_transfer_state_tab,
    wait_for_ongoing_tranfers_to_finish,
    wait_for_transfers_page_to_load,
    wait_for_waiting_transfer_to_start,
)
from tests.gui.steps.onezone.spaces import click_on_option_of_space_on_left_sidebar_menu
from tests.gui.type_definitions import TmpMemory, VisibleColumns
from tests.gui.utils import Modals, Popups
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    TransferState,
    parse_elements_sequence,
)
from tests.gui.utils.oneprovider.transfers import TransferItemType
from tests.gui.utils.text import transform
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees files"
        r" in (?P<transfer_state>ended|waiting) transfers:\n(?P<descriptions>(.|\s)*)"
    ),
    converters={"transfer_state": TransferState},
)
def assert_transfers(
    selenium: SeleniumDrivers,
    browser_id: str,
    descriptions: str,
    transfer_state: TransferState,
    visible_columns: VisibleColumns,
) -> None:
    parsed_desc = yaml.load(descriptions, yaml.Loader)
    select_transfer_state_tab(selenium, browser_id, transfer_state)
    select_columns_to_be_visible_in_transfers(
        selenium, browser_id, ADDITIONAL_TRANSFER_COLUMNS_USED_IN_TESTS, visible_columns
    )
    for name, description in parsed_desc.items():
        assert_transfer(
            name,
            description,
            transfer_state,
            selenium,
            browser_id,
        )


def assert_first_transfer(
    selenium: SeleniumDrivers,
    browser_id: str,
    yaml_config: Any,
    transfer_state: TransferState,
) -> None:
    transfer_id = 0
    assert_transfer(
        transfer_id,
        yaml_config,
        transfer_state,
        selenium,
        browser_id,
    )


def assert_transfer_column(
    selenium: SeleniumDrivers,
    browser_id: str,
    transfer_id: str | int,
    column_name: str,
    expected: Any,
) -> None:
    actual = get_transfer_column_value(
        selenium,
        browser_id,
        transfer_id,
        column_name,
    )
    assert_transfer_column_value(column_name, actual, expected)


def assert_transfer(
    transfer_id: str | int,
    desc: dict[str, Any],
    transfer_state: TransferState,
    selenium: SeleniumDrivers,
    browser_id: str,
) -> None:
    for key, configured_expected in desc.items():
        # to handle case with 'type & destination'
        act_key = transform(key.replace(" & ", "_and_"))

        if act_key in ALWAYS_VISIBLE_TRANSFER_COLUMNS:
            if act_key == "item_type":
                assert_transfer_item_type(
                    selenium,
                    browser_id,
                    transfer_id,
                    transfer_state,
                    TransferItemType(configured_expected),
                )
            elif act_key == "status":
                assert_transfer_status(
                    selenium,
                    browser_id,
                    transfer_id,
                    transfer_state,
                    configured_expected,
                )
        else:
            assert_transfer_column(
                selenium,
                browser_id,
                transfer_id,
                key,
                configured_expected,
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
