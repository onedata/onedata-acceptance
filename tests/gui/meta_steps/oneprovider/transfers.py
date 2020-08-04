"""This module contains meta steps for operations on transfers
using web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import parsers

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.oneprovider.data_tab import (
    click_choose_other_oneprovider_on_file_browser,
    choose_provider_in_file_browser, check_current_provider_in_space)
from tests.gui.steps.oneprovider.transfers import (
    wait_for_transfers_page_to_load)
from tests.gui.steps.onezone.spaces import (
    click_on_option_of_space_on_left_sidebar_menu)
from tests.utils.bdd_utils import wt
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
