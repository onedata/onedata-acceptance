"""This module contains meta steps for operations on tokens in Onezone
using web GUI.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import parsers

from tests.gui.conftest import WAIT_BACKEND
from tests.gui.steps.onezone.access_tokens import (
    click_on_consume_token_in_tokens_oz_page,
    click_on_join_button_on_tokens_page)
from tests.gui.steps.onezone.spaces import click_on_option_in_the_sidebar
from tests.utils.bdd_utils import wt
from tests.utils.utils import repeat_failed


def _paste_token_into_text_field(selenium, browser_id, oz_page, token):
    page = oz_page(selenium[browser_id])['tokens']
    page.input_name = token


@wt(parsers.parse('user of {browser_id} pastes copied token '
                  'into token text field'))
@repeat_failed(timeout=WAIT_BACKEND)
def paste_copied_token_into_text_field(selenium, browser_id, oz_page,
                                       clipboard, displays):
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

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_on_consume_token_in_tokens_oz_page(selenium, browser_id,
                                             oz_page)
    paste_received_token_into_text_field(selenium, browser_id,
                                         oz_page, tmp_memory)
    click_on_join_button_on_tokens_page(selenium, browser_id, oz_page)


@wt(parsers.parse('user of {browser_id} joins group using copied token'))
@wt(parsers.parse('user of {browser_id} joins to harvester in Onezone page'))
def consume_token_from_copied_token(selenium, browser_id, oz_page,
                                    clipboard, displays):
    option = 'Tokens'

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_on_consume_token_in_tokens_oz_page(selenium, browser_id,
                                             oz_page)
    paste_copied_token_into_text_field(selenium, browser_id, oz_page,
                                       clipboard, displays)
    click_on_join_button_on_tokens_page(selenium, browser_id, oz_page)