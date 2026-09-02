"""This module contains gherkin steps to run acceptance tests featuring
public shares interface in oneprovider web GUI.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from collections.abc import Iterable

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from tests.gui.constants import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils import PrivateShareView as private_share
from tests.gui.utils import PublicShareView as public_share
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    parse_elements_sequence,
    transform,
)
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        "user of {browser_id} changes current working directory "
        "to {path} using breadcrumbs on share's public interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def change_public_share_cwd_using_breadcrumbs(
    selenium: SeleniumDrivers, browser_id: str, path: str
) -> None:
    public_share(selenium[browser_id]).breadcrumbs.chdir(path)


@wt(
    parsers.parse(
        "user of {browser_id} changes current working "
        "directory to current share using breadcrumbs on share's public interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def change_public_share_to_home_cwd_using_breadcrumbs(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    public_share(selenium[browser_id]).breadcrumbs.home.click()


def _change_iframe_for_public_share_page(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    iframe = driver.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(iframe)


@wt(
    parsers.parse('user of {browser_id} sees that public share is named "{share_name}"')
)
@repeat_failed(timeout=WAIT_BACKEND, interval=0.5)
def assert_public_share_named(
    selenium: SeleniumDrivers, browser_id: str, share_name: str
) -> None:
    _change_iframe_for_public_share_page(selenium, browser_id)
    displayed_name = public_share(selenium[browser_id]).share_name
    assert displayed_name == share_name, (
        "displayed public share name "
        f'is "{displayed_name}" instead of '
        f'expected "{share_name}"'
    )


@wt(
    parsers.parse(
        "user of {browser_id} sees that current working directory "
        "path visible in share's public interface file browser is as follows: {cwd}"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def is_public_share_cwd_correct(
    selenium: SeleniumDrivers, browser_id: str, cwd: str
) -> None:
    displayed_cwd = public_share(selenium[browser_id]).breadcrumbs.pwd()
    assert displayed_cwd == cwd, (
        "displayed share cwd in file browser"
        f" is {displayed_cwd} "
        f"instead of expected {cwd}"
    )


@wt(
    parsers.parse(
        "user of {browser_id} sees share's file browser on share's public interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_file_browser_in_public_share(
    selenium: SeleniumDrivers, browser_id: str, tmp_memory: TmpMemory
) -> None:
    file_browser = public_share(selenium[browser_id]).shares_file_browser
    tmp_memory[browser_id]["shares_file_browser"] = file_browser


@wt(parsers.parse('user of {browser_id} sees "{error_msg}" error'))
@repeat_failed(timeout=WAIT_FRONTEND)
def no_public_share_view(
    selenium: SeleniumDrivers, browser_id: str, error_msg: str
) -> None:
    error_msg = error_msg.upper()
    driver = selenium[browser_id]

    assert (
        error_msg == public_share(driver).share_not_found
    ), f"displayed error msg does not contain {error_msg}"


@wt(
    parsers.parse(
        'user of {browser_id} sees "{description}" description '
        "on share's public interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_proper_description(
    selenium: SeleniumDrivers, browser_id: str, description: str
) -> None:
    driver = selenium[browser_id]
    _change_iframe_for_public_share_page(selenium, browser_id)

    description_on_page = public_share(driver).description
    error_message = f"found {description_on_page} instead of {description}"
    assert description_on_page == description, error_message


@wt(
    parsers.parse(
        'user of {browser_id} sees "{message}" '
        "instead of file browser on share's public interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_message_no_file_browser(
    selenium: SeleniumDrivers, browser_id: str, message: str
) -> None:
    driver = selenium[browser_id]
    _change_iframe_for_public_share_page(selenium, browser_id)
    msg = public_share(driver).no_files_message_header
    assert msg == message, f"{message} not on share's public interface"


@wt(
    parsers.parse(
        "user of {browser_id} clicks share link type selector "
        "on share's public interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_public_share_link_type_selector(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    public_share(selenium[browser_id]).link_type_selector()


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{url_type}" share link type '
        "on share's public interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_public_share_link_type(
    selenium: SeleniumDrivers, browser_id: str, url_type: str
) -> None:
    driver = selenium[browser_id]
    type_popup = public_share(driver).url_type_popup
    getattr(type_popup, transform(url_type))()


@wt(
    parsers.parse(
        "user of {browser_id} copies share REST endpoint on share's public interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_public_share_link(selenium: SeleniumDrivers, browser_id: str) -> None:
    public_share(selenium[browser_id]).copy_icon()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) opens "(?P<tab>.*)" tab on share\'s'
        r" (public|private) interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def open_tab_in_public_share(
    selenium: SeleniumDrivers, browser_id: str, tab: str
) -> None:
    tab = transform(tab) + "_tab"
    driver = selenium[browser_id]
    _change_iframe_for_public_share_page(selenium, browser_id)
    getattr(public_share(driver), tab)()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) sees "(?P<tab_name>.*)" tab '
        r"on share's (public|private) interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_tab_in_public_share(
    selenium: SeleniumDrivers, browser_id: str, tab_name: str
) -> None:
    tab_name = transform(tab_name)
    driver = selenium[browser_id]
    _change_iframe_for_public_share_page(selenium, browser_id)
    tabs = driver.find_elements(By.CSS_SELECTOR, ".nav-tabs-share-mode li")
    for tab in tabs:
        if transform(tab.text) == tab_name:
            error_message = f"tab {tab_name} is not active"
            assert "active" in tab.get_attribute("class"), error_message
            return
    raise AssertionError(f"did not manage to find tab {tab_name}")


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) clicks "(?P<button>.*)" button on '
        r"share's (?P<option>public|private) interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_in_share(
    selenium: SeleniumDrivers, browser_id: str, button: str, option: str
) -> None:
    driver = selenium[browser_id]
    if option == "public":
        getattr(public_share(driver), transform(button))()
    else:
        getattr(private_share(driver), transform(button))()


def check_item_presence_in_dublin_core_metadata(
    driver: WebDriver, item: str, data: Iterable[WebElement]
) -> None:
    for info in data:
        if info.text == "":
            driver.execute_script("arguments[0].scrollIntoView();", info)
        if info.text == item:
            break
    else:
        raise AssertionError(f'{item} was not found in "Dublin Core Metadata"')


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_data_in_dublin_core_metadata(
    browser_id: str, data: list[str], selenium: SeleniumDrivers
) -> None:
    driver = selenium[browser_id]
    dublin_core = public_share(driver).dublin_core_metadata_data

    for item in data:
        check_item_presence_in_dublin_core_metadata(
            selenium[browser_id], item, dublin_core
        )


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) copies "(?P<link>.*?)" from'
        r" share's (public|private) interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_link_in_shares_interface(browser_id: str, selenium: SeleniumDrivers) -> None:
    driver = selenium[browser_id]
    public_share(driver).copy_link()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) sees that XML data contains "
        rf"(?P<data>{ELEMENTS_SEQUENCE_PATTERN}) on share's (public|private) interface"
    ),
    converters={
        "data": parse_elements_sequence,
    },
)
def assert_xml_data_in_shares(
    selenium: SeleniumDrivers, browser_id: str, data: list[str]
) -> None:
    driver = selenium[browser_id]
    xml_data = public_share(driver).xml_data_dublin_core
    for item in data:
        assert item in xml_data, f"{item} not in XML data on share's public interface"
