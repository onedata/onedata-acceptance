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
from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.utils.generic import transform
from tests.gui.steps.common.miscellaneous import _enter_text


@wt(parsers.parse('user of {browser_id} clicks on {button} '
                  'button in clusters {where}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_in_cluster_page(selenium, browser_id, oz_page, button):
    driver = selenium[browser_id]
    getattr(oz_page(driver)['clusters'], transform(button)).click()


@wt(parsers.parse('user of {browser_id} copies registration token '
                  'from clusters page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_registration_cluster_token(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['clusters'].token_page.copy()


@wt(parsers.parse('user of {browser_id} sees "{record}" in clusters '
                  'menu'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_record_in_clusters_menu(selenium, browser_id, oz_page, record,
                                     hosts):
    driver = selenium[browser_id]
    record = hosts[record]['name']
    assert record in oz_page(driver)['clusters'].menu


@wt(parsers.parse('user of {browser_id} does not see "{record}" in clusters '
                  'menu'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_record_not_in_clusters_menu(selenium, browser_id, oz_page, record,
                                     hosts):
    driver = selenium[browser_id]
    record = hosts[record]['name']
    assert record not in oz_page(driver)['clusters'].menu


@wt(parsers.parse('user of {browser_id} clicks on "{record}" in clusters menu'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_record_in_clusters_menu(selenium, browser_id, oz_page, record,
                                     hosts):
    driver = selenium[browser_id]
    record = hosts[record]['name']
    oz_page(driver)['clusters'].menu[record]()


@wt(parsers.parse('user of {browser_id} clicks {option} of "{record}" '
                  'in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_of_record_in_the_sidebar(selenium, browser_id, oz_page, option):
    driver = selenium[browser_id]
    oz_page(driver)['clusters'].submenu[option].click()


@wt(parsers.parse('user of {browser_id} checks the understand notice '
                  'in clusters page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_the_understand_notice(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['clusters'].deregistration_checkbox()

