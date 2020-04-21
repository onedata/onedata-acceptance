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


def _click_on_btn_for_token(driver, oz_page, ordinal, btn):
    action = btn + '_token'
    oz_page(driver)['tokens'].elements_list[int(ordinal[:-2]) - 1].click()
    getattr(oz_page(driver)['tokens'], action).click()


@given(parsers.re(r'user of (?P<browser_id>.*?) clicked on (?P<btn>copy|remove) '
                  r'icon for (?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|'
                  r'\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) '
                  r'item on tokens list in tokens sidebar'))
@repeat_failed(timeout=WAIT_BACKEND)
def g_click_on_btn_for_oz_access_token(selenium, browser_id, btn,
                                       ordinal, oz_page):
    driver = selenium[browser_id]
    _click_on_btn_for_token(driver, oz_page, ordinal, btn)


@when(parsers.re(r'user of (?P<browser_id>.*?) clicks on (?P<btn>copy|remove) '
                 r'button for (?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|'
                 r'\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) '
                 r'item on tokens list in tokens page'))
@then(parsers.re(r'user of (?P<browser_id>.*?) clicks on (?P<btn>copy|remove) '
                 r'button for (?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|'
                 r'\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) '
                 r'item on tokens list in tokens page'))
@repeat_failed(timeout=WAIT_BACKEND)
def wt_click_on_btn_for_oz_access_token(selenium, browser_id, btn,
                                        ordinal, oz_page):
    driver = selenium[browser_id]
    _click_on_btn_for_token(driver, oz_page, ordinal, btn)


@given(parsers.parse(r'user of {browser_id} recorded copied access token '
                     r'for future use'))
@repeat_failed(timeout=WAIT_BACKEND)
def g_record_copied_access_token(browser_id, tmp_memory, displays, clipboard):
    token = clipboard.paste(display=displays[browser_id])
    tmp_memory[browser_id]['access_token'] = token


@when(parsers.re(r'user of (?P<browser_id>.+?) sees that token for '
                 r'(?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|'
                 r'\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) '
                 r'item on tokens list in tokens sidebar '
                 r'has been copied correctly'))
@then(parsers.re(r'user of (?P<browser_id>.+?) sees that token for '
                 r'(?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|'
                 r'\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) '
                 r'item on tokens list in tokens sidebar '
                 r'has been copied correctly'))
def assert_oz_access_token_has_been_copied_correctly(selenium, browser_id,
                                                     ordinal, oz_page,
                                                     displays, clipboard):
    driver = selenium[browser_id]
    oz_page(driver)['tokens'].elements_list[int(ordinal[:-2]) - 1].click()
    val = oz_page(driver)['tokens'].token
    copied_val = clipboard.paste(display=displays[browser_id])
    assert val == copied_val, 'Access Token has been copied incorrectly. ' \
                              'Expected {}, got {}'.format(val, copied_val)


@when(parsers.parse('user of {browser_id} sees exactly {expected_num:d} item(s) '
                    'on tokens list in tokens sidebar'))
@then(parsers.parse('user of {browser_id} sees exactly {expected_num:d} item(s) '
                    'on tokens list in tokens sidebar'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_oz_access_tokens_list_has_num_tokens(selenium, browser_id,
                                                expected_num, oz_page):
    driver = selenium[browser_id]
    displayed_tokens_num = len(oz_page(driver)['tokens'].elements_list)
    assert displayed_tokens_num == expected_num, \
        ('Displayed number of tokens in ACCESS TOKENS oz panel: {seen} '
         'instead of excepted: {excepted}'.format(seen=displayed_tokens_num,
                                                  excepted=expected_num))


@when(parsers.parse('user of {browser_id} clicks on "Create new '
                    'token" button in tokens sidebar'))
@then(parsers.parse('user of {browser_id} clicks on "Create new '
                    'token" button in tokens sidebar'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_create_new_token_in_oz_access_tokens_panel(selenium, browser_id,
                                                        oz_page):
    oz_page(selenium[browser_id])['tokens'].create_token()


@wt(parsers.parse('user of {browser_id} clicks on "Consume token" button '
                  'in tokens sidebar'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_consume_token_in_tokens_oz_page(selenium, browser_id,
                                             oz_page):
    oz_page(selenium[browser_id])['tokens'].consume_token()


@given(parsers.parse('user of {browser_id} created and recorded access token '
                     'for later use with CDMI API'))
@repeat_failed(timeout=WAIT_BACKEND)
def create_and_record_access_token_for_cdmi(selenium, browser_id,
                                            oz_page, tmp_memory,
                                            displays, clipboard):
    driver = selenium[browser_id]
    panel = oz_page(driver)['access tokens']
    panel.expand()

    with implicit_wait(driver, 0.05, SELENIUM_IMPLICIT_WAIT):
        if panel.tokens.count() > 0:
            panel.tokens[0].copy()
        else:
            panel.create_new_access_token()
            now = time.time()
            time_limit = now + 10
            while now < time_limit:
                try:
                    panel.tokens[0].copy()
                except (RuntimeError, Exception) as ex:
                    print(ex)
                    now = time.time()
                else:
                    break
            else:
                raise RuntimeError("couldn't create and copy "
                                   "access token in oz")
    token = clipboard.paste(display=displays[browser_id])
    tmp_memory[browser_id]['access_token'] = token


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

