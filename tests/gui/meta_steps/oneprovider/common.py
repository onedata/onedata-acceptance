"""This module contains meta steps for common operations in Oneprovider
using web GUI
"""

import yaml

from tests.gui.meta_steps.onezone.common import g_wt_visit_op
from tests.gui.steps.oneprovider.transfers import (
    replicate_item,
    assert_item_never_synchronized,
    migrate_item)
from tests.gui.steps.oneprovider_common import (
    g_click_on_the_given_main_menu_tab,
    wt_click_on_the_given_main_menu_tab)
from tests.gui.steps.oneprovider.data_tab import (
    assert_file_browser_in_data_tab_in_op,
    click_tooltip_from_toolbar_in_data_tab_in_op,
    assert_provider_chunk_in_data_distribution_empty,
    assert_provider_chunk_in_data_distribution_filled,
    assert_nonempty_file_browser_in_data_tab_in_op,
    click_button_from_file_browser_menu_bar)
from tests.gui.steps.oneprovider.file_browser import (
    select_files_from_file_list_using_ctrl,
    assert_items_presence_in_file_browser,
    deselect_items_from_file_browser,
    confirm_create_new_directory, click_menu_for_elem_in_file_browser,
    click_option_in_data_row_menu_in_file_browser)
from tests.gui.steps.modal import (wt_wait_for_modal_to_appear,
                                   wt_click_on_confirmation_btn_in_modal,
                                   wt_wait_for_modal_to_disappear,
                                   write_name_into_text_field_in_modal)
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
def meta_replicate_item(selenium, browser_id, name, tmp_memory,
                        provider, op_page, hosts, modals, popups):
    option = 'Data distribution'
    modal_name = 'Data distribution'

    click_menu_for_elem_in_file_browser(browser_id, name, tmp_memory)
    click_option_in_data_row_menu_in_file_browser(selenium, browser_id,
                                                  option, modals)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)

    replicate_item(selenium, browser_id, provider, hosts, popups)

    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, 'Close',
                                          tmp_memory)


@wt(parsers.re('user of (?P<browser_id>.*) sees file chunks for file '
               '"(?P<file_name>.*)" as follows:\n(?P<desc>(.|\s)*)'))
def wt_assert_file_chunks(selenium, browser_id, file_name, desc, tmp_memory,
                          op_page, hosts, modals):
    option = 'Data distribution'
    modal_name = 'Data distribution'

    click_menu_for_elem_in_file_browser(browser_id, file_name, tmp_memory)
    click_option_in_data_row_menu_in_file_browser(selenium, browser_id,
                                                  option, modals)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    _assert_file_chunks(selenium, browser_id, hosts, desc, modals)
    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, 'Close',
                                          tmp_memory)


@repeat_failed(timeout=WAIT_BACKEND)
def _assert_file_chunks(selenium, browser_id, hosts, desc, modals):
    desc = yaml.load(desc)
    for provider, chunks in desc.items():
        if chunks == 'never synchronized':
            assert_item_never_synchronized(selenium, browser_id, provider,
                                           hosts)
        elif chunks == 'entirely empty':
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
def create_directory(selenium, browser_id, name, tmp_memory, op_page, modals):
    button = 'New directory'
    modal_header = 'Create new directory:'
    modal_name = 'Create dir'
    option = 'enter'

    click_button_from_file_browser_menu_bar(selenium, browser_id,
                                            button, op_page)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_header, tmp_memory)
    write_name_into_text_field_in_modal(selenium, browser_id, name,
                                        modal_name, modals)
    confirm_create_new_directory(selenium, browser_id, option, modals)
    assert_items_presence_in_file_browser(browser_id, name, tmp_memory)


@wt(parsers.re('user of (?P<browser_id>.*) migrates "(?P<name>.*)" from '
               'provider "(?P<source>.*)" to provider "(?P<target>.*)"'))
def meta_migrate_item(selenium, browser_id, name, tmp_memory, source,
                      target, op_page, hosts, modals, popups):
    option = 'Data distribution'
    modal_name = 'Data distribution'

    click_menu_for_elem_in_file_browser(browser_id, name, tmp_memory)
    click_option_in_data_row_menu_in_file_browser(selenium, browser_id,
                                                  option, modals)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    migrate_item(selenium, browser_id, source, target, hosts, popups)
    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, 'Close',
                                          tmp_memory)

