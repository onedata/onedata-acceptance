"""Meta steps for operations in browser tab in Oneprovider"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import time
from typing import Literal

from tests.gui.constants import RESPONSIVE_LAYOUT_DELAY, ScreenSize
from tests.gui.steps.modals.details_modal import assert_tab_in_modal
from tests.gui.steps.modals.modal import wt_wait_for_modal_to_appear
from tests.gui.steps.oneprovider.browser import click_configure_columns_button
from tests.gui.steps.oneprovider.common import wait_for_item_to_appear
from tests.gui.steps.oneprovider.file_browser import (
    click_on_status_tag_for_file_in_file_browser,
)
from tests.gui.type_definitions import TmpMemory, WhichBrowser
from tests.gui.utils import Popups
from tests.gui.utils.generic import perform_action, transform
from tests.gui.utils.oneprovider.browser_row import BrowserRow
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) creates new xattr column with "
        r'"(?P<key_name>.*)" key in (?P<which_browser>file browser|'
        r"archive browser|dataset browser) table"
    ),
    converters={"which_browser": WhichBrowser},
)
def wt_create_xattr_columns_in_columns_menu_in_browser(
    selenium: SeleniumDrivers,
    browser_id: str,
    which_browser: WhichBrowser,
    tmp_memory: TmpMemory,
    key_name: str,
) -> None:
    create_xattr_columns_in_columns_menu_in_browser(
        selenium, browser_id, which_browser, tmp_memory, key_name
    )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) creates new xattr column with"
        r' "(?P<key_name>.*)" key and "(?P<label_name>.*)" column label'
        r" in (?P<which_browser>file browser|archive browser|"
        r"dataset browser) table"
    ),
    converters={"which_browser": WhichBrowser},
)
def wt_create_xattr_columns_in_columns_menu_in_browser_with_label(
    selenium: SeleniumDrivers,
    browser_id: str,
    which_browser: WhichBrowser,
    tmp_memory: TmpMemory,
    key_name: str,
    label_name: str,
) -> None:
    create_xattr_columns_in_columns_menu_in_browser(
        selenium,
        browser_id,
        which_browser,
        tmp_memory,
        key_name,
        with_label=True,
        label_name=label_name,
    )


def create_xattr_columns_in_columns_menu_in_browser(
    selenium: SeleniumDrivers,
    browser_id: str,
    which_browser: WhichBrowser,
    tmp_memory: TmpMemory,
    name: str,
    with_label: bool = False,
    label_name: str | None = None,
) -> None:
    driver = selenium[browser_id]
    browser = tmp_memory[browser_id][transform(which_browser.value)]

    click_configure_columns_button(browser)
    wait_for_item_to_appear(Popups(selenium[browser_id]).configure_columns_menu.web_elem)

    new_column_button = Popups(driver).configure_columns_menu.new_column_button
    wait_for_item_to_appear(new_column_button.web_elem)
    new_column_button.click()

    new_xattr_column = Popups(driver).configure_columns_menu.xattr_column_editor
    new_xattr_column.enter_an_xattr_key.send_keys(name)

    if with_label:
        new_xattr_column.column_label.clear()
        new_xattr_column.column_label.send_keys(label_name)

    new_xattr_column.create.click()

    # hide columns menu popup
    click_configure_columns_button(browser)


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) creates new json column with "Whole'
        r' document" mode and "(?P<label_name>.*)" custom label'
        r" in (?P<which_browser>file browser|archive browser|"
        r"dataset browser) table"
    ),
    converters={"which_browser": WhichBrowser},
)
def wt_create_json_column_for_whole_document_with_label(
    selenium: SeleniumDrivers,
    browser_id: str,
    which_browser: WhichBrowser,
    tmp_memory: TmpMemory,
    label_name: str,
) -> None:
    create_json_column_in_columns_menu(
        selenium,
        browser_id,
        tmp_memory,
        which_browser,
        label_name,
        "whole document",
        None,
    )


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) creates new json column with "Whole'
        r' document" mode in (?P<which_browser>file browser|'
        r"archive browser|dataset browser) table"
    ),
    converters={"which_browser": WhichBrowser},
)
def wt_create_json_column_for_whole_document(
    selenium: SeleniumDrivers,
    browser_id: str,
    which_browser: WhichBrowser,
    tmp_memory: TmpMemory,
) -> None:
    create_json_column_in_columns_menu(
        selenium,
        browser_id,
        tmp_memory,
        which_browser,
        None,
        "whole document",
        None,
    )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) creates new json column with"
        r' "(?P<mode>Extract key|Query)" mode for "(?P<option>.*)" '
        r"(?P<input_type>key|query) and with"
        r' "(?P<label_name>.*)" custom label in (?P<which_browser>file'
        r" browser|archive browser|dataset browser) table"
    ),
    converters={"which_browser": WhichBrowser},
)
def wt_create_json_column_for_query_or_key_with_label(
    selenium: SeleniumDrivers,
    browser_id: str,
    tmp_memory: TmpMemory,
    which_browser: WhichBrowser,
    label_name: str,
    mode: str,
    option: str,
) -> None:
    create_json_column_in_columns_menu(
        selenium,
        browser_id,
        tmp_memory,
        which_browser,
        label_name,
        mode.lower(),
        option,
    )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) creates new json column with"
        r' "(?P<mode>Query|Extract key)" mode'
        r' for "(?P<option>.*)" (?P<input_type>key|query) '
        r"in (?P<which_browser>file"
        r" browser|archive browser|dataset browser) table"
    ),
    converters={"which_browser": WhichBrowser},
)
def wt_create_json_column_for_query_or_key(
    selenium: SeleniumDrivers,
    browser_id: str,
    tmp_memory: TmpMemory,
    which_browser: WhichBrowser,
    mode: str,
    option: str,
) -> None:
    create_json_column_in_columns_menu(
        selenium,
        browser_id,
        tmp_memory,
        which_browser,
        None,
        mode.lower(),
        option=option,
    )


def create_json_column_in_columns_menu(
    selenium: SeleniumDrivers,
    browser_id: str,
    tmp_memory: TmpMemory,
    which_browser: WhichBrowser,
    label_name: str | None,
    mode: str,
    option: str | None,
) -> None:
    driver = selenium[browser_id]
    browser = tmp_memory[browser_id][transform(which_browser.value)]

    click_configure_columns_button(browser)
    wait_for_item_to_appear(Popups(selenium[browser_id]).configure_columns_menu.web_elem)

    columns_menu = Popups(driver).configure_columns_menu
    columns_menu.new_column_button.click()

    columns_menu.choose_json.click()
    new_json_col = columns_menu.json_column_editor
    mode = mode.lower()
    getattr(new_json_col.choose_mode, transform(mode)).click()

    if mode == "query":
        assert option is not None
        new_json_col.query.clear()
        new_json_col.query.send_keys(option)
    elif mode == "extract key":
        assert option is not None
        new_json_col.json_key.click()
        Popups(driver).dropdown.options[option].click()

    if label_name:
        new_json_col.column_label.clear()
        new_json_col.column_label.send_keys(label_name)

    new_json_col.create.click()

    # hide columns menu popup
    click_configure_columns_button(browser)


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) opens "Metadata" tab in "(?P<modal_name>.*)" modal'
        r' via clicking on metadata status tag for "(?P<item_name>.*)"'
    )
)
def open_metadata_tab_using_tag(
    selenium: SeleniumDrivers,
    browser_id: str,
    tmp_memory: TmpMemory,
    item_name: str,
    modal_name: str,
) -> None:
    tab_name = "Metadata"
    click_on_status_tag_for_file_in_file_browser(
        browser_id, tab_name.lower(), item_name, tmp_memory
    )

    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)

    assert_tab_in_modal(selenium, browser_id, tab_name, modal_name)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) scrolls (?P<direction>up|down) (?P<num>\d+)"
        r" screens in (?P<which_browser>(?:file|archive|dataset) browser)"
    ),
    converters={"which_browser": WhichBrowser},
)
def scroll_few_screens_in_file_browser(
    browser_id: str,
    tmp_memory: TmpMemory,
    num: int,
    direction: Literal["up", "down"],
    which_browser: WhichBrowser,
) -> None:
    browser = tmp_memory[browser_id][transform(which_browser.value)]
    browser.scroll_few_screens(direction, num)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) remembers visible files list"
        r" in (?P<which_browser>(?:file|archive|dataset) browser)"
    ),
    converters={"which_browser": WhichBrowser},
)
def remember_visible_files_list(
    browser_id: str, tmp_memory: TmpMemory, which_browser: WhichBrowser
) -> None:
    browser = tmp_memory[browser_id][transform(which_browser.value)]
    visible_file_names: list[str] = browser.get_field_value_from_visible_rows()
    tmp_memory[browser_id]["visible_files"] = visible_file_names


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that visible files list is the same as remembered"
        r" in (?P<which_browser>(?:file|archive|dataset) browser)"
    ),
    converters={"which_browser": WhichBrowser},
)
def assert_currently_visible_files_list_matches_remembered_list(
    browser_id: str, tmp_memory: TmpMemory, which_browser: WhichBrowser
) -> None:
    browser = tmp_memory[browser_id][transform(which_browser.value)]
    visible_file_names: list[str] = browser.get_field_value_from_visible_rows()
    remembered_file_names = tmp_memory[browser_id]["visible_files"]
    assert visible_file_names == remembered_file_names, (
        "Current list differs from remembered\n"
        f"Current: {visible_file_names}\n"
        f"Remembered: {remembered_file_names}"
    )


@wt(
    parsers.re(
        r"^for each supported screen size, user of (?P<browser_id>.+?) performs "
        r"(?P<trials>\d+) trials of scrolling "
        r"(?P<direction>up|down) (?P<num>\d+) screens from the "
        r"(?P<starting_edge>top|bottom) of "
        r'(?P<which_browser>(?:file|archive|dataset) browser) \(with "'
        r'(?P<expected_last_file>.+?)" as the expected last file\) '
        r"and sees the same files in every trial$"
    ),
    converters={"which_browser": WhichBrowser},
)
def scroll_few_screens_in_browser(
    selenium: SeleniumDrivers,
    browser_id: str,
    which_browser: WhichBrowser,
    num: int,
    expected_last_file: str,
    direction: Literal["up", "down"],
    starting_edge: Literal["top", "bottom"],
    tmp_memory: TmpMemory,
    trials: int,
) -> None:
    driver = selenium[browser_id]
    browser = tmp_memory[browser_id][transform(which_browser.value)]

    def wait_until_files_list_not_stale() -> list[BrowserRow]:
        files = browser.files_list
        _ = files[0].name
        return files

    for screen_size in ScreenSize:
        size = screen_size.value
        driver.set_window_size(size.width, size.height)
        time.sleep(RESPONSIVE_LAYOUT_DELAY)

        unique_file_name_lists: set[tuple[str, ...]] = set()

        for _ in range(trials):
            if starting_edge == "bottom":
                browser.scroll_to_last_file_on_files_list(expected_last_file=expected_last_file)
            else:
                browser.scroll_to_top()
            perform_action(wait_until_files_list_not_stale)

            browser.scroll_few_screens(direction, num)

            current_file_names = browser.get_field_value_from_visible_rows()

            unique_file_name_lists.add(tuple(current_file_names))

        assert len(unique_file_name_lists) == 1, (
            f"Unique seen file names lists for screen size ({size.width}, {size.height}):\n"
            + "\n".join(map(str, unique_file_name_lists))
        )
