"""Selenium WebDriver extensions used by acceptance tests."""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver


class WebDriver(SeleniumWebDriver):
    """Selenium WebDriver type shared by acceptance tests."""
