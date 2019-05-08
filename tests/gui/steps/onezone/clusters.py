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
from tests.gui.utils.generic import transform
from tests.gui.steps.common.miscellaneous import _enter_text


@wt(parsers.parse('user of {browser_id} clicks on {button} '
                  'button in clusters menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_add_new_provider_cluster(selenium, browser_id, oz_page, button):
    driver = selenium[browser_id]
    getattr(oz_page(driver)['clusters'], transform(button)).click()


@wt(parsers.parse('user of {browser_id} copies registration token '
                  'from clusters page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_registration_cluster_token(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['clusters'].token_page.copy()


@wt(parsers.parse('user of {browser_id} clicks on "{record}" in clusters menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_record_in_clusters_menu(selenium, browser_id, oz_page, record, hosts):
    driver = selenium[browser_id]
    record = hosts[record]['name']
    oz_page(driver)['clusters'].menu[record].click()


@wt(parsers.parse('user of {browser_id} clicks {option} of "{record}" '
                  'in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_of_record_in_the_sidebar(selenium, browser_id, oz_page, option):
    driver = selenium[browser_id]
    oz_page(driver)['clusters'].submenu[option].click()


@wt(parsers.parse('user of {browser_id} pastes copied token into join cluster '
                  'token text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def input_join_cluster_token_into_token_input_field(selenium, browser_id,
                                                    oz_page, displays,
                                                    clipboard):
    token = clipboard.paste(display=displays[browser_id])
    token_input = (oz_page(selenium[browser_id])['clusters']
                   .join_cluster_token_input)
    _enter_text(token_input, token)


@wt(parsers.parse('user of {browser_id} clicks on join the cluster button '
                  'in clusters page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_join_the_cluster_button(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['clusters'].join_the_cluster()

