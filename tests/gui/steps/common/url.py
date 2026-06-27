"""This module contains gherkin steps to run acceptance tests featuring
url handling.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import re
from typing import Union

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.expected_conditions import (
    invisibility_of_element_located,
    staleness_of,
    visibility_of_element_located,
)
from selenium.webdriver.support.ui import WebDriverWait as Wait

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.common.common import try_click_without_throwing_error
from tests.gui.type_definitions import Clipboard, TmpMemory
from tests.gui.utils import Popups
from tests.gui.utils.generic import parse_seq, parse_url
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.utils import repeat_failed

HOST_PATTERN = (
    r"(?:"
    r"oneprovider-[0-9]+ provider panel|"
    r"onezone zone panel|"
    r"onezone panel|"
    r"Onezone panel|"
    r"onezone|"
    r"Onezone|"
    r"emergency interface of Onepanel|"
    r"node[0-9]+ of oneprovider-[0-9]+ provider panel"
    r")"
)

HOSTS_LIST_PATTERN = (
    rf"(?:"
    rf"{HOST_PATTERN}"
    rf"|"
    rf"\[\s*{HOST_PATTERN}(?:\s*,\s*{HOST_PATTERN})*\s*\]"
    rf")"
)


def open_onedata_service_page(
    selenium: SeleniumDrivers, browser_id_list: str, hosts_list: str, hosts: Hosts
) -> None:
    """hosts_list may contains:
    onezone,
    onezone zone panel,
    oneprovider-[0-9] provider panel,
    node[0-9] of oneprovider-[0-9] provider panel,
    emergency interface of Onepanel
    emergency interface of Onezone
    """
    for browser_id, host in zip(parse_seq(browser_id_list), parse_seq(hosts_list)):
        driver = selenium[browser_id]
        if host == "emergency interface of Onepanel":
            host = "oneprovider-1 provider panel"
        host_parts = host.lower().split()
        node_number: Union[int, str]

        if "node" in host_parts[0]:
            node_number = int(host_parts[0][-1:])
            host_parts = host_parts[2:]
        else:
            node_number = ""

        alias, service = host_parts[0], "_".join(host_parts[1:])
        if "panel" in service:
            hostname = hosts[alias]["panel"]["hostname"]

            if node_number == 0:
                driver.get(f"https://{hostname}")
            elif node_number != "":
                driver.get(f"https://{hostname.split('.')[0]}-{node_number}.{hostname}")
            else:
                driver.get(f"https://{hostname}")
        else:
            driver.get(f"https://{hosts[alias]['hostname']}")


@given(
    parsers.re(
        r"users? of (?P<browser_id_list>.+?) opened "
        rf"(?P<hosts_list>{HOSTS_LIST_PATTERN}) "
        r"page"
    )
)
def g_open_onedata_service_page(
    selenium: SeleniumDrivers, browser_id_list: str, hosts_list: str, hosts: Hosts
) -> None:
    open_onedata_service_page(selenium, browser_id_list, hosts_list, hosts)


@wt(
    parsers.re(
        r"users? of (?P<browser_id_list>.+?) opens "
        rf"(?P<hosts_list>{HOSTS_LIST_PATTERN}) "
        r"page"
    )
)
def wt_open_onedata_service_page(
    selenium: SeleniumDrivers, browser_id_list: str, hosts_list: str, hosts: Hosts
) -> None:
    open_onedata_service_page(selenium, browser_id_list, hosts_list, hosts)


@wt(parsers.re("user of (?P<browser_id>.+) should be redirected to (?P<page>.+) page"))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_being_redirected_to_page(
    page: str, selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    match = re.match(r"https?://.*?(/#)?(/.*)", driver.current_url)
    if match is None:
        raise ValueError(f"Cannot parse current URL: {driver.current_url}")
    curr_page = match.group(2)
    assert (
        curr_page == page
    ), f"currently on {curr_page} page instead of expected {page}"


@wt(parsers.re(r"user of (?P<browser_id>.+) changes the relative URL to (?P<path>.+)"))
def change_relative_url(selenium: SeleniumDrivers, browser_id: str, path: str) -> None:
    driver = selenium[browser_id]
    driver.get(parse_url(driver.current_url).group("base_url") + path)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) changes "
        r"application path to plain (?P<path>.+)"
    )
)
def change_application_path(
    selenium: SeleniumDrivers, browser_id: str, path: str
) -> None:
    driver = selenium[browser_id]
    driver.get(parse_url(driver.current_url).group("base_url") + "/#" + path)


@wt(
    parsers.re(
        "user of (?P<browser_id>.+?) sees that (?:url|URL) matches: (?P<path>.+)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def is_url_matching(selenium: SeleniumDrivers, browser_id: str, path: str) -> None:
    driver = selenium[browser_id]
    regexp = r"{}$".format(path.replace("\\", "\\\\"))
    err_msg = rf"expected url: {path} does not match current one: {{}}"

    @repeat_failed(timeout=WAIT_BACKEND)
    def assert_url_match(d: WebDriver, regex: str, msg: str) -> None:
        curr_url = d.current_url
        assert re.match(regex, curr_url), msg.format(curr_url)

    assert_url_match(driver, regexp, err_msg)


def _open_url(selenium: SeleniumDrivers, browser_id: str, url: str) -> None:
    driver = selenium[browser_id]
    old_page = driver.find_element(By.CSS_SELECTOR, "html")
    driver.get(url)
    Wait(driver, WAIT_BACKEND).until(
        staleness_of(old_page),
        message=f"waiting for page {url:s} to load",
    )


@wt(parsers.re("user of (?P<browser_id>.+?) opens received (?:url|URL)"))
def open_received_url_with_base_url(
    selenium: SeleniumDrivers,
    browser_id: str,
    tmp_memory: TmpMemory,
    base_url: str,
) -> None:
    url = tmp_memory[browser_id]["mailbox"]["url"]
    url = url.replace(parse_url(url).group("base_url"), base_url, 1)
    _open_url(selenium, browser_id, url)


@wt(
    parsers.re(
        r"user of (?P<browser_id>\S+) opens (?:url|URL) received from "
        r"user of (?P<browser_id2>\S+)"
    )
)
def open_exactly_received_url(
    selenium: SeleniumDrivers, browser_id: str, tmp_memory: TmpMemory
) -> None:
    url = tmp_memory[browser_id]["mailbox"]["url"]

    _open_url(selenium, browser_id, url)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) changes webapp path to "
        r'"?(?P<path>.+?)"? concatenated with copied item'
    )
)
def change_app_path_with_copied_item(
    selenium: SeleniumDrivers,
    browser_id: str,
    path: str,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:
    driver = selenium[browser_id]
    base_url = parse_url(driver.current_url).group("base_url")
    item = clipboard.paste(display=displays[browser_id])
    url = f"{base_url}{path}/{item}"
    # We use javascript instead of driver.get because of chromedriver being
    # unable to determine whether page has been loaded
    driver.execute_script(f"window.location = '{url}'")


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) changes webapp path to "
        r'"?(?P<path>.+?)"? concatenated with received (?P<item>.*)'
    )
)
def change_app_path_with_recv_item(
    selenium: SeleniumDrivers,
    browser_id: str,
    path: str,
    tmp_memory: TmpMemory,
    item: str,
) -> None:
    driver = selenium[browser_id]
    base_url = parse_url(driver.current_url).group("base_url")
    item = tmp_memory[browser_id]["mailbox"][item.lower()]
    url = f"{base_url}{path}/{item}"
    # We use javascript instead of driver.get because of chromedriver being
    # unable to determine whether page has been loaded
    driver.execute_script(f"window.location = '{url}'")


@wt(parsers.parse("user of {browser_id} copies url from browser's location bar"))
def copy_site_url(
    selenium: SeleniumDrivers,
    browser_id: str,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:
    driver = selenium[browser_id]
    clipboard.copy(driver.current_url, display=displays[browser_id])


@wt(parsers.parse("user of {browser_id} opens copied URL in browser's location bar"))
def open_site_url(
    selenium: SeleniumDrivers,
    browser_id: str,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:
    driver = selenium[browser_id]
    url = clipboard.paste(display=displays[browser_id])
    # We use javascript instead of driver.get because of chromedriver being
    # unable to determine whether page has been loaded
    driver.execute_script(f"window.location = '{url}'")


@wt(
    parsers.parse(
        "user of {browser_id} opens URL received from user of {browser2_id} without"
        " waiting"
    )
)
def open_received_url_without_waiting(
    selenium: SeleniumDrivers, browser_id: str, tmp_memory: TmpMemory
) -> None:
    driver = selenium[browser_id]
    url = tmp_memory[browser_id]["mailbox"]["url"]
    driver.get(url)


@wt(parsers.parse("user of {browser_id} copies a first resource ID from URL"))
@repeat_failed(timeout=WAIT_FRONTEND)
def cp_part_of_url(
    selenium: SeleniumDrivers,
    browser_id: str,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:
    driver = selenium[browser_id]
    item_value = parse_url(driver.current_url).group("id")
    assert len(item_value) > 10, f"did not manage to get resource ID, got: {item_value}"
    clipboard.copy(
        item_value,
        display=displays[browser_id],
    )


@wt(parsers.parse("using web GUI, {browser_id_list} refreshes site"))
@wt(parsers.re("users? of (?P<browser_id_list>.*?) refreshes site"))
def refresh_site(selenium: SeleniumDrivers, browser_id_list: str) -> None:
    for browser_id in parse_seq(browser_id_list):
        selenium[browser_id].refresh()


@wt(
    parsers.re(
        "users? of (?P<browser_id_list>.*?) refreshes site and waits for page to load"
    )
)
def refresh_site_and_wait(selenium: SeleniumDrivers, browser_id_list: str) -> None:
    for browser_id in parse_seq(browser_id_list):
        selenium[browser_id].refresh()
    for browser_id in parse_seq(browser_id_list):
        assert_main_page_loaded(selenium, browser_id)


def assert_main_page_loaded(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    wait_till_main_content_loaded(driver)
    wait_till_authentication_info_disappear(driver)


@repeat_failed(timeout=WAIT_BACKEND * 2)
def wait_till_main_content_loaded(driver: WebDriver) -> None:
    elems = driver.find_elements(
        By.CSS_SELECTOR, ".main-menu-content li.main-menu-item"
    )
    assert len(elems) > 0, "did not manage to load main page"


def wait_till_authentication_info_disappear(driver: WebDriver) -> None:
    # If popup don't appear don't throw error
    # If appeared and not closed raise
    try:
        Wait(driver, WAIT_FRONTEND).until(
            visibility_of_element_located((By.CSS_SELECTOR, ".alert-info"))
        )
    except TimeoutException:
        pass
    else:
        try_click_without_throwing_error(
            lambda: Popups(  # pylint: disable=unnecessary-lambda
                driver
            ).authentication_succeeded.close.click()
        )

        Wait(driver, WAIT_FRONTEND).until(
            invisibility_of_element_located((By.CSS_SELECTOR, ".alert-info"))
        )


@wt(parsers.parse("if {client} is web GUI, {user} refreshes site"))
def if_gui_refresh_site(selenium: SeleniumDrivers, client: str, user: str) -> None:
    if client == "web GUI":
        refresh_site(selenium, user)


@wt(parsers.parse("user of {browser_id} refreshes webapp"))
@repeat_failed(timeout=WAIT_FRONTEND, exceptions=AttributeError)
def refresh_webapp(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    driver.get(parse_url(driver.current_url).group("base_url"))


@wt(parsers.parse("user of {browser_id} is redirected to newly opened tab"))
def switch_to_last_tab(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    driver.switch_to.window(driver.window_handles[-1])


@wt(
    parsers.parse(
        "user of {browser_id} switches to the previously opened tab in the web browser"
    )
)
def switch_to_first_tab(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    driver.switch_to.window(driver.window_handles[0])


@wt(parsers.parse('user of {browser_id} sees image named "{image_name}" in browser'))
def assert_image_in_browser(
    browser_id: str, selenium: SeleniumDrivers, image_name: str
) -> None:
    driver = selenium[browser_id]
    url = driver.find_elements(By.TAG_NAME, "img")[0].get_attribute("src")
    err_msg = f"{image_name} is not visible in browser"
    assert image_name in url, err_msg
