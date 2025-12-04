"""Meta steps for operations in browser tab in Oneprovider"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json

from tests.gui.steps.oneprovider.browser import sort_json_keys
from tests.gui.steps.oneprovider.common import wait_for_item_to_appear
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import parsers, wt


@wt(
    parsers.re(
        'user of (?P<browser_id>.*) creates new xattr column named "(?P<name>.*)" in '
        "(?P<which_browser>file browser|archive browser|"
        "dataset browser) table"
    )
)
def wt_create_xattr_columns_in_columns_menu_in_browser(
    selenium, browser_id, which_browser, tmp_memory, popups, name
):
    create_xattr_columns_in_columns_menu_in_browser(
        selenium, browser_id, which_browser, tmp_memory, popups, name
    )


@wt(
    parsers.re(
        'user of (?P<browser_id>.*) creates new xattr column named "(?P<name>.*)" with'
        ' custom label named "(?P<label_name>.*)" in (?P<which_browser>file'
        " browser|archive browser|dataset browser) table"
    )
)
def wt_create_xattr_columns_in_columns_menu_in_browser_with_label(
    selenium, browser_id, which_browser, tmp_memory, popups, name, label_name
):
    create_xattr_columns_in_columns_menu_in_browser(
        selenium,
        browser_id,
        which_browser,
        tmp_memory,
        popups,
        name,
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
    new_column_button = popups(driver).configure_columns_menu.new_column_button
    wait_for_item_to_appear(new_column_button.web_elem)
    new_column_button.click()

    new_xattr_column = popups(driver).configure_columns_menu.new_xattr_column
    new_xattr_column.enter_an_xattr_key.send_keys(name)

    if with_label:
        new_xattr_column.column_label.clear()
        new_xattr_column.column_label.send_keys(label_name)

    new_xattr_column.create.click()

    # hide columns menu popup
    browser.configure_columns.click()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) creates new json column with mode "(?P<mode>Whole'
        r' document|Extract key|Query)" and'
        r' custom label named "(?P<label_name>.*)" in (?P<which_browser>file'
        r" browser|archive browser|dataset browser) table"
    )
)
def wt_create_json_column_with_label_in_columns_menu(
    selenium, browser_id, which_browser, tmp_memory, popups, mode: str, label_name: str
):
    driver = selenium[browser_id]
    browser = tmp_memory[browser_id][transform(which_browser)]
    browser.configure_columns.click()
    columns_menu = popups(driver).configure_columns_menu

    new_column_button = columns_menu.new_column_button
    new_column_button.click()

    columns_menu.choose_json.click()

    new_json_col = columns_menu.new_json_column
    getattr(new_json_col.choose_mode, transform(mode.lower())).click()

    new_json_col.column_label.clear()
    new_json_col.column_label.send_keys(label_name)

    new_json_col.create()

    # hide columns menu popup
    browser.configure_columns.click()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) copies content of json column"
        r" for item \"(?P<item_name>.*)\" and sees that it is equal to '(?P<value>.*)'"
        r" in (?P<which_browser>file"
        r" browser|archive browser|dataset browser)"
    )
)
def assert_copied_josn_column_content(
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

    copied = copied.replace("\n", "").replace(" ", "")

    json_value = json.loads(value)
    value_sorted_reversed = sort_json_keys(json_value)
    value = json.dumps(value_sorted_reversed)
    value = value.replace(" ", "")

    assert (
        copied == value
    ), f"Copied value: {copied} not equal to expected value: {value}"
