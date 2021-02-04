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
from tests.utils.bdd_utils import wt
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} deletes all QoS requirements'))
@repeat_failed(timeout=WAIT_FRONTEND)
def delete_all_qualities_of_service(selenium, browser_id, modals, popups):
    driver = selenium[browser_id]
    modal = modals(driver).quality_of_service
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
    modal = modals(driver).quality_of_service
    for requirement in modal.requirements:
        assert hasattr(requirement, state), (f'No all QoS requirements are '
                                             f'{state}')


@wt(parsers.parse('user of {browser_id} sees that replicas number is equal '
                  '{number} in modal "Quality of Service"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_replicas_number_in_qualities_of_service_modal(selenium, browser_id,
                                                         modals, number):
    driver = selenium[browser_id]
    replicas_number = modals(driver).quality_of_service.replicas_number
    assert number == replicas_number, (f'Found {replicas_number} instead '
                                       f'of {number} replicas number')


def process_storage_expression(expression, hosts):
    split_expression = expression.split('@')
    if len(split_expression) == 1:
        return expression
    provider = split_expression[1].strip('/')
    provider_name = hosts[provider]['name']
    return f'{split_expression[0]}@{provider_name}'


def process_provider_expression(expression, hosts, users):
    split_expression = expression.split(' is ')
    if len(split_expression) == 1:
        return expression
    provider = split_expression[1].strip('/')
    provider_name = hosts[provider]['name']
    provider_id = get_provider_id(provider, hosts, users)[:6]
    return f'{split_expression[0]} is {provider_name} #{provider_id}'


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
                  'in modal "Quality of Service"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_expression_in_quality_of_service_modal(selenium, browser_id,
                                                  modals, expression, hosts,
                                                  users):
    driver = selenium[browser_id]
    requirements = modals(driver).quality_of_service.requirements
    ready_expression = process_expression(expression, hosts, users)
    for requirement in requirements:
        expression_in_modal = requirement.expression.replace('\n', ' ')
        if expression_in_modal == ready_expression:
            assert True
            return
    assert False, (f'Not found "{expression}" QoS requirement '
                   f'in modal "Quality of Service"')


def process_operand_expression(expression, hosts, users, operand):
    split_expression = expression.split(operand)
    processed = [process_nested_expression(exp, hosts, users) for exp in
                 split_expression]
    return operand.join(processed)


def process_and_expression(expression, hosts, users):
    return process_operand_expression(expression, hosts, users, ' AND ')


def process_or_expression(expression, hosts, users):
    return process_operand_expression(expression, hosts, users, ' OR ')


def process_except_expression(expression, hosts, users):
    return process_operand_expression(expression, hosts, users, ' EXCEPT ')


def process_nested_expression(expression, hosts, users):
    and_index = expression.find('AND')
    and_index = and_index if and_index > 0 else len(expression)
    or_index = expression.find('OR')
    or_index = or_index if or_index > 0 else len(expression)
    except_index = expression.find('EXCEPT')
    except_index = except_index if except_index > 0 else len(expression)

    # only possibility that they are equal is that none operand was found
    if and_index == or_index == except_index:
        return process_expression(expression, hosts, users)
    min_index = min(and_index, or_index, except_index)
    if min_index == and_index:
        return process_and_expression(expression, hosts, users)
    elif min_index == or_index:
        return process_or_expression(expression, hosts, users)
    elif min_index == except_index:
        return process_except_expression(expression, hosts, users)


def process_whole_nested_expression(expression, hosts, users):
    plain_expression = expression.replace('[', '').replace(']', '')
    return process_nested_expression(plain_expression, hosts, users)


# to process such expressions, parser would be needed so this only processes
# expressions with assumptions:
# -- there is only one level of the same operand (e.g.
# [...AND... [...AND...]...] is forbidden)
# -- first operand for the left is the highest level operand
# also, this function does not check proper nesting - this belongs to gui
@wt(parsers.parse('user of {browser_id} sees nested QoS requirement '
                  'in modal "Quality of Service":\n{expression}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_nested_expression_in_quality_of_service_modal(selenium, browser_id,
                                                         modals, expression,
                                                         hosts, users):
    driver = selenium[browser_id]
    requirements = modals(driver).quality_of_service.requirements
    ready_expression = process_whole_nested_expression(expression, hosts, users)

    for requirement in requirements:
        expression_in_modal = requirement.expression.replace('\n', ' ')
        if expression_in_modal == ready_expression:
            assert True
            return
    assert False, (f'Not found "{expression}" QoS requirement '
                   f'in modal "Quality of Service"')


@wt(parsers.parse('user of {browser_id} doesn\'t see any QoS requirement '
                  'in modal "Quality of Service"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_no_expression_in_qualities_of_service_modal(selenium, browser_id,
                                                       modals):
    driver = selenium[browser_id]
    try:
        modals(driver).quality_of_service.requirements
    except RuntimeError:
        assert True
    else:
        assert False, 'Found QoS requirement in modal "Quality of Service"'


@wt(parsers.parse('user of {browser_id} clicks "enter as text" label in '
                  '"Quality of Service" modal'))
def click_enter_as_text_link(selenium, browser_id, modals):
    driver = selenium[browser_id]
    modals(driver).quality_of_service.enter_as_text()


@wt(parsers.parse('user of {browser_id} confirms entering expression in '
                  'expression text field in modal "Quality of Service"'))
def confirm_entering_text(selenium, browser_id, modals):
    driver = selenium[browser_id]
    modals(driver).quality_of_service.confirm_text()


@wt(parsers.parse('user of {browser_id} clicks on add query block icon in '
                  'modal "Quality of Service"'))
def click_add_query_block(selenium, browser_id, modals):
    driver = selenium[browser_id]
    modal = modals(driver).quality_of_service.query_builder
    modal.another_block_buttons[0].click()


@wt(parsers.parse('user of {browser_id} clicks on {number} from the left add '
                  'query block icon in modal "Quality of Service"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def start_query_block_no(selenium, browser_id, modals, number):
    driver = selenium[browser_id]
    no = int(number.split()[0])
    modal = modals(driver).quality_of_service.query_builder
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
def choose_value_of_item_at_provider_in_add_cond_popup(selenium, browser_id,
                                                       popups, item,
                                                       provider, hosts):
    provider_name = hosts[provider]['name']
    driver = selenium[browser_id]
    popup = popups(driver).get_query_builder_not_hidden_popup()
    popup.qos_values_choice()
    popups(driver).power_select.choose_item(f'{item} @{provider_name}')


@wt(parsers.parse('user of {browser_id} chooses value of "{provider}" provider '
                  'in "Add QoS condition" popup'))
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


@wt(parsers.parse('user of {browser_id} sees that {number} storage matches '
                  'condition in modal "Quality of Service"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_num_of_matching_storages(selenium, browser_id, number, modals):
    driver = selenium[browser_id]
    modal = modals(driver).quality_of_service
    if number == 'no':
        actual = modal.no_storage_matching
        number = 'No storages match'
    else:
        actual = modal.storage_matching
    assert number == actual, (f'{number} storages should match but {actual} '
                              f'matches')


@wt(parsers.parse('user of browser_unified chooses "{operator}" operator in '
                  '"Add QoS condition" popup'))
def choose_operator_in_add_cond_popup(selenium, browser_id, popups, operator):
    driver = selenium[browser_id]
    popup = popups(driver).get_query_builder_not_hidden_popup()
    getattr(popup, f'{operator.lower()}_operator').click()
