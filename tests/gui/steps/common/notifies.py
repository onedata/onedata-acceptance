"""This module contains gherkin steps to run acceptance tests featuring
ember notifies in web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import re
from collections.abc import Callable
from typing import TypeVar

from selenium.common.exceptions import (
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.expected_conditions import staleness_of

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.common.common import click_close_button_and_wait_to_disappear
from tests.gui.utils import OnePage, PublicOnePage
from tests.gui.utils.common.popups import Popups
from tests.gui.utils.generic import (
    is_web_element_visible_on_page,
    suppress,
)
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import element_has_class, repeat_failed

T = TypeVar("T")


def _handler_for(value: T) -> Callable[[WebDriver], T]:
    def handler(_driver: WebDriver) -> T:
        return value

    return handler


@wt(
    parsers.parse(
        "user of {browser_id} sees an {notify_type} notify "
        "with text matching to: {text_regexp}"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def notify_visible_with_text(
    selenium: SeleniumDrivers,
    browser_id: str,
    notify_type: str,
    text_regexp: str,
) -> None:
    driver = selenium[browser_id]
    # css_selector = f".ember-notify-show[class*={notify_type}] .message"
    regexp = re.compile(text_regexp)
    popups = Popups(driver)

    for notify in list(popups.alert_info_popups) + list(popups.notify_popups):
        get_notify_web_elem = _handler_for(notify.web_elem)
        if is_web_element_visible_on_page(driver, get_notify_web_elem) and regexp.match(
            notify.message
        ):
            print(element_has_class(notify.web_elem, f"alert-{notify_type}"))
            click_close_button_and_wait_to_disappear(
                driver,
                get_notify_web_elem,
                _handler_for(notify.close),
            )
            break
    else:
        raise AssertionError(f'no {notify_type} notify with "{text_regexp}" msg found')


@wt(parsers.parse("user of {browser_id} closes all notifies"))
@repeat_failed(timeout=WAIT_FRONTEND)
def close_visible_notifies(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    notifies = driver.find_elements(By.CSS_SELECTOR, ".ember-notify a.close-button")

    with suppress(StaleElementReferenceException):
        map(lambda btn: btn.click(), notifies)

    assert all(
        staleness_of(notify) for notify in notifies
    ), "not all notifies were closed"


@wt(parsers.parse('user of {browser_id} sees "{error_msg}" error on Onedata page'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_loading_error(
    selenium: SeleniumDrivers, browser_id: str, error_msg: str
) -> None:
    given_msg = OnePage(selenium[browser_id]).loading_error.lower()
    assert (
        error_msg.lower() in given_msg
    ), f"{error_msg} not in {given_msg} error message"


@wt(
    parsers.parse(
        'user of {browser_id} sees "{error_msg}" error on public Onedata page'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_loading_error_public_page(
    selenium: SeleniumDrivers, browser_id: str, error_msg: str
) -> None:
    given_msg = PublicOnePage(selenium[browser_id]).loading_error.lower()
    assert (
        error_msg.lower() in given_msg
    ), f"{error_msg} not in {given_msg} error message"
