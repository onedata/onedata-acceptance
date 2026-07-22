"""This module contains gherkin steps to run acceptance tests featuring
common operations in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.utils import OZLoggedIn
from tests.gui.utils.generic import ELEMENTS_SEQUENCE_PATTERN, parse_elements_sequence
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_BACKEND)
def _expand_oz_panel(driver: WebDriver, panel: str) -> None:
    getattr(OZLoggedIn(driver), panel).expand()


@given(
    parsers.re(
        rf"users? of (?P<browser_id_list>{ELEMENTS_SEQUENCE_PATTERN}) expanded the "
        r'"(?P<panel_name>.*)" Onezone sidebar panel'
    ),
    converters={"browser_id_list": parse_elements_sequence},
)
def g_expand_oz_panel(
    selenium: SeleniumDrivers, browser_id_list: list[str], panel_name: str
) -> None:
    for browser_id in browser_id_list:
        _expand_oz_panel(selenium[browser_id], panel_name)


@wt(
    parsers.re(
        rf"users? of (?P<browser_id_list>{ELEMENTS_SEQUENCE_PATTERN}) expands? the "
        r'"(?P<panel_name>.*)" Onezone sidebar panel'
    ),
    converters={"browser_id_list": parse_elements_sequence},
)
def wt_expand_oz_panel(
    selenium: SeleniumDrivers, browser_id_list: list[str], panel_name: str
) -> None:
    for browser_id in browser_id_list:
        _expand_oz_panel(selenium[browser_id], panel_name)


@wt(
    parsers.parse(
        'user of {browser_id} sees alert with title "{title}" on Onezone page'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_alert_with_title_in_oz(
    selenium: SeleniumDrivers, browser_id: str, title: str
) -> None:
    driver = selenium[browser_id]
    alert = OZLoggedIn(driver).provider_alert_message
    error_message = f"expected alert: {title}, found: {alert}"
    assert alert == title, error_message


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) clicks on "
        r'"(?P<btn>Create new space|Join space)" button in expanded '
        r'"(?P<oz_panel>DATA SPACE MANAGEMENT)" Onezone panel'
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) clicks on "
        r'"(?P<btn>Join a group)" button in expanded '
        r'"(?P<oz_panel>GROUP MANAGEMENT)" Onezone panel'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_btn_in_oz_panel(
    selenium: SeleniumDrivers, browser_id: str, btn: str, oz_panel: str
) -> None:
    driver = selenium[browser_id]
    panel = getattr(OZLoggedIn(driver), oz_panel)
    action = getattr(panel, btn.lower().replace(" ", "_"))
    action()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that there is "
        r'(?P<item_type>provider) "(?P<item_name>.+?)" '
        r'in expanded "(?P<oz_panel>GO TO YOUR FILES)" Onezone panel'
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that (?P<item_type>provider) "
        r'"(?P<item_name>.+?)" has appeared in expanded '
        r'"(?P<oz_panel>GO TO YOUR FILES)" Onezone panel'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_there_is_item_with_known_name_in_oz_panel_list(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_type: str,
    item_name: str,
    oz_panel: str,
    hosts: Hosts,
) -> None:
    driver = selenium[browser_id]
    item_name = hosts[item_name]["name"]
    panel = getattr(OZLoggedIn(driver), oz_panel)
    items = getattr(panel, f"{item_type}s")
    assert (
        item_name in items
    ), f'no {item_type} named "{item_name}" found in {oz_panel} oz panel'


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that there is "
        r'(?P<item_type>provider) named "(?P<item_name>.+?)" '
        r'in expanded "(?P<oz_panel>GO TO YOUR FILES)" Onezone panel'
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that (?P<item_type>provider) "
        r'named "(?P<item_name>.+?)" has appeared in expanded '
        r'"(?P<oz_panel>GO TO YOUR FILES)" Onezone panel'
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that there is "
        r'(?P<item_type>space) named "(?P<item_name>.+?)" in expanded '
        r'"(?P<oz_panel>DATA SPACE MANAGEMENT)" Onezone panel'
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that (?P<item_type>space) "
        r'named "(?P<item_name>.+?)" has appeared in expanded '
        r'"(?P<oz_panel>DATA SPACE MANAGEMENT)" Onezone panel'
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that there is "
        r'(?P<item_type>group) named "(?P<item_name>.+?)" in expanded '
        r'"(?P<oz_panel>GROUP MANAGEMENT)" Onezone panel'
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that (?P<item_type>group) "
        r'named "(?P<item_name>.+?)" has appeared in expanded '
        r'"(?P<oz_panel>GROUP MANAGEMENT)" Onezone panel'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_there_is_item_named_in_oz_panel_list(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_type: str,
    item_name: str,
    oz_panel: str,
) -> None:
    driver = selenium[browser_id]
    panel = getattr(OZLoggedIn(driver), oz_panel)
    items = getattr(panel, f"{item_type}s")
    assert (
        item_name in items
    ), f'no {item_type} named "{item_name}" found in {oz_panel} oz panel'


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that (?P<item_type>provider) "
        r'named "(?P<item_name>.+?)" has disappeared from expanded '
        r'"(?P<oz_panel>GO TO YOUR FILES)" Onezone panel'
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that there is no "
        r'(?P<item_type>provider) named "(?P<item_name>.+?)" '
        r'in expanded "(?P<oz_panel>GO TO YOUR FILES)" Onezone panel'
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that (?P<item_type>space) "
        r'named "(?P<item_name>.+?)" has disappeared from expanded '
        r'"(?P<oz_panel>DATA SPACE MANAGEMENT)" Onezone panel'
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that there is no "
        r'(?P<item_type>space) named "(?P<item_name>.+?)" in expanded '
        r'"(?P<oz_panel>DATA SPACE MANAGEMENT)" Onezone panel'
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that (?P<item_type>group) "
        r'named "(?P<item_name>.+?)" has disappeared from expanded '
        r'"(?P<oz_panel>GROUP MANAGEMENT)" Onezone panel'
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that there is no "
        r'(?P<item_type>group) named "(?P<item_name>.+?)" in expanded '
        r'"(?P<oz_panel>GROUP MANAGEMENT)" Onezone panel'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_there_is_no_item_named_in_oz_panel_list(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_type: str,
    item_name: str,
    oz_panel: str,
    hosts: Hosts,
) -> None:
    driver = selenium[browser_id]
    if item_type == "provider":
        item_name = hosts[item_name]["name"]
    panel = getattr(OZLoggedIn(driver), oz_panel)
    items = {item.name for item in getattr(panel, f"{item_type}s")}
    assert item_name not in items, (
        f'{item_type} named "{item_name}" found in {oz_panel} oz panel while it'
        " should not be found"
    )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that "
        r"(?P<counter_type>space)s counter for (?P<item_type>provider) "
        r'"(?P<item_name>.+?)" displays (?P<number>\d+) in expanded '
        r'"(?P<oz_panel>GO TO YOUR FILES)" Onezone panel'
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that "
        r"(?P<counter_type>provider)s counter for (?P<item_type>space) "
        r'named "(?P<item_name>.+?)" displays (?P<number>\d+) '
        r'in expanded "(?P<oz_panel>DATA SPACE MANAGEMENT)" Onezone panel'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_item_counter_match_given_num(
    selenium: SeleniumDrivers,
    browser_id: str,
    counter_type: str,
    item_type: str,
    item_name: str,
    number: str,
    oz_panel: str,
    hosts: Hosts,
) -> None:
    driver = selenium[browser_id]
    if item_type == "provider":
        item_name = hosts[item_name]["name"]
    panel = getattr(OZLoggedIn(driver), oz_panel)
    items = getattr(panel, f"{item_type}s")
    item = items[item_name]
    item_counter = int(getattr(item, f"{counter_type}s_count"))

    msg = (
        "expected {counter_type}s number {num} does not match "
        "displayed {counter_type}s counter {displayed} "
        'for {type} named "{name}"'
    )
    assert item_counter == int(number), msg.format(
        type=item_type,
        name=item_name,
        counter_type=counter_type,
        displayed=item_counter,
        num=number,
    )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that "
        r'(?P<counter_type>space)s counter for "(?P<item_name>.+?)" '
        r"match number of displayed  supported spaces in expanded "
        r"submenu of given (?P<item_type>provider) in expanded "
        r'"(?P<oz_panel>GO TO YOUR FILES)" Onezone panel'
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that "
        r"(?P<counter_type>provider)s "
        r'counter for "(?P<item_name>.+?)" match number of displayed '
        r"supporting providers in expanded submenu "
        r"of given (?P<item_type>space) in expanded "
        r'"(?P<oz_panel>DATA SPACE MANAGEMENT)" Onezone panel'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_number_of_items_match_items_counter(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_name: str,
    item_type: str,
    counter_type: str,
    oz_panel: str,
    hosts: Hosts,
) -> None:
    driver = selenium[browser_id]
    if item_type == "provider":
        item_name = hosts[item_name]["name"]
    panel = getattr(OZLoggedIn(driver), oz_panel)
    items = getattr(panel, f"{item_type}s")
    item = items[item_name]
    subitems = getattr(item, f"{counter_type}s")
    counter = int(getattr(item, f"{counter_type}s_count"))

    error_message = (
        "{type}s counter number {counter} does not match displayed "
        "number of {type}s {list_len}"
    )
    assert counter == subitems.count(), error_message.format(
        type=counter_type, counter=counter, list_len=subitems.count()
    )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) expands submenu of "
        r'(?P<item_type>provider) "(?P<item_name>.+?)" by '
        r"clicking on cloud in provider record in expanded "
        r'"(?P<oz_panel>GO TO YOUR FILES)" Onezone panel'
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) expands submenu of "
        r'(?P<item_type>space) named "(?P<item_name>.+?)" '
        r"by clicking on space record in expanded "
        r'"(?P<oz_panel>DATA SPACE MANAGEMENT)" Onezone panel'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def expand_items_submenu_in_oz_panel(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_type: str,
    item_name: str,
    oz_panel: str,
    hosts: Hosts,
) -> None:
    driver = selenium[browser_id]
    if item_type == "provider":
        item_name = hosts[item_name]["name"]
    panel = getattr(OZLoggedIn(driver), oz_panel)
    items = getattr(panel, f"{item_type}s")
    item = items[item_name]
    item.expand()
    error_message = 'submenu for {type} named "{name}" has not been expanded'
    assert item.is_expanded(), error_message.format(type=item_type, name=item_name)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that there is "
        r'(?P<subitem_type>provider) "(?P<subitem_name>.+?)" in '
        r'submenu of (?P<item_type>space) named "(?P<item_name>.+?)" '
        r'in expanded "(?P<oz_panel>DATA SPACE MANAGEMENT)" Onezone panel'
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that there is "
        r'(?P<subitem_type>space) named "(?P<subitem_name>.+?)" '
        r'in submenu of (?P<item_type>provider) "(?P<item_name>.+?)" '
        r'in expanded "(?P<oz_panel>GO TO YOUR FILES)" Onezone panel'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_item_in_submenu_of_item_in_oz_panel(
    selenium: SeleniumDrivers,
    browser_id: str,
    subitem_type: str,
    subitem_name: str,
    item_type: str,
    item_name: str,
    oz_panel: str,
    hosts: Hosts,
) -> None:
    driver = selenium[browser_id]
    if item_type == "provider":
        item_name = hosts[item_name]["name"]
    if subitem_type == "provider":
        subitem_name = hosts[subitem_name]["name"]
    panel = getattr(OZLoggedIn(driver), oz_panel)
    items = getattr(panel, f"{item_type}s")
    item = items[item_name]
    subitems = getattr(item, f"{subitem_type}s")
    assert (
        subitem_name in subitems
    ), f'no "{subitem_name}" found in subitems of "{item_name}" in {oz_panel}'
