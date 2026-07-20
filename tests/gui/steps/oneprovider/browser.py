"""Steps used for common in different browsers operations in Oneprovider GUI"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
import re
import time
from collections.abc import Callable, Collection, Sequence
from datetime import datetime
from typing import Optional, Protocol

from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import network_throttling_download
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils import OPLoggedIn, OZLoggedIn, Popups
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    WhichBrowser,
    parse_elements_sequence,
    parse_seq,
    sort_json_from_string,
    transform,
)
from tests.gui.utils.oneprovider.browser import Browser
from tests.gui.utils.oneprovider.browser_row import BrowserRow
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


class MenuOption(Protocol):
    def get_state(self) -> str: ...


class RowMenu(Protocol):
    def choose_option(self, option: str) -> None: ...

    def return_option(self, name: str) -> MenuOption: ...


@repeat_failed(timeout=WAIT_BACKEND)
def click_and_press_enter_on_item_in_browser(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_name: str,
    tmp_memory: TmpMemory,
    which_browser: str,
) -> None:
    which_browser = transform(which_browser)
    browser = tmp_memory[browser_id][which_browser]
    driver = selenium[browser_id]

    # clicking on the background of browser to ensure correct
    # working of click_and enter
    browser.click_on_background()
    # checking if file is located in file browser
    start = time.time()
    while item_name not in browser.data:
        time.sleep(1)
        if time.time() > start + WAIT_BACKEND:
            raise RuntimeError("waited too long")

    click_and_enter_with_check(driver, browser, which_browser, item_name)


@wt(
    parsers.parse(
        "user of {browser_id} clicks and presses enter on item named"
        ' "{item_name}" in {which_browser}'
    )
)
def wt_click_and_press_enter_on_item_in_browser(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_name: str,
    tmp_memory: TmpMemory,
    which_browser: str,
) -> None:
    click_and_press_enter_on_item_in_browser(
        selenium,
        browser_id,
        item_name,
        tmp_memory,
        which_browser=which_browser,
    )


@repeat_failed(timeout=WAIT_BACKEND)
def click_and_enter_with_check(
    driver: WebDriver, browser: Browser, which_browser: str, item_name: str
) -> None:
    # this function does not check correctly if parent and children directory
    # have the same name
    browser.data[item_name].click_and_enter()
    if item_name.startswith("dir"):
        for _ in range(5):
            breadcrumbs = check_if_breadcrumbs_on_share_page(driver, which_browser)
            if breadcrumbs.split("/")[-1] == item_name:
                return
            time.sleep(1)
        raise RuntimeError("Click and enter has not entered the directory")


@repeat_failed(timeout=WAIT_BACKEND)
def check_if_breadcrumbs_on_share_page(driver: WebDriver, which_browser: str) -> str:
    try:
        breadcrumbs = OPLoggedIn(driver).shares_page.breadcrumbs.pwd()
    except RuntimeError:
        which_browser = transform(which_browser)
        if which_browser == "shares_file_browser":
            which_browser = "file_browser"
        breadcrumbs = getattr(OPLoggedIn(driver), which_browser).breadcrumbs.pwd()
    return breadcrumbs


@wt(
    parsers.parse(
        "user of {browser_id} sees that current working directory "
        'displayed in breadcrumbs on {which_browser} is "{path}"'
    )
)
def wt_is_displayed_breadcrumbs_in_data_tab_in_op_correct(
    selenium: SeleniumDrivers, browser_id: str, path: str, which_browser: str
) -> None:
    is_displayed_breadcrumbs_in_data_tab_in_op_correct(
        selenium, browser_id, path, which_browser=which_browser
    )


@repeat_failed(timeout=WAIT_BACKEND)
def is_displayed_breadcrumbs_in_data_tab_in_op_correct(
    selenium: SeleniumDrivers,
    browser_id: str,
    path: str,
    which_browser: str = "file browser",
) -> None:
    driver = selenium[browser_id]
    breadcrumbs = getattr(
        OPLoggedIn(driver), transform(which_browser)
    ).breadcrumbs.pwd()

    if which_browser == "archive file browser":
        breadcrumbs = re.split("/", breadcrumbs, 2)[-1]
        path = re.split("/", path, 2)[-1]

    assert path == breadcrumbs, f"expected breadcrumbs {path}; displayed: {breadcrumbs}"


@wt(
    parsers.parse(
        "user of {browser_id} clicks on menu on breadcrumbs in {which_browser}"
    )
)
def wt_click_on_breadcrumbs_menu(
    selenium: SeleniumDrivers, browser_id: str, which_browser: str
) -> None:
    click_on_breadcrumbs_menu(selenium, browser_id, which_browser=which_browser)


@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_breadcrumbs_menu(
    selenium: SeleniumDrivers,
    browser_id: str,
    which_browser: str = "file browser",
) -> None:
    driver = selenium[browser_id]
    breadcrumbs = getattr(OPLoggedIn(driver), transform(which_browser)).breadcrumbs
    breadcrumbs.menu_button()


@repeat_failed(timeout=WAIT_FRONTEND)
def _get_items_list_from_browser(
    selenium: SeleniumDrivers,
    browser_id: str,
    tmp_memory: TmpMemory,
    which_browser: str = "file browser",
) -> Collection[str]:

    browser = tmp_memory[browser_id][transform(which_browser)]
    data: Collection[str] = {f.name for f in browser.data if f.name}
    driver = selenium[browser_id]
    if len(data) != len(browser.data):

        def condition(data_: dict[str, BrowserRow]) -> bool:
            return len(data_) != len(browser.data)

        data = _gather_data_from_browser(driver, browser, condition)
        browser.scroll_to_number_file(driver, 2, browser)

    return data


def _gather_data_from_browser(
    driver: WebDriver,
    browser: Browser,
    condition: Callable[[dict[str, BrowserRow]], bool],
) -> dict[str, BrowserRow]:
    data = {f.name: f for f in browser.data if f.name}
    while condition(data):
        browser.scroll_to_number_file(driver, len(data), browser)
        partial_data = {f.name: f for f in browser.data if f.name}
        data.update(partial_data)

    return data


@wt(
    parsers.parse(
        "user of {browser_id} sees item(s) named "
        "{item_list:ElementsSequence} in "
        "{which_browser:WhichBrowser}",
        extra_types={
            "ElementsSequence": parse_elements_sequence,
            "WhichBrowser": WhichBrowser,
        },
    )
)
@wt(
    parsers.re(
        rf"user of (?P<browser_id>.*?) sees that items? named "
        rf"(?P<item_list>{ELEMENTS_SEQUENCE_PATTERN}) (?:has|have) appeared in "
        rf"(?P<which_browser>{r'|'.join(re.escape(item.value) for item in WhichBrowser)})"
    ),
    converters={
        "item_list": parse_elements_sequence,
    },
)
def wt_assert_items_presence_in_browser(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_list: list[str],
    tmp_memory: TmpMemory,
    which_browser: WhichBrowser | str,
) -> None:
    browser_name = (
        which_browser.value
        if isinstance(which_browser, WhichBrowser)
        else which_browser
    )
    assert_items_presence_in_browser(
        selenium, browser_id, item_list, tmp_memory, which_browser=browser_name
    )


@repeat_failed(timeout=WAIT_BACKEND)
def assert_items_presence_in_browser(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_list: list[str],
    tmp_memory: TmpMemory,
    which_browser: str = "file browser",
) -> None:
    data = _get_items_list_from_browser(selenium, browser_id, tmp_memory, which_browser)
    for item_name in item_list:
        assert item_name in data, f'not found "{item_name}" in browser'


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_only_expected_items_presence_in_browser(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_list: str | Sequence[str],
    tmp_memory: TmpMemory,
    which_browser: str = "file browser",
) -> None:
    data = _get_items_list_from_browser(selenium, browser_id, tmp_memory, which_browser)

    expected_items = parse_seq(item_list) if isinstance(item_list, str) else item_list
    assert len(expected_items) == len(data), (
        f"there is different number of items in {which_browser}, "
        f"actual items: {data}, expected items: {item_list}"
    )

    assert_items_presence_in_browser(
        selenium, browser_id, list(expected_items), tmp_memory, which_browser
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def check_if_item_is_dir_in_browser(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_name: str,
    tmp_memory: TmpMemory,
    which_browser: str = "file browser",
) -> bool:
    driver = selenium[browser_id]
    browser = tmp_memory[browser_id][transform(which_browser)]
    data = [f.name for f in browser.data if f.name]

    while item_name not in data and len(data) != len(browser.data):
        browser.scroll_to_number_file(driver, len(data), browser)
        partial_data = [f.name for f in browser.data if f.name]
        data.extend(partial_data)

    try:
        item = browser.data[item_name]
    except RuntimeError:
        browser.scroll_to_number_file(driver, data.index(item_name), browser)
        item = browser.data[item_name]

    return not item.is_file()


@wt(
    parsers.re(
        rf"user of (?P<browser_id>.*?) sees that items? named "
        rf"(?P<item_list>{ELEMENTS_SEQUENCE_PATTERN}) (?:has|have) disappeared "
        r"from (?P<which_browser>.*)"
    ),
    converters={
        "item_list": parse_elements_sequence,
    },
)
@wt(
    parsers.parse(
        "user of {browser_id} does not see any item(s) named "
        "{item_list:ElementsSequence} in {which_browser}",
        extra_types={"ElementsSequence": parse_elements_sequence},
    ),
)
def wt_assert_items_absence_in_browser(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_list: list[str],
    tmp_memory: TmpMemory,
    which_browser: str,
) -> None:
    assert_items_absence_in_browser(
        selenium, browser_id, item_list, tmp_memory, which_browser=which_browser
    )


@repeat_failed(timeout=WAIT_BACKEND)
def assert_items_absence_in_browser(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_list: list[str],
    tmp_memory: TmpMemory,
    which_browser: str = "file browser",
) -> None:
    data = _get_items_list_from_browser(selenium, browser_id, tmp_memory, which_browser)
    for item_name in item_list:
        assert (
            item_name not in data
        ), f'found "{item_name}" in browser, while it should not'


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that there "
        r"(is 1|are (?P<num>\d+)) items? in (?P<which_browser>.*)"
    )
)
def assert_num_of_files_are_displayed_in_browser_(
    browser_id: str, num: Optional[str], tmp_memory: TmpMemory, which_browser: str
) -> None:
    expected_num = 1 if num is None else int(num)
    assert_num_of_files_are_displayed_in_browser(
        browser_id, expected_num, tmp_memory, which_browser=which_browser
    )


@repeat_failed(timeout=WAIT_BACKEND)
def assert_num_of_files_are_displayed_in_browser(
    browser_id: str,
    num: int,
    tmp_memory: TmpMemory,
    which_browser: str = "file_browser",
) -> None:
    browser = tmp_memory[browser_id][transform(which_browser)]
    error_message = "displayed number of files {} does not match expected {}"
    files_num = browser.data.count()
    assert files_num == num, error_message.format(files_num, num)


@wt(
    parsers.parse(
        "user of {browser_id} sees {status_type} "
        'status tag for "{item_name}" in {which_browser}'
    )
)
def wt_assert_status_tag_for_file_in_browser(
    browser_id: str,
    status_type: str,
    item_name: str,
    tmp_memory: TmpMemory,
    which_browser: str,
) -> None:
    assert_status_tag_for_file_in_browser(
        browser_id,
        status_type,
        item_name,
        tmp_memory,
        which_browser=which_browser,
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_status_tag_for_file_in_browser(
    browser_id: str,
    status_type: str,
    item_name: str,
    tmp_memory: TmpMemory,
    which_browser: str = "file browser",
) -> None:
    browser = tmp_memory[browser_id][transform(which_browser)]
    error_message = f"{status_type} tag for {item_name} in {which_browser} not visible"
    assert browser.data[item_name].is_tag_visible(transform(status_type)), error_message


@wt(
    parsers.parse(
        "user of {browser_id} sees {status_type} "
        'status tag with "{text}" text for "{item_name}" in {which_browser}'
    )
)
def wt_assert_status_tag_text_for_file_in_browser(
    browser_id: str,
    status_type: str,
    text: str,
    item_name: str,
    tmp_memory: TmpMemory,
    which_browser: str,
) -> None:
    assert_status_tag_text_for_file_in_browser(
        browser_id,
        status_type,
        text,
        item_name,
        tmp_memory,
        which_browser=which_browser,
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_status_tag_text_for_file_in_browser(
    browser_id: str,
    status_type: str,
    text: str,
    item_name: str,
    tmp_memory: TmpMemory,
    which_browser: str = "file browser",
) -> None:
    assert_status_tag_for_file_in_browser(
        browser_id, status_type, item_name, tmp_memory, which_browser
    )
    browser = tmp_memory[browser_id][transform(which_browser)]
    actual_text = browser.data[item_name].get_tag_text(transform(status_type))
    error_message = (
        f"{status_type} tag for {item_name} in browser has text "
        f"{actual_text} not {text}"
    )
    assert actual_text == text, error_message


@wt(
    parsers.parse(
        "user of {browser_id} does not see {status_type} "
        'status tag for "{item_name}" in {which_browser}'
    )
)
def wt_assert_not_status_tag_for_file_in_browser(
    browser_id: str,
    status_type: str,
    item_name: str,
    tmp_memory: TmpMemory,
    which_browser: str,
) -> None:
    assert_not_status_tag_for_file_in_browser(
        browser_id,
        status_type,
        item_name,
        tmp_memory,
        which_browser=which_browser,
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_not_status_tag_for_file_in_browser(
    browser_id: str,
    status_type: str,
    item_name: str,
    tmp_memory: TmpMemory,
    which_browser: str = "file browser",
) -> None:
    browser = tmp_memory[browser_id][transform(which_browser)]
    error_message = (
        f"{status_type} tag for {item_name} in {which_browser} visible, "
        "while should not be"
    )
    assert not browser.data[item_name].is_tag_visible(status_type), error_message


def _choose_menu(
    selenium: SeleniumDrivers, browser_id: str, which_browser: str
) -> RowMenu:
    if which_browser in ["archive browser", "dataset archive browser"]:
        return Popups(selenium[browser_id]).archive_row_menu
    if which_browser == "dataset browser":
        return Popups(selenium[browser_id]).dataset_row_menu
    if which_browser == "automation workflows page":
        return Popups(selenium[browser_id]).workflow_menu
    return Popups(selenium[browser_id]).data_row_menu


@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_data_row_menu_in_browser(
    selenium: SeleniumDrivers,
    browser_id: str,
    option: str,
    which_browser: str = "file browser",
) -> None:
    menu = _choose_menu(selenium, browser_id, which_browser)
    menu.choose_option(option)


@wt(
    parsers.re(
        r'(using web GUI, )?user of (?P<browser_id>.*) clicks "(?P<option>.*)" option '
        r"in data row menu in (?P<which_browser>.*)"
    )
)
def wt_click_option_in_data_row_menu_in_browser(
    selenium: SeleniumDrivers, browser_id: str, option: str, which_browser: str
) -> None:
    click_option_in_data_row_menu_in_browser(
        selenium, browser_id, option, which_browser=which_browser
    )


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{option}" option is '
        "{option_state} in opened item menu in {which_browser}"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_option_state_in_data_row_menu(
    selenium: SeleniumDrivers,
    browser_id: str,
    option: str,
    option_state: str,
    which_browser: str,
) -> None:
    error_message = (
        f"{option} option is not {option_state} in opened item menu in file browser"
    )

    menu = _choose_menu(selenium, browser_id, which_browser)
    menu_option = menu.return_option(option)
    assert menu_option.get_state() == option_state, error_message


@wt(
    parsers.parse(
        "user of {browser_id} clicks on {state} view mode on {which} browser page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_state_view_mode_tab(
    browser_id: str,
    selenium: SeleniumDrivers,
    state: str,
    which: str,
    tmp_memory: TmpMemory,
) -> None:
    driver = selenium[browser_id]
    if which == "archive file":
        which_browser = which + " browser"
        browser = tmp_memory[browser_id][transform(which_browser)]
        browser.click_on_dip_aip_view_mode(driver, transform(state))
    else:
        driver.switch_to.default_content()
        header = f"{transform(which)}_header"
        getattr(getattr(OZLoggedIn(driver).data, header), transform(state))()
    # if we make call to fast after changing view mode
    # we do not see items in this mode, to avoid this wait some time
    time.sleep(0.5)


@wt(
    parsers.re(
        r"(using web GUI, )?user of (?P<browser_id>.*) clicks on menu for"
        r' "(?P<item_name>.*)" '
        r"(?P<type>dataset|directory|file) in (?P<which_browser>.*)"
    )
)
def wt_click_menu_for_elem_in_browser(
    browser_id: str, item_name: str, tmp_memory: TmpMemory, which_browser: str
) -> None:
    click_menu_for_elem_in_browser(
        browser_id, item_name, tmp_memory, which_browser=which_browser
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def click_menu_for_elem_in_browser(
    browser_id: str,
    item_name: str | int,
    tmp_memory: TmpMemory,
    which_browser: str = "file browser",
) -> None:
    browser = tmp_memory[browser_id][transform(which_browser)]
    browser.data[item_name].menu_button()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) clicks on (?P<tag>.*tag.*|.*icon.*) "
        r'for "(?P<item_name>.*)" (?P<type>.*) in (?P<which_browser>.*)'
    )
)
@wt(
    parsers.re(
        r"using web GUI, user of (?P<browser_id>.*) clicks on"
        r" (?P<tag>.*tag.*|.*icon.*) "
        r'for "(?P<item_name>.*)" in (?P<which_browser>.*) in (?P<host>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_tag_for_elem_in_browser(
    browser_id: str,
    item_name: str,
    tmp_memory: TmpMemory,
    tag: str,
    which_browser: str,
) -> None:
    browser = tmp_memory[browser_id][transform(which_browser)]
    getattr(browser.data[item_name], transform(tag)).click()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees that item named "
        r'"(?P<item_name>.*)" is of (?P<value>.*) (?P<option>size) in '
        r"(?P<which_browser>archive file browser|file browser)"
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees that item named "
        r'"(?P<item_name>.*)" has (?P<value>.*) (?P<option>replication '
        r"rate) in (?P<which_browser>archive file browser|file browser)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_value_in_column_for_item(
    browser_id: str,
    item_name: str,
    value: str,
    option: str,
    which_browser: str,
    selenium: SeleniumDrivers,
) -> None:
    driver = selenium[browser_id]
    browser = getattr(OPLoggedIn(driver), transform(which_browser))
    item_elem = getattr(browser.data[item_name], transform(option))
    error_message = (
        f"displayed {option} {item_elem} for {item_name} does not "
        f"match expected {value}"
    )

    assert value == item_elem, error_message


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees that item named "
        r'"(?P<item_name>.*)" (?P<res>has|does not have)'
        r' "(?P<value>.*)" value in (?P<option>xattr)'
        r" column in (?P<which_browser>archive file browser|file browser)"
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees that "
        r'item named "(?P<item_name>.*)"'
        r" (?P<res>has|does not have) '(?P<value>.*)'"
        r" value in (?P<option>json) column "
        r"in (?P<which_browser>archive file browser|file browser)"
    )
)
def assert_value_in_xattr_or_json_column_for_item(
    browser_id: str,
    item_name: str,
    res: str,
    value: str,
    option: str,
    which_browser: str,
    selenium: SeleniumDrivers,
) -> None:
    driver = selenium[browser_id]
    browser = getattr(OPLoggedIn(driver), transform(which_browser))
    item_elem = getattr(browser.data[item_name], option)
    error_message_prefix = f"displayed {option} value {item_elem} for {item_name}"

    if option == "json":
        if not item_elem.endswith("…"):  # json column is not truncated in UI
            expected_value = sort_json_from_string(value)
            item_elem = json.loads(item_elem.replace("\n", ""))
        else:
            expected_value = value.replace(" ", "")
            item_elem = item_elem.replace("\n", "").replace(" ", "")
    else:
        expected_value = value

    if res == "has":
        error_message = (
            error_message_prefix + f" does not match expected {expected_value}"
        )
        assert expected_value == item_elem, error_message
    else:
        error_message = (
            error_message_prefix + f" is not supposed to be equal to {expected_value}"
        )
        assert expected_value != item_elem, error_message


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees that item named "
        r'"(?P<item_name>.*)" has no (?P<option>json|xattr) column '
        r"in (?P<which_browser>archive file browser|file browser)"
    )
)
def assert_no_column_for_item(
    browser_id: str,
    item_name: str,
    option: str,
    which_browser: str,
    selenium: SeleniumDrivers,
) -> None:
    driver = selenium[browser_id]
    browser = getattr(OPLoggedIn(driver), transform(which_browser))

    try:  # this try except block covers cases when xattr value doesn't exist
        _ = getattr(browser.data[item_name], option)

    except RuntimeError as e:
        if "item found in" not in str(e):
            raise AssertionError from e  # if the error does not match expected error
            # The expected error:
            # RuntimeError: no {} item found in {} in file browser in Oneprovider page


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) saves content of "(?P<option>.*)" '
        r'column for "(?P<item_name>.*)" in '
        r"(?P<which_browser>archive file browser|file browser)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def save_value_in_column_for_item(
    browser_id: str,
    item_name: str,
    option: str,
    which_browser: str,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
) -> None:
    driver = selenium[browser_id]
    browser = getattr(OPLoggedIn(driver), transform(which_browser))
    value = getattr(browser.data[item_name], transform(option))
    tmp_memory["columns-content"] = {item_name: value}


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees that date time in "
        r'"(?P<option>.*)" column for "(?P<item_name>.*)" has become '
        r"more current in (?P<which_browser>archive file browser|file browser)"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def compare_value_in_column_for_item(
    browser_id: str,
    item_name: str,
    option: str,
    which_browser: str,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
) -> None:
    driver = selenium[browser_id]
    browser = getattr(OPLoggedIn(driver), transform(which_browser))
    new_value = getattr(browser.data[item_name], transform(option))
    old_value = tmp_memory["columns-content"][item_name]
    new_value = datetime.strptime(new_value, "%d %b %Y %H:%M:%S")
    old_value = datetime.strptime(old_value, "%d %b %Y %H:%M:%S")
    error_message = (
        f"visible date time: {new_value} is not more current than {old_value}"
    )
    assert new_value > old_value, error_message


@wt(
    parsers.re(
        rf"user of (?P<browser_id>.*) sees only "
        rf"(?P<columns>{ELEMENTS_SEQUENCE_PATTERN}) columns "
        r"in (?P<which_browser>file browser|archive browser|dataset browser)"
    ),
    converters={
        "columns": parse_elements_sequence,
    },
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_visible_columns_in_browser(
    browser_id: str, tmp_memory: TmpMemory, columns: list[str], which_browser: str
) -> None:
    browser = tmp_memory[browser_id][transform(which_browser)]
    browser_columns = browser.column_headers
    browser_columns = list(map(lambda x: x.name.lower(), browser_columns))
    error_message = (
        "there is different number of columns visible: "
        f"{len(browser_columns)} than expected: {len(columns)}, in "
        f"{which_browser}"
    )
    assert len(columns) == len(browser_columns), error_message
    for column in columns:
        if column.lower() not in browser_columns:
            raise AssertionError(f"column {column} is not visible in {which_browser}")


@wt(
    parsers.parse(
        'user of {browser_id} does not see button "{button}" in {which_browser}'
    )
)
def assert_button_not_visible_in_browser(
    browser_id: str, tmp_memory: TmpMemory, button: str, which_browser: str
) -> None:
    browser = tmp_memory[browser_id][transform(which_browser)]
    try:
        getattr(browser, transform(button) + "_button")
        raise AssertionError(f"button {button} is visible in {which_browser} browser")
    except RuntimeError:
        pass


@wt(parsers.parse('user of {browser_id} clicks on "navigate to root directory" button'))
def navigate_to_root_from_error_page(
    browser_id: str,
    tmp_memory: TmpMemory,
) -> None:
    browser = tmp_memory[browser_id]["file_browser"]
    browser.navigate_root_btn.click()


@wt(
    parsers.parse(
        'user of {browser_id} downloads item named "{item_name}" '
        "with slow connection in {which_browser}"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def download_file_with_network_throttling(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_name: str,
    tmp_memory: TmpMemory,
) -> None:
    driver = selenium[browser_id]
    network_throttling_download(driver)

    click_and_press_enter_on_item_in_browser(
        selenium, browser_id, item_name, tmp_memory, WhichBrowser.FILE_BROWSER.value
    )
