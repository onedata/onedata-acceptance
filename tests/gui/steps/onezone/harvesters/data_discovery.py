"""This module contains gherkin steps to run acceptance tests featuring
harvester data discovery management in onezone web GUI.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import switch_to_iframe
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(parsers.parse("user of {browser_id} sees Data Discovery page"))
@wt(parsers.parse("user of {browser_id} sees public data discovery page"))
def assert_data_discovery_page(selenium, browser_id, data_discovery):
    # this function can only be used when we are sure that
    # there will be some files harvested as to use active waiting
    # instead of just sleep
    # to activate this view with no harvested files use
    # assert_empty_data_discovery_page(...) function

    switch_to_iframe(selenium, browser_id, ".plugin-frame")
    _wait_for_files_list(selenium, browser_id, data_discovery)


@repeat_failed(timeout=WAIT_BACKEND, interval=1.5)
def _wait_for_files_list(selenium, browser_id, data_discovery):
    button_name = "Query"

    click_button_on_data_disc_page(
        selenium, browser_id, data_discovery, button_name
    )
    assert_files_list_on_data_disc(selenium, browser_id, data_discovery)


@repeat_failed(timeout=WAIT_FRONTEND / 2)
def assert_files_list_on_data_disc(selenium, browser_id, data_discovery):
    msg = "files list is not visible on data discovery page"
    assert len(data_discovery(selenium[browser_id]).results_list), msg


@wt(
    parsers.parse(
        "user of {browser_id} sees public data discovery page with "
        "no harvested data"
    )
)
def assert_empty_data_discovery_page(selenium, browser_id, data_discovery):
    button_name = "Query"

    switch_to_iframe(selenium, browser_id, ".plugin-frame")
    click_button_on_data_disc_page(
        selenium, browser_id, data_discovery, button_name
    )


@wt(
    parsers.parse(
        'user of {browser_id} sees "{error_msg}" alert on Data discovery page'
    )
)
@repeat_failed(timeout=WAIT_BACKEND * 9, interval=10)
def assert_alert_text_on_data_disc_page(
    selenium, browser_id, error_msg, data_discovery
):
    msg = f"alert with {error_msg} message is not visible"
    assert error_msg == data_discovery(selenium[browser_id]).error_message, msg


@wt(
    parsers.parse(
        'user of {browser_id} sees "{error_msg}" alert on empty Data '
        "discovery page"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def see_alert_on_data_discovery_page(
    selenium, browser_id, data_discovery, error_msg
):
    switch_to_iframe(selenium, browser_id, ".plugin-frame")
    assert_alert_text_on_data_disc_page(
        selenium, browser_id, error_msg, data_discovery
    )


@wt(
    parsers.parse(
        "user of {browser_id} sees Data Discovery page with Ecrin GUI"
    )
)
@wt(
    parsers.parse(
        "user of {browser_id} sees public data discovery page with Ecrin GUI"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_data_discovery_page_ecrin(selenium, browser_id, data_discovery):
    switch_to_iframe(selenium, browser_id, ".plugin-frame")
    driver = selenium[browser_id]
    assert (
        data_discovery(driver).ecrin_gui_app_logo == "MDR"
    ), "Ecrin GUI not loaded in given time"


@wt(
    parsers.parse(
        "user of {browser_id} clicks on add query block icon in data "
        "discovery page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def start_query_block(selenium, browser_id, data_discovery):
    driver = selenium[browser_id]
    data_discovery(driver).query_builder.root_block()


@wt(
    parsers.parse(
        "user of {browser_id} clicks on add another query block icon "
        "in data discovery page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def start_another_query_block(selenium, browser_id, data_discovery):
    driver = selenium[browser_id]
    data_discovery(driver).query_builder.another_block_buttons[0].click()


@wt(
    parsers.parse(
        "user of {browser_id} clicks on {number} from the left add "
        "query block icon in data discovery page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def start_query_block_no(selenium, browser_id, data_discovery, number: str):
    driver = selenium[browser_id]
    no = int(number.split()[0])
    data_discovery(driver).query_builder.another_block_buttons[no - 1].click()


@wt(
    parsers.parse(
        "user of {browser_id} clicks on condition properties "
        "expander in query builder"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def open_condition_properties_list(selenium, browser_id, popups):
    driver = selenium[browser_id]
    query_builder_popup = popups(driver).get_query_builder_not_hidden_popup()
    query_builder_popup.expand_properties()


@wt(
    parsers.parse(
        "user of {browser_id} sees {properties_list} on condition "
        "properties list"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_properties_on_condition_properties_list(
    selenium, browser_id, properties_list, popups
):
    driver = selenium[browser_id]
    properties = parse_seq(properties_list)
    query_builder_popup = popups(driver).get_query_builder_not_hidden_popup()
    for prop in properties:
        assert query_builder_popup.assert_property(
            prop
        ), f"{prop} property not found in condition properties list"


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{property_name}" property '
        "for a query in query builder popup"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_property_for_query(selenium, browser_id, property_name, popups):
    driver = selenium[browser_id]
    query_builder_popup = popups(driver).get_query_builder_not_hidden_popup()
    query_builder_popup.choose_property(property_name)


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{comparator}" from '
        "comparators list in query builder popup"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_comparator_in_query_builder(
    selenium, browser_id, comparator, popups
):
    driver = selenium[browser_id]
    query_builder_popup = popups(driver).get_query_builder_not_hidden_popup()
    query_builder_popup.choose_comparator(comparator)


@wt(
    parsers.parse(
        'user of {browser_id} writes "{value}" to value input in '
        "query builder popup"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def write_value_in_query_builder(selenium, browser_id, value: str, popups):
    driver = selenium[browser_id]
    query_builder_popup = popups(driver).get_query_builder_not_hidden_popup()
    query_builder_popup.value = value


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{value}" from property values '
        "list in query builder popup"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_value_in_query_builder(selenium, browser_id, value: str, popups):
    driver = selenium[browser_id]
    query_builder_popup = popups(driver).get_query_builder_not_hidden_popup()
    query_builder_popup.choose_value(value)


@wt(
    parsers.parse(
        'user of {browser_id} clicks "Add" button in query builder popup'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_add_button_in_query_builder(selenium, browser_id, popups):
    driver = selenium[browser_id]
    query_builder_popup = popups(driver).get_query_builder_not_hidden_popup()
    query_builder_popup.add_button()


@wt(
    parsers.parse(
        "user of {browser_id} clicks {operator} operator in query builder popup"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_operator_in_query_builder(selenium, browser_id, operator, popups):
    driver = selenium[browser_id]
    query_builder = popups(driver).get_query_builder_not_hidden_popup()
    getattr(query_builder, f"{operator.lower()}_operator")()


@wt(
    parsers.parse(
        'user of {browser_id} clicks "{button_name}" button on Data '
        "discovery page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_on_data_disc_page(
    selenium, browser_id, data_discovery, button_name
):
    driver = selenium[browser_id]
    page = data_discovery(driver)
    getattr(page, f"{transform(button_name)}_button")()


@wt(
    parsers.parse(
        "user of {browser_id} sees that paging is set for {number} pages"
    )
)
def assert_page_size(selenium, browser_id, data_discovery, number: str):
    driver = selenium[browser_id]
    given = data_discovery(driver).page_size
    assert given == number, f"Expected page size was {number}, but got {given}"


@wt(
    parsers.parse("user of {browser_id} opens next page of data discovery page")
)
def open_next_data_disc_page(selenium, browser_id, data_discovery):
    driver = selenium[browser_id]
    data_discovery(driver).next_page()


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{parameter}" sorting '
        "{item} on data discovery page"
    )
)
def choose_sorting_parameter_or_order(
    selenium, browser_id, parameter, item, data_discovery
):
    driver = selenium[browser_id]
    getattr(data_discovery(driver), f"sorting_{item}_selector")()
    data_discovery(driver).choose_item(parameter)
