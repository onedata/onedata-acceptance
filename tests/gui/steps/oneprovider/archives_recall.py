"""This module contains gherkin steps to run acceptance tests featuring
archives recall in oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import re
import time
from datetime import datetime
from typing import Any

from tests.conftest import SeleniumDrivers
from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.utils import Modals, Popups
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        'user of {browser_id} sees {info}: "{text}" in archive recall information modal'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_info_in_archive_recall_information_modal(
    selenium: SeleniumDrivers, browser_id: Any, info: Any, text: Any
) -> Any:
    info_type = transform(info)
    recall_modal = Modals(selenium[browser_id]).archive_recall_information
    information = getattr(recall_modal, info_type)
    if info_type in ["files_recalled", "data_recalled"]:
        current_progress = recall_modal.get_progress_info(info_type)
        expected_progress = recall_modal.parse_progress(text)
        info_equal = current_progress == expected_progress
        assert info_equal, (
            f"{info}: {current_progress} progress info does "
            f"not match {expected_progress} in archive recall "
            f'information modal, raw text content: "{text}"'
        )
    else:
        assert text.lower() in information.lower().replace("\n", ""), (
            f"{info}: {text} does not match {information} in archive recall "
            "information modal"
        )


@wt(
    parsers.parse(
        "user of {browser_id} fails to see statistics of {info} "
        "in archive recall information modal"
    )
)
def fail_to_see_recalled_data_statistics(
    selenium: SeleniumDrivers, browser_id: Any, info: Any
) -> Any:

    recall_modal = Modals(selenium[browser_id]).archive_recall_information
    information = getattr(recall_modal, transform(info)).split("/")
    err_msg = f"There is visible statistics of {info}"
    assert information[0] == "", err_msg


@wt(
    parsers.parse(
        'user of {browser_id} waits for status "{status}" in archive '
        "recall information modal"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wait_for_status_in_archive_recall_information_modal(
    selenium: SeleniumDrivers, browser_id: Any, status: Any
) -> Any:
    driver = selenium[browser_id]
    recall_status = Modals(driver).archive_recall_information.status
    for _ in range(100):
        if recall_status == status:
            break
        time.sleep(2)
        recall_status = Modals(driver).archive_recall_information.status
    else:
        err_msg = f"Archive status:{recall_status} does not match expected"
        assert recall_status == status, err_msg


@wt(
    parsers.parse(
        "user of {browser_id} sees that recall has been {stop} at "
        "the same time or after recall has been {start}"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_recall_duration_in_archive_recall_information_modal(
    selenium: SeleniumDrivers, browser_id: Any, start: Any, stop: Any
) -> Any:
    """
    start variable could be the time of starting or canceling the recall,
    stop variable could be the time of canceling or finishing the recall
    """

    archive_recall_information = Modals(selenium[browser_id]).archive_recall_information
    start = f"{start}_at"
    stop = f"{stop}_at"

    started_at = getattr(archive_recall_information, start)
    finished_at = getattr(archive_recall_information, stop)
    begin = datetime.strptime(started_at, "%d %b %Y %H:%M:%S")
    finish = datetime.strptime(finished_at, "%d %b %Y %H:%M:%S")

    err_msg = f"Recall start time {begin} is greater than finish time {finish}"
    assert begin <= finish, err_msg


@wt(parsers.parse("user of {browser_id} sees that not all {kind} were recalled"))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_not_all_files_were_recalled(
    selenium: SeleniumDrivers, browser_id: Any, kind: Any
) -> Any:
    kind = kind + " recalled"
    characters = "[\nMiB ]"
    data_info = getattr(
        Modals(selenium[browser_id]).archive_recall_information, transform(kind)
    )
    info = re.sub(characters, "", data_info).split("/")
    all_data = float(info[1])
    recalled = float(info[0]) / 1024 if "KiB" in data_info else float(info[0])
    err_msg = f"Number of recalled {kind} is not smaller then all {kind}"
    assert all_data > recalled, err_msg


@wt(
    parsers.parse(
        "user of {browser_id} sees that number of items failed is greater than 0"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_number_of_item_greater_than_zero(
    selenium: SeleniumDrivers, browser_id: Any
) -> Any:
    driver = selenium[browser_id]
    items_failed = Modals(driver).archive_recall_information.items_failed
    try:
        number = int(items_failed)
    except ValueError:
        number = int(items_failed.split(" ")[0])
    assert number > 0, "Zero items failed"


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{option}" in dropdown menu in modal "{modal}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_option_in_dropdown_menu_in_modal(
    selenium: SeleniumDrivers, browser_id: Any, option: Any, modal: Any
) -> Any:
    driver = selenium[browser_id]
    modal = transform(modal)
    getattr(Modals(driver), modal).dropdown_menu.click()

    Popups(driver).power_select.choose_item(option)


@wt(
    parsers.parse(
        "user of {browser_id} waits for recalled status tag for "
        '"{name}" in file browser'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wait_for_recalled_status_tag(browser_id: Any, name: Any, tmp_memory: Any) -> Any:
    status_type = "recalled"
    browser = tmp_memory[browser_id]["file_browser"]

    for _ in range(100):
        is_visible = browser.data[name].is_tag_visible(status_type)
        if is_visible:
            break
        time.sleep(2)


@wt(
    parsers.parse(
        "user of {browser_id} sees that archive recall error logs "
        "table contain number of entries "
        "which is equal to number of items failed in status tab"
    )
)
def assert_number_of_entries_in_archive_recall(
    browser_id: Any, selenium: SeleniumDrivers
) -> Any:
    driver = selenium[browser_id]
    modal = Modals(driver).archive_recall_information
    items_failed = modal.items_failed
    try:
        number_of_items_failed = int(items_failed)
    except ValueError:
        number_of_items_failed = int(items_failed.split(" ")[0])
    # change tab
    modal.error_log.click()
    # if we want to scroll cursor need to be somewhere on the
    # table containing error logs
    modal.move_to_error_logs_table(driver)

    def condition(index: Any = 0) -> Any:
        # just pass
        _ = index

    detected_entries = _scroll_and_check_condition(browser_id, selenium, condition)
    err_msg = (
        f"number of entries is {len(detected_entries)} is not equal to "
        f"number of items failed {number_of_items_failed}"
    )
    assert len(detected_entries) == number_of_items_failed, err_msg


@wt(
    parsers.parse(
        "user of {browser_id} sees that archive recall error logs "
        "table contain only entries with the "
        'file name "{file_name}" or its duplicate names'
    )
)
def assert_entries_with_file_names_in_archive_recall(
    browser_id: Any, file_name: Any, selenium: SeleniumDrivers
) -> Any:
    # this test assumes that original file name does not
    # contain '(' or ')' characters
    driver = selenium[browser_id]
    modal = Modals(driver).archive_recall_information
    file_name_p = file_name.split(".")[0]
    file_name_s = file_name.split(".")[1]
    # if we want to scroll cursor need to be somewhere on the
    # table containing error logs
    modal.move_to_error_logs_table(driver)

    def condition(index: Any = 0) -> Any:
        entries = modal.error_file_row
        new_entries_names = [
            entry.text.split("\n")[1]
            for entry in entries
            if len(entry.text.split("\n")) > 1
        ]
        new_entries_names = new_entries_names[index:]
        for entry_name in new_entries_names:
            file_name_p_ = entry_name.split(".")[0]
            file_name_s_ = entry_name.split(".")[1]
            file_name_p_ = file_name_p_.split("(")[0]
            err_msg = (
                f"file name {entry_name} does not match name or name "
                f"duplicated of {file_name}"
            )
            assert file_name_p == file_name_p_ and file_name_s == file_name_s_, err_msg

    _scroll_and_check_condition(browser_id, selenium, condition)


@wt(
    parsers.parse(
        "user of {browser_id} sees that archive recall error "
        "logs table contain only entries with "
        'error message "{message}"'
    )
)
def assert_entries_with_error_messages_in_archive_recall(
    browser_id: Any, message: Any, selenium: SeleniumDrivers
) -> Any:
    driver = selenium[browser_id]
    modal = Modals(driver).archive_recall_information
    # if we want to scroll cursor need to be somewhere on the
    # table containing error logs
    modal.move_to_error_logs_table(driver)

    def condition(index: Any = 0) -> Any:
        entries = modal.error_file_row
        new_entries_mes = [
            entry.text.split("\n")[2]
            for entry in entries
            if len(entry.text.split("\n")) > 1
        ]
        new_entries_mes = new_entries_mes[index:]
        for entry_mes in new_entries_mes:
            err_msg = (
                f"There is visible error message {entry_mes}, but "
                f"expected message is {message}"
            )
            assert entry_mes == message, err_msg

    _scroll_and_check_condition(browser_id, selenium, condition)


def _scroll_and_check_condition(
    browser_id: Any, selenium: SeleniumDrivers, condition: Any, *args: Any
) -> Any:
    driver = selenium[browser_id]
    modal = Modals(driver).archive_recall_information
    entries = modal.error_file_row
    new_entries = [
        entry.text.split("\n")[1]
        for entry in entries
        if len(entry.text.split("\n")) > 1
    ]
    detected_entries = []
    detected_entries.extend(new_entries)
    index = 0
    while new_entries:
        condition(*args, index=index)

        modal.scroll_by_press_space()
        entries = modal.error_file_row
        new_entries = [
            entry.text.split("\n")[1]
            for entry in entries
            if len(entry.text.split("\n")) > 1
        ]
        index = 0
        for entry in new_entries:
            if entry not in detected_entries:
                break
            index += 1
        new_entries = new_entries[index:]
        detected_entries.extend(new_entries)
    return detected_entries


@wt(
    parsers.parse(
        "user of {browser_id} scrolls to the top in archive recall information"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def scroll_to_top_in_archive_recall_information(
    browser_id: Any, selenium: SeleniumDrivers
) -> Any:
    driver = selenium[browser_id]
    modal = Modals(driver).archive_recall_information
    modal.scroll_to_top()
