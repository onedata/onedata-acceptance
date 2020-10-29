"""This module contains gherkin steps to run acceptance tests featuring
ceph management in onepanel web GUI.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} sees that Ceph cluster works '
                  'correctly'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_ceph_correct_work(selenium, browser_id, onepanel):
    _ = onepanel(selenium[browser_id]).content.ceph.status_page.success_alert


@wt(parsers.parse('user of {browser_id} sees that OSDS usage is {usage}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_osds_usage(selenium, browser_id, onepanel, usage):
    given = onepanel(selenium[
                         browser_id]).content.ceph.status_page.osds_usage
    assert given == usage, f'Expected {usage} but got {given} osds usage'


@wt(parsers.parse('user of {browser_id} sees that OSDS limit is {limit}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_osds_limit(selenium, browser_id, onepanel, limit):
    given = onepanel(selenium[
                         browser_id]).content.ceph.status_page.osds_limit
    assert given == limit, f'Expected {limit} but got {given} osds limit'


@wt(parsers.parse('user of {browser_id} clicks on {tab_name} tab on Ceph '
                  'page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_ceph_tab(selenium, browser_id, onepanel, tab_name):
    tab_name = tab_name.lower() + '_tab'
    getattr(onepanel(selenium[browser_id]).content.ceph, tab_name)()


@wt(parsers.parse('user of {browser_id} sees that cluster name is '
                  '"{name}" on Ceph page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_ceph_cluster_name_on_ceph_page(selenium, browser_id, name, onepanel):
    driver = selenium[browser_id]
    given = onepanel(driver).content.ceph.configuration_page.cluster_name
    assert given == name, f'Expected {name} as Ceph cluster name, got {given}'


@wt(parsers.parse('user of {browser_id} opens Ceph nodes list on Ceph page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def open_ceph_nodes_on_ceph_page(selenium, browser_id, onepanel):
    driver = selenium[browser_id]
    onepanel(driver).content.ceph.configuration_page.node.click()


@wt(parsers.parse('user of {browser_id} sees that Manager & Monitor '
                  'is enabled for Ceph node on Ceph page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_manager_monitor_enabled(selenium, browser_id, onepanel):
    driver = selenium[browser_id]
    assert (onepanel(driver).content.ceph.configuration_page.node
            .manager_and_monitor.is_checked()), ('Manager & Monitor for Ceph '
                                                 'node is disabled')


@wt(parsers.parse('user of {browser_id} sees that Ceph node has {number} OSD '
                  'on Ceph page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_osd_number(selenium, browser_id, number: float, onepanel):
    driver = selenium[browser_id]
    given = len(onepanel(driver).content.ceph.configuration_page.node.osds)
    assert given == number, f'Expected {number} OSDs but got {given} instead'


@wt(parsers.parse('user of {browser_id} clicks on "{ceph_name}" on pools list '
                  'on Ceph page'))
@repeat_failed(timeout=WAIT_BACKEND * 2)
def click_pool_on_pools_list(selenium, browser_id, ceph_name, onepanel):
    onepanel(selenium[browser_id]).content.ceph.pools_page.pools[
        ceph_name].click()


@wt(parsers.parse('user of {browser_id} sees that pool usage of "{ceph_name}" '
                  'is {usage} on Ceph page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_pool_usage_on_ceph_page(selenium, browser_id, ceph_name, usage,
                                   onepanel):
    given = onepanel(selenium[browser_id]).content.ceph.pools_page.pools[
        ceph_name].pool_usage
    assert usage == given, f'Expected pool usage: {usage}, but got {given}.'


# I needed to make this step "about usage" because there are slightly
# different values on bamboo and local deployment and I wanted tests to work
# both ways
@wt(parsers.parse('user of {browser_id} sees that pool usage of "{ceph_name}" '
                  'is about {usage} on Ceph page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_approx_pool_usage_on_ceph_page(selenium, browser_id, ceph_name,
                                          usage, onepanel):
    given = onepanel(selenium[browser_id]).content.ceph.pools_page.pools[
        ceph_name].pool_usage
    [number_given, unit_given] = given.split()
    [number_usage, unit_usage] = usage.split()
    assert abs(float(number_given) - float(number_usage)) < 1, (
        f'Expected pool usage: {number_usage}, but got {number_given}.')
    assert unit_usage == unit_given, (f'Expected pool usage in: {unit_usage}, '
                                      f'but got in {unit_given}.')


@wt(parsers.parse('user of {browser_id} clicks on "Create pool" button '
                  'on Ceph page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_button_on_ceph_page(selenium, browser_id, onepanel):
    onepanel(selenium[browser_id]).content.ceph.pools_page.create_pool()