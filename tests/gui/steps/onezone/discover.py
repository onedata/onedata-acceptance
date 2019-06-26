"""This module contains gherkin steps to run acceptance tests featuring
harvester management in onezone web GUI.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import parsers

from tests.utils.acceptance_utils import wt
from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.utils import repeat_failed
from tests.gui.steps.common.miscellaneous import _enter_text


@wt(parsers.parse('user of {browser_id} clicks on Create harvester button '
                  'in discovery sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_new_harvester_on_discovery_on_left_sidebar_menu(selenium,
                                                                 browser_id,
                                                                 oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['discovery'].create_new_harvester_button()


@wt(parsers.parse('user of {browser_id} types "{text}" to {input_name} input '
                  'field in discovery page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_to_input_field_in_discovery_page(selenium, browser_id, oz_page,
                                               text, input_name):
    driver = selenium[browser_id]
    input_field = getattr(oz_page(driver)['discovery'], input_name)
    _enter_text(input_field, text)


@wt(parsers.parse('user of {browser_id} types elasticsearch client endpoint '
                  'to {input_name} input field in discovery page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_endpoint_to_input_field_in_discovery_page(selenium, browser_id,
                                                   oz_page, input_name, hosts):
    driver = selenium[browser_id]
    input_field = getattr(oz_page(driver)['discovery'], input_name)
    text = hosts['elasticsearch']['ip'] + ':9200'
    _enter_text(input_field, text)


@wt(parsers.parse('user of {browser_id} clicks on Create button '
                  'in discovery page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_button_in_discovery_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['discovery'].create_button()


@wt(parsers.parse('user of {browser_id} sees that "{harvester_name}" '
                  'has {option} on the harvesters list in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_new_created_harvester_has_appeared_on_harvesters_list(selenium,
                                                                 browser_id,
                                                                 oz_page,
                                                                 harvester_name,
                                                                 option):
    driver = selenium[browser_id]
    if option == 'appeared':
        assert harvester_name in oz_page(driver)['discovery'].elements_list, \
            'harvester "{}" not found'.format(harvester_name)
    else:
        assert harvester_name not in oz_page(driver)['discovery'].elements_list, \
            'harvester "{}" found'.format(harvester_name)


@wt(parsers.re('user of (?P<browser_id>.*) clicks on '
               '"(?P<option>Rename|Leave|Remove)" '
               'button in harvester "(?P<name>.*)" menu '
               'in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_group_menu_button(selenium, browser_id, option, name, oz_page):
    page = oz_page(selenium[browser_id])['discovery']
    page.elements_list[name]()
    page.elements_list[name].menu_button()
    page.menu[option]()


@wt(parsers.parse('user of {browser_id} types "{text}" to rename harvester '
                  'input field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_to_input_field_in_discovery_page(selenium, browser_id, oz_page,
                                               text):
    driver = selenium[browser_id]
    input_field = oz_page(driver)['discovery'].rename_input
    _enter_text(input_field, text)


@wt(parsers.parse('user of {browser_id} confirms harvester rename using button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_harvester_rename_using_button(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['discovery'].rename_button()



