"""Steps for tests of Oneprovider transfers
"""

__author__ = "Michal Stanisz, Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import time

import yaml

from selenium.common.exceptions import StaleElementReferenceException

from tests.gui.steps.common.miscellaneous import (
    switch_to_iframe, click_option_in_popup_labeled_menu)
from tests.gui.utils.common.modals import Modals as modals
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.utils import repeat_failed
from tests.utils.bdd_utils import wt, parsers
from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND


def _assert_transfer(transfer, item_type, desc, sufix, hosts):
    assert getattr(transfer, 'is_{}'.format(item_type))(), \
        'Transferred item is not {} in {}'.format(item_type, sufix)

    desc = yaml.load(desc)
    for key, val in desc.items():
        if key == 'destination':
            val = hosts[val]['name']
        transfer_val = getattr(transfer, key.replace(' ', '_'))
        try:
            assert transfer_val == str(val), (f'Transfer {key} is '
                                              f'{transfer_val} instead of '
                                              f'{val} in {sufix}')
        except AssertionError as e:
            if '<' in val:
                symbol = val.split(' ')[0]
                value = float(val.split(' ')[1])
                unit = val.split(' ')[2]
                val = value if unit == 'MiB' else value * 1024
                transfer_val = float(transfer_val.split(' ')[0])
                if symbol == '<=':
                    assert transfer_val <= val, (f'{key}: {transfer_val} MiB is'
                                                 f' greater than {val} MiB')
                else:
                    assert transfer_val < val, (f'{key}: {transfer_val} MiB is'
                                                f' no less than {val} MiB')
            else:
                raise e


@wt(parsers.re('user of (?P<browser_id>.*) sees (?P<item_type>file|directory)'
               ' in ended transfers:\n(?P<desc>(.|\s)*)'))
@repeat_failed(interval=0.5, timeout=240)
def assert_ended_transfer(selenium, browser_id, item_type, desc, hosts,
                          op_container):
    transfer = op_container(selenium[browser_id]).transfers.ended[0]
    _assert_transfer(transfer, item_type, desc, 'ended', hosts)


@wt(parsers.re('user of (?P<browser_id>.*) sees (?P<item_type>file|directory)'
               ' in waiting transfers:\n(?P<desc>(.|\s)*)'))
@repeat_failed(interval=0.5, timeout=40)
def assert_waiting_transfer(selenium, browser_id, item_type, desc, hosts,
                            op_container):
    transfer = op_container(selenium[browser_id]).transfers.waiting[0]
    _assert_transfer(transfer, item_type, desc, 'waiting', hosts)


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>cancels|reruns) transfer '
               'in transfers tab for (?P<state>certain file)'))
@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>cancels|reruns) transfer '
               'in (?P<state>waiting|ended) transfers'))
@repeat_failed(timeout=WAIT_BACKEND)
def cancel_or_rerun_transfer(selenium, browser_id, op_container, popups,
                             option, state):
    transfers = op_container(selenium[browser_id]).transfers
    if state == 'waiting':
        try:
            getattr(transfers, state)[0].menu_button()
        except RuntimeError:
            transfers.ongoing[0].menu_button()
    else:
        getattr(transfers, transform(state))[0].menu_button()

    option = 'Cancel transfer' if option == 'cancels' else 'Rerun transfer'
    click_option_in_popup_labeled_menu(selenium, browser_id, option, popups)


@wt(parsers.re('user of (?P<browser_id>.*) waits for all transfers to start'))
@repeat_failed(interval=1, timeout=420,
               exceptions=(AssertionError, StaleElementReferenceException))
def wait_for_waiting_transfer_to_start(selenium, browser_id, op_container):
    assert len(op_container(selenium[browser_id]).transfers.waiting) == 0, \
        'Waiting transfers did not start'


@wt(parsers.re('user of (?P<browser_id>.*) waits for all transfers to finish'))
@repeat_failed(interval=1, timeout=240,
               exceptions=(AssertionError, StaleElementReferenceException))
def wait_for_ongoing_tranfers_to_finish(selenium, browser_id, op_container):
    assert len(op_container(selenium[browser_id]).transfers.ongoing) == 0, \
        'Ongoing transfers did not finish'


@wt(parsers.re('user of (?P<browser_id>.*) expands first transfer record'))
def expand_transfer_record(selenium, browser_id, op_container):
    op_container(selenium[browser_id]).transfers.ended[0].expand()


@wt(parsers.re('user of (?P<browser_id>.*) sees that there is non-zero '
               'throughput in transfer chart'))
def assert_non_zero_transfer_speed(selenium, browser_id, op_container):
    chart = op_container(selenium[browser_id]).transfers.ended[0].get_chart()
    assert chart.get_speed() != '0', 'Transfer throughput is 0'


@repeat_failed(timeout=WAIT_BACKEND)
def _expand_dropdown_in_migrate_record(driver, popups):
    data_distribution_modal = modals(driver).details_modal.data_distribution
    data_distribution_modal.migrate.expand_dropdown()
    assert len(popups(driver).migrate_dropdown.providers_list) > 0


def check_provider_in_migrate_dropdown(driver, provider_name):
    data_distribution_modal = modals(driver).details_modal.data_distribution
    return provider_name == data_distribution_modal.migrate.target_provider


@wt(parsers.re('user of (?P<browser_id>.*) migrates selected item from '
               'provider "(?P<source>.*)" to provider "(?P<target>.*)"'))
def migrate_item(selenium, browser_id, source, target, hosts, popups):
    menu_option = 'Migrate...'

    driver = selenium[browser_id]
    source_name = hosts[source]['name']
    target_name = hosts[target]['name']

    data_distribution_modal = modals(driver).details_modal.data_distribution
    data_distribution_modal.providers[source_name].menu_button()
    popups(driver).data_distribution_popup.menu[menu_option]()

    if not check_provider_in_migrate_dropdown(driver, target_name):
        _expand_dropdown_in_migrate_record(driver, popups)
        popups(driver).migrate_dropdown.providers_list[target_name].click()

    data_distribution_modal.migrate.migrate_button()


@wt(parsers.re('user of (?P<browser_id>.*) replicates selected item'
               ' to provider "(?P<provider>.*)"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def replicate_item(selenium, browser_id, provider, hosts, popups):
    menu_option = 'Replicate here'
    driver = selenium[browser_id]
    provider_name = hosts[provider]['name']
    modals(driver).details_modal.data_distribution.providers[
        provider_name].menu_button()
    popups(driver).data_distribution_popup.menu[menu_option]()


@wt(parsers.parse('user of {browser_id} clicks on menu button for '
                  '"{provider}" provider in "Data distribution" panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_menu_button_in_data_distribution_panel(selenium, browser_id,
                                                 provider, hosts):
    driver = selenium[browser_id]
    provider_name = hosts[provider]['name']
    modals(driver).details_modal.data_distribution.providers[
        provider_name].menu_button()


@wt(parsers.parse('user of {browser_id} cannot click "{option}" option in data'
                  ' row menu for "{provider}" provider in "Data distribution" '
                  'panel'))
def fail_to_click_option_in_data_distribution_popup(browser_id, option,
                                                    selenium, popups):
    driver = selenium[browser_id]
    try:
        popups(driver).data_distribution_popup.menu[option]()
        raise Exception('User can click on "{option}" option in in data row '
                        'menu in "Data distribution" panel')
    except RuntimeError:
        pass


@wt(parsers.re('user of (?P<browser_id>.*) evicts selected item'
               ' from provider "(?P<provider>.*)"'))
def evict_selected_item(selenium, browser_id, provider, hosts, popups):
    menu_option = 'Evict'
    driver = selenium[browser_id]

    provider_name = hosts[provider]['name']
    (modals(driver)
     .data_distribution
     .providers[provider_name]
     .menu_button())
    popups(driver).menu_popup_with_text.menu[menu_option]()


@wt(parsers.re('user of {browser_id} sees "see history" button in data '
               'distribution modal'))
@repeat_failed(interval=1, timeout=90, exceptions=RuntimeError)
def assert_see_history_btn_shown(selenium, browser_id):
    driver = selenium[browser_id]
    assert hasattr(modals(driver).details_modal.data_distribution,
                   'see_history_btn'), (
        'Button "see history" not found in data distribution modal')


@wt(parsers.re('user of (?P<browser_id>.*) selects "(?P<space>.*)" space '
               'in transfers tab'))
def change_transfer_space(selenium, browser_id, space, op_container):
    op_container(selenium[browser_id]).transfers.spaces[space].select()


@wt(parsers.re('user of (?P<browser_id>.*) waits for Transfers page to load'))
@repeat_failed(timeout=WAIT_BACKEND)
def wait_for_transfers_page_to_load(selenium, browser_id, op_container):
    switch_to_iframe(selenium, browser_id)
    op_container(selenium[browser_id]).transfers.ongoing_map_header


@wt(parsers.re('user of (?P<browser_id>.*) does not see "(?P<options>Replicate '
               'here|Migrate...|Evict)" options when clicking on provider "('
               '?P<provider>.*)" menu button'))
def assert_option_in_provider_popup_menu(selenium, browser_id, provider, hosts,
                                         popups, options):

    driver = selenium[browser_id]

    provider_name = hosts[provider]['name']
    modals(driver).details_modal.data_distribution.providers[
        provider_name].menu_button()

    menu = popups(driver).menu_popup_with_text.menu
    for element in parse_seq(options):
        assert element not in menu, f'{element} should not be in selection menu'
