"""This module contains meta steps for common operations in Oneprovider
using web GUI
"""

import yaml
from tests.gui.conftest import WAIT_BACKEND
from tests.gui.meta_steps.onezone.common import g_wt_visit_op
from tests.gui.steps.modals.details_modal import assert_tab_in_modal
from tests.gui.steps.modals.modal import (
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
    migrate_item,
    replicate_item,
)
from tests.gui.steps.oneprovider_common import (
    g_click_on_the_given_main_menu_tab,
    wt_click_on_the_given_main_menu_tab,
)
from tests.gui.steps.onezone.clusters import click_on_record_in_clusters_menu
from tests.gui.steps.onezone.spaces import click_on_option_in_the_sidebar
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.utils import repeat_failed


@given(
    parsers.re(
        'opened "(?P<tab_name>spaces)" tab in web GUI by '
        "(users? of )?(?P<browser_id_list>.*)"
    )
)
def go_to_tab_in_provider(browser_id_list, tab_name, selenium):
    g_click_on_the_given_main_menu_tab(selenium, browser_id_list, tab_name)


def navigate_to_tab_in_op_using_gui(
    selenium, user, oz_page, provider, main_menu_tab, hosts, popups
):
    title = selenium[user].title

    if "onezone" in title.lower():
        g_wt_visit_op(selenium, oz_page, user, provider, hosts, popups)

    wt_click_on_the_given_main_menu_tab(selenium, user, main_menu_tab)


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) "
        '(?P<result>replicates|fails to replicate) "(?P<name>.*)"'
        ' to provider "(?P<provider>.*)"'
    )
)
def replicate_file_to_provider(
    selenium,
    browser_id,
    name,
    tmp_memory,
    provider,
    hosts,
    popups,
    modals,
    result,
):
    option = "Data distribution"
    tab = "Distribution"
    details_modal = "Details modal"
    close_button = "X"

    click_menu_for_elem_in_browser(browser_id, name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option, popups)
    assert_tab_in_modal(selenium, browser_id, tab, modals, details_modal)

    replicate_item(selenium, browser_id, provider, hosts, popups)

    if result == "replicates":
        click_modal_button(selenium, browser_id, close_button, details_modal, modals)


@wt(parsers.parse('user of {browser_id} waits for "{name}" file eviction to finish'))
def assert_eviction_done(selenium, browser_id, name, tmp_memory, popups, modals):
    option = "Data distribution"
    tab = "Distribution"
    details_modal = "Details modal"
    close_button = "X"

    click_menu_for_elem_in_browser(browser_id, name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option, popups)
    assert_tab_in_modal(selenium, browser_id, tab, modals, details_modal)
    assert_see_history_btn_shown(selenium, browser_id)
    click_modal_button(selenium, browser_id, close_button, details_modal, modals)


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) sees file chunks for file "
        r'"(?P<file_name>.*)" as follows:\n(?P<desc>(.|\s)*)'
    )
)
def wt_assert_file_chunks(
    selenium,
    browser_id,
    file_name,
    desc,
    tmp_memory,
    hosts,
    modals,
    popups,
):
    option = "Data distribution"
    details_modal = "Details modal"
    tab = "Distribution"
    close_button = "X"
    click_menu_for_elem_in_browser(browser_id, file_name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option, popups)
    assert_tab_in_modal(selenium, browser_id, tab, modals, details_modal)
    _assert_file_chunks(selenium, browser_id, hosts, desc, modals)
    click_modal_button(selenium, browser_id, close_button, details_modal, modals)


@repeat_failed(timeout=WAIT_BACKEND)
def _assert_file_chunks(selenium, browser_id, hosts, desc, modals):
    desc = yaml.load(desc, yaml.Loader)
    for provider, chunks in desc.items():
        if chunks == "entirely empty":
            assert_provider_chunk_in_data_distribution_empty(
                selenium, browser_id, provider, modals, hosts
            )
        elif chunks == "entirely filled":
            assert_provider_chunk_in_data_distribution_filled(
                selenium, browser_id, provider, modals, hosts
            )


@wt(parsers.re('user of (?P<browser_id>.*) creates directory "(?P<name>.*)"'))
def create_directory(selenium, browser_id, name, tmp_memory, modals):
    button = "New directory"
    modal_header = "Create new directory:"
    modal_name = "Create dir"
    option = "enter"
    click_button_from_file_browser_menu_bar(browser_id, button, tmp_memory)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_header, tmp_memory)
    write_name_into_text_field_in_modal(selenium, browser_id, name, modal_name, modals)
    confirm_create_new_directory(selenium, browser_id, option, modals)
    assert_items_presence_in_browser(selenium, browser_id, name, tmp_memory)


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) "
        '(?P<result>migrates|fails to migrate) "(?P<name>.*)" from '
        'provider "(?P<source>.*)" to provider "(?P<target>.*)"'
    )
)
def migrate_file_to_provider(
    selenium,
    browser_id,
    name,
    tmp_memory,
    source,
    target,
    hosts,
    popups,
    modals,
    result,
):
    option = "Data distribution"
    tab = "Distribution"
    details_modal = "Details modal"
    close_button = "X"

    click_menu_for_elem_in_browser(browser_id, name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option, popups)
    assert_tab_in_modal(selenium, browser_id, tab, modals, details_modal)
    migrate_item(selenium, browser_id, source, target, hosts, popups)

    if result == "migrates":
        click_modal_button(selenium, browser_id, close_button, details_modal, modals)


@wt(parsers.parse('user of {browser_id} opens "{provider_name}" clusters submenu'))
def open_record_of_clusters_submenu(
    selenium, browser_id, provider_name, oz_page, hosts
):
    sidebar = "Clusters"
    click_on_option_in_the_sidebar(selenium, browser_id, sidebar, oz_page)
    click_on_record_in_clusters_menu(
        selenium, browser_id, oz_page, provider_name, hosts
    )


@wt(
    parsers.parse(
        'user of {browser_id} opens "{modal_name}" modal on '
        '"{tab}" tab for "{filename}" file using context menu'
    )
)
def open_modal_on_tab(
    selenium, browser_id, filename, popups, tmp_memory, tab, modals, modal_name
):
    option = "Quality of Service" if tab == "QoS" else tab
    click_menu_for_elem_in_browser(browser_id, filename, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option, popups)
    assert_tab_in_modal(selenium, browser_id, tab, modals, modal_name)
