"""This module contains meta steps for common operations in Oneprovider
using web GUI
"""

import yaml

from tests.gui.meta_steps.onezone.common import g_wt_visit_op
from tests.gui.steps.oneprovider.transfers import (
    replicate_item, migrate_item, assert_see_history_btn_shown)
from tests.gui.steps.oneprovider_common import (
    g_click_on_the_given_main_menu_tab,
    wt_click_on_the_given_main_menu_tab)
from tests.gui.steps.oneprovider.data_tab import (
    assert_browser_in_tab_in_op,
    click_tooltip_from_toolbar_in_data_tab_in_op,
    assert_provider_chunk_in_data_distribution_empty,
    assert_provider_chunk_in_data_distribution_filled,
    assert_nonempty_file_browser_in_files_tab_in_op,
    click_button_from_file_browser_menu_bar)
from tests.gui.steps.oneprovider.file_browser import (
    select_files_from_file_list_using_ctrl,
    deselect_items_from_file_browser,
    confirm_create_new_directory)
from tests.gui.steps.oneprovider.browser import (
    assert_items_presence_in_browser,
    click_option_in_data_row_menu_in_browser,
    click_menu_for_elem_in_browser)
from tests.gui.steps.modal import (wt_wait_for_modal_to_appear,
                                   wt_click_on_confirmation_btn_in_modal,
                                   wt_wait_for_modal_to_disappear,
                                   write_name_into_text_field_in_modal)
from tests.gui.steps.onezone.clusters import click_on_record_in_clusters_menu
from tests.gui.steps.onezone.spaces import click_on_option_in_the_sidebar
from tests.utils.bdd_utils import wt, given, parsers
from tests.utils.utils import repeat_failed
from tests.gui.conftest import WAIT_BACKEND


@given(parsers.re('opened "(?P<tab_name>spaces)" tab in web GUI by '
                  '(users? of )?(?P<browser_id_list>.*)'))
def go_to_tab_in_provider(browser_id_list, tab_name, selenium):
    g_click_on_the_given_main_menu_tab(selenium, browser_id_list, tab_name)


def navigate_to_tab_in_op_using_gui(selenium, user, oz_page, provider,
                                    main_menu_tab, hosts, modals):
    title = selenium[user].title

    if 'onezone' in title.lower():
        g_wt_visit_op(selenium, oz_page, user, provider, hosts,
                      modals)

    wt_click_on_the_given_main_menu_tab(selenium, user, main_menu_tab)


@wt(parsers.re('user of (?P<browser_id>.*) replicates "(?P<name>.*)" to '
               'provider "(?P<provider>.*)"'))
def replicate_file_to_provider(selenium, browser_id, name, tmp_memory,
                               provider, op_container, hosts, modals, popups):
    option = 'Data distribution'
    modal_name = 'Data distribution'

    click_menu_for_elem_in_browser(browser_id, name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)

    replicate_item(selenium, browser_id, provider, hosts, popups)

    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, 'Close',
                                          tmp_memory)


@wt(parsers.parse('user of {browser_id} waits for "{name}" file eviction '
                  'to finish'))
def assert_eviction_done(selenium, browser_id, name, tmp_memory, modals):
    option = 'Data distribution'
    modal_name = 'Data distribution'
    close_option = 'Close'

    click_menu_for_elem_in_browser(browser_id, name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)

    assert_see_history_btn_shown(selenium, browser_id)

    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, close_option,
                                          tmp_memory)


@wt(parsers.re('user of (?P<browser_id>.*) sees file chunks for file '
               r'"(?P<file_name>.*)" as follows:\n(?P<desc>(.|\s)*)'))
def wt_assert_file_chunks(selenium, browser_id, file_name, desc, tmp_memory,
                          op_container, hosts, modals):
    option = 'Data distribution'
    modal_name = 'Data distribution'

    click_menu_for_elem_in_browser(browser_id, file_name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    _assert_file_chunks(selenium, browser_id, hosts, desc, modals)
    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, 'Close',
                                          tmp_memory)


@repeat_failed(timeout=WAIT_BACKEND)
def _assert_file_chunks(selenium, browser_id, hosts, desc, modals):
    desc = yaml.load(desc)
    for provider, chunks in desc.items():
        if chunks == 'entirely empty':
            assert_provider_chunk_in_data_distribution_empty(selenium,
                                                             browser_id,
                                                             provider, modals,
                                                             hosts)
        elif chunks == 'entirely filled':
            assert_provider_chunk_in_data_distribution_filled(selenium,
                                                              browser_id,
                                                              provider, modals,
                                                              hosts)


@wt(parsers.re('user of (?P<browser_id>.*) creates directory "(?P<name>.*)"'))
def create_directory(selenium, browser_id, name, tmp_memory,
                     op_container, modals):
    button = 'New directory'
    modal_header = 'Create new directory:'
    modal_name = 'Create dir'
    option = 'enter'

    click_button_from_file_browser_menu_bar(selenium, browser_id,
                                            button, op_container)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_header, tmp_memory)
    write_name_into_text_field_in_modal(selenium, browser_id, name,
                                        modal_name, modals)
    confirm_create_new_directory(selenium, browser_id, option, modals)
    assert_items_presence_in_browser(selenium, browser_id, name, tmp_memory)


@wt(parsers.re('user of (?P<browser_id>.*) migrates "(?P<name>.*)" from '
               'provider "(?P<source>.*)" to provider "(?P<target>.*)"'))
def migrate_file_to_provider(selenium, browser_id, name, tmp_memory, source,
                             target, op_container, hosts, modals, popups):
    option = 'Data distribution'
    modal_name = 'Data distribution'

    click_menu_for_elem_in_browser(browser_id, name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    migrate_item(selenium, browser_id, source, target, hosts, popups)
    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, 'Close',
                                          tmp_memory)


@wt(parsers.parse('user of {browser_id} opens "{provider_name}" clusters '
                  'submenu'))
def open_record_of_clusters_submenu(selenium, browser_id, provider_name,
                                    oz_page, hosts):
    sidebar = 'Clusters'
    click_on_option_in_the_sidebar(selenium, browser_id, sidebar, oz_page)
    click_on_record_in_clusters_menu(selenium, browser_id, oz_page,
                                     provider_name, hosts)

