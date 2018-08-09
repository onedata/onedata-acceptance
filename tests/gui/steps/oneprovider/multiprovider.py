"""Steps for test suite for multiprovider.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import parsers
from tests.utils.acceptance_utils import wt
from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.utils.generic import parse_seq, repeat_failed

from tests.gui.steps.oneprovider.common import g_wait_for_op_session_to_start
from tests.gui.meta_steps.onezone.common import visit_op


@wt(parsers.parse('user of {browser_id} clicks on "{provider_name}" provider on left sidebar menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_new_space_on_spaces_on_left_sidebar_menu(selenium, browser_id, provider_name, oz_page, hosts):
    driver = selenium[browser_id]
    # provider = hosts[provider_name]['name']
    # oz_page(driver)['providers'].elements_list[provider].click()
    visit_op(selenium, browser_id, oz_page, hosts[provider_name]['name'])
    g_wait_for_op_session_to_start(selenium, browser_id)


@wt(parsers.parse('user of {browser_id} sees "{group_name}" is in groups on left sidebar menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_groups_list_contains_group_on_left_sidebar_menu(selenium, browser_id, group_name, oz_page):
    driver = selenium[browser_id]
    assert group_name in oz_page(driver)['groups'].elements_list


@wt(parsers.parse('user of {browser_id} sees "{group_name}" is not in groups on left sidebar menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_groups_list_not_contains_group_on_left_sidebar_menu(selenium, browser_id, group_name, oz_page):
    driver = selenium[browser_id]
    assert group_name not in oz_page(driver)['groups'].elements_list
