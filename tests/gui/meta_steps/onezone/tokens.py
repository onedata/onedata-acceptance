"""This module contains meta steps for operations on tokens in Onezone
using web GUI.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import parsers
import yaml

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.onezone.tokens import *
from tests.gui.steps.onezone.spaces import click_on_option_in_the_sidebar
from tests.utils.bdd_utils import wt
from tests.utils.utils import repeat_failed


def _paste_token_into_text_field(selenium, browser_id, oz_page, token):
    page = oz_page(selenium[browser_id])['tokens']
    page.input_name = token


@wt(parsers.parse('user of {browser_id} pastes copied token '
                  'into token text field'))
@repeat_failed(timeout=WAIT_BACKEND)
def paste_copied_token_into_text_field(selenium, browser_id, oz_page, clipboard,
                                       displays):
    token = clipboard.paste(display=displays[browser_id])
    _paste_token_into_text_field(selenium, browser_id, oz_page, token)


@wt(parsers.parse('user of {browser_id} pastes received token '
                  'into token text field'))
def paste_received_token_into_text_field(selenium, browser_id, oz_page,
                                         tmp_memory):
    token = tmp_memory[browser_id]['mailbox']['token']
    _paste_token_into_text_field(selenium, browser_id, oz_page, token)


@wt(parsers.re('user of (?P<browser_id>.*) joins group using received token'))
def consume_received_token(selenium, browser_id, oz_page, tmp_memory):
    option = 'Tokens'

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_on_consume_token_in_tokens_oz_page(selenium, browser_id, oz_page)
    paste_received_token_into_text_field(selenium, browser_id, oz_page,
                                         tmp_memory)
    click_on_join_button_on_tokens_page(selenium, browser_id, oz_page)


@wt(parsers.parse('user of {browser_id} joins group using copied token'))
@wt(parsers.parse('user of {browser_id} joins to harvester in Onezone page'))
def consume_token_from_copied_token(selenium, browser_id, oz_page, clipboard,
                                    displays):
    option = 'Tokens'

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_on_consume_token_in_tokens_oz_page(selenium, browser_id, oz_page)
    paste_copied_token_into_text_field(selenium, browser_id, oz_page, clipboard,
                                       displays)
    click_on_join_button_on_tokens_page(selenium, browser_id, oz_page)


@wt(parsers.parse('user of {browser_id} adds group "{elem_name}" as subgroup '
                  'using copied token'))
@wt(parsers.parse('user of {browser_id} adds space "{elem_name}" to harvester '
                  'using copied token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_element_with_copied_token(selenium, browser_id, elem_name, oz_page,
                                  clipboard, displays, modals):
    option = 'Tokens'

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_on_consume_token_in_tokens_oz_page(selenium, browser_id, oz_page)
    paste_copied_token_into_text_field(selenium, browser_id, oz_page, clipboard,
                                       displays)
    select_member_from_dropdown(selenium, browser_id, elem_name, modals,
                                oz_page)
    click_on_join_button_on_tokens_page(selenium, browser_id, oz_page)


@wt(parsers.parse('user of {browser_id} adds group "{group}" as subgroup '
                  'using received token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_element_with_received_token(selenium, browser_id, group, oz_page,
                                    tmp_memory, modals):
    option = 'Tokens'

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_on_consume_token_in_tokens_oz_page(selenium, browser_id, oz_page)
    paste_received_token_into_text_field(selenium, browser_id, oz_page,
                                         tmp_memory)
    select_member_from_dropdown(selenium, browser_id, group, modals, oz_page)
    click_on_join_button_on_tokens_page(selenium, browser_id, oz_page)


def _create_token_of_type(selenium, browser_id, token_type, oz_page,
                          iteration=None):
    click_on_create_new_token_in_oz_tokens_panel(selenium, browser_id,
                                                        oz_page)
    choose_token_type_to_create(selenium, browser_id, oz_page, token_type)
    if token_type == 'invite':
        invite_type = 'Register Oneprovider'
        choose_invite_type_in_oz_token_page(selenium, browser_id, oz_page,
                                            invite_type)
    if iteration:
        append_token_name_in_create_token_page(selenium, browser_id, oz_page,
                                               str(iteration))
    click_create_token_button_in_create_token_page(selenium, browser_id,
                                                   oz_page)


@wt(parsers.re('user of (?P<browser_id>.*?) creates (?P<number>\d*?) '
               '(?P<token_type>.*?) tokens?'))
def create_number_of_typed_token(selenium, browser_id, number: int, token_type,
                                 oz_page):
    for i in range(number):
        _create_token_of_type(selenium, browser_id, token_type, oz_page, i)


@wt(parsers.parse('user of {browser_id} creates invite token with following '
                  'configuration:\n{config}'))
def create_invite_token_with_config(selenium, browser_id, config, oz_page,
                                    popups, users):
    token_type = 'invite'

    click_on_create_new_token_in_oz_tokens_panel(selenium, browser_id, oz_page)
    choose_token_type_to_create(selenium, browser_id, oz_page, token_type)

    data = yaml.load(config)
    invite_type = data['invite type']
    invite_target = data['invite target']
    usage_limit = data['usage limit']
    caveats = data['caveats']

    choose_invite_type_in_oz_token_page(selenium, browser_id, oz_page,
                                        invite_type)
    choose_invite_select(selenium, browser_id, oz_page, invite_target)
    select_token_usage_limit(selenium, browser_id, usage_limit, oz_page)
    _set_tokens_caveats(selenium, browser_id, oz_page, caveats, popups, users)


def _set_tokens_caveats(selenium, browser_id, oz_page, caveats, popups, users):
    expand_caveats(selenium, browser_id, oz_page)
    consumer_caveats = caveats.get('consumer', False)
    if consumer_caveats:
        _set_consumer_caveats(selenium, browser_id, popups, consumer_caveats,
                              oz_page, users)


def _set_consumer_caveats(selenium, browser_id, popups, consumer_caveats,
                          oz_page, users):
    caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'consumer')
    caveat.activate()
    for consumer in consumer_caveats:
        consumer_type = consumer.get('type')
        method = consumer.get('by')
        value = consumer.get('value')
        if method == 'id':
            value = users[value].id
        caveat.new_item()
        set_consumer_in_consumer_caveat(selenium, browser_id, popups,
                                        consumer_type, method, value)
