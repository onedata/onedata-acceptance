"""Development-only utilities for debugging GUI tests.

This module must not be imported or used in production code.
"""

__author__ = "Mateusz Zajac Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from selenium.webdriver.remote.webdriver import WebDriver


def breakpoint_with_paused_website(driver: WebDriver) -> None:
    """Pause both browser JavaScript and the Python test."""
    driver.execute_cdp_cmd("Debugger.enable", {})

    try:
        driver.execute_script("""
            setTimeout(() => {
                debugger;
            }, 0);
            """)
        breakpoint()  # pylint: disable=forgotten-debug-statement
    finally:
        try:
            driver.execute_cdp_cmd("Debugger.resume", {})
        finally:
            driver.execute_cdp_cmd("Debugger.disable", {})
