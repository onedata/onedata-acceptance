"""This module contains gherkin steps to run acceptance tests featuring
ember notifies in web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import re

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import staleness_of
from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.utils.generic import suppress
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        "user of {browser_id} sees an {notify_type} notify "
        "with text matching to: {text_regexp}"
    )
)
@repeat_failed(timeout=2 * WAIT_BACKEND)
def notify_visible_with_text(selenium, browser_id, notify_type, text_regexp):
    driver = selenium[browser_id]
    css_sel = f".ember-notify-show[class*={notify_type}] .message"
    regexp = re.compile(text_regexp)
    with suppress(NoSuchElementException, StaleElementReferenceException):
        assert any(
            regexp.match(notify.text)
            for notify in driver.find_elements(By.CSS_SELECTOR, css_sel)
        ), f'no {notify_type} notify with "{text_regexp}" msg found'


@wt(parsers.parse("user of {browser_id} closes all notifies"))
@repeat_failed(timeout=WAIT_FRONTEND)
def close_visible_notifies(selenium, browser_id):
    driver = selenium[browser_id]
    notifies = driver.find_elements(By.CSS_SELECTOR, ".ember-notify a.close-button")

    with suppress(StaleElementReferenceException):
        map(lambda btn: btn.click(), notifies)

    assert all(
        staleness_of(notify) for notify in notifies
    ), "not all notifies were closed"


@wt(parsers.parse('user of {browser_id} sees "{error_msg}" error on Onedata page'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_loading_error(selenium, browser_id, onepage, error_msg):
    given_msg = onepage(selenium[browser_id]).loading_error.lower()
    assert (
        error_msg.lower() in given_msg
    ), f"{error_msg} not in {given_msg} error message"


@wt(
    parsers.parse(
        'user of {browser_id} sees "{error_msg}" error on public Onedata page'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_loading_error_public_page(selenium, browser_id, public_onepage, error_msg):
    given_msg = public_onepage(selenium[browser_id]).loading_error.lower()
    assert (
        error_msg.lower() in given_msg
    ), f"{error_msg} not in {given_msg} error message"
