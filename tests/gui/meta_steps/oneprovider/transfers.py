"""This module contains meta steps for operations on transfers
using web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.modal import (wt_wait_for_modal_to_appear,
                                   wt_click_on_confirmation_btn_in_modal)
from tests.gui.steps.oneprovider.data_tab import (
    click_choose_other_oneprovider_on_file_browser,
    choose_provider_in_file_browser, check_current_provider_in_space)
from tests.gui.steps.oneprovider.browser import (
    click_option_in_data_row_menu_in_browser,
    click_menu_for_elem_in_browser)
from tests.gui.steps.oneprovider.transfers import (
    wait_for_transfers_page_to_load)
from tests.gui.steps.onezone.spaces import (
    click_on_option_of_space_on_left_sidebar_menu)
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@wt(parsers.re('user of (?P<browser_id>.*) opens (?P<provider>.*) '
               'Oneprovider transfers for "(?P<space>.*)" space'))
@repeat_failed(timeout=WAIT_FRONTEND)
def open_transfers_page(selenium, browser_id, provider, space, hosts, oz_page,
                        op_container):
    option = 'Transfers'
    provider_name = hosts[provider]['name']

    click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                  space, option, oz_page)

    if provider_name != check_current_provider_in_space(selenium, browser_id,
                                                        oz_page):
        click_choose_other_oneprovider_on_file_browser(selenium, browser_id,
                                                       oz_page)
        choose_provider_in_file_browser(selenium, browser_id, provider,
                                        hosts, oz_page)

    wait_for_transfers_page_to_load(selenium, browser_id, op_container)


@wt(parsers.parse('user of {browser_id} evicts file "{file_name}" from provider'
                  ' {provider}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def evict_file(selenium, browser_id, provider, popups, file_name, tmp_memory,
               modals, hosts):
    option = 'Data distribution'
    modal_name = 'Data distribution'
    menu_option = 'Evict'
    driver = selenium[browser_id]
    provider_name = hosts[provider]['name']
    confirm_button = 'Close'

    click_menu_for_elem_in_browser(browser_id, file_name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)

    data_distribution_modal = modals(driver).data_distribution
    data_distribution_modal.providers[provider_name].menu_button()
    popups(driver).data_distribution_popup.menu[menu_option]()
    wt_click_on_confirmation_btn_in_modal(selenium, browser_id, confirm_button,
                                          tmp_memory)
