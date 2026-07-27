"""This module contains gherkin steps to run acceptance tests featuring
ember notifies in web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import re
from functools import partial

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import invisibility_of_element
from selenium.webdriver.support.ui import WebDriverWait

from tests.gui.conftest import WAIT_BACKEND
from tests.gui.steps.common.common import (
    click_close_button_and_wait_to_disappear,
)
from tests.gui.utils import OnePage, PublicOnePage
from tests.gui.utils.common.popups import Popups
from tests.gui.utils.common.popups.alert_info_popup import AlertInfoPopup
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        "user of {browser_id} sees an {notify_type} notify "
        "with text matching to: {text_regexp}"
    )
)
def notify_visible_with_text(
    selenium: SeleniumDrivers,
    browser_id: str,
    notify_type: str,
    text_regexp: str,
) -> None:
    driver = selenium[browser_id]
    regexp = re.compile(text_regexp)
    # for each popup store message and web_elem  for future use

    seen_popups: dict[str, WebElement] = {}

    def capture_matching_popup(
        driver: WebDriver,
    ) -> bool:
        popups = Popups(driver)
        detected_popups = [
            *popups.alert_info_popups,
            *popups.notify_popups,
        ]

        for popup in detected_popups:
            try:
                if web_elem.is_displayed():
                    seen_popups[popup.message] = web_elem
            except (NoSuchElementException, StaleElementReferenceException):
                continue

        for message in seen_popups:
            if regexp.match(message):
                return True

        return False

    try:
        WebDriverWait(driver, 2 * WAIT_BACKEND, poll_frequency=0.1).until(
            capture_matching_popup
        )

    except TimeoutException as exc:
        raise AssertionError(
            f'no {notify_type} notify with "{text_regexp}" msg found; '
            f"observed messages: {list(seen_popups)}"
        ) from exc

    for web_elem in seen_popups.values():

        def get_close_button(
            driver: WebDriver,
            popup_elem: WebElement = web_elem,
        ) -> WebElement:
            return AlertInfoPopup(driver, popup_elem).close

        if invisibility_of_element(web_elem)(driver):
            continue

        click_close_button_and_wait_to_disappear(
            driver,
            web_elem,
            partial(get_close_button, popup_elem=web_elem),
        )


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
