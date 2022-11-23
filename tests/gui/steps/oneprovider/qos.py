"""Steps implementation for quality of service GUI tests.
"""

__author__ = "Michal Dronka, Natalia Organek"
__copyright__ = "Copyright (C) 2020-2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from pytest_bdd import parsers
from selenium.common.exceptions import NoSuchElementException

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.rest.provider import get_provider_id
from tests.gui.utils.core import scroll_to_css_selector_bottom
from tests.gui.utils.generic import parse_seq
from tests.utils.bdd_utils import wt
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} deletes all QoS requirements'))
@repeat_failed(timeout=WAIT_FRONTEND)
def delete_all_qualities_of_service(selenium, browser_id, modals, popups):
    driver = selenium[browser_id]
    modal = modals(driver).details_modal.qos
    while len(modal.requirements):
        modal.requirements[0].delete.click()
        popups(driver).delete_qos_popup.confirm.click()


@wt(parsers.parse('user of {browser_id} sees that all QoS requirements are '
                  '{state}'))
@repeat_failed(interval=1, timeout=90,
               exceptions=(NoSuchElementException, RuntimeError))
def assert_all_qualities_of_service_are_fulfilled(selenium, browser_id,
                                                  modals, state):
    driver = selenium[browser_id]
    modal = modals(driver).details_modal.qos
    for requirement in modal.requirements:
        assert hasattr(requirement, state), (f'No all QoS requirements are '
                                             f'{state}')


@wt(parsers.parse('user of {browser_id} sees that replicas number is equal '
                  '{number} in QoS panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_replicas_number_in_qualities_of_service_modal(selenium, browser_id,
                                                         modals, number):
    driver = selenium[browser_id]
    replicas_number = modals(driver).details_modal.qos.replicas_number
    assert number == replicas_number, (f'Found {replicas_number} instead '
                                       f'of {number} replicas number')


def process_storage_expression(expression, hosts):
    split_expression = expression.split('@')
    if len(split_expression) == 1:
        return expression
    provider = split_expression[1]
    provider_name = hosts[provider]['name']
    return f'{split_expression[0]}@{provider_name}'


def process_provider_expression(expression, hosts, users):
    split_expression = expression.split(' is ')
    if len(split_expression) == 1:
        return expression
    provider = split_expression[1]
    provider_name = hosts[provider]['name']
    provider_id = get_provider_short_id(provider, hosts, users)
    return f'{split_expression[0]} is {provider_name} #{provider_id}'


def get_provider_short_id(provider, hosts, users):
    visible_id_index = 6
    return get_provider_id(provider, hosts, users)[:visible_id_index]


def process_expression(expression, hosts, users):
    split_expression = expression.split(' is')
    if len(split_expression) == 1:
        return expression
    domain = split_expression[0]
    if domain == 'storage':
        return process_storage_expression(expression, hosts)
    elif domain == 'provider':
        return process_provider_expression(expression, hosts, users)


@wt(parsers.parse('user of {browser_id} sees [{expression}] QoS requirement '
                  'in QoS panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_expression_in_qos_panel(selenium, browser_id, modals, expression,
                                   hosts, users):
    driver = selenium[browser_id]
    requirements = modals(driver).details_modal.qos.requirements
    ready_expression = process_expression(expression, hosts, users)
    for requirement in requirements:
        expression_in_modal = requirement.expression.replace('\n', ' ')
        if expression_in_modal == ready_expression:
            assert True
            return
    assert False, (f'Not found "{expression}" QoS requirement '
                   f'in modal "Quality of Service"')


def process_whole_nested_expression(expression, hosts, users):
    plain_exp = expression.replace('[', '').replace(']', '')
    provider1 = 'oneprovider-1'
    provider2 = 'oneprovider-2'
    provider1_name = hosts[provider1]['name']
    provider2_name = hosts[provider2]['name']
    provider1_id = get_provider_short_id(provider1, hosts, users)
    provider2_id = get_provider_short_id(provider2, hosts, users)

    plain_exp = plain_exp.replace('@oneprovider-1', f'@{provider1_name}')
    plain_exp = plain_exp.replace('@oneprovider-2', f'@{provider2_name}')
    plain_exp = plain_exp.replace('oneprovider-1', f'{provider1_name} '
                                                   f'#{provider1_id}')
    plain_exp = plain_exp.replace('oneprovider-2', f'{provider2_name} '
                                                   f'#{provider2_id}')
    return plain_exp


@wt(parsers.parse('user of {browser_id} sees nested QoS requirement '
                  'in QoS panel:\n{expression}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_nested_expression_in_qos_panel(selenium, browser_id, modals,
                                          expression, hosts, users):
    driver = selenium[browser_id]
    requirements = modals(driver).details_modal.qos.requirements
    ready_expression = process_whole_nested_expression(expression, hosts, users)

    for requirement in requirements:
        expression_in_modal = requirement.expression.replace('\n', ' ')
        if expression_in_modal == ready_expression:
            assert True
            return
    assert False, (f'Not found "{ready_expression}" QoS requirement '
                   f'in modal "Quality of Service"')


@wt(parsers.parse('user of {browser_id} doesn\'t see any QoS requirement '
                  'in QoS panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_no_expression_in_qualities_of_service_modal(selenium, browser_id,
                                                       modals):
    driver = selenium[browser_id]
    try:
        modals(driver).details_modal.qos.requirements
    except RuntimeError:
        assert True
    else:
        assert False, 'Found QoS requirement in modal "Quality of Service"'


@wt(parsers.parse('user of {browser_id} clicks "enter as text" label in '
                  'QoS panel'))
def click_enter_as_text_link(selenium, browser_id, modals):
    driver = selenium[browser_id]
    modals(driver).details_modal.qos.enter_as_text()


@wt(parsers.parse('user of {browser_id} confirms entering expression in '
                  'expression text field in QoS panel'))
def confirm_entering_text(selenium, browser_id, modals):
    driver = selenium[browser_id]
    modals(driver).details_modal.qos.confirm_text()


@wt(parsers.parse('user of {browser_id} clicks on add query block icon in '
                  'QoS panel'))
def click_add_query_block(selenium, browser_id, modals):
    driver = selenium[browser_id]
    modal = modals(driver).details_modal.qos.query_builder
    modal.another_block_buttons[0].click()


@wt(parsers.parse('user of {browser_id} clicks on {number} from the left add '
                  'query block icon in QoS panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def start_query_block_no(selenium, browser_id, modals, number):
    driver = selenium[browser_id]
    no = int(number.split()[0])
    modal = modals(driver).details_modal.qos.query_builder
    modal.another_block_buttons[no-1].click()


@wt(parsers.parse('user of {browser_id} chooses "{property_name}" property in '
                  '"Add QoS condition" popup'))
def choose_property_in_add_condition_popup(selenium, browser_id,
                                           property_name, popups):
    driver = selenium[browser_id]
    popup = popups(driver).get_query_builder_not_hidden_popup()
    popup.choose_property(property_name)


@wt(parsers.parse('user of {browser_id} chooses value of "{item}" at '
                  '"{provider}" in "Add QoS condition" popup'))
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_value_of_item_at_provider_in_add_cond_popup(selenium, browser_id,
                                                       popups, item,
                                                       provider, hosts):
    provider_name = hosts[provider]['name']
    driver = selenium[browser_id]
    popup = popups(driver).get_query_builder_not_hidden_popup()
    popup.qos_values_choice()
    popups(driver).power_select.choose_item(f'{item} @{provider_name}')


@wt(parsers.re('user of (?P<browser_id>.*?) sees (?P<providers>.*?) '
               'providers? on values list in "Add QoS condition" popup'))
def assert_list_of_providers_in_add_cond_popup(selenium, browser_id,
                                               providers, hosts, popups):
    expected = [hosts[provider]['name'] for provider in parse_seq(providers)]

    driver = selenium[browser_id]
    popup = popups(driver).get_query_builder_not_hidden_popup()
    popup.qos_values_choice()
    actual = [v.text.split(' #')[0] for v in popups(driver).power_select.items]
    compare_lists(expected, actual)


@wt(parsers.re('user of (?P<browser_id>.*?) sees (?P<storages>.*?) '
               'storages? on values list in "Add QoS condition" popup'))
def assert_list_of_storages_in_add_cond_popup(selenium, browser_id,
                                              storages, hosts, popups):
    expected_expressions = parse_seq(storages)
    expected = []
    for expression in expected_expressions:
        [name, provider] = expression.split(' @')
        provider_name = hosts[provider]['name']
        expected.append(f'{name} @{provider_name}')

    driver = selenium[browser_id]
    popup = popups(driver).get_query_builder_not_hidden_popup()
    popup.qos_values_choice()
    actual = [v.text for v in popups(driver).power_select.items]
    compare_lists(expected, actual)


@wt(parsers.parse('user of {browser_id} chooses value of '
                  '"{provider}" provider in "Add QoS condition" popup'))
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_value_of_provider_item_in_add_cond_popup(selenium, browser_id,
                                                    popups, provider, hosts):
    provider_name = hosts[provider]['name']
    driver = selenium[browser_id]
    popup = popups(driver).get_query_builder_not_hidden_popup()
    popup.qos_values_choice()
    popups(driver).power_select.choose_item_with_id(f'{provider_name}')


@wt(parsers.parse('user of {browser_id} clicks "Add" in "Add QoS condition" '
                  'popup'))
def click_add_in_add_cond_popup(selenium, browser_id, popups):
    driver = selenium[browser_id]
    popup = popups(driver).get_query_builder_not_hidden_popup()
    popup.add_button()


@wt(parsers.re('user of (?P<browser_id>.*?) sees that (?P<number>.*?) '
               'storages? match(es)? condition in QoS panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_num_of_matching_storages(selenium, browser_id, number, modals):
    driver = selenium[browser_id]
    modal = modals(driver).details_modal.qos
    if number == 'no':
        actual = modal.no_storage_matching
        number = 'No storages match'
    else:
        actual = modal.storage_matching
    assert number == actual, (f'{number} storages should match but {actual} '
                              f'matches')


@wt(parsers.re('user of (?P<browser_id>.*?) sees that matching storages? '
               '(is|are) (?P<storages>.+)'))
def assert_matching_storage(selenium, browser_id, storages, hosts, popups):
    css_sel = '.storages-matching-info-icon'
    driver = selenium[browser_id]
    expected_expressions = parse_seq(storages)
    expected = []
    for expression in expected_expressions:
        [name, provider] = expression.split(' provided by ')
        provider_name = hosts[provider]['name']
        expected.append(f'{name} provided by {provider_name}')

    scroll_to_css_selector_bottom(driver, css_sel)
    driver.find_element_by_css_selector(css_sel).click()

    actual = [elem.text for elem in popups(
        driver).storages_matching_popover.storages]
    compare_lists(expected, actual)


def compare_lists(expected, actual):
    assert len(actual) == len(expected), ('Expected number of providers does '
                                          'not match actual')
    for val in expected:
        assert val in actual, f'Expected {val} provider not in actual'


@wt(parsers.parse('user of {browser_id} chooses "{operator}" operator in '
                  '"Add QoS condition" popup'))
def choose_operator_in_add_cond_popup(selenium, browser_id, popups, operator):
    driver = selenium[browser_id]
    popup = popups(driver).get_query_builder_not_hidden_popup()
    getattr(popup, f'{operator.lower()}_operator').click()


@wt(parsers.re('user of (?P<browser_id>.*?) sees "(?P<text>.*?)" in QoS '
               'panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_error_label_in_qos_modal(selenium, browser_id, modals, text):
    driver = selenium[browser_id]

    assert text in modals(driver).details_modal.qos.privileges_error, \
        f'Label with "{text}" not found '
