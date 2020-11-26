"""This module contains gherkin steps to run acceptance tests featuring
harvester data discovery management in onezone web GUI.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.steps.common.miscellaneous import switch_to_iframe
from tests.gui.utils.generic import parse_seq
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} chooses "{property_name}" property to '
                  'query for'))
def choose_property_to_query(selenium, browser_id, property_name, popups):
    driver = selenium[browser_id]
    popups(driver).query_builder_popup.choose_property(property_name)


@wt(parsers.parse('user of {browser_id} sees Data Discovery page'))
@wt(parsers.parse('user of {browser_id} sees public data discovery page'))
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


@wt(parsers.parse('user of {browser_id} sees public data discovery page with '
                  'no harvested data'))
def assert_empty_data_discovery_page(selenium, browser_id, data_discovery):
    switch_to_iframe(selenium, browser_id, '.plugin-frame')
    data_discovery(selenium[browser_id]).query_builder.query_button()


@wt(parsers.parse('user of {browser_id} sees "{error_msg}" alert on Data '
                  'discovery page'))
@repeat_failed(timeout=WAIT_BACKEND*9, interval=10)
def assert_alert_text_on_data_disc_page(selenium, browser_id, error_msg,
                                        data_discovery):
    msg = f'alert with {error_msg} message is not visible'
    assert error_msg == data_discovery(selenium[browser_id]).error_message, msg


@wt(parsers.parse('user of {browser_id} sees Data Discovery page with Ecrin '
                  'GUI'))
@wt(parsers.parse('user of {browser_id} sees public data discovery page with '
                  'Ecrin GUI'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_data_discovery_page_ecrin(selenium, browser_id, data_discovery):
    switch_to_iframe(selenium, browser_id, '.plugin-frame')
    driver = selenium[browser_id]
    assert data_discovery(driver).ecrin_gui_app_logo == 'MDR', ('Ecrin GUI '
                                                                'not loaded '
                                                                'in given time')


# queries
@wt(parsers.parse('user of {browser_id} clicks on start query icon in data '
                  'discovery page'))
def start_query(selenium, browser_id, data_discovery):
    driver = selenium[browser_id]
    data_discovery(driver).query_builder.root_block()


@wt(parsers.parse('user of {browser_id} clicks on start another query icon in '
                  'data discovery page'))
def start_another_query(selenium, browser_id, data_discovery):
    driver = selenium[browser_id]
    data_discovery(driver).query_builder.another_query_button()


@wt(parsers.parse('user of {browser_id} clicks on condition properties '
                  'expander in query builder'))
def open_condition_properties_list(selenium, browser_id, popups):
    driver = selenium[browser_id]
    popups(driver).query_builder_popup.expand_properties()


@wt(parsers.parse('user of {browser_id} sees {properties_list} on condition '
                  'properties list'))
def assert_properties_on_condition_properties_list(selenium, browser_id,
                                                   properties_list, popups):
    driver = selenium[browser_id]
    properties = parse_seq(properties_list)
    for prop in properties:
        popups(driver).query_builder_popup.assert_property(prop), (
            f'{prop} property not found in condition properties list'
        )


@wt(parsers.parse('user of {browser_id} chooses "{property_name}" property '
                  'for a query in query builder popup'))
def choose_property_for_query(selenium, browser_id, property_name, popups):
    driver = selenium[browser_id]
    popups(driver).query_builder_popup.choose_property(property_name)


@wt(parsers.parse('user of {browser_id} chooses "{comparator}" from '
                  'comparators list in query builder popup'))
def choose_comparator_in_query_builder(selenium, browser_id, comparator,
                                       popups):
    driver = selenium[browser_id]
    popups(driver).query_builder_popup.choose_comparator(comparator)


@wt(parsers.parse('user of {browser_id} writes "{value}" to value input in '
                  'query builder popup'))
def write_value_in_query_builder(selenium, browser_id, value: str, popups):
    driver = selenium[browser_id]
    popups(driver).query_builder_popup.value = value


@wt(parsers.parse('user of {browser_id} clicks "Add" button in query builder '
                  'popup'))
def click_add_button_in_query_builder(selenium, browser_id, popups):
    driver = selenium[browser_id]
    popups(driver).query_builder_popup.add_button()


@wt(parsers.parse('user of {browser_id} clicks {operator} operator in query '
                  'builder popup'))
def click_operator_in_query_builder(selenium, browser_id, operator, popups):
    driver = selenium[browser_id]
    getattr(popups(driver).query_builder_popup,
            f'{operator.lower()}_operator')()


@wt(parsers.parse('user of {browser_id} clicks "Query" button on Data '
                  'discovery page'))
def click_query_button_on_data_disc_page(selenium, browser_id, data_discovery):
    driver = selenium[browser_id]
    data_discovery(driver).query_builder.query_button()