"""This module contains gherkin steps to run acceptance tests in web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from tests.gui.utils.generic import transform
from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.utils import repeat_failed
from tests.utils.bdd_utils import given, when, then, wt, parsers


@repeat_failed(attempts=WAIT_FRONTEND)
def _enter_text(input_box, text):
    input_box.clear()
    input_box.send_keys(text)
    if input_box.get_attribute('value') != text:
        raise RuntimeError('entering "{}" to input box failed'.format(text))


@wt(parsers.parse('user of {browser_id} types "{text}" on keyboard'))
def type_string_into_active_element(selenium, browser_id, text):
    _enter_text(selenium[browser_id].switch_to.active_element, text)


@wt(parsers.parse('user of {browser_id} types received '
                    '{item_type} on keyboard'))
def type_item_into_active_element(selenium, browser_id, item_type,
                                  tmp_memory):
    item = tmp_memory[browser_id]['mailbox'][item_type]
    _enter_text(selenium[browser_id].switch_to.active_element, item)


@wt(parsers.parse('user of {browser_id} presses enter on keyboard'))
def press_enter_on_active_element(selenium, browser_id):
    driver = selenium[browser_id]
    driver.switch_to.active_element.send_keys(Keys.RETURN)


@wt(parsers.parse('user of {browser_id} presses tab on keyboard'))
def press_tab_on_active_element(selenium, browser_id):
    driver = selenium[browser_id]
    driver.switch_to.active_element.send_keys(Keys.TAB)


@wt(parsers.parse('user of {browser_id} presses backspace on keyboard'))
def press_backspace_on_active_element(selenium, browser_id):
    driver = selenium[browser_id]
    driver.switch_to.active_element.send_keys(Keys.BACKSPACE)


@wt(parsers.parse('user of {browser_id} should see that the page title '
                  'contains "{text}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def title_contains(selenium, browser_id, text):
    page_title = selenium[browser_id].title
    assert text in page_title, \
        '{} page title should contain {}'.format(page_title, text)


@wt(parsers.re('users? of (?P<browser_id_list>.*) clicks on '
               '"(?P<btn_name>.+?)" button in "(?P<popup>.+?)" popup'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_btn_in_popup(selenium, browser_id, btn, popup, popups):
    getattr(popups(selenium[browser_id]),
            transform(popup)).buttons[btn].click()


@given(parsers.re('users? of (?P<browser_id_list>.*) clicked on '
                  '"(?P<btn_name>.+?)" button in "(?P<popup>.+?)" popup'))
@repeat_failed(timeout=WAIT_FRONTEND)
def g_click_on_btn_in_popup(selenium, browser_id, btn, popup, popups):
    getattr(popups(selenium[browser_id]),
            transform(popup)).buttons[btn].click()


@wt(parsers.re('pass'))
def pass_test():
    pass


@repeat_failed(interval=1, timeout=90, exceptions=NoSuchElementException)
def switch_to_iframe(selenium, browser_id, selector=None):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    iframe = driver.find_element_by_tag_name('iframe')
    driver.switch_to.frame(iframe)

