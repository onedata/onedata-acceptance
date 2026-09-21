"""Meta steps for browser columns configuration"""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json

import yaml
from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.steps.oneprovider.browser import (
    change_column_visibility,
    click_configure_columns_button,
    get_column_from_configure_columns_menu,
    get_column_names_from_configure_columns_menu,
)
from tests.gui.steps.oneprovider.common import wait_for_item_to_appear
from tests.gui.steps.oneprovider.transfers import get_transfers
from tests.gui.type_definitions import (
    Clipboard,
    ColumnContext,
    TmpMemory,
    VisibleColumns,
    WhichBrowser,
)
from tests.gui.utils import Popups
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    parse_elements_sequence,
    sort_json_from_string,
    transform,
)
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt

ADDITIONAL_TRANSFER_COLUMNS_USED_IN_TESTS = ["replicated", "type & destination"]
ALWAYS_VISIBLE_TRANSFER_COLUMNS = ["item type", "status"]


def set_column_visibility_in_configure_columns_menu(
    driver: WebDriver, column_name: str, visible: bool
) -> None:
    column = get_column_from_configure_columns_menu(driver, column_name)
    change_column_visibility(column, column_name, visible)


def set_exact_columns_visible_in_configure_columns_menu(
    driver: WebDriver, expected_columns: list[str]
) -> None:
    available_columns = transform_columns(get_column_names_from_configure_columns_menu(driver))
    expected_columns = transform_columns(expected_columns)

    for current_column in available_columns:
        set_column_visibility_in_configure_columns_menu(
            driver, current_column, current_column in expected_columns
        )


def select_columns_to_be_visible_in_transfers(
    selenium: SeleniumDrivers,
    browser_id: str,
    columns: list[str],
    visible_columns: VisibleColumns,
) -> None:
    columns = transform_columns(columns)
    driver = selenium[browser_id]

    visible_columns[ColumnContext.transfers(browser_id)] = set(columns)

    transfers = get_transfers(driver)
    click_configure_columns_button(transfers)
    set_exact_columns_visible_in_configure_columns_menu(driver, columns)
    click_configure_columns_button(transfers)


@wt(
    parsers.re(
        rf"user of (?P<browser_id>.*) enables only "
        rf"(?P<columns>{ELEMENTS_SEQUENCE_PATTERN}) "
        r"columns in columns configuration popover in transfers table"
    ),
    converters={
        "columns": parse_elements_sequence,
    },
)
def wt_select_columns_to_be_visible_in_transfers(
    selenium: SeleniumDrivers,
    browser_id: str,
    columns: list[str],
    visible_columns: VisibleColumns,
) -> None:
    select_columns_to_be_visible_in_transfers(selenium, browser_id, columns, visible_columns)


def select_initial_columns_to_be_visible_in_transfers(
    selenium: SeleniumDrivers, browser_id: str, visible_columns: VisibleColumns
) -> None:
    select_columns_to_be_visible_in_transfers(
        selenium,
        browser_id,
        ADDITIONAL_TRANSFER_COLUMNS_USED_IN_TESTS,
        visible_columns,
    )


def transform_columns(columns: list[str]) -> list[str]:
    return [transform(column) for column in columns]


@wt(
    parsers.re(
        rf"user of (?P<browser_id>.*) enables only "
        rf"(?P<columns>{ELEMENTS_SEQUENCE_PATTERN}) "
        r"columns? in columns configuration popover in "
        r"(?P<which_browser>file browser|archive browser|"
        r"dataset browser) table"
    ),
    converters={"columns": parse_elements_sequence, "which_browser": WhichBrowser},
)
def select_columns_to_be_visible_in_browser(
    selenium: SeleniumDrivers,
    browser_id: str,
    columns: list[str],
    which_browser: WhichBrowser,
    tmp_memory: TmpMemory,
    visible_columns: VisibleColumns,
) -> None:
    # This function enables the selected columns and disables the rest.
    browser = tmp_memory[browser_id][transform(which_browser.value)]

    visible_columns[ColumnContext.browser(browser_id, which_browser)] = set(
        transform_columns(columns)
    )

    click_configure_columns_button(browser)
    set_exact_columns_visible_in_configure_columns_menu(
        selenium[browser_id], expected_columns=columns
    )
    click_configure_columns_button(browser)


@wt(
    parsers.re(
        rf"user of (?P<browser_id>.*) (?P<res>disables|enables) "
        rf"(?P<columns>{ELEMENTS_SEQUENCE_PATTERN}) "
        r"columns? in columns configuration popover in "
        r"(?P<which_browser>file browser|archive browser|"
        r"dataset browser) table"
    ),
    converters={"columns": parse_elements_sequence, "which_browser": WhichBrowser},
)
def change_visibility_for_browser_columns(
    selenium: SeleniumDrivers,
    browser_id: str,
    res: str,
    columns: list[str],
    which_browser: WhichBrowser,
    tmp_memory: TmpMemory,
    visible_columns: VisibleColumns,
) -> None:
    # This function updates only the specified columns (enable/disable).
    # All other columns remain unchanged.

    browser = tmp_memory[browser_id][transform(which_browser.value)]
    driver = selenium[browser_id]
    click_configure_columns_button(browser)
    parsed_columns = transform_columns(columns)
    available_columns = transform_columns(get_column_names_from_configure_columns_menu(driver))

    for column_name in set(available_columns) & set(parsed_columns):
        if res == "enables":
            visible_columns[ColumnContext.browser(browser_id, which_browser)].add(column_name)
        set_column_visibility_in_configure_columns_menu(driver, column_name, res == "enables")

    click_configure_columns_button(browser)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) removes (?P<option>json|xattr) column "
        r'named "(?P<name>.*)" in columns configuration popover in (?P<which_browser>'
        r"file browser|archive browser|dataset browser) table"
    ),
    converters={"which_browser": WhichBrowser},
)
def remove_column(
    selenium: SeleniumDrivers,
    browser_id: str,
    name: str,
    which_browser: WhichBrowser,
    tmp_memory: TmpMemory,
) -> None:
    driver = selenium[browser_id]
    browser = tmp_memory[browser_id][transform(which_browser.value)]
    click_configure_columns_button(browser)

    wait_for_item_to_appear(Popups(selenium[browser_id]).configure_columns_menu.web_elem)

    current_column = get_column_from_configure_columns_menu(driver, name)
    current_column.hover_to_button_and_click("remove", driver)

    click_configure_columns_button(browser)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) modifies xattr column with"
        r' "(?P<name>.*)" key by changing (?P<elem>label|key)'
        r' to "(?P<new_elem_name>.*)" in (?P<which_browser>file'
        r" browser|archive browser|dataset browser) table"
    ),
    converters={"which_browser": WhichBrowser},
)
def modify_props_of_xattr_column_in_columns_menu(
    selenium: SeleniumDrivers,
    browser_id: str,
    which_browser: WhichBrowser,
    tmp_memory: TmpMemory,
    name: str,
    elem: str,
    new_elem_name: str,
) -> None:

    driver = selenium[browser_id]
    browser = tmp_memory[browser_id][transform(which_browser.value)]

    click_configure_columns_button(browser)
    wait_for_item_to_appear(Popups(selenium[browser_id]).configure_columns_menu.web_elem)

    current_xattr_column = get_column_from_configure_columns_menu(driver, name)

    current_xattr_column.hover_to_button_and_click("modify", driver)
    modify_xattr_column = Popups(driver).configure_columns_menu.xattr_column_editor

    if elem == "label":
        modify_xattr_column.column_label.clear()
        modify_xattr_column.column_label.send_keys(new_elem_name)
    elif elem == "key":
        enter_key = modify_xattr_column.enter_an_xattr_key
        modify_xattr_column.clear_actual_key()
        enter_key.send_keys(new_elem_name)

    modify_xattr_column.apply_changes.click()

    click_configure_columns_button(browser)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) modifies json column with"
        r' name "(?P<col_name>.*)" in (?P<which_browser>file'
        r" browser|archive browser|dataset browser) table"
        r" by changing it as follows:\n(?P<config>(.|\s)*)"
    ),
    converters={"which_browser": WhichBrowser},
)
def modify_json_column_in_columns_menu(
    selenium: SeleniumDrivers,
    browser_id: str,
    col_name: str,
    config: str,
    which_browser: WhichBrowser,
    tmp_memory: TmpMemory,
) -> None:
    """
    Config is a list of column updates applied sequentially.

    Each item in the list represents a single update and may define
    the following optional fields, which are applied in this order:

    1. mode        – New column mode
    2. key/query   – New column key or query
    3. label       – New column label

    Only the fields provided in an item are updated.

    Updates are always applied in the order listed above to ensure
    safe and predictable behavior.
    """

    driver = selenium[browser_id]
    browser = tmp_memory[browser_id][transform(which_browser.value)]

    click_configure_columns_button(browser)
    wait_for_item_to_appear(Popups(selenium[browser_id]).configure_columns_menu.web_elem)

    current_column = get_column_from_configure_columns_menu(driver, col_name)

    current_column.hover_to_button_and_click("modify", driver)
    modify_json_column = Popups(driver).configure_columns_menu.json_column_editor

    config_dict = dict(yaml.load(config, yaml.Loader).items())

    if "mode" in config_dict:
        getattr(modify_json_column.choose_mode, transform(config_dict["mode"].lower())).click()
    if "label" in config_dict:
        modify_json_column.column_label.clear()
        modify_json_column.column_label.send_keys(config_dict["label"])

    if "query" in config_dict:
        modify_json_column.query.clear()
        modify_json_column.query.send_keys(config_dict["query"])
    elif "key" in config_dict:
        modify_json_column.json_key.click()
        modify_json_column.clear_actual_key(driver)
        Popups(driver).dropdown.options[config_dict["key"]].click()

    modify_json_column.apply_changes.click()
    click_configure_columns_button(browser)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) copies content of json column"
        r' for item "(?P<item_name>.*)" and sees that it is equal to'
        r" '(?P<value>.*)' in (?P<which_browser>file"
        r" browser|archive browser|dataset browser)"
    ),
    converters={"which_browser": WhichBrowser},
)
def assert_json_column_content(
    selenium: SeleniumDrivers,
    browser_id: str,
    tmp_memory: TmpMemory,
    which_browser: WhichBrowser,
    item_name: str,
    value: str,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:

    driver = selenium[browser_id]
    browser = tmp_memory[browser_id][transform(which_browser.value)]
    item = browser.data[item_name]

    item.hover_to_btn_and_click("copy_json_icon", driver)
    copied = clipboard.paste(display=displays[browser_id])

    expected_value = sort_json_from_string(value)
    copied = json.loads(copied.replace("\n", ""))

    assert copied == expected_value, (
        f"Copied value: {copied} is not equal to expected value: {expected_value}"
    )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) (?P<res>sees|does not see) (?P<option>xattr|json)"
        r' column named "(?P<name>.*)" in '
        r"columns configuration popover in (?P<which_browser>file"
        r" browser|archive browser|dataset browser) table"
    ),
    converters={"which_browser": WhichBrowser},
)
def assert_column_presence(
    selenium: SeleniumDrivers,
    browser_id: str,
    res: str,
    name: str,
    which_browser: WhichBrowser,
    tmp_memory: TmpMemory,
    option: str,
) -> None:

    browser = tmp_memory[browser_id][transform(which_browser.value)]
    click_configure_columns_button(browser)
    column_names = get_column_names_from_configure_columns_menu(selenium[browser_id])
    if name in column_names:
        if res == "does not see":
            raise AssertionError(
                f"{option} column named '{name}' is present, but it was expected not to."
            )
    elif res == "sees":
        raise AssertionError(f"An xattr column with name: {name} is not present")

    click_configure_columns_button(browser)
