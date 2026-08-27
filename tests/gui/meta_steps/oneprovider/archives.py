"""This module contains meta steps for operations on archives in Onezone
using web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import re
import time

import yaml
from selenium.common.exceptions import NoSuchElementException

from tests.gui.meta_steps.oneprovider.data import (
    go_to_and_assert_browser,
    go_to_path_without_last_elem,
)
from tests.gui.meta_steps.oneprovider.dataset import get_item_name_from_path
from tests.gui.steps.common.common import assert_n_items_in_items_list
from tests.gui.steps.modals.modal import (
    click_modal_button,
    write_name_into_text_field_in_modal,
)
from tests.gui.steps.oneprovider.archives import (
    assert_archive_info_in_properties_modal,
    assert_not_archive_with_description,
    assert_number_of_archives_for_item_in_dataset_browser,
    assert_tag_for_archive_in_archive_browser,
    check_toggle_in_create_archive_modal,
    click_and_press_enter_on_archive,
    click_menu_for_archive,
    get_archive_with_description,
    write_description_in_create_archive_modal,
    write_in_confirmation_input,
)
from tests.gui.steps.oneprovider.archives_audit import (
    assert_archive_names_match,
    extract_archive_name_and_path,
    get_loaded_archive_file_path,
)
from tests.gui.steps.oneprovider.archives_recall import (
    assert_recall_duration_in_archive_recall_information_modal,
    get_archive_recall_information_property_without_whitespace,
)
from tests.gui.steps.oneprovider.browser import (
    assert_items_presence_in_browser,
    assert_option_state_in_data_row_menu,
    click_menu_for_elem_in_browser,
    click_option_in_data_row_menu_in_browser,
)
from tests.gui.steps.oneprovider.data_tab import (
    assert_browser_in_tab_in_op,
    check_content_for_provider,
    check_size_statistic_in_dir_details,
    check_size_stats_for_provider,
)
from tests.gui.steps.oneprovider.dataset import click_on_dataset
from tests.gui.steps.oneprovider.file_browser import (
    click_on_status_tag_for_file_in_file_browser,
)
from tests.gui.steps.onezone.spaces import click_on_option_of_space_on_left_sidebar_menu
from tests.gui.type_definitions import Clipboard, TmpMemory
from tests.gui.utils import Modals, OPLoggedIn
from tests.gui.utils.common.constants import ScreenSize
from tests.gui.utils.generic import ListElement, WhichBrowser, transform
from tests.gui.utils.shortened_path import (
    IndexedPathSequence,
    parse_indexed_path_sequence,
)
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt

OPTION_IN_SPACE = "Datasets, Archives"
DATASET_BROWSER = "dataset browser"
ARCHIVE_BROWSER = "archive browser"
ARCHIVE_FILE_BROWSER = "archive file browser"


@wt(
    parsers.parse(
        "user of {browser_id} {option} to create archive for item "
        '"{item_name}" in "{space_name}" with following '
        "configuration:\n{config}"
    )
)
def create_archive(
    browser_id: str,
    selenium: SeleniumDrivers,
    config: str,
    item_name: str,
    space_name: str,
    tmp_memory: TmpMemory,
    clipboard: Clipboard,
    displays: dict[str, str],
    option: str,
) -> None:
    """Create archive according to given config.

    Config format given in yaml is as follows:

            description: archive_description        ---> optional
            layout: plain/BagIt
            create nested archives: True/False      ---> optional,
            incremental:                            ---> optional
                enabled: True/False
            include DIP: True/False                 ---> optional


    Example configuration:

          layout: plain
          incremental:
            enabled: True
    """
    _create_archive(
        browser_id,
        selenium,
        config,
        item_name,
        space_name,
        tmp_memory,
        clipboard,
        displays,
        option,
    )


@wt(
    parsers.parse(
        "user of {browser_id} {option} to create archive for item "
        '"{item_name}" in "{space_name}" with following '
        "configuration and follow symbolic links set as"
        " {follow_symbolic_links}:\n{config}"
    )
)
def create_archive_with_follow_symbolic_link(
    browser_id: str,
    selenium: SeleniumDrivers,
    config: str,
    item_name: str,
    space_name: str,
    tmp_memory: TmpMemory,
    clipboard: Clipboard,
    displays: dict[str, str],
    option: str,
    follow_symbolic_links: str,
) -> None:
    should_follow_symbolic_links = follow_symbolic_links == "true"

    _create_archive(
        browser_id,
        selenium,
        config,
        item_name,
        space_name,
        tmp_memory,
        clipboard,
        displays,
        option,
        should_follow_symbolic_links,
    )


def _create_archive(
    browser_id: str,
    selenium: SeleniumDrivers,
    config: str,
    item_name: str,
    space_name: str,
    tmp_memory: TmpMemory,
    clipboard: Clipboard,
    displays: dict[str, str],
    option: str,
    follow_symbolic_links: bool = True,
) -> None:
    option_in_data_row_menu = "Create archive"
    button_name = "Create"
    option_state = "disabled"
    try:
        OPLoggedIn(selenium[browser_id]).dataset_browser.breadcrumbs
    except NoSuchElementException:
        click_on_option_of_space_on_left_sidebar_menu(
            selenium, browser_id, space_name, OPTION_IN_SPACE
        )
        assert_browser_in_tab_in_op(selenium, browser_id, tmp_memory, DATASET_BROWSER)

    if "/" in item_name:
        go_to_path_without_last_elem(
            selenium,
            browser_id,
            tmp_memory,
            item_name,
            DATASET_BROWSER,
        )
        item_name = item_name.split("/")[-1]
    click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory, DATASET_BROWSER)
    if option in ("succeeds", "tries"):
        click_option_in_data_row_menu_in_browser(
            selenium,
            browser_id,
            option_in_data_row_menu,
            DATASET_BROWSER,
        )
        data = yaml.load(config, yaml.Loader)

        description = data.get("description", False)
        layout = data["layout"]
        create_nested_archives = data.get("create nested archives", False)
        incremental = data.get("incremental", False)
        include_dip = data.get("include DIP", False)
        if follow_symbolic_links:
            follow_symbolic_links = data.get("follow symbolic links", True)

        if description:
            write_description_in_create_archive_modal(selenium, browser_id, description)
        if layout == "BagIt":
            click_modal_button(selenium, browser_id, layout, option_in_data_row_menu)
        if create_nested_archives:
            option = "create_nested_archives"
            check_toggle_in_create_archive_modal(browser_id, selenium, option)
        if incremental:
            if incremental["enabled"]:
                option = "incremental"
                check_toggle_in_create_archive_modal(browser_id, selenium, option)
        if include_dip:
            option = "include_dip"
            check_toggle_in_create_archive_modal(browser_id, selenium, option)
        if not follow_symbolic_links:
            option = "follow_symbolic_links"
            check_toggle_in_create_archive_modal(browser_id, selenium, option)
        click_modal_button(selenium, browser_id, button_name, option_in_data_row_menu)
        client = "web GUI"
        if description:
            copy_archive_id_to_tmp_memory(
                selenium,
                browser_id,
                client,
                tmp_memory,
                clipboard,
                displays,
                description,
            )
            # wait for "archive id copied to clipboard" message to disappear
            time.sleep(5)
    elif option == "fails":
        assert_option_state_in_data_row_menu(
            selenium,
            browser_id,
            option_in_data_row_menu,
            option_state,
            DATASET_BROWSER,
        )


def copy_archive_id_to_tmp_memory(
    selenium: SeleniumDrivers,
    browser_id: str,
    client: str,
    tmp_memory: TmpMemory,
    clipboard: Clipboard,
    displays: dict[str, str],
    description: str,
) -> None:
    if client.lower() == "web gui":
        option_in_menu = "Copy archive ID"
        assert_browser_in_tab_in_op(selenium, browser_id, tmp_memory, ARCHIVE_BROWSER)
        click_menu_for_archive(browser_id, tmp_memory, description, selenium)
        click_option_in_data_row_menu_in_browser(
            selenium, browser_id, option_in_menu, ARCHIVE_BROWSER
        )
        tmp_memory[description] = clipboard.paste(display=displays[browser_id])


def assert_archive_in_op_gui(
    browser_id: str,
    selenium: SeleniumDrivers,
    item_name: str,
    space_name: str,
    tmp_memory: TmpMemory,
    option: str,
    description: str,
) -> None:
    go_to_and_assert_browser(
        selenium,
        browser_id,
        space_name,
        OPTION_IN_SPACE,
        tmp_memory,
        item_browser=DATASET_BROWSER,
    )
    if "/" in item_name:
        item_name = get_item_name_from_path(
            selenium,
            browser_id,
            space_name,
            tmp_memory,
            item_name,
            OPTION_IN_SPACE,
            DATASET_BROWSER,
        )

    if option == "sees":
        click_on_dataset(browser_id, tmp_memory, item_name)
        assert_browser_in_tab_in_op(
            selenium,
            browser_id,
            tmp_memory,
            item_browser=ARCHIVE_BROWSER,
        )
        click_and_press_enter_on_archive(
            browser_id, tmp_memory, description, ARCHIVE_BROWSER
        )
        assert_browser_in_tab_in_op(
            selenium,
            browser_id,
            tmp_memory,
            item_browser=ARCHIVE_FILE_BROWSER,
        )
        assert_items_presence_in_browser(
            selenium,
            browser_id,
            [item_name],
            tmp_memory,
            which_browser=ARCHIVE_FILE_BROWSER,
        )
    else:
        try:
            number = 0
            assert_number_of_archives_for_item_in_dataset_browser(
                browser_id, item_name, str(number), tmp_memory
            )
        except AssertionError:
            click_on_dataset(browser_id, tmp_memory, item_name)
            assert_browser_in_tab_in_op(
                selenium,
                browser_id,
                tmp_memory,
                item_browser=ARCHIVE_BROWSER,
            )
            assert_not_archive_with_description(tmp_memory, browser_id, description)


def remove_archive_in_op_gui(
    browser_id: str,
    selenium: SeleniumDrivers,
    item_name: str,
    space_name: str,
    tmp_memory: TmpMemory,
    description: str,
    option: str,
) -> None:
    option_in_menu = "Delete archive"
    text = "I understand that data of the archive will be lost"
    button_name = "Delete archive"
    option_state = "disabled"
    go_to_and_assert_browser(
        selenium,
        browser_id,
        space_name,
        OPTION_IN_SPACE,
        tmp_memory,
        item_browser=DATASET_BROWSER,
    )
    click_on_dataset(browser_id, tmp_memory, item_name)
    assert_browser_in_tab_in_op(
        selenium,
        browser_id,
        tmp_memory,
        item_browser=ARCHIVE_BROWSER,
    )
    click_menu_for_archive(browser_id, tmp_memory, description, selenium)

    if option == "succeeds":
        click_option_in_data_row_menu_in_browser(
            selenium,
            browser_id,
            option_in_menu,
            which_browser=ARCHIVE_BROWSER,
        )
        write_in_confirmation_input(browser_id, text, selenium)
        click_modal_button(selenium, browser_id, button_name, option_in_menu)
    elif option == "fails":
        assert_option_state_in_data_row_menu(
            selenium,
            browser_id,
            button_name,
            option_state,
            ARCHIVE_BROWSER,
        )


def assert_archive_with_option_in_op_gui(
    browser_id: str,
    selenium: SeleniumDrivers,
    space_name: str,
    tmp_memory: TmpMemory,
    item_name: str,
    option: str,
    description: str,
) -> None:
    tag_type = transform(option)
    go_to_and_assert_browser(
        selenium,
        browser_id,
        space_name,
        OPTION_IN_SPACE,
        tmp_memory,
        item_browser=DATASET_BROWSER,
    )
    click_on_dataset(browser_id, tmp_memory, item_name)
    assert_browser_in_tab_in_op(
        selenium,
        browser_id,
        tmp_memory,
        item_browser=ARCHIVE_BROWSER,
    )
    assert_tag_for_archive_in_archive_browser(
        browser_id, tag_type, tmp_memory, description
    )


def assert_number_of_archive_in_op_gui(
    browser_id: str,
    selenium: SeleniumDrivers,
    item_name: str,
    space_name: str,
    tmp_memory: TmpMemory,
    number: int,
) -> None:
    go_to_and_assert_browser(
        selenium,
        browser_id,
        space_name,
        OPTION_IN_SPACE,
        tmp_memory,
        item_browser=DATASET_BROWSER,
    )
    if "/" in item_name:
        item_name = get_item_name_from_path(
            selenium,
            browser_id,
            space_name,
            tmp_memory,
            item_name,
            OPTION_IN_SPACE,
            DATASET_BROWSER,
        )
    assert_number_of_archives_for_item_in_dataset_browser(
        browser_id, item_name, str(number), tmp_memory
    )


@wt(
    parsers.parse(
        "user of {browser_id} can see {number} of archives in"
        " {which_browser:WhichBrowser}",
        extra_types={"WhichBrowser": WhichBrowser},
    )
)
def assert_number_of_archives_with_scrolling(
    browser_id: str,
    selenium: SeleniumDrivers,
    number: str,
    tmp_memory: TmpMemory,
    which_browser: WhichBrowser,
) -> None:
    browser = tmp_memory[browser_id][transform(which_browser.value)]
    assert_n_items_in_items_list(
        browser, selenium, browser_id, int(number), ListElement.FILES, "description"
    )


def assert_base_archive_for_archive_in_op_gui(
    browser_id: str,
    selenium: SeleniumDrivers,
    item_name: str,
    space_name: str,
    tmp_memory: TmpMemory,
    description: str,
    base_description: str,
) -> None:
    go_to_and_assert_browser(
        selenium,
        browser_id,
        space_name,
        OPTION_IN_SPACE,
        tmp_memory,
        item_browser=DATASET_BROWSER,
    )
    click_on_dataset(browser_id, tmp_memory, item_name)
    assert_browser_in_tab_in_op(
        selenium,
        browser_id,
        tmp_memory,
        item_browser=ARCHIVE_BROWSER,
    )
    browser = tmp_memory[browser_id]["archive_browser"]
    archive = get_archive_with_description(browser, description)
    error_message = (
        f"Base archive: {archive.base_archive} does not match expected "
        f"archive with description {base_description}"
    )
    assert base_description in archive.base_archive_description, error_message


def assert_archive_callback_in_op_gui(
    browser_id: str,
    tmp_memory: TmpMemory,
    description: str,
    selenium: SeleniumDrivers,
    expected: str,
    option: str,
) -> None:
    modal = "Archive Details"
    option_in_menu = "Properties"
    info = f"{option} callback URL"
    button_name = "X"
    click_menu_for_archive(browser_id, tmp_memory, description, selenium)
    click_option_in_data_row_menu_in_browser(
        selenium, browser_id, option_in_menu, ARCHIVE_BROWSER
    )
    assert_archive_info_in_properties_modal(selenium, browser_id, expected, info)
    click_modal_button(selenium, browser_id, button_name, modal)


def recall_archive_for_archive_in_op_gui(
    browser_id: str,
    description: str,
    tmp_memory: TmpMemory,
    selenium: SeleniumDrivers,
    name: str,
) -> None:
    option_in_menu = "Recall to..."
    modal_name = "Recall archive"
    name_textfield = "target name input"
    button_name = "Recall"
    click_menu_for_archive(browser_id, tmp_memory, description, selenium)
    click_option_in_data_row_menu_in_browser(
        selenium, browser_id, option_in_menu, ARCHIVE_BROWSER
    )
    write_name_into_text_field_in_modal(
        selenium, browser_id, name, modal_name, name_textfield
    )
    click_modal_button(selenium, browser_id, button_name, modal_name)


def recalled_archive_details_in_op_gui(
    browser_id: str,
    item_name: str,
    tmp_memory: TmpMemory,
    data: dict[str, str],
    selenium: SeleniumDrivers,
) -> None:
    status_type = "recalled"
    click_on_status_tag_for_file_in_file_browser(
        browser_id, status_type, item_name, tmp_memory
    )

    for key, expected_value in data.items():
        if key == "time":
            expected_times = expected_value.split(" >= ")
            start = expected_times[-1]
            stop = expected_times[0]
            if "cancelled" in expected_times:
                cancelled = expected_times[1]
                assert_recall_duration_in_archive_recall_information_modal(
                    selenium, browser_id, start, cancelled
                )
                assert_recall_duration_in_archive_recall_information_modal(
                    selenium, browser_id, cancelled, stop
                )
            assert_recall_duration_in_archive_recall_information_modal(
                selenium, browser_id, start, stop
            )
        else:
            value = get_archive_recall_information_property_without_whitespace(
                selenium, browser_id, key
            )
            expected_value = re.sub(r"\s*", "", expected_value)
            error_message = (
                f'{key} for archive recall "{item_name}" is {value} '
                f"but expected value is {expected_value} "
            )
            if expected_value == "Cancelled":
                assert expected_value in value, error_message
            elif "<=" in expected_value:
                characters = "[\nMBGi ]"
                error_message = (
                    f'{key} for archive recall "{item_name}" is {value} '
                    "and is not lower or equal to expected value: "
                    f"{expected_value} "
                )
                value = re.sub(characters, "", value).split("/")[0]
                expected_value = re.sub(characters, "", expected_value).split("<=")[-1]
                assert int(value) <= int(expected_value), error_message
            else:
                assert value == expected_value, error_message


@wt(
    parsers.parse(
        "user of {browser_id} sees that current size statistics "
        "are as follow:\n{config}"
    )
)
def check_size_stats_for_archive(
    selenium: SeleniumDrivers, browser_id: str, config: str
) -> None:
    """Check size stats in directory details according to given config.

    Config format given in yaml is as follows:

        logical size: storage_type
        total physical size: total_physical_size
        contain counter: contain_counter
    """

    size_statistics = yaml.load(config, yaml.Loader)
    for stat_type, expected_value in size_statistics.items():
        check_size_statistic_in_dir_details(
            selenium, browser_id, stat_type, expected_value
        )


@wt(
    parsers.parse(
        "user of {browser_id} sees that size statistics for "
        "{provider} are as follow:\n{config}"
    )
)
def check_size_stats_for_archive_per_provider(
    selenium: SeleniumDrivers,
    browser_id: str,
    hosts: Hosts,
    config: str,
    provider: str,
) -> None:
    """Check size stats in directory details for specified provider according
    to given config.

        Config format given in yaml is as follows:

            logical size: storage_type
            physical size: physical_size
            content: content
    """

    size_statistics = yaml.load(config, yaml.Loader)
    for stat_type, expected_value in size_statistics.items():
        if stat_type != "content":
            check_size_stats_for_provider(
                selenium,
                hosts,
                browser_id,
                stat_type,
                [provider],
                [expected_value],
            )
        else:
            check_content_for_provider(
                selenium, hosts, browser_id, provider, expected_value
            )


@wt(
    parsers.parse(
        "user of {browser_id} sees that path in Entry Details in archive audit log"
        " matches the config and displayed archive name is correct for different screen"
        " sizes:\n{config}"
    )
)
def assert_archived_file_path_and_archive_name(
    browser_id: str,
    selenium: SeleniumDrivers,
    config: str,
) -> None:
    driver = selenium[browser_id]
    expected_path = IndexedPathSequence.from_yaml_dict(yaml.safe_load(config))

    for screen_size in ScreenSize:
        driver.set_window_size(screen_size.value.width, screen_size.value.height)
        time.sleep(1.0)
        archive_audit_log = Modals(driver).archive_audit_log
        entry_details_file_path = get_loaded_archive_file_path(driver)
        archive_name, file_path = extract_archive_name_and_path(entry_details_file_path)

        # Example shortened path:
        # 'long-directory_0\n›\n25 Aug 2026 21:21\n/\n...\n/\n'
        # 'long-directory_19\n/\nvery-long-file_20'

        assert_archive_names_match(archive_audit_log.archive_name, archive_name)
        actual_path = parse_indexed_path_sequence(file_path)

        assert actual_path.matches(expected_path), (
            "Path parameters shown in audit log entry details for "
            f"{screen_size.name.lower()} screen size: '{actual_path}' "
            f"do not match expected parameters: '{expected_path}'"
        )
