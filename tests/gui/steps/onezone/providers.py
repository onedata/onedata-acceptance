"""This module contains gherkin steps to run acceptance tests featuring
providers management in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time
from itertools import zip_longest

import requests

from tests import OP_REST_PORT
from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.utils import OZLoggedIn, Popups
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.onenv_utils import run_onenv_command
from tests.utils.rest_utils import get_provider_rest_path, http_get
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
    selenium, browser_id, provider_name
):
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
    selenium, browser_id, provider, hosts, clipboard, displays
):
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
def assert_provider_hostname_matches_known_domain(selenium, browser_id, host, hosts):
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
    selenium, browser_id, provider, hosts, displays, clipboard
):
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
def _click_copy_hostname(driver):
    Popups(driver).provider_map_popover.copy_hostname()


def _click_on_btn_in_provider_popup(driver, btn, provider, hosts):
    err_msg = 'Popup displayed for provider named "{}" instead of "{}"'
    provider = hosts[provider]["name"]
    prov = getattr(OZLoggedIn(driver), "world map").get_provider_with_displayed_popup()
    assert provider == prov.name, err_msg.format(prov.name, provider)
    getattr(prov, transform(btn)).click()


@given(
    parsers.re(
        r"users? of (?P<browser_id_list>.+?) clicked on the "
        r'"(?P<btn>Go to your files|copy hostname)" button in '
        r'"(?P<provider_list>.+?)" provider\'s popup displayed '
        r"on world map"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def g_click_on_btn_in_provider_popup(
    selenium, browser_id_list, btn, provider_list, hosts
):
    browser_ids = parse_seq(browser_id_list)
    providers = parse_seq(provider_list)
    for browser_id, provider in zip_longest(
        browser_ids, providers, fillvalue=providers[-1]
    ):
        _click_on_btn_in_provider_popup(selenium[browser_id], btn, provider, hosts)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) clicks on the "
        r'"(?P<btn>Go to your files|copy hostname)" button in '
        r'"(?P<provider>.+?)" provider\'s popup displayed on world map'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def wt_click_on_btn_in_provider_popup(selenium, browser_id, btn, provider, hosts):
    _click_on_btn_in_provider_popup(selenium[browser_id], btn, provider, hosts)


@given(
    parsers.re(
        "users? of (?P<browser_id_list>.*) clicked on the "
        '"(?P<btn_name>.+?)" button in provider popup'
    )
)
def g_click_on_go_to_files_provider(selenium, browser_id_list, btn_name):
    for browser_id in parse_seq(browser_id_list):
        driver = selenium[browser_id]
        popup = getattr(
            OZLoggedIn(driver), "world map"
        ).get_provider_with_displayed_popup()
        getattr(popup, transform(btn_name)).click()


@wt(
    parsers.re(
        "users? of (?P<browser_id_list>.*) clicks on the "
        '"(?P<btn_name>.+?)" button in provider popup'
    )
)
def wt_click_on_go_to_files_provider(selenium, browser_id_list, btn_name):
    for browser_id in parse_seq(browser_id_list):
        driver = selenium[browser_id]
        popup = getattr(
            OZLoggedIn(driver), "world map"
        ).get_provider_with_displayed_popup()
        getattr(popup, transform(btn_name)).click()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that there is no "
        r"displayed provider popup next to "
        r"(?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|"
        r"\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) "
        r"provider circle on Onezone world map"
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that provider popup next to "
        r"(?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|"
        r"\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) "
        r"provider circle on Onezone world map has disappeared"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_no_provider_popup_next_to_provider_circle(selenium, browser_id, ordinal):
    driver = selenium[browser_id]
    prov_circle = getattr(OZLoggedIn(driver), "world map").providers[
        int(ordinal[:-2]) - 1
    ]
    assert (
        not prov_circle.is_displayed()
    ), f"provider popup for {ordinal} circle is displayed while it should not be"


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) does not see provider popover "
        r"on Onezone world map"
    )
)
def assert_no_provider_popup_on_world_map(selenium, browser_id):
    driver = selenium[browser_id]
    try:
        Popups(driver).provider_map_popover
    except RuntimeError:
        pass
    else:
        raise RuntimeError("found provider popover on world map")


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) clicks on "
        r"(?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|\d*?11th|"
        r"\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|\d*?[^1]3rd) "
        r"provider circle on Onezone world map"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_provider_circle(selenium, browser_id, ordinal):
    driver = selenium[browser_id]
    getattr(OZLoggedIn(driver), "world map").providers[int(ordinal[:-2]) - 1].click()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) clicks on the other provider "
        r"circle on Onezone world map"
    )
)
def click_other_provider_icons(selenium, browser_id):
    driver = selenium[browser_id]
    OZLoggedIn(driver).providers.icons[0].icon()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that provider popup has "
        r"appeared next to (?P<ordinal>1st|2nd|3rd|\d*?[4567890]th|"
        r"\d*?11th|\d*?12th|\d*?13th|\d*?[^1]1st|\d*?[^1]2nd|"
        r"\d*?[^1]3rd) provider circle on Onezone world map"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_provider_popup_next_to_provider_circle(selenium, browser_id, ordinal):
    driver = selenium[browser_id]
    prov_circle = getattr(OZLoggedIn(driver), "world map").providers[
        int(ordinal[:-2]) - 1
    ]
    assert (
        prov_circle.is_displayed()
    ), f"provider popup for {ordinal} circle is not displayed while it should be"


@wt(parsers.parse("user of {browser_id} clicks on Onezone world map"))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_world_map(selenium, browser_id):
    OZLoggedIn(selenium[browser_id]).providers.map_point.click()


@wt(
    parsers.parse(
        'user of {browser_id} sees that provider "{provider}" in Onezone is working'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_provider_working_in_oz_panel(selenium, browser_id, provider, hosts):
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
    selenium, browser_id, provider_name
):
    driver = selenium[browser_id]
    OZLoggedIn(driver).providers.providers_list[provider_name]()


@wt(
    parsers.parse(
        'user of {browser_id} clicks on provider "{provider}" in providers sidebar'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_provider_in_data_sidebar(selenium, browser_id, provider, hosts):
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
    selenium, browser_id, provider, hosts
):
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
def click_on_visit_provider_in_provider_popover(selenium, browser_id, option):
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
    selenium, browser_id, space_name
):
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
    selenium, browser_id, provider, number, hosts
):
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
def assert_len_of_spaces_list_in_provider_popover(selenium, browser_id, number):
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
    selenium, browser_id, provider, hosts
):
    button = "menu button"
    click_on_button_on_providers_list(selenium, browser_id, provider, hosts, button)


@wt(
    parsers.parse(
        'user of {browser_id} clicks {button} for "{provider}"'
        " provider on space providers data page"
    )
)
def click_on_button_on_providers_list(selenium, browser_id, provider, hosts, button):
    driver = selenium[browser_id]
    provider_name = hosts[provider]["name"]
    getattr(
        OZLoggedIn(driver).data.providers_page.providers_list[provider_name],
        transform(button),
    )()


def click_on_cease_support_in_menu_of_provider_on_providers_list(driver):
    Popups(driver).menu_popup_with_text.cease_support_from_providers_list_menu()


@wt(
    parsers.parse(
        'user of {browser_id} waits until provider "{provider_name}" '
        "goes offline on providers map"
    )
)
def wait_until_provider_goes_offline_by_gui(selenium, browser_id, hosts, provider_name):
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


def wait_until_provider_goes_online_by_rest(hosts, provider_name, users):
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


def _start_and_wait_for_providers(hosts, provider_list, users):
    start_providers(hosts, provider_list)
    for provider in parse_seq(provider_list):
        wait_until_provider_goes_online_by_rest(hosts, provider, users)


@wt(parsers.re(r'provider named "(?P<provider_list>.*?)" is stopped'))
@wt(parsers.re(r"providers named (?P<provider_list>.*?) are stopped"))
def wt_stop_providers(provider_list, hosts, users):
    _stop_providers(hosts, provider_list)
    yield
    _start_and_wait_for_providers(hosts, provider_list, users)


def _stop_providers(hosts, provider_list):
    for provider in parse_seq(provider_list):
        pod_name = hosts[provider]["pod-name"]
        run_onenv_command("service", ["stop", pod_name])


@repeat_failed(timeout=WAIT_BACKEND)
def start_providers(hosts, provider_list):
    for provider in parse_seq(provider_list):
        pod_name = hosts[provider]["pod-name"]
        run_onenv_command("service", ["start", pod_name])
