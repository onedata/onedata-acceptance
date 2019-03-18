"""Steps for tests of Oneprovider transfers
"""

__author__ = "Michal Stanisz, Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import yaml

from selenium.common.exceptions import StaleElementReferenceException
from pytest_bdd import parsers

from tests.gui.utils.common.modals import Modals as modals
from tests.utils.utils import repeat_failed
from tests.utils.acceptance_utils import wt


def _assert_transfer(transfer, item_type, desc, sufix, hosts):
    assert getattr(transfer, 'is_{}'.format(item_type))(), \
        'Transferred item is not {} in {}'.format(item_type, sufix)

    desc = yaml.load(desc)
    for key, val in desc.items():
        if key == 'destination':
            val = hosts[val]['name']
        transfer_val = getattr(transfer, key.replace(' ', '_'))
        assert transfer_val == str(val), \
            'Transfer {} is {} instead of {} in {}'.format(key, transfer_val,
                                                           val, sufix)


@wt(parsers.re('user of (?P<browser_id>.*) sees (?P<item_type>file|directory)'
               ' in ongoing transfers:\n(?P<desc>(.|\s)*)'))
@repeat_failed(interval=0.5)
def assert_ongoing_transfer(selenium, browser_id, item_type, desc, hosts,
                            op_page):
    transfer = op_page(selenium[browser_id]).transfers.ongoing[0]
    _assert_transfer(transfer, item_type, desc, 'ongoing', hosts)


@wt(parsers.re('user of (?P<browser_id>.*) sees (?P<item_type>file|directory)'
               ' in ended transfers:\n(?P<desc>(.|\s)*)'))
@repeat_failed(interval=0.5, timeout=90)
def assert_ended_transfer(selenium, browser_id, item_type, desc, hosts,
                          op_page):
    transfer = op_page(selenium[browser_id]).transfers.ended[0]
    _assert_transfer(transfer, item_type, desc, 'ended', hosts)


@wt(parsers.re('user of (?P<browser_id>.*) sees (?P<item_type>file|directory)'
               ' in waiting transfers:\n(?P<desc>(.|\s)*)'))
@repeat_failed(interval=0.5, timeout=40)
def assert_waiting_transfer(selenium, browser_id, item_type, desc, hosts,
                              op_page):
    transfer = op_page(selenium[browser_id]).transfers.waiting[0]
    _assert_transfer(transfer, item_type, desc, 'waiting', hosts)


@wt(parsers.re('user of (?P<browser_id>.*) waits for all transfers to start'))
@repeat_failed(interval=1, timeout=90,
               exceptions=(AssertionError, StaleElementReferenceException))
def wait_for_waiting_tranfers_to_start(selenium, browser_id, op_page):
    assert len(op_page(selenium[browser_id]).transfers.waiting) == 0, \
        'Waiting transfers did not start'


@wt(parsers.re('user of (?P<browser_id>.*) waits for all transfers to finish'))
@repeat_failed(interval=1, timeout=90,
               exceptions=(AssertionError, StaleElementReferenceException))
def wait_for_ongoing_tranfers_to_finish(selenium, browser_id, op_page):
    assert len(op_page(selenium[browser_id]).transfers.ongoing) == 0, \
        'Ongoing transfers did not finish'


@wt(parsers.re('user of (?P<browser_id>.*) expands first transfer record'))
def expand_transfer_record(selenium, browser_id, op_page):
    op_page(selenium[browser_id]).transfers.ended[0].expand()


@wt(parsers.re('user of (?P<browser_id>.*) sees that there is non-zero '
               'throughput in transfer chart'))
def assert_non_zero_transfer_speed(selenium, browser_id, op_page):
    chart = op_page(selenium[browser_id]).transfers.ended[0].get_chart()
    assert chart.get_speed() != '0', 'Transfer throughput is 0'


@wt(parsers.re('user of (?P<browser_id>.*) migrates selected item from '
               'provider "(?P<source>.*)" to provider "(?P<target>.*)"'))
def migrate_item(selenium, browser_id, source, target, hosts):
    modal = modals(selenium[browser_id])
    source_name = hosts[source]['name']
    target_name = hosts[target]['name']
    modal.data_distribution.providers[source_name].migrate()
    modal.data_distribution.migrate[target_name].select()


@wt(parsers.re('user of (?P<browser_id>.*) replicates selected item'
               ' to provider "(?P<provider>.*)"'))
def replicate_item(selenium, browser_id, provider, hosts):
    provider_name = hosts[provider]['name']
    (modals(selenium[browser_id])
     .data_distribution
     .providers[provider_name]
     .replicate())


@wt(parsers.re('user of (?P<browser_id>.*) sees that item is never '
               'synchronized in provider "(?P<provider>.*)"'))
def assert_item_never_synchronized(selenium, browser_id, provider, hosts):
    provider_name = hosts[provider]['name']
    if (modals(selenium[browser_id])
            .data_distribution
            .providers[provider_name]
            .distribution
            .is_never_synchronized()):
        return ''
    else:
        return 'Item is synchronized in provider {}'.format(provider_name)


@wt(parsers.re('user of (?P<browser_id>.*) selects "(?P<space>.*)" space '
               'in transfers tab'))
def change_transfer_space(selenium, browser_id, space, op_page):
    op_page(selenium[browser_id]).transfers.spaces[space].select()
