"""This module contains gherkin steps to run acceptance tests featuring
browser creation.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import os
import time
from itertools import cycle
from typing import cast

from pytest_bdd import given
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from urllib3.exceptions import HTTPError

from tests.gui.conftest import DRIVER_CREATION_RETRIES, SELENIUM_IMPLICIT_WAIT
from tests.gui.utils.generic import parse_seq, redirect_display
from tests.type_definitions import Capabilities, SeleniumDrivers, WebDriverFactory
from tests.utils.bdd_utils import parsers


@given(parsers.parse("user opened {browser_id_list} window"))
@given(parsers.parse("users opened {browser_id_list} browsers' windows"))
def create_instances_of_webdriver(
    selenium: SeleniumDrivers,
    driver: WebDriverFactory,
    browser_id_list: str,
    tmpdir: object,
    tmp_memory: dict[str, dict[str, dict[str, object]]],
    driver_type: str,
    xvfb: list[str],
    screen_width: int,
    screen_height: int,
    displays: dict[str, str],
    capabilities: Capabilities,
) -> None:

    for browser_id, display in zip(parse_seq(browser_id_list), cycle(xvfb)):
        if browser_id in selenium:
            raise AttributeError(f"{browser_id:s} already in use")
        tmp_memory[browser_id] = {
            "shares": {},
            "spaces": {},
            "groups": {},
            "mailbox": {},
            "oz": {},
            "window": {"modal": None},
        }

        with redirect_display(display):
            temp_dir = str(tmpdir)
            download_dir = os.path.join(temp_dir, browser_id, "download")
            browser_data = os.path.join(temp_dir, browser_id, "browser_data")
            os.makedirs(download_dir, exist_ok=True)
            os.makedirs(browser_data, exist_ok=True)

            if driver_type.lower() == "chrome":
                chrome_prefs = {"download.default_directory": download_dir}
                options = cast(Options, capabilities["options"])
                options.add_experimental_option("prefs", chrome_prefs)
                options.add_argument(f"--user-data-dir={browser_data}")

            for i in range(DRIVER_CREATION_RETRIES):
                try:
                    browser = driver()
                    assert_driver_working_properly(browser)
                    break
                except (WebDriverException, HTTPError) as e:
                    print(
                        f"failed to start webdriver instance at attempt: {i + 1} "
                        f"due to:\n {e}"
                    )
                    if i == 4:
                        raise e
                    time.sleep(2)

            _config_driver(browser, screen_width, screen_height)

        displays[browser_id] = display
        selenium[browser_id] = browser


# TODO: VFS-2205 configure different window sizes for responsiveness
#  tests: https://jira.plgrid.pl/jira/browse/VFS-2205
def _config_driver(driver: WebDriver, window_width: int, window_height: int) -> None:
    driver.implicitly_wait(SELENIUM_IMPLICIT_WAIT)

    # perform attempts to change window size
    for i in range(DRIVER_CREATION_RETRIES):
        try:
            driver.set_window_size(window_width, window_height)
            break
        except WebDriverException as e:
            if i == 4:
                raise e
            time.sleep(2)

    # possible solution to chromedriver crushes: Timed out receiving message from renderer
    driver.set_page_load_timeout(60)


def assert_driver_working_properly(driver: WebDriver) -> None:
    try:
        _ = driver.get_screenshot_as_base64()
    except (WebDriverException, HTTPError) as e:
        driver.quit()
        raise e
