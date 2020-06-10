"""This module contains meta steps for operations on tokens in Onezone
using web GUI.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import parsers

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
def paste_received_token_into_text_field(selenium, browser_id,
                                         oz_page, tmp_memory):
    token = tmp_memory[browser_id]['mailbox']['token']
    _paste_token_into_text_field(selenium, browser_id, oz_page, token)


@wt(parsers.re('user of (?P<browser_id>.*) joins group using received token'))
def consume_received_token(selenium, browser_id, oz_page, tmp_memory):
    option = 'Tokens'
    button = 'Consume token'

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_on_button_in_tokens_sidebar(selenium, browser_id, oz_page, button)
    paste_received_token_into_text_field(selenium, browser_id, oz_page,
                                         tmp_memory)
    click_on_join_button_on_tokens_page(selenium, browser_id, oz_page)


@wt(parsers.parse('user of {browser_id} joins group using copied token'))
@wt(parsers.parse('user of {browser_id} joins to harvester in Onezone page'))
def consume_token_from_copied_token(selenium, browser_id, oz_page, clipboard,
                                    displays):
    option = 'Tokens'
    button = 'Consume token'

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_on_button_in_tokens_sidebar(selenium, browser_id, oz_page, button)
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
    button = 'Consume token'

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_on_button_in_tokens_sidebar(selenium, browser_id, oz_page, button)
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
    button = 'Consume token'

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_on_button_in_tokens_sidebar(selenium, browser_id, oz_page, button)
    paste_received_token_into_text_field(selenium, browser_id, oz_page,
                                         tmp_memory)
    select_member_from_dropdown(selenium, browser_id, group, modals, oz_page)
    click_on_join_button_on_tokens_page(selenium, browser_id, oz_page)


def _create_token_of_type(selenium, browser_id, token_type, oz_page,
                          iteration=None):
    button = 'Create new token'
    token_name = f'{token_type}_token'
    if iteration:
        token_name = token_name + str(iteration)

    click_on_button_in_tokens_sidebar(selenium, browser_id, oz_page, button)
    type_new_token_name(selenium, browser_id, oz_page, token_name)
    choose_token_type_to_create(selenium, browser_id, oz_page, token_type)
    if token_type == 'invite':
        invite_type = 'Register Oneprovider'
        choose_invite_type_in_oz_token_page(selenium, browser_id, oz_page,
                                            invite_type)
    click_create_token_button_in_create_token_page(selenium, browser_id,
                                                   oz_page)


@wt(parsers.re('user of (?P<browser_id>.*?) creates (?P<number>\d*?) '
               '(?P<token_type>.*?) tokens?'))
def create_number_of_typed_token(selenium, browser_id, number: int, token_type,
                                 oz_page):
    for i in range(number):
        _create_token_of_type(selenium, browser_id, token_type, oz_page, i)
