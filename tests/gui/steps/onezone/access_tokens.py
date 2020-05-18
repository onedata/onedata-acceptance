"""This module contains gherkin steps to run acceptance tests featuring
access tokens management in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


import time

from pytest_bdd import given, when, then, parsers

from tests.gui.conftest import WAIT_BACKEND, SELENIUM_IMPLICIT_WAIT
from tests.gui.utils.generic import implicit_wait
from tests.utils.bdd_utils import wt
from tests.utils.utils import repeat_failed

def get_token_by_ordinal(oz_page, ordinal, driver):
    return oz_page(driver)['tokens'].sidebar.tokens[int(ordinal[:-2]) - 1]

def _open_menu_for_token(driver, oz_page, ordinal):
    get_token_by_ordinal(oz_page, ordinal, driver).menu_button.click()


def _click_option_for_token_row_menu(driver, option, popups):
    popups(driver).token_row_menu.menu[option.capitalize()]()


def _click_on_btn_for_token(driver, oz_page, ordinal, btn, modals):
    _open_menu_for_token(driver, oz_page, ordinal)
    _click_option_for_token_row_menu(driver, btn, modals)


@wt(parsers.re(r'user of (?P<browser_id>.*?) clicks on (?P<btn>rename|remove) '
               r'button for (?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|'
               r'\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) '
               r'item on tokens list in tokens page'))
@repeat_failed(timeout=WAIT_BACKEND)
def wt_click_on_btn_for_oz_token(selenium, browser_id, btn,
                                        ordinal, oz_page, popups):
    driver = selenium[browser_id]
    _click_on_btn_for_token(driver, oz_page, ordinal, btn, popups)


@wt(parsers.parse('user of {browser_id} sees that token '
                  'has been copied correctly'))
def assert_oz_access_token_has_been_copied_correctly(selenium, browser_id,
                                                     ordinal, oz_page,
                                                     displays, clipboard):
    driver = selenium[browser_id]
    val = oz_page(driver)['tokens'].token
    copied_val = clipboard.paste(display=displays[browser_id])
    assert val == copied_val, (f'Token has been copied incorrectly. '
                               f'Expected {val}, got {copied_val}')


@wt(parsers.parse('user of {browser_id} sees exactly {expected_num:d} item(s) '
                  'on tokens list in tokens sidebar'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_oz_access_tokens_list_has_num_tokens(selenium, browser_id,
                                                expected_num, oz_page):
    driver = selenium[browser_id]
    displayed_tokens_num = len(oz_page(driver)['tokens'].sidebar.tokens)
    assert displayed_tokens_num == expected_num, \
        (f'Displayed number of tokens in TOKENS oz panel: {displayed_tokens_num}'
         f' instead of excepted: {expected_num}')


@wt(parsers.parse('user of {browser_id} clicks on create new token '
                  'button in tokens sidebar'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_create_new_token_in_oz_access_tokens_panel(selenium, browser_id,
                                                        oz_page):
    oz_page(selenium[browser_id])['tokens'].sidebar.create_token()


@wt(parsers.parse('user of {browser_id} clicks on "Consume token" button '
                  'in tokens sidebar'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_consume_token_in_tokens_oz_page(selenium, browser_id,
                                             oz_page):
    oz_page(selenium[browser_id])['tokens'].sidebar.consume_token()


@wt(parsers.parse('user of {browser_id} clicks on Join button '
                  'on consume token page'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_join_button_on_tokens_page(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['tokens'].join_button()


@wt(parsers.parse('user of {browser_id} chooses "{member_name}" {type} '
                  'from dropdown on tokens page'))
@repeat_failed(timeout=WAIT_BACKEND)
def select_member_from_dropdown(selenium, browser_id, member_name,
                                modals, oz_page):
    driver = selenium[browser_id]

    oz_page(driver)['tokens'].expand_dropdown()
    modals(driver).dropdown.options[member_name].click()


@wt(parsers.parse('user of {browser_id} clicks on "Create token" button '
                  'in "Create new token" view'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_create_token_button_in_create_token_page(selenium, browser_id,
                                                   oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['tokens'].create_token_page.create_token()


@wt(parsers.parse('user of {browser_id} chooses {token_type} token type in '
                  '"Create new token" view'))
def choose_token_type_to_create(selenium, browser_id, oz_page, token_type):
    driver = selenium[browser_id]
    option = f'{token_type}_option'
    getattr(oz_page(driver)['tokens'].create_token_page, option).click()


@wt(parsers.re(r'user of (?P<browser_id>.*?) clicks on '
               r'(?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|'
               r'\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) '
               r'item on tokens list in tokens sidebar'))
def click_on_token_in_sidebar_by_ordinal(selenium, browser_id, oz_page,
                                         ordinal):
    driver = selenium[browser_id]
    get_token_by_ordinal(oz_page, ordinal, driver).click()


@wt(parsers.parse('user of {browser_id} clicks on copy button in token view'))
def click_copy_button_in_token_view(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['tokens'].copy_token()


@wt(parsers.parse('user of {browser_id} chooses "{invite_type}" invite type'))
def choose_invite_type_in_oz_token_page(selenium, browser_id, oz_page,
                                        invite_type):
    driver = selenium[browser_id]
    new_token_page = oz_page(driver)['tokens'].create_token_page
    new_token_page.expand_invite_type_dropdown()
    new_token_page.invite_types[invite_type].click()


#TODO to nie działa
@wt(parsers.parse(r'user of (?P<browser_id>.*?) sees that '
                  r'(?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|'
                  r'\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) '
                  r'token type is (?P<token_type>.*?)'))
def assert_token_is_type(selenium, browser_id, token_type, oz_page, ordinal):
    driver = selenium[browser_id]
    token = get_token_by_ordinal(oz_page, ordinal, driver)
    assert token.is_type_of(token_type), (f'Token should be type of '
                                          f'{token_type} but is not')
