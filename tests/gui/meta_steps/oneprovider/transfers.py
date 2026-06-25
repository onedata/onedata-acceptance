"""This module contains meta steps for operations on transfers
using web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.meta_steps.oneprovider.common import replicate_files_to_provider
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
    wait_for_ongoing_tranfers_to_finish,
    wait_for_transfers_page_to_load,
    wait_for_waiting_transfer_to_start,
)
from tests.gui.steps.onezone.spaces import click_on_option_of_space_on_left_sidebar_menu
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils import Modals, Popups
from tests.gui.utils.generic import transform
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) opens (?P<provider>.*) "
        'Oneprovider transfers for "(?P<space>.*)" space'
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
        "user of (?P<browser_id>.*) opens transfer page using "
        '"(?P<link>.*)" link on "Distribution" tab for '
        '"(?P<file>.*)" file'
    )
)
def open_transfer_page_by_clicking_on_link(
    browser_id: str,
    file: str,
    tmp_memory: TmpMemory,
    selenium: SeleniumDrivers,
    link: str,
) -> None:
    option = "Data distribution"
    click_menu_for_elem_in_browser(browser_id, file, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option)
    getattr(
        Modals(selenium[browser_id]).details_modal.data_distribution,
        transform(link),
    )()
    wait_for_transfers_page_to_load(selenium, browser_id)


@wt(
    parsers.parse(
        'user of {browser_id} evicts file "{file_name}" from provider {provider}'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
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


def wait_for_all_transfers_to_start_and_finish(
    selenium: SeleniumDrivers, browser_id: str, provider: str, space: str, hosts: Hosts
) -> None:
    open_transfers_page(selenium, browser_id, provider, space, hosts)
    wait_for_waiting_transfer_to_start(selenium, browser_id)
    wait_for_ongoing_tranfers_to_finish(selenium, browser_id)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+) "
        r'replicates (?P<names>.*) in space "(?P<space>.+)"'
        r' to provider "(?P<provider>.+)"'
        r" and waits for all transfers to complete"
    )
)
def replicate_and_wait_to_complete(
    selenium: SeleniumDrivers,
    browser_id: str,
    names: str,
    space: str,
    provider: str,
    tmp_memory: TmpMemory,
    hosts: Hosts,
) -> None:
    replicate_files_to_provider(
        selenium, browser_id, names, tmp_memory, provider, hosts, "replicates"
    )
    wait_for_all_transfers_to_start_and_finish(
        selenium, browser_id, provider, space, hosts
    )
