"""Steps implementation for quality of service GUI tests."""

__author__ = "Michal Dronka, Natalia Organek"
__copyright__ = "Copyright (C) 2020-2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from datetime import datetime
from typing import cast

import yaml
from pytest_bdd import parsers
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.common import assert_logs_order_with_optional_logs
from tests.gui.steps.rest.provider import get_provider_id
from tests.gui.utils import Modals, OPLoggedIn, Popups
from tests.gui.utils.common.constants import CONFLICT_NAME_SEPARATOR
from tests.gui.utils.core import scroll_to_css_selector_bottom
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    parse_elements_sequence,
    transform,
)
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import wt
from tests.utils.user_utils import Users
from tests.utils.utils import repeat_failed

# Character used to separate provider name from storage name in QoS expressions editor.
# Eg. "storage is my_posix @provider-krakow"
PROVIDER_PREFIX_CHAR = "@"


@wt(parsers.parse("user of {browser_id} deletes all QoS requirements"))
@repeat_failed(timeout=WAIT_FRONTEND)
def delete_all_qualities_of_service(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).details_modal.qos
    while len(modal.requirements):
        modal.requirements[0].delete.click()
        Popups(driver).delete_qos_popup.confirm.click()


@wt(parsers.parse("user of {browser_id} sees that all QoS requirements are {state}"))
@repeat_failed(
    interval=1, timeout=90, exceptions=(NoSuchElementException, RuntimeError)
)
def assert_all_qualities_of_service_are_fulfilled(
    selenium: SeleniumDrivers, browser_id: str, state: str
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).details_modal.qos
    for requirement in modal.requirements:
        assert hasattr(requirement, state), f"No all QoS requirements are {state}"


@wt(
    parsers.parse(
        'user of {browser_id} selects "{option_name}" view in Show '
        "Details toggle in QoS panel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def select_option_qos(
    selenium: SeleniumDrivers, browser_id: str, option_name: str
) -> None:
    driver = selenium[browser_id]

    modal_qos = Modals(driver).details_modal.qos
    option_btn = getattr(modal_qos, "show_details_" + transform(option_name))
    modal_qos.scroll_to_top()

    # the need to scroll back to the top is due to the fact,
    # that the header covers the part of the button,

    option_btn.click()


@wt(
    parsers.parse(
        "user of {browser_id} sees the following logs in audit log files list"
        ' in given order for "{files_list:ElementsSequence}" files:\n{config}',
        extra_types={"ElementsSequence": parse_elements_sequence},
    ),
)
def assert_audit_log_logs_for_each_file_in_list(
    selenium: SeleniumDrivers, browser_id: str, files_list: list[str], config: str
) -> None:
    driver = selenium[browser_id]
    modal_qos = Modals(driver).details_modal.qos
    entries = modal_qos.audit_log_list.entries
    expected_logs = cast(list[dict[str, str]], yaml.load(config, yaml.Loader))

    for file_name in files_list:
        if len(files_list) > 1:
            actual_logs = [
                entry.event.text for entry in entries if entry.file.text == file_name
            ]
        else:
            actual_logs = [entry.event.text for entry in entries]

        assert_logs_order_with_optional_logs(expected_logs, actual_logs)


@wt(
    parsers.parse(
        "user of {browser_id} sees that there are no logs in audit log files list"
        ' and can see following information: "{info}"'
    )
)
def assert_no_logs_in_qos_audit_log(
    selenium: SeleniumDrivers, browser_id: str, info: str
) -> None:
    driver = selenium[browser_id]
    modal_qos = Modals(driver).details_modal.qos
    audit_log = modal_qos.audit_log_list
    if audit_log.is_empty():
        assert audit_log.empty_info.text == info, (
            f"The actual no logs info: {audit_log.empty_info.text} is not equal to"
            f" expected: {info}"
        )
        return
    raise AssertionError("Audit Log logs list is not empty")


@wt(
    parsers.parse(
        "user of {browser_id} sees that all logs in audit log files list"
        " are ordered from newest to oldest"
    )
)
def assert_qos_audit_log_entries_times_ordered(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    modal_qos = Modals(driver).details_modal.qos
    entries = modal_qos.audit_log_list.entries
    actual_log_dates = [entry.time.text for entry in entries]

    actual_log_datetimes = [
        datetime.strptime(date, "%d %b %Y %H:%M:%S.%f") for date in actual_log_dates
    ]

    prev_date = actual_log_datetimes[0]
    for i, date in enumerate(actual_log_datetimes[1:]):
        assert date <= prev_date, f"{i+1}-th log should not be newer than {i}-th"
        # logs are enumerated from 0 in loop, when it fact the first index is 1
        prev_date = date


@wt(
    parsers.parse(
        'user of {browser_id} clicks on first link with filename: "{file_name}",'
        " in audit log files list"
    )
)
def click_on_first_link_with_file_name_in_qos_audit_log(
    selenium: SeleniumDrivers, browser_id: str, file_name: str
) -> None:
    driver = selenium[browser_id]
    modal_qos = Modals(driver).details_modal.qos
    entries = modal_qos.audit_log_list.entries
    file_entries = [entry for entry in entries if entry.file.text == file_name]
    file_entries[0].click()


@wt(
    parsers.parse(
        "user of {browser_id} sees that replicas number is equal {number} in QoS panel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_replicas_number_in_qualities_of_service_modal(
    selenium: SeleniumDrivers, browser_id: str, number: str
) -> None:
    driver = selenium[browser_id]
    replicas_number = Modals(driver).details_modal.qos.replicas_number
    assert (
        number == replicas_number
    ), f"Found {replicas_number} instead of {number} replicas number"


def process_storage_expression(expression: str, hosts: Hosts) -> str:
    split_expression = expression.split(PROVIDER_PREFIX_CHAR)
    if len(split_expression) == 1:
        return expression
    provider = split_expression[1]
    provider_name = hosts[provider]["name"]
    return f"{split_expression[0]}{PROVIDER_PREFIX_CHAR}{provider_name}"


def process_provider_expression(expression: str, hosts: Hosts, users: Users) -> str:
    split_expression = expression.split(" is ")
    if len(split_expression) == 1:
        return expression
    provider = split_expression[1]
    provider_name = hosts[provider]["name"]
    provider_id = get_provider_short_id(provider, hosts, users)
    id_separator = CONFLICT_NAME_SEPARATOR
    return f"{split_expression[0]} is {provider_name} {id_separator}{provider_id}"


def get_provider_short_id(provider: str, hosts: Hosts, users: Users) -> str:
    visible_id_index = 6
    return get_provider_id(provider, hosts, users)[:visible_id_index]


def process_expression(expression: str, hosts: Hosts, users: Users) -> str:
    split_expression = expression.split(" is")
    if len(split_expression) == 1:
        return expression
    domain = split_expression[0]
    if domain == "storage":
        return process_storage_expression(expression, hosts)
    if domain == "provider":
        return process_provider_expression(expression, hosts, users)
    raise ValueError("unknown expression type")


@wt(
    parsers.parse(
        "user of {browser_id} sees [{expression}] QoS requirement in QoS panel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_expression_in_qos_panel(
    selenium: SeleniumDrivers,
    browser_id: str,
    expression: str,
    hosts: Hosts,
    users: Users,
) -> None:
    driver = selenium[browser_id]
    requirements = Modals(driver).details_modal.qos.requirements
    ready_expression = process_expression(expression, hosts, users)
    for requirement in requirements:
        expression_in_modal = requirement.expression.replace("\n", " ")
        if expression_in_modal == ready_expression:
            assert True
            return
    assert (
        False
    ), f'Not found "{expression}" QoS requirement in modal "Quality of Service"'


def process_whole_nested_expression(expression: str, hosts: Hosts, users: Users) -> str:
    plain_exp = expression.replace("[", "").replace("]", "")
    provider1 = "oneprovider-1"
    provider2 = "oneprovider-2"
    provider1_name = hosts[provider1]["name"]
    provider2_name = hosts[provider2]["name"]
    provider1_id = get_provider_short_id(provider1, hosts, users)
    provider2_id = get_provider_short_id(provider2, hosts, users)

    id_separator = CONFLICT_NAME_SEPARATOR
    plain_exp = plain_exp.replace(
        f"{PROVIDER_PREFIX_CHAR}oneprovider-1",
        f"{PROVIDER_PREFIX_CHAR}{provider1_name}",
    )
    plain_exp = plain_exp.replace(
        f"{PROVIDER_PREFIX_CHAR}oneprovider-2",
        f"{PROVIDER_PREFIX_CHAR}{provider2_name}",
    )
    plain_exp = plain_exp.replace(
        "oneprovider-1",
        f"{provider1_name} {id_separator}{provider1_id}",
    )
    plain_exp = plain_exp.replace(
        "oneprovider-2",
        f"{provider2_name} {id_separator}{provider2_id}",
    )
    return plain_exp


@wt(
    parsers.parse(
        "user of {browser_id} sees nested QoS requirement in QoS panel:\n{expression}"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_nested_expression_in_qos_panel(
    selenium: SeleniumDrivers,
    browser_id: str,
    expression: str,
    hosts: Hosts,
    users: Users,
) -> None:
    driver = selenium[browser_id]
    requirements = Modals(driver).details_modal.qos.requirements
    ready_expression = process_whole_nested_expression(expression, hosts, users)

    for requirement in requirements:
        expression_in_modal = requirement.expression.replace("\n", " ")
        if expression_in_modal == ready_expression:
            assert True
            return
    assert (
        False
    ), f'Not found "{ready_expression}" QoS requirement in modal "Quality of Service"'


@wt(parsers.parse("user of {browser_id} doesn't see any QoS requirement in QoS panel"))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_no_expression_in_qualities_of_service_modal(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    try:
        Modals(driver).details_modal.qos.requirements
    except RuntimeError:
        assert True
    else:
        assert False, 'Found QoS requirement in modal "Quality of Service"'


@wt(parsers.parse('user of {browser_id} clicks "enter as text" label in QoS panel'))
def click_enter_as_text_link(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    Modals(driver).details_modal.qos.enter_as_text()


@wt(
    parsers.parse(
        "user of {browser_id} confirms entering expression in "
        "expression text field in QoS panel"
    )
)
def confirm_entering_text(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    Modals(driver).details_modal.qos.confirm_text()


@wt(parsers.parse("user of {browser_id} clicks on add query block icon in QoS panel"))
def click_add_query_block(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).details_modal.qos.query_builder
    modal.another_block_buttons[0].click()


@wt(
    parsers.parse(
        "user of {browser_id} clicks on {number} from the left add "
        "query block icon in QoS panel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def start_query_block_no(
    selenium: SeleniumDrivers, browser_id: str, number: str
) -> None:
    driver = selenium[browser_id]
    no = int(number.split()[0])
    modal = Modals(driver).details_modal.qos.query_builder
    modal.another_block_buttons[no - 1].click()


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{property_name}" property in '
        '"Add QoS condition" popup'
    )
)
def choose_property_in_add_condition_popup(
    selenium: SeleniumDrivers, browser_id: str, property_name: str
) -> None:
    driver = selenium[browser_id]
    popup = Popups(driver).get_query_builder_not_hidden_popup()
    popup.choose_property(property_name)


@wt(
    parsers.parse(
        'user of {browser_id} chooses value of "{item}" at '
        '"{provider}" in "Add QoS condition" popup'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_value_of_item_at_provider_in_add_cond_popup(
    selenium: SeleniumDrivers,
    browser_id: str,
    item: str,
    provider: str,
    hosts: Hosts,
) -> None:
    provider_name = hosts[provider]["name"]
    driver = selenium[browser_id]
    popup = Popups(driver).get_query_builder_not_hidden_popup()
    popup.qos_values_choice()
    separator = PROVIDER_PREFIX_CHAR
    Popups(driver).power_select.choose_item(f"{item} {separator}{provider_name}")


@wt(
    parsers.re(
        rf"user of (?P<browser_id>.*?) sees (?P<providers>{ELEMENTS_SEQUENCE_PATTERN}) "
        r'providers? on values list in "Add QoS condition" popup'
    ),
    converters={
        "providers": parse_elements_sequence,
    },
)
def assert_list_of_providers_in_add_cond_popup(
    selenium: SeleniumDrivers, browser_id: str, providers: list[str], hosts: Hosts
) -> None:
    expected = [hosts[provider]["name"] for provider in providers]

    driver = selenium[browser_id]
    popup = Popups(driver).get_query_builder_not_hidden_popup()
    popup.qos_values_choice()
    separator = f" {PROVIDER_PREFIX_CHAR}"
    actual = [v.text.split(separator)[0] for v in Popups(driver).power_select.items]
    compare_lists(expected, actual)


@wt(
    parsers.re(
        rf"user of (?P<browser_id>.*?) sees (?P<storages>{ELEMENTS_SEQUENCE_PATTERN}) "
        r'storages? on values list in "Add QoS condition" popup'
    ),
    converters={
        "storages": parse_elements_sequence,
    },
)
def assert_list_of_storages_in_add_cond_popup(
    selenium: SeleniumDrivers, browser_id: str, storages: list[str], hosts: Hosts
) -> None:
    expected = []
    separator = f" {PROVIDER_PREFIX_CHAR}"
    for expression in storages:
        [name, provider] = expression.split(separator)
        provider_name = hosts[provider]["name"]
        expected.append(f"{name} {PROVIDER_PREFIX_CHAR}{provider_name}")

    driver = selenium[browser_id]
    popup = Popups(driver).get_query_builder_not_hidden_popup()
    popup.qos_values_choice()
    actual = [v.text for v in Popups(driver).power_select.items]
    compare_lists(expected, actual)


@wt(
    parsers.parse(
        "user of {browser_id} chooses value of "
        '"{provider}" provider in "Add QoS condition" popup'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_value_of_provider_item_in_add_cond_popup(
    selenium: SeleniumDrivers, browser_id: str, provider: str, hosts: Hosts
) -> None:
    provider_name = hosts[provider]["name"]
    driver = selenium[browser_id]
    popup = Popups(driver).get_query_builder_not_hidden_popup()
    popup.qos_values_choice()
    Popups(driver).power_select.choose_item_with_id(f"{provider_name}")


@wt(parsers.parse('user of {browser_id} clicks "Add" in "Add QoS condition" popup'))
def click_add_in_add_cond_popup(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    popup = Popups(driver).get_query_builder_not_hidden_popup()
    popup.add_button()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) sees that (?P<number>.*?) "
        r"storages? match(es)? condition in QoS panel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_num_of_matching_storages(
    selenium: SeleniumDrivers, browser_id: str, number: str
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).details_modal.qos
    if number == "no":
        actual = modal.no_storage_matching
        number = "No storage backends match"
    else:
        actual = modal.storage_matching
    assert number == actual, f"{number} storages should match but {actual} matches"


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) sees that matching storages? "
        rf"(is|are) (?P<storages>{ELEMENTS_SEQUENCE_PATTERN})"
    ),
    converters={
        "storages": parse_elements_sequence,
    },
)
def assert_matching_storage(
    selenium: SeleniumDrivers, browser_id: str, storages: list[str], hosts: Hosts
) -> None:
    css_selector = ".storages-matching-info-icon"
    driver = selenium[browser_id]
    expected = []
    for expression in storages:
        [name, provider] = expression.split(" provided by ")
        provider_name = hosts[provider]["name"]
        expected.append(f"{name} provided by {provider_name}")

    scroll_to_css_selector_bottom(driver, css_selector)
    driver.find_element(By.CSS_SELECTOR, css_selector).click()
    compare_matching_storages(driver, expected)
    # unclick element
    driver.find_element(By.CSS_SELECTOR, css_selector).click()


@repeat_failed(timeout=WAIT_FRONTEND)
def compare_matching_storages(driver: WebDriver, expected: list[str]) -> None:
    actual = [elem.text for elem in Popups(driver).storages_matching_popover.storages]
    compare_lists(expected, actual)


def compare_lists(expected: list[str], actual: list[str]) -> None:
    assert len(actual) == len(
        expected
    ), "Expected number of providers does not match actual"
    for val in expected:
        assert val in actual, f"Expected {val} provider not in actual {actual}"


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{operator}" operator in '
        '"Add QoS condition" popup'
    )
)
def choose_operator_in_add_cond_popup(
    selenium: SeleniumDrivers, browser_id: str, operator: str
) -> None:
    driver = selenium[browser_id]
    popup = Popups(driver).get_query_builder_not_hidden_popup()
    getattr(popup, f"{operator.lower()}_operator").click()


@wt(parsers.re(r'user of (?P<browser_id>.*?) sees "(?P<text>.*?)" in QoS panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_error_label_in_qos_modal(
    selenium: SeleniumDrivers, browser_id: str, text: str
) -> None:
    driver = selenium[browser_id]

    assert (
        text in Modals(driver).details_modal.qos.privileges_message
    ), f'Label with "{text}" not found '


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{button}" button is disabled in QoS panel'
    )
)
def assert_button_disabled_in_qos_panel(
    selenium: SeleniumDrivers, browser_id: str, button: str
) -> None:

    driver = selenium[browser_id]
    enabled = getattr(Modals(driver).details_modal.qos, transform(button)).is_enabled()
    assert not enabled, f"{button} is not disabled"


@wt(
    parsers.parse(
        'user of {browser_id} sees "{status}" status in QoS column '
        'for "{item_name}" in {which_browser}'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_qos_status_in_browser(
    selenium: SeleniumDrivers,
    browser_id: str,
    status: str,
    item_name: str,
    which_browser: str,
) -> None:

    driver = selenium[browser_id]
    browser = getattr(OPLoggedIn(driver), transform(which_browser))
    visible_status = getattr(browser.data[item_name], "qos_status")
    error_message = (
        f"status {status} for item {item_name} is not displayed in {which_browser}"
    )
    if status.lower() == "impossible":
        assert "qos-status-impossible" in visible_status.get_attribute(
            "class"
        ), error_message
    elif status.lower() == "fulfilled":
        assert "qos-status-fulfilled" in visible_status.get_attribute(
            "class"
        ), error_message


@wt(
    parsers.parse(
        "user of {browser_id} clicks on status in QoS column "
        'for "{item_name}" in {which_browser}'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_qos_status_in_browser(
    selenium: SeleniumDrivers, browser_id: str, item_name: str, which_browser: str
) -> None:
    driver = selenium[browser_id]
    browser = getattr(OPLoggedIn(driver), transform(which_browser))
    getattr(browser.data[item_name], "qos_status").click()
