"""This module contains gherkin steps to run acceptance tests featuring
harvester management in onezone web GUI.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time

from pytest_bdd import parsers

from tests import ELASTICSEARCH_PORT
from tests.utils.acceptance_utils import wt
from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.utils.utils import repeat_failed
from tests.gui.steps.common.miscellaneous import _enter_text, switch_to_iframe
from tests.gui.utils.generic import transform


@wt(parsers.parse('user of {browser_id} clicks on {button_name} button '
                  'in discovery sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_on_discovery_on_left_sidebar_menu(selenium, browser_id,
                                                   button_name, oz_page):
    driver = selenium[browser_id]
    button = transform(button_name) + '_button'
    getattr(oz_page(driver)['discovery'], button).click()


@wt(parsers.parse('user of {browser_id} types "{text}" to {input_name} input '
                  'field in discovery page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_to_input_field_in_discovery_page(selenium, browser_id, oz_page,
                                               text, input_name):
    driver = selenium[browser_id]
    input_field = getattr(oz_page(driver)['discovery'], input_name)
    _enter_text(input_field, text)


@wt(parsers.parse('user of {browser_id} types the endpoint of deployed '
                  'elasticsearch client to {input_name} input field '
                  'in discovery page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_endpoint_to_input_field_in_discovery_page(selenium, browser_id,
                                                   oz_page, input_name, hosts):
    driver = selenium[browser_id]
    input_field = getattr(oz_page(driver)['discovery'], input_name)
    text = '{}:{}'.format(hosts['elasticsearch']['ip'], ELASTICSEARCH_PORT)
    _enter_text(input_field, text)


@wt(parsers.parse('user of {browser_id} clicks "{text}" in '
                  'harvester indices page menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_member_menu_option_in_harvester_indices_page(selenium, browser_id,
                                                          text, oz_page,
                                                          popups):
    driver = selenium[browser_id]
    oz_page(driver)['discovery'].indices_page.menu_button.click()
    popups(driver).popover_menu.menu[text]()


@wt(parsers.parse('user of {browser_id} clicks on Create button '
                  'in discovery page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_button_in_discovery_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['discovery'].create_button()


@wt(parsers.parse('user of {browser_id} sees that "{harvester_name}" '
                  'has {option} the harvesters list in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_harvester_exists_on_harvesters_list(selenium, browser_id, oz_page,
                                              harvester_name, option):
    driver = selenium[browser_id]

    if option.startswith('appeared'):
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
def click_on_option_in_harvester_menu(selenium, browser_id, option,
                                      name, oz_page):
    page = oz_page(selenium[browser_id])['discovery']
    page.elements_list[name]()
    page.elements_list[name].menu_button()
    page.menu[option]()


@wt(parsers.parse('user of {browser_id} types "{text}" to rename harvester '
                  'input field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_to_rename_input_field_in_discovery_page(selenium, browser_id,
                                                      oz_page, text):
    driver = selenium[browser_id]
    input_field = oz_page(driver)['discovery'].rename_input
    _enter_text(input_field, text)


@wt(parsers.parse('user of {browser_id} confirms harvester rename using button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_harvester_rename_using_button(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['discovery'].rename_button()


@wt(parsers.re('user of (?P<browser_id>.*?) clicks (?P<option>.*?) '
               'of "(?P<harvester_name>.*?)" harvester in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_of_harvester_on_left_sidebar_menu(selenium, browser_id,
                                                      harvester_name, option,
                                                      oz_page):
    driver = selenium[browser_id]
    getattr(oz_page(driver)['discovery'].elements_list[harvester_name],
            transform(option)).click()


@wt(parsers.parse('user of {browser_id} clicks {button_name} button '
                  'in harvester spaces page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_in_harvester_spaces_page(selenium, browser_id, oz_page,
                                          button_name):
    driver = selenium[browser_id]
    button_name = transform(button_name) + '_button'
    getattr(oz_page(driver)['discovery'], button_name).click()


@wt(parsers.parse('user of {browser_id} chooses "{element_name}" from dropdown '
                  'in add {element} modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_element_from_dropdown_in_add_element_modal(selenium, browser_id,
                                                      element_name, modals,
                                                      element):
    driver = selenium[browser_id]
    modal_name = 'add_one_of_{}s'.format(element)

    add_one_of_elements_modal = getattr(modals(driver), modal_name)
    add_one_of_elements_modal.expand_dropdown()
    modals(driver).dropdown.options[element_name].click()


@wt(parsers.parse('user of {browser_id} sees that "{space_name}" has appeared '
                  'on the spaces list in discovery page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_space_has_appeared_in_discovery_page(selenium, browser_id,
                                                space_name, oz_page):
    driver = selenium[browser_id]
    assert space_name in oz_page(driver)['discovery'].spaces_list, \
        'space "{}" not found'.format(space_name)


@wt(parsers.parse('user of {browser_id} types "{index_name}" '
                  'to name input field in indices page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_index_name_to_input_field_in_indices_page(selenium, browser_id,
                                                   oz_page, index_name):
    driver = selenium[browser_id]
    name_input = oz_page(driver)['discovery'].indices_page.name_input
    _enter_text(name_input, index_name)


@wt(parsers.parse('user of {browser_id} clicks on Create button '
                  'in indices page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_button_in_indices_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['discovery'].indices_page.create_button()


@wt(parsers.parse('user of {browser_id} sees that "{index_name}" '
                  'has appeared on the indices list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_index_has_appeared_in_indices_page(selenium, browser_id, oz_page,
                                              index_name):
    driver = selenium[browser_id]
    indices_list = oz_page(driver)['discovery'].indices_page.indices_list
    assert index_name in indices_list, 'index "{}" not found'.format(index_name)


@wt(parsers.parse('user of {browser_id} expands "{index_name}" index record '
                  'in indices page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def expand_index_record_in_indices_page(selenium, browser_id, oz_page,
                                        index_name):
    driver = selenium[browser_id]
    indices_list = oz_page(driver)['discovery'].indices_page.indices_list
    indices_list[index_name].click()


@wt(parsers.parse('user of {browser_id} sees {value} progress in '
                  '"{index_name}" index harvesting'))
@repeat_failed(timeout=WAIT_FRONTEND * 2)
def assert_progress_in_harvesting(selenium, browser_id, oz_page,
                                  index_name, value):
    driver = selenium[browser_id]
    indices_list = oz_page(driver)['discovery'].indices_page.indices_list
    progress_value = indices_list[index_name].progress_value

    assert value == progress_value, 'found {} instead of {}'.format(progress_value,
                                                                    value)


def click_remove_space_option_in_menu_in_discover_spaces_page(selenium,
                                                              browser_id,
                                                              space_name,
                                                              oz_page):
    driver = selenium[browser_id]
    page = oz_page(driver)['discovery']
    page.spaces_list[space_name].click_menu()
    page.menu['Remove this space'].click()


def click_option_in_discovery_page_menu(selenium, browser_id, oz_page,
                                        button_name):
    driver = selenium[browser_id]
    page = oz_page(driver)['discovery']
    page.menu_button()
    page.menu[button_name].click()


@wt(parsers.re('user of (?P<browser_id>.*) sees '
               '(?P<alert_text>Insufficient permissions) alert '
               'on (?P<where>Spaces|Indices) subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def see_insufficient_permissions_alert_on_discovery_page(selenium, browser_id,
                                                         oz_page, alert_text):
    driver = selenium[browser_id]
    forbidden_alert = oz_page(driver)['discovery'].forbidden_alert.text

    assert alert_text in forbidden_alert, ('alert with text "{}" not found'
                                           .format(alert_text))


@wt(parsers.parse('user of {browser_id} clicks on start query icon in data '
                  'discovery page'))
def start_query(selenium, browser_id, oz_page):
    driver = selenium(browser_id)
    oz_page(driver)['discovery'].data_discovery_page.query_builder.root_block()


@wt(parsers.parse('user of {browser_id} chooses "{property_name}" property to '
                  'query for'))
def choose_property_to_query(selenium, browser_id, property_name, popups):
    driver = selenium[browser_id]
    popups(driver).query_builder_popup.choose_property(property_name)


@wt(parsers.parse('user of {browser_id} sees Data Discovery page'))
def assert_data_discovery_page(selenium, browser_id, data_discovery):
    # this function can only be used when we are sure that
    # there will be some files harvested as to use active waiting
    # instead of just sleep
    # to activate this view with no harvested files use
    # assert_empty_data_discovery_page(...) function

    switch_to_iframe(selenium, browser_id, '.plugin-frame')
    _wait_for_files_list(selenium, browser_id, data_discovery)


@repeat_failed(timeout=WAIT_BACKEND, interval=1.5)
def _wait_for_files_list(selenium, browser_id, data_discovery):
    click_query_button_on_data_disc_page(selenium, browser_id, data_discovery)
    assert_files_list_on_data_disc(selenium, browser_id, data_discovery)


@repeat_failed(timeout=WAIT_FRONTEND/2)
def assert_files_list_on_data_disc(selenium, browser_id, data_discovery):
    msg = 'files list is not visible on data discovery page'
    assert len(data_discovery(selenium[browser_id]).results_list), msg


def assert_empty_data_discovery_page(selenium, browser_id):
    switch_to_iframe(selenium, browser_id, '.plugin-frame')


@wt(parsers.parse('user of {browser_id} clicks "Query" button on Data '
                  'discovery page'))
def click_query_button_on_data_disc_page(selenium, browser_id, data_discovery):
    driver = selenium[browser_id]
    data_discovery(driver).query_builder.query_button()


@wt(parsers.parse('user of {browser_id} sees "{error_msg}" alert on Data '
                  'discovery page'))
@repeat_failed(timeout=WAIT_BACKEND*9, interval=10)
def assert_alert_text_on_data_disc_page(selenium, browser_id, error_msg,
                                        data_discovery):
    msg = f'alert with {error_msg} message is not visible'
    assert error_msg == data_discovery(selenium[browser_id]).error_message, msg
