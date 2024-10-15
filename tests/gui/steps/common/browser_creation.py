"""This module contains gherkin steps to run acceptance tests featuring
browser creation.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


import os
from itertools import cycle

from pytest_bdd import given
from tests.gui.conftest import SELENIUM_IMPLICIT_WAIT
from tests.gui.utils.generic import parse_seq, redirect_display
from tests.utils.bdd_utils import parsers


@given(parsers.parse("user opened {browser_id_list} window"))
@given(parsers.parse("users opened {browser_id_list} browsers' windows"))
def create_instances_of_webdriver(
    selenium,
    driver,
    browser_id_list,
    tmpdir,
    tmp_memory,
    driver_type,
    xvfb,
    xvfb_recorder,
    screen_width,
    screen_height,
    displays,
    capabilities,
):

    _ = xvfb_recorder
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
                capabilities["options"].add_experimental_option(
                    "prefs", chrome_prefs
                )
                capabilities["options"].add_argument(
                    f"--user-data-dir={browser_data}"
                )

            browser = driver()
            _config_driver(browser, screen_width, screen_height)

        displays[browser_id] = display
        selenium[browser_id] = browser


# TODO: VFS-2205 configure different window sizes for responsiveness
#  tests: https://jira.plgrid.pl/jira/browse/VFS-2205
def _config_driver(driver, window_width, window_height):
    driver.implicitly_wait(SELENIUM_IMPLICIT_WAIT)
    driver.set_window_size(window_width, window_height)
    # possible solution to chromedriver cruches: Timed out receiving message from renderer
    driver.set_page_load_timeout(60)
    # currenlty, we rather set window size
    # driver.maximize_window()
