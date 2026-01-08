"""Meta steps for operations in browser tab in Oneprovider"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json

import yaml

from tests.gui.steps.modals.details_modal import assert_tab_in_modal
from tests.gui.steps.modals.modal import wt_wait_for_modal_to_appear
from tests.gui.steps.oneprovider.common import wait_for_item_to_appear
from tests.gui.steps.oneprovider.file_browser import (
    click_on_status_tag_for_file_in_file_browser,
)
from tests.gui.utils.generic import sort_json_from_string, transform
from tests.utils.bdd_utils import parsers, wt


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) creates new xattr column with "
        r'"(?P<key_name>.*)" key in (?P<which_browser>file browser|'
        r"archive browser|dataset browser) table"
    )
)
def wt_create_xattr_columns_in_columns_menu_in_browser(
    selenium, browser_id, which_browser, tmp_memory, popups, key_name
):
    create_xattr_columns_in_columns_menu_in_browser(
        selenium, browser_id, which_browser, tmp_memory, popups, key_name
    )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) creates new xattr column with"
        r' "(?P<key_name>.*)" key and "(?P<label_name>.*)" column label'
        r" in (?P<which_browser>file browser|archive browser|"
        r"dataset browser) table"
    )
)
def wt_create_xattr_columns_in_columns_menu_in_browser_with_label(
    selenium, browser_id, which_browser, tmp_memory, popups, key_name, label_name
):
    create_xattr_columns_in_columns_menu_in_browser(
        selenium,
        browser_id,
        which_browser,
        tmp_memory,
        popups,
        key_name,
        with_label=True,
        label_name=label_name,
    )


def create_xattr_columns_in_columns_menu_in_browser(
    selenium,
    browser_id,
    which_browser,
    tmp_memory,
    popups,
    name,
    with_label=False,
    label_name=None,
):
    driver = selenium[browser_id]
    browser = tmp_memory[browser_id][transform(which_browser)]

    browser.configure_columns.click()
    wait_for_item_to_appear(
        popups(selenium[browser_id]).configure_columns_menu.web_elem
    )

    new_column_button = popups(driver).configure_columns_menu.new_column_button
    wait_for_item_to_appear(new_column_button.web_elem)
    new_column_button.click()

    new_xattr_column = popups(driver).configure_columns_menu.xattr_column_editor
    new_xattr_column.enter_an_xattr_key.send_keys(name)

    if with_label:
        new_xattr_column.column_label.clear()
        new_xattr_column.column_label.send_keys(label_name)

    new_xattr_column.create.click()

    # hide columns menu popup
    browser.configure_columns.click()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) (?P<res>sees|does not see) (?P<option>xattr|json)"
        r' column named "(?P<name>.*)" in '
        r"columns configuration popover in (?P<which_browser>file"
        r" browser|archive browser|dataset browser) table"
    )
)
def assert_column_presence(
    selenium, browser_id, res, name, which_browser, tmp_memory, popups
):

    browser = tmp_memory[browser_id][transform(which_browser)]
    browser.configure_columns.click()
    wait_for_item_to_appear(
        popups(selenium[browser_id]).configure_columns_menu.web_elem
    )

    columns_menu = popups(selenium[browser_id]).configure_columns_menu.columns
    if name in [col.name for col in columns_menu]:
        if res == "does not see":
            raise AssertionError(
                f"An xattr column named '{name}' exists, but it was expected not to."
            )
    elif res == "sees":
        raise AssertionError(f"An xattr column with name: {name} does not exist")
    browser.configure_columns.click()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) creates new json column with "Whole'
        r' document" mode and "(?P<label_name>.*)" custom label'
        r" in (?P<which_browser>file browser|archive browser|"
        r"dataset browser) table"
    )
)
def wt_create_json_column_for_whole_document_with_label(
    selenium,
    browser_id,
    which_browser,
    tmp_memory,
    popups,
    label_name,
):
    create_json_column_in_columns_menu(
        selenium,
        browser_id,
        tmp_memory,
        which_browser,
        popups,
        label_name,
        "whole document",
        option=None,
    )


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) creates new json column with "Whole'
        r' document" mode in (?P<which_browser>file browser|'
        r"archive browser|dataset browser) table"
    )
)
def wt_create_json_column_for_whole_document(
    selenium,
    browser_id,
    which_browser,
    tmp_memory,
    popups,
):
    create_json_column_in_columns_menu(
        selenium,
        browser_id,
        tmp_memory,
        which_browser,
        popups,
        None,
        "whole document",
        option=None,
    )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) creates new json column with"
        r' "(?P<mode>Extract key|Query)" mode for "(?P<option>.*)" '
        r"(?P<input_type>key|query) and with"
        r' "(?P<label_name>.*)" custom label in (?P<which_browser>file'
        r" browser|archive browser|dataset browser) table"
    )
)
def wt_create_json_column_for_query_or_key_with_label(
    selenium,
    browser_id,
    tmp_memory,
    which_browser,
    popups,
    label_name: str,
    mode: str,
    option: str,
):
    create_json_column_in_columns_menu(
        selenium,
        browser_id,
        tmp_memory,
        which_browser,
        popups,
        label_name,
        mode.lower(),
        option=option,
    )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) creates new json column with"
        r' "(?P<mode>Query|Extract key)" mode'
        r' for "(?P<option>.*)" (?P<input_type>key|query) '
        r"in (?P<which_browser>file"
        r" browser|archive browser|dataset browser) table"
    )
)
def wt_create_json_column_for_query_or_key(
    selenium, browser_id, tmp_memory, which_browser, popups, mode: str, option: str
):
    create_json_column_in_columns_menu(
        selenium,
        browser_id,
        tmp_memory,
        which_browser,
        popups,
        None,
        mode.lower(),
        option=option,
    )


def create_json_column_in_columns_menu(
    selenium,
    browser_id,
    tmp_memory,
    which_browser,
    popups,
    label_name: str | None,
    mode: str,
    option,
):
    driver = selenium[browser_id]
    browser = tmp_memory[browser_id][transform(which_browser)]

    browser.configure_columns.click()
    wait_for_item_to_appear(
        popups(selenium[browser_id]).configure_columns_menu.web_elem
    )

    columns_menu = popups(driver).configure_columns_menu
    columns_menu.new_column_button.click()

    columns_menu.choose_json.click()
    new_json_col = columns_menu.json_column_editor
    mode = mode.lower()
    getattr(new_json_col.choose_mode, transform(mode)).click()

    if mode == "query":
        new_json_col.query.clear()
        new_json_col.query.send_keys(option)
    elif mode == "extract key":
        new_json_col.json_key.click()
        popups(driver).dropdown.options[option].click()

    if label_name:
        new_json_col.column_label.clear()
        new_json_col.column_label.send_keys(label_name)

    new_json_col.create()

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
    selenium,
    browser_id,
    tmp_memory,
    which_browser,
    item_name,
    value,
    clipboard,
    displays,
):

    driver = selenium[browser_id]
    browser = tmp_memory[browser_id][transform(which_browser)]
    item = browser.data[item_name]

    item.hover_to_btn_and_click("copy_json_icon", driver)
    copied = clipboard.paste(display=displays[browser_id])

    value = sort_json_from_string(value)
    copied = json.loads(copied.replace("\n", ""))

    assert (
        copied == value
    ), f"Copied value: {copied} is not equal to expected value: {value}"


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) modifies json column with"
        r' name "(?P<col_name>.*)" in (?P<which_browser>file'
        r" browser|archive browser|dataset browser) table"
        r" by changing it as follows:\n"
        r"(?P<config>(.|\s)*)"
    )
)
def modify_json_column_in_columns_menu(
    selenium,
    browser_id,
    col_name,
    config,
    which_browser,
    tmp_memory,
    popups,
):
    """
    Config is a list of changes applied sequentially.

    Each item in the list may contain the following optional fields:
    - mode:   New column mode
    - key/query:    New column key/query
    - label:  New column label

    Only provided fields are updated.
    """

    driver = selenium[browser_id]
    browser = tmp_memory[browser_id][transform(which_browser)]

    browser.configure_columns.click()
    wait_for_item_to_appear(
        popups(selenium[browser_id]).configure_columns_menu.web_elem
    )

    current_column = popups(driver).configure_columns_menu.columns[col_name]

    current_column.hover_to_button_and_click("modify", driver)
    modify_json_column = popups(driver).configure_columns_menu.json_column_editor

    config = yaml.load(config, yaml.Loader)

    for option, new_option_name in config.items():
        if option == "label":
            modify_json_column.column_label.clear()
            modify_json_column.column_label.send_keys(new_option_name)
        elif option == "key":
            enter_key = modify_json_column.json_key
            enter_key.click()
            modify_json_column.clear_actual_key(driver)
            popups(driver).dropdown.options[new_option_name].click()
        elif option == "query":
            modify_json_column.query.clear()
            modify_json_column.query.send_keys(new_option_name)
        elif option == "mode":
            getattr(
                modify_json_column.choose_mode, transform(new_option_name.lower())
            ).click()

    modify_json_column.apply_changes.click()
    # hide columns menu popup
    browser.configure_columns.click()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) opens "Metadata" tab in "(?P<modal_name>.*)" modal'
        r' via clicking on metadata status tag for "(?P<item_name>.*)"'
    )
)
def open_metadata_tab_using_tag(
    selenium, browser_id, tmp_memory, item_name, modal_name, modals
):
    tab_name = "Metadata"
    click_on_status_tag_for_file_in_file_browser(
        browser_id, tab_name.lower(), item_name, tmp_memory
    )

    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)

    assert_tab_in_modal(selenium, browser_id, tab_name, modals, modal_name)
