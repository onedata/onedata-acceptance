"""This module contains gherkin steps to run acceptance tests featuring
providers management in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time
from collections.abc import Iterator
from itertools import zip_longest

import requests
from selenium.webdriver.remote.webdriver import WebDriver

from tests import OP_REST_PORT
from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.type_definitions import Clipboard
from tests.gui.utils import OZLoggedIn, Popups
from tests.gui.utils.generic import parse_seq, transform
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.onenv_utils import run_onenv_command
from tests.utils.rest_utils import get_provider_rest_path, http_get
from tests.utils.user_utils import Users
from tests.utils.utils import repeat_failed

TIMEOUT_FOR_PROVIDER_GOING_OFFLINE = 300
TIMEOUT_FOR_PROVIDER_GOING_ONLINE = 120


@wt(
    parsers.parse(
        "user of {browser_id} sees that provider popup for "
        'provider named "{provider_name}" has appeared on '
        "world map"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_popup_for_provider_with_name_has_appeared_on_map(
    selenium: SeleniumDrivers, browser_id: str, provider_name: str
) -> None:
    driver = selenium[browser_id]
    err_msg = 'Popup displayed for provider named "{}" instead of "{}"'
    prov = Popups(driver).provider_map_popover.provider_name
    assert provider_name == prov, err_msg.format(prov, provider_name)


@wt(
    parsers.parse(
        "user of {browser_id} sees that provider popup for "
        'provider "{provider}" has appeared on world map'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_popup_for_provider_has_appeared_on_map(
    selenium: SeleniumDrivers,
    browser_id: str,
    provider: str,
    hosts: Hosts,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
    driver = selenium[browser_id]
    err_msg = 'Popup displayed for provider named "{}" instead of "{}"'
    try:
        prov = Popups(driver).provider_map_popover.provider_name
    except RuntimeError:
        Popups(driver).provider_details.values[0].copy_to_clipboard()
        prov = clipboard.paste(display=displays[browser_id])
    provider_name = hosts[provider]["name"]
    assert provider_name == prov, err_msg.format(prov, provider_name)


@wt(
    parsers.parse(
        "user of {browser_id} sees that hostname in displayed "
        'provider popup matches that of "{host}" provider'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_provider_hostname_matches_known_domain(
    selenium: SeleniumDrivers, browser_id: str, host: str, hosts: Hosts
) -> None:
    driver = selenium[browser_id]
    displayed_domain = Popups(driver).provider_map_popover.provider_hostname
    domain = hosts[host]["hostname"]
    assert (
        displayed_domain == domain
    ), f"displayed {displayed_domain} provider hostname instead of expected {domain}"


@wt(
    parsers.parse(
        "user of {browser_id} sees that hostname in displayed "
        "provider popup matches test hostname of provider "
        '"{provider}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_provider_hostname_matches_test_hostname(
    selenium: SeleniumDrivers,
    browser_id: str,
    provider: str,
    hosts: Hosts,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:
    driver = selenium[browser_id]
    expected_domain = f"{hosts[provider]['hostname']}.test"
    page = OZLoggedIn(driver).open_page_and_click("providers")
    page.providers_list[0]()
    _click_copy_hostname(driver)
    displayed_domain = clipboard.paste(display=displays[browser_id])
    assert displayed_domain == expected_domain, (
        f"displayed {displayed_domain} provider hostname instead of expected"
        f" {expected_domain}"
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def _click_copy_hostname(driver: WebDriver) -> None:
    Popups(driver).provider_map_popover.click_copy_hostname_icon()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) does not see provider popover "
        r"on Onezone world map"
    )
)
def assert_no_provider_popup_on_world_map(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    try:
        Popups(driver).provider_map_popover
    except RuntimeError:
        pass
    else:
        raise RuntimeError("found provider popover on world map")


@wt(parsers.parse("user of {browser_id} clicks on Onezone world map"))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_world_map(selenium: SeleniumDrivers, browser_id: str) -> None:
    OZLoggedIn(selenium[browser_id])["providers"].map_point.click()


@given(
    parsers.re(
        r"users? of (?P<browser_id_list>.*?) clicked on "
        r"(?P<providers>.*?) provider in expanded "
        r'"GO TO YOUR FILES" Onezone panel'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def g_click_on_provider_in_go_to_your_files_oz_panel(
    selenium: SeleniumDrivers, browser_id_list: str, providers: str, hosts: Hosts
) -> None:
    browser_ids = parse_seq(browser_id_list)
    provider_names = parse_seq(providers)
    for browser_id, provider in zip_longest(
        browser_ids, provider_names, fillvalue=provider_names[-1]
    ):
        provider_name = hosts[provider]["name"]
        (
            OZLoggedIn(selenium[browser_id])["go to your files"]
            .providers[provider_name]
            .click()
        )


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "{provider}" provider '
        'in expanded "GO TO YOUR FILES" Onezone panel'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def wt_click_on_provider_in_go_to_your_files_oz_panel(
    selenium: SeleniumDrivers, browser_id: str, provider: str, hosts: Hosts
) -> None:
    provider = hosts[provider]["name"]
    (OZLoggedIn(selenium[browser_id])["go to your files"].providers[provider].click())


@wt(
    parsers.parse(
        "user of {browser_id} clicks on provider named "
        '"{provider}" in expanded "GO TO YOUR FILES" Onezone '
        "panel"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def wt_click_on_provider_with_name_in_go_to_your_files_oz_panel(
    selenium: SeleniumDrivers, browser_id: str, provider: str
) -> None:
    (OZLoggedIn(selenium[browser_id])["go to your files"].providers[provider].click())


@wt(
    parsers.parse(
        "user of {browser_id} sees that there is no provider "
        'in "GO TO YOUR FILES" Onezone panel'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_list_of_providers_is_empty(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    count = OZLoggedIn(driver)["go to your files"].providers.count()
    assert count == 0, f"Providers count is {count} instead of expected 0"


@wt(
    parsers.parse(
        'user of {browser_id} sees that provider "{provider}" in Onezone is working'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_provider_working_in_oz_panel(
    selenium: SeleniumDrivers, browser_id: str, provider: str, hosts: Hosts
) -> None:
    driver = selenium[browser_id]
    provider = hosts[provider]["name"]
    page = OZLoggedIn(driver).open_page_and_click("providers")
    try:
        provider_record = page.providers_list[provider]
        provider_record.click()
    except RuntimeError:
        assert False, f'no provider "{provider}" found on providers list'
    else:
        assert (
            page.is_working()
        ), f'provider icon in Onezone for "{provider}" is not green'


def click_on_provider_in_providers_sidebar_with_provider_name(
    selenium: SeleniumDrivers, browser_id: str, provider_name: str
) -> None:
    driver = selenium[browser_id]
    OZLoggedIn(driver).providers.providers_list[provider_name]()


@wt(
    parsers.parse(
        'user of {browser_id} clicks on provider "{provider}" in providers sidebar'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_provider_in_data_sidebar(
    selenium: SeleniumDrivers, browser_id: str, provider: str, hosts: Hosts
) -> None:
    provider = hosts[provider]["name"]
    click_on_provider_in_providers_sidebar_with_provider_name(
        selenium, browser_id, provider
    )


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{provider}" provider is not '
        "in providers list in data sidebar"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_provider_is_not_in_providers_list_in_data_sidebar(
    selenium: SeleniumDrivers, browser_id: str, provider: str, hosts: Hosts
) -> None:
    driver = selenium[browser_id]
    provider = hosts[provider]["name"]
    providers_list = OZLoggedIn(driver).providers.providers_list
    assert (
        provider not in providers_list
    ), f"{provider} is in providers list in data sidebar"


@wt(
    parsers.re(
        "user of (?P<browser_id>.+?) clicks on "
        "(?P<option>Visit provider|Toggle home provider) button "
        "on provider popover"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_visit_provider_in_provider_popover(
    selenium: SeleniumDrivers, browser_id: str, option: str
) -> None:
    driver = selenium[browser_id]
    getattr(Popups(driver).provider_map_popover, transform(option)).click()


@wt(
    parsers.parse(
        'user of {browser_id} sees "{space_name}" is '
        "on the spaces list on provider popover"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_space_is_in_spaces_list_in_provider_popover(
    selenium: SeleniumDrivers, browser_id: str, space_name: str
) -> None:
    driver = selenium[browser_id]
    spaces_list = Popups(driver).provider_map_popover.spaces_list
    assert space_name in spaces_list


@wt(
    parsers.parse(
        "user of {browser_id} sees that spaces counter for "
        '"{provider}" provider displays {number} in data sidebar'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_number_of_supported_spaces_in_data_sidebar(
    selenium: SeleniumDrivers, browser_id: str, provider: str, number: str, hosts: Hosts
) -> None:
    driver = selenium[browser_id]
    provider = hosts[provider]["name"]
    supported_spaces_number = (
        OZLoggedIn(driver).providers.providers_list[provider].supported_spaces_number
    )
    assert (
        number == supported_spaces_number
    ), f"number of supported spaces is not equal {number}"


@wt(
    parsers.parse(
        "user of {browser_id} sees that length of spaces list on "
        "provider popover is {number}"
    )
)
def assert_len_of_spaces_list_in_provider_popover(
    selenium: SeleniumDrivers, browser_id: str, number: str
) -> None:
    driver = selenium[browser_id]
    spaces_list = Popups(driver).provider_map_popover.spaces_list
    assert int(number) == len(
        spaces_list
    ), f"number of supported spaces is not equal {number}"


@wt(
    parsers.re(
        r'user of (?P<browser_id>.+) opens "(?P<provider>oneprovider-[0-9]+)"'
        r" provider menu "
        r"on space providers data page"
    )
)
def click_on_menu_button_of_provider_on_providers_list(
    selenium: SeleniumDrivers, browser_id: str, provider: str, hosts: Hosts
) -> None:
    button = "menu button"
    click_on_button_on_providers_list(selenium, browser_id, provider, hosts, button)


@wt(
    parsers.parse(
        'user of {browser_id} clicks {button} for "{provider}"'
        " provider on space providers data page"
    )
)
def click_on_button_on_providers_list(
    selenium: SeleniumDrivers,
    browser_id: str,
    provider: str,
    hosts: Hosts,
    button: str,
) -> None:
    driver = selenium[browser_id]
    provider_name = hosts[provider]["name"]
    getattr(
        OZLoggedIn(driver).data.providers_page.providers_list[provider_name],
        transform(button),
    )()


def click_on_cease_support_in_menu_of_provider_on_providers_list(
    driver: WebDriver,
) -> None:
    Popups(driver).menu_popup_with_text.cease_support_from_providers_list_menu()


@wt(
    parsers.parse(
        'user of {browser_id} waits until provider "{provider_name}" '
        "goes offline on providers map"
    )
)
def wait_until_provider_goes_offline_by_gui(
    selenium: SeleniumDrivers, browser_id: str, hosts: Hosts, provider_name: str
) -> None:
    driver = selenium[browser_id]
    provider = hosts[provider_name]["name"]
    page = OZLoggedIn(driver).open_page_and_click("providers")
    time.sleep(0.5)
    provider_record = page.providers_list[provider]
    provider_record.click()
    start = time.time()
    while page.is_working():
        time.sleep(0.5)
        if time.time() > start + TIMEOUT_FOR_PROVIDER_GOING_OFFLINE:
            raise RuntimeError(
                "Provider did not go offline within "
                f"{TIMEOUT_FOR_PROVIDER_GOING_OFFLINE}s."
            )


def wait_until_provider_goes_online_by_rest(
    hosts: Hosts, provider_name: str, users: Users
) -> None:
    user = "admin"
    provider_hostname = hosts[provider_name]["hostname"]
    start = time.time()
    exception_message = ""
    while time.time() < start + TIMEOUT_FOR_PROVIDER_GOING_ONLINE:
        time.sleep(0.5)
        try:
            res = http_get(
                ip=provider_hostname,
                port=OP_REST_PORT,
                path=get_provider_rest_path("health"),
                auth=(user, users[user].password),
            )
            if res.status_code == requests.codes["ok"]:
                return
        except requests.exceptions.ConnectionError as e:
            exception_message = str(e)
    raise RuntimeError(
        "Provider is still not working after "
        f"{TIMEOUT_FOR_PROVIDER_GOING_ONLINE}s. "
        f"Last response from health check request: {res} "
        f"Exception from request: {exception_message}"
    )


def _start_and_wait_for_providers(
    hosts: Hosts, provider_list: str, users: Users
) -> None:
    start_providers(hosts, provider_list)
    for provider in parse_seq(provider_list):
        wait_until_provider_goes_online_by_rest(hosts, provider, users)


@wt(parsers.re(r'provider named "(?P<provider_list>.*?)" is stopped'))
@wt(parsers.re(r"providers named (?P<provider_list>.*?) are stopped"))
def wt_stop_providers(provider_list: str, hosts: Hosts, users: Users) -> Iterator[None]:
    _stop_providers(hosts, provider_list)
    yield
    _start_and_wait_for_providers(hosts, provider_list, users)


def _stop_providers(hosts: Hosts, provider_list: str) -> None:
    for provider in parse_seq(provider_list):
        pod_name = hosts[provider]["pod_name"]
        run_onenv_command("service", ["stop", pod_name])


@repeat_failed(timeout=WAIT_BACKEND)
def start_providers(hosts: Hosts, provider_list: str) -> None:
    for provider in parse_seq(provider_list):
        pod_name = hosts[provider]["pod_name"]
        run_onenv_command("service", ["start", pod_name])
