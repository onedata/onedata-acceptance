"""This module contains gherkin steps to run acceptance tests featuring clusters
management in onezone web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import parsers

from tests.utils.utils import repeat_failed
from tests.utils.acceptance_utils import wt
from tests.gui.conftest import WAIT_FRONTEND


@wt(parsers.parse('user of {browser_id} clicks on add new provider cluster '
                  'button in clusters menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_add_new_provider_cluster(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['clusters'].add_new_provider_cluster()


@wt(parsers.parse('user of {browser_id} copies registration token '
                  'from clusters page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_registration_cluster_token(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['clusters'].token_page.copy()


@wt(parsers.parse('user of {browser_id} clicks on "{record}" in clusters menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_registration_cluster_token(selenium, browser_id, oz_page, record, hosts):
    driver = selenium[browser_id]
    record = hosts[record]['name']
    oz_page(driver)['clusters'].menu[record].click()


@wt(parsers.parse('user of {browser_id} clicks {option} of "{record}" in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_registration_cluster_token(selenium, browser_id, oz_page, option):
    driver = selenium[browser_id]
    oz_page(driver)['clusters'].submenu[option].click()
