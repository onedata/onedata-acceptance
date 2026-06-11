"""This module contains gherkin steps to run acceptance tests featuring
harvester data discovery management in onezone web GUI.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.conftest import SeleniumDrivers
from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import switch_to_iframe
from tests.gui.utils import DataDiscoveryPage as DataDiscovery
from tests.gui.utils import Popups
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(parsers.parse("user of {browser_id} sees Data Discovery page"))
@wt(parsers.parse("user of {browser_id} sees public data discovery page"))
def assert_data_discovery_page(selenium: SeleniumDrivers, browser_id: str) -> None:
    # this function can only be used when we are sure that
    # there will be some files harvested as to use active waiting
    # instead of just sleep
    # to activate this view with no harvested files use
    # assert_empty_data_discovery_page(...) function

    switch_to_iframe(selenium, browser_id, ".plugin-frame")
    _wait_for_files_list(selenium, browser_id)


@repeat_failed(timeout=WAIT_BACKEND * 4, interval=1.5)
def _wait_for_files_list(selenium: SeleniumDrivers, browser_id: str) -> None:
    button_name = "Query"

    click_button_on_data_disc_page(selenium, browser_id, button_name)
    assert_files_list_on_data_disc(selenium, browser_id)


@repeat_failed(timeout=WAIT_FRONTEND / 2)
def assert_files_list_on_data_disc(selenium: SeleniumDrivers, browser_id: str) -> None:
    msg = "files list is not visible on data discovery page"
    assert len(DataDiscovery(selenium[browser_id]).results_list), msg


@wt(
    parsers.parse(
        "user of {browser_id} sees public data discovery page with no harvested data"
    )
)
def assert_empty_data_discovery_page(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    button_name = "Query"

    switch_to_iframe(selenium, browser_id, ".plugin-frame")
    click_button_on_data_disc_page(selenium, browser_id, button_name)


@wt(
    parsers.parse(
        'user of {browser_id} sees "{error_msg}" alert on Data discovery page'
    )
)
@repeat_failed(timeout=WAIT_BACKEND * 9, interval=10)
def assert_alert_text_on_data_disc_page(
    selenium: SeleniumDrivers, browser_id: str, error_msg: str
) -> None:
    msg = f"alert with {error_msg} message is not visible"
    assert error_msg == DataDiscovery(selenium[browser_id]).error_message, msg


@wt(
    parsers.parse(
        'user of {browser_id} sees "{error_msg}" alert on empty Data discovery page'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def see_alert_on_data_discovery_page(
    selenium: SeleniumDrivers, browser_id: str, error_msg: str
) -> None:
    switch_to_iframe(selenium, browser_id, ".plugin-frame")
    assert_alert_text_on_data_disc_page(selenium, browser_id, error_msg)


@wt(parsers.parse("user of {browser_id} sees Data Discovery page with Ecrin GUI"))
@wt(
    parsers.parse("user of {browser_id} sees public data discovery page with Ecrin GUI")
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_data_discovery_page_ecrin(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    switch_to_iframe(selenium, browser_id, ".plugin-frame")
    driver = selenium[browser_id]
    assert (
        DataDiscovery(driver).ecrin_gui_app_logo == "MDR"
    ), "Ecrin GUI not loaded in given time"


@wt(
    parsers.parse(
        "user of {browser_id} clicks on add query block icon in data discovery page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def start_query_block(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    DataDiscovery(driver).query_builder.root_block()


@wt(
    parsers.parse(
        "user of {browser_id} clicks on add another query block icon "
        "in data discovery page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def start_another_query_block(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    DataDiscovery(driver).query_builder.another_block_buttons[0].click()


@wt(
    parsers.parse(
        "user of {browser_id} clicks on {number} from the left add "
        "query block icon in data discovery page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def start_query_block_no(
    selenium: SeleniumDrivers, browser_id: str, number: str
) -> None:
    driver = selenium[browser_id]
    no = int(number.split()[0])
    DataDiscovery(driver).query_builder.another_block_buttons[no - 1].click()


@wt(
    parsers.parse(
        "user of {browser_id} clicks on condition properties expander in query builder"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def open_condition_properties_list(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    query_builder_popup = Popups(driver).get_query_builder_not_hidden_popup()
    query_builder_popup.expand_properties()


@wt(
    parsers.parse(
        "user of {browser_id} sees {properties_list} on condition properties list"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_properties_on_condition_properties_list(
    selenium: SeleniumDrivers, browser_id: str, properties_list: str
) -> None:
    driver = selenium[browser_id]
    properties = parse_seq(properties_list)
    query_builder_popup = Popups(driver).get_query_builder_not_hidden_popup()
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
def choose_property_for_query(
    selenium: SeleniumDrivers, browser_id: str, property_name: str
) -> None:
    driver = selenium[browser_id]
    query_builder_popup = Popups(driver).get_query_builder_not_hidden_popup()
    query_builder_popup.choose_property(property_name)


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{comparator}" from '
        "comparators list in query builder popup"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_comparator_in_query_builder(
    selenium: SeleniumDrivers, browser_id: str, comparator: str
) -> None:
    driver = selenium[browser_id]
    query_builder_popup = Popups(driver).get_query_builder_not_hidden_popup()
    query_builder_popup.choose_comparator(comparator)


@wt(
    parsers.parse(
        'user of {browser_id} writes "{value}" to value input in query builder popup'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def write_value_in_query_builder(
    selenium: SeleniumDrivers, browser_id: str, value: str
) -> None:
    driver = selenium[browser_id]
    query_builder_popup = Popups(driver).get_query_builder_not_hidden_popup()
    query_builder_popup.value = value


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{value}" from property values '
        "list in query builder popup"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_value_in_query_builder(
    selenium: SeleniumDrivers, browser_id: str, value: str
) -> None:
    driver = selenium[browser_id]
    query_builder_popup = Popups(driver).get_query_builder_not_hidden_popup()
    query_builder_popup.choose_value(value)


@wt(parsers.parse('user of {browser_id} clicks "Add" button in query builder popup'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_add_button_in_query_builder(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    query_builder_popup = Popups(driver).get_query_builder_not_hidden_popup()
    query_builder_popup.add_button()


@wt(
    parsers.parse(
        "user of {browser_id} clicks {operator} operator in query builder popup"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_operator_in_query_builder(
    selenium: SeleniumDrivers, browser_id: str, operator: str
) -> None:
    driver = selenium[browser_id]
    query_builder = Popups(driver).get_query_builder_not_hidden_popup()
    getattr(query_builder, f"{operator.lower()}_operator")()


@wt(
    parsers.parse(
        'user of {browser_id} clicks "{button_name}" button on Data discovery page'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_on_data_disc_page(
    selenium: SeleniumDrivers, browser_id: str, button_name: str
) -> None:
    driver = selenium[browser_id]
    page = DataDiscovery(driver)
    getattr(page, f"{transform(button_name)}_button")()


@wt(parsers.parse("user of {browser_id} sees that paging is set for {number} pages"))
def assert_page_size(selenium: SeleniumDrivers, browser_id: str, number: str) -> None:
    driver = selenium[browser_id]
    given = DataDiscovery(driver).page_size
    assert given == number, f"Expected page size was {number}, but got {given}"


@wt(parsers.parse("user of {browser_id} opens next page of data discovery page"))
def open_next_data_disc_page(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    DataDiscovery(driver).next_page()


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{parameter}" sorting '
        "{item} on data discovery page"
    )
)
def choose_sorting_parameter_or_order(
    selenium: SeleniumDrivers, browser_id: str, parameter: str, item: str
) -> None:
    driver = selenium[browser_id]
    getattr(DataDiscovery(driver), f"sorting_{item}_selector")()
    DataDiscovery(driver).choose_item(parameter)
