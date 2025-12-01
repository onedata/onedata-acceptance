"""Meta steps for operations in browser tab in Oneprovider"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.steps.modals.details_modal import assert_tab_in_modal
from tests.gui.steps.modals.modal import wt_wait_for_modal_to_appear
from tests.gui.steps.oneprovider.common import wait_for_item_to_appear
from tests.gui.steps.oneprovider.file_browser import (
    click_on_status_tag_for_file_in_file_browser,
)
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import parsers, wt


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) creates new xattr column with "(?P<key_name>.*)"'
        r" key in "
        r"(?P<which_browser>file browser|archive browser|"
        r"dataset browser) table"
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
        r'user of (?P<browser_id>.*) creates new xattr column with "(?P<key_name>.*)"'
        r" key and"
        r' "(?P<label_name>.*)" column label in (?P<which_browser>file'
        r" browser|archive browser|dataset browser) table"
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
    new_column_button = popups(driver).configure_columns_menu.new_xattr_column_button
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
        r"user of (?P<browser_id>.*) (?P<res>sees|does not see) xattr column named"
        r' "(?P<name>.*)"'
        r" in columns configuration popover in (?P<which_browser>file"
        r" browser|archive browser|dataset browser) table"
    )
)
def assert_xattr_column_presence(
    selenium, browser_id, res, name, which_browser, tmp_memory, popups
):

    browser = tmp_memory[browser_id][transform(which_browser)]
    browser.configure_columns.click()
    wait_for_item_to_appear(
        popups(selenium[browser_id]).configure_columns_menu.web_elem
    )

    columns_menu = popups(selenium[browser_id]).configure_columns_menu.columns
    for col in columns_menu:
        if col.name == name:
            if res == "sees":
                browser.configure_columns.click()
                return
            raise AssertionError(
                f"An xattr column named '{name}' exists, but it was expected not to."
            )

    if res == "sees":
        raise AssertionError(f"An xattr column with name: {name} does not exist")
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
