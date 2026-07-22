"""This module contains meta steps for common operations in Oneprovider
using web GUI
"""

import pytest
import yaml

from tests.gui.conftest import WAIT_BACKEND
from tests.gui.meta_steps.onezone.common import g_wt_visit_op
from tests.gui.steps.modals.details_modal import assert_tab_in_modal
from tests.gui.steps.modals.modal import (
    assert_error_modal_with_subtext_appeared,
    click_modal_button,
    write_name_into_text_field_in_modal,
    wt_wait_for_modal_to_appear,
)
from tests.gui.steps.oneprovider.browser import (
    assert_items_presence_in_browser,
    click_menu_for_elem_in_browser,
    click_option_in_data_row_menu_in_browser,
)
from tests.gui.steps.oneprovider.data_tab import (
    assert_provider_chunk_in_data_distribution_empty,
    assert_provider_chunk_in_data_distribution_filled,
    click_button_from_file_browser_menu_bar,
)
from tests.gui.steps.oneprovider.file_browser import confirm_create_new_directory
from tests.gui.steps.oneprovider.transfers import (
    assert_see_history_btn_shown,
    is_current_item_fully_on_provider,
    migrate_item,
    replicate_item,
)
from tests.gui.steps.oneprovider_common import (
    g_click_on_the_given_main_menu_tab,
    wt_click_on_the_given_main_menu_tab,
)
from tests.gui.steps.onezone.clusters import click_on_record_in_clusters_menu
from tests.gui.steps.onezone.spaces import click_on_option_in_the_sidebar
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    parse_elements_sequence,
)
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.utils import repeat_failed


@given(
    parsers.re(
        r'opened "(?P<tab_name>spaces)" tab in web GUI by '
        rf"(users? of )?(?P<browser_id_list>{ELEMENTS_SEQUENCE_PATTERN})"
    ),
    converters={
        "browser_id_list": parse_elements_sequence,
    },
)
def go_to_tab_in_provider(
    browser_id_list: list[str], tab_name: str, selenium: SeleniumDrivers
) -> None:
    g_click_on_the_given_main_menu_tab(selenium, browser_id_list, tab_name)


def navigate_to_tab_in_op_using_gui(
    selenium: SeleniumDrivers,
    user: str,
    provider: str,
    main_menu_tab: str,
    hosts: Hosts,
) -> None:
    title = selenium[user].title

    if "onezone" in title.lower():
        g_wt_visit_op(selenium, [user], [provider], hosts)

    wt_click_on_the_given_main_menu_tab(selenium, [user], main_menu_tab)


def assert_cannot_click_replicate_button(
    selenium: SeleniumDrivers, browser_id: str, provider: str, hosts: Hosts
) -> None:
    with pytest.raises(RuntimeError, match="Replicate button is not clickable"):
        replicate_item(selenium, browser_id, provider, hosts)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) "
        rf"(?P<result>replicates|fails to replicate) "
        rf"(?P<names>{ELEMENTS_SEQUENCE_PATTERN}) to "
        rf"(?:each provider: |provider )(?P<providers>{ELEMENTS_SEQUENCE_PATTERN})"
    ),
    converters={
        "names": parse_elements_sequence,
        "providers": parse_elements_sequence,
    },
)
def replicate_files_to_providers(
    selenium: SeleniumDrivers,
    browser_id: str,
    names: list[str],
    tmp_memory: TmpMemory,
    providers: list[str],
    hosts: Hosts,
    result: str,
) -> None:
    details_modal_str = "Details modal"
    for name in names:
        click_menu_for_elem_in_browser(browser_id, name, tmp_memory)
        click_option_in_data_row_menu_in_browser(
            selenium, browser_id, "Data distribution"
        )
        assert_tab_in_modal(selenium, browser_id, "Distribution", details_modal_str)

        for provider in providers:
            if is_current_item_fully_on_provider(
                selenium[browser_id], hosts[provider]["name"]
            ):
                assert_cannot_click_replicate_button(
                    selenium, browser_id, provider, hosts
                )
                continue
            replicate_item(selenium, browser_id, provider, hosts)
            if result == "fails to replicate":
                assert_error_modal_with_subtext_appeared(
                    selenium, browser_id, "Starting replication failed!"
                )
                click_modal_button(selenium, browser_id, "Close", "Error")

        click_modal_button(selenium, browser_id, "X", details_modal_str)


@wt(parsers.parse('user of {browser_id} waits for "{name}" file eviction to finish'))
def assert_eviction_done(
    selenium: SeleniumDrivers, browser_id: str, name: str, tmp_memory: TmpMemory
) -> None:
    option = "Data distribution"
    tab = "Distribution"
    details_modal = "Details modal"
    close_button = "X"

    click_menu_for_elem_in_browser(browser_id, name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option)
    assert_tab_in_modal(selenium, browser_id, tab, details_modal)
    assert_see_history_btn_shown(selenium, browser_id)
    click_modal_button(selenium, browser_id, close_button, details_modal)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees file chunks for file "
        r'"(?P<file_name>.*)" as follows:\n(?P<desc>(.|\s)*)'
    )
)
def wt_assert_file_chunks(
    selenium: SeleniumDrivers,
    browser_id: str,
    file_name: str,
    desc: str,
    tmp_memory: TmpMemory,
    hosts: Hosts,
) -> None:
    option = "Data distribution"
    details_modal = "Details modal"
    tab = "Distribution"
    close_button = "X"
    click_menu_for_elem_in_browser(browser_id, file_name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option)
    assert_tab_in_modal(selenium, browser_id, tab, details_modal)
    _assert_file_chunks(selenium, browser_id, hosts, desc)
    click_modal_button(selenium, browser_id, close_button, details_modal)


@repeat_failed(timeout=WAIT_BACKEND)
def _assert_file_chunks(
    selenium: SeleniumDrivers, browser_id: str, hosts: Hosts, desc: str
) -> None:
    parsed_desc = yaml.load(desc, yaml.Loader)
    for provider, chunks in parsed_desc.items():
        if chunks == "entirely empty":
            assert_provider_chunk_in_data_distribution_empty(
                selenium, browser_id, provider, hosts
            )
        elif chunks == "entirely filled":
            assert_provider_chunk_in_data_distribution_filled(
                selenium, browser_id, provider, hosts
            )


@wt(parsers.re(r'user of (?P<browser_id>.*) creates directory "(?P<name>.*)"'))
def create_directory(
    selenium: SeleniumDrivers, browser_id: str, name: str, tmp_memory: TmpMemory
) -> None:
    button = "New directory"
    modal_header = "Create new directory:"
    modal_name = "Create dir"
    option = "enter"
    click_button_from_file_browser_menu_bar(browser_id, button, tmp_memory)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_header, tmp_memory)
    write_name_into_text_field_in_modal(selenium, browser_id, name, modal_name)
    confirm_create_new_directory(selenium, browser_id, option)
    assert_items_presence_in_browser(selenium, browser_id, [name], tmp_memory)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) "
        r'(?P<result>migrates|fails to migrate) "(?P<name>.*)" from '
        r'provider "(?P<source>.*)" to provider "(?P<target>.*)"'
    )
)
def migrate_file_to_provider(
    selenium: SeleniumDrivers,
    browser_id: str,
    name: str,
    tmp_memory: TmpMemory,
    source: str,
    target: str,
    hosts: Hosts,
    result: str,
) -> None:
    option = "Data distribution"
    tab = "Distribution"
    details_modal = "Details modal"
    close_button = "X"

    click_menu_for_elem_in_browser(browser_id, name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option)
    assert_tab_in_modal(selenium, browser_id, tab, details_modal)
    migrate_item(selenium, browser_id, source, target, hosts)

    if result == "migrates":
        click_modal_button(selenium, browser_id, close_button, details_modal)


@wt(parsers.parse('user of {browser_id} opens "{provider_name}" clusters submenu'))
def open_record_of_clusters_submenu(
    selenium: SeleniumDrivers, browser_id: str, provider_name: str, hosts: Hosts
) -> None:
    sidebar = "Clusters"
    click_on_option_in_the_sidebar(selenium, browser_id, sidebar)
    click_on_record_in_clusters_menu(selenium, browser_id, provider_name, hosts)


@wt(
    parsers.parse(
        'user of {browser_id} opens "{modal_name}" modal on '
        '"{tab}" tab for "{filename}" file using context menu'
    )
)
def open_modal_on_tab(
    selenium: SeleniumDrivers,
    browser_id: str,
    filename: str,
    tmp_memory: TmpMemory,
    tab: str,
    modal_name: str,
) -> None:
    if tab == "QoS":
        option = "Quality of Service"
    elif tab == "Info":
        option = "Information"
    else:
        option = tab

    click_menu_for_elem_in_browser(browser_id, filename, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option)
    assert_tab_in_modal(selenium, browser_id, tab, modal_name)
