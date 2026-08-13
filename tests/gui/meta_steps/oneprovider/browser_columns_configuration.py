"""Meta steps for browser columns configuration"""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2025 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json

import yaml

from tests.gui.steps.oneprovider.common import wait_for_item_to_appear
from tests.gui.type_definitions import Clipboard, TmpMemory
from tests.gui.utils import Popups
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    parse_elements_sequence,
    sort_json_from_string,
    transform,
)
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt


@wt(
    parsers.re(
        rf"user of (?P<browser_id>.*) enables only "
        rf"(?P<columns>{ELEMENTS_SEQUENCE_PATTERN}) "
        r"columns? in columns configuration popover in "
        r"(?P<which_browser>file browser|archive browser|"
        r"dataset browser) table"
    ),
    converters={
        "columns": parse_elements_sequence,
    },
)
def select_columns_to_be_visible_in_browser(
    selenium: SeleniumDrivers,
    browser_id: str,
    columns: list[str],
    which_browser: str,
    tmp_memory: TmpMemory,
) -> None:
    # This function enables the selected columns and disables the rest.
    option_select = "select"
    option_unselect = "unselect"
    browser = tmp_memory[browser_id][transform(which_browser)]
    browser.configure_columns.click()
    columns_menu = Popups(selenium[browser_id]).configure_columns_menu.columns
    wait_for_item_to_appear(
        Popups(selenium[browser_id]).configure_columns_menu.web_elem
    )
    parsed_columns = [column.lower() for column in columns]
    for column in columns_menu:
        if column.name.lower() in parsed_columns:
            getattr(columns_menu[column.name], option_select)()
        else:
            getattr(columns_menu[column.name], option_unselect)()
    # hide columns menu popup
    browser.configure_columns.click()


@wt(
    parsers.re(
        rf"user of (?P<browser_id>.*) (?P<res>disables|enables) "
        rf"(?P<columns>{ELEMENTS_SEQUENCE_PATTERN}) "
        r"columns? in columns configuration popover in "
        r"(?P<which_browser>file browser|archive browser|"
        r"dataset browser) table"
    ),
    converters={
        "columns": parse_elements_sequence,
    },
)
def change_visibility_for_browser_columns(
    selenium: SeleniumDrivers,
    browser_id: str,
    res: str,
    columns: list[str],
    which_browser: str,
    tmp_memory: TmpMemory,
) -> None:
    # This function updates only the specified columns (enable/disable).
    # All other columns remain unchanged.

    option_select = "select"
    option_unselect = "unselect"
    browser = tmp_memory[browser_id][transform(which_browser)]
    browser.configure_columns.click()

    columns_menu = Popups(selenium[browser_id]).configure_columns_menu.columns
    wait_for_item_to_appear(
        Popups(selenium[browser_id]).configure_columns_menu.web_elem
    )

    parsed_columns = [column.lower() for column in columns]
    for column in columns_menu:
        if column.name.lower() in parsed_columns:
            if res == "enables":
                getattr(columns_menu[column.name], option_select)()
            else:
                getattr(columns_menu[column.name], option_unselect)()

    # hide columns menu popup
    browser.configure_columns.click()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) removes (?P<option>json|xattr) column "
        r'named "(?P<name>.*)" in columns configuration popover in (?P<which_browser>'
        r"file browser|archive browser|dataset browser) table"
    )
)
def remove_column(
    selenium: SeleniumDrivers,
    browser_id: str,
    name: str,
    which_browser: str,
    tmp_memory: TmpMemory,
) -> None:
    driver = selenium[browser_id]
    browser = tmp_memory[browser_id][transform(which_browser)]
    browser.configure_columns.click()

    wait_for_item_to_appear(
        Popups(selenium[browser_id]).configure_columns_menu.web_elem
    )

    current_column = Popups(driver).configure_columns_menu.columns[name]
    current_column.hover_to_button_and_click("remove", driver)

    # hide columns menu popup
    browser.configure_columns.click()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) modifies xattr column with"
        r' "(?P<name>.*)" key by changing (?P<elem>label|key)'
        r' to "(?P<new_elem_name>.*)" in (?P<which_browser>file'
        r" browser|archive browser|dataset browser) table"
    )
)
def modify_props_of_xattr_column_in_columns_menu(
    selenium: SeleniumDrivers,
    browser_id: str,
    which_browser: str,
    tmp_memory: TmpMemory,
    name: str,
    elem: str,
    new_elem_name: str,
) -> None:

    driver = selenium[browser_id]
    browser = tmp_memory[browser_id][transform(which_browser)]

    browser.configure_columns.click()
    wait_for_item_to_appear(
        Popups(selenium[browser_id]).configure_columns_menu.web_elem
    )

    current_xattr_column = Popups(driver).configure_columns_menu.columns[name]

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

    # hide columns menu popup
    browser.configure_columns.click()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) modifies json column with"
        r' name "(?P<col_name>.*)" in (?P<which_browser>file'
        r" browser|archive browser|dataset browser) table"
        r" by changing it as follows:\n(?P<config>(.|\s)*)"
    )
)
def modify_json_column_in_columns_menu(
    selenium: SeleniumDrivers,
    browser_id: str,
    col_name: str,
    config: str,
    which_browser: str,
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
    browser = tmp_memory[browser_id][transform(which_browser)]

    browser.configure_columns.click()
    wait_for_item_to_appear(
        Popups(selenium[browser_id]).configure_columns_menu.web_elem
    )

    current_column = Popups(driver).configure_columns_menu.columns[col_name]

    current_column.hover_to_button_and_click("modify", driver)
    modify_json_column = Popups(driver).configure_columns_menu.json_column_editor

    config_dict = dict(yaml.load(config, yaml.Loader).items())

    if "mode" in config_dict:
        getattr(
            modify_json_column.choose_mode, transform(config_dict["mode"].lower())
        ).click()
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
    # hide columns menu popup
    browser.configure_columns.click()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) copies content of json column"
        r' for item "(?P<item_name>.*)" and sees that it is equal to'
        r" '(?P<value>.*)' in (?P<which_browser>file"
        r" browser|archive browser|dataset browser)"
    )
)
def assert_json_column_content(
    selenium: SeleniumDrivers,
    browser_id: str,
    tmp_memory: TmpMemory,
    which_browser: str,
    item_name: str,
    value: str,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:

    driver = selenium[browser_id]
    browser = tmp_memory[browser_id][transform(which_browser)]
    item = browser.data[item_name]

    item.hover_to_btn_and_click("copy_json_icon", driver)
    copied = clipboard.paste(display=displays[browser_id])

    expected_value = sort_json_from_string(value)
    copied = json.loads(copied.replace("\n", ""))

    assert (
        copied == expected_value
    ), f"Copied value: {copied} is not equal to expected value: {expected_value}"


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) (?P<res>sees|does not see) (?P<option>xattr|json)"
        r' column named "(?P<name>.*)" in '
        r"columns configuration popover in (?P<which_browser>file"
        r" browser|archive browser|dataset browser) table"
    )
)
def assert_column_presence(
    selenium: SeleniumDrivers,
    browser_id: str,
    res: str,
    name: str,
    which_browser: str,
    tmp_memory: TmpMemory,
    option: str,
) -> None:

    browser = tmp_memory[browser_id][transform(which_browser)]
    browser.configure_columns.click()
    wait_for_item_to_appear(
        Popups(selenium[browser_id]).configure_columns_menu.web_elem
    )

    columns_menu = Popups(selenium[browser_id]).configure_columns_menu.columns
    if name in [col.name for col in columns_menu]:
        if res == "does not see":
            raise AssertionError(
                f"{option} column named '{name}' exists, but it was expected not to."
            )
    elif res == "sees":
        raise AssertionError(f"An xattr column with name: {name} does not exist")
    browser.configure_columns.click()
