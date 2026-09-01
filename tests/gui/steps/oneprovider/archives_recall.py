"""This module contains gherkin steps to run acceptance tests featuring
archives recall in oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import re
import time
from collections.abc import Callable
from datetime import datetime
from typing import List

from tests.gui.steps.common.common import parse_size
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils import Modals, Popups
from tests.gui.utils.common.constants import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.utils.generic import transform
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_FRONTEND)
def get_archive_recall_information_property_without_whitespace(
    selenium: SeleniumDrivers, browser_id: str, property_name: str
) -> str:
    modal = Modals(selenium[browser_id]).archive_recall_information
    return re.sub(r"\s*", "", getattr(modal, property_name))


@wt(
    parsers.parse(
        'user of {browser_id} sees {info}: "{text}" in archive recall information modal'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_info_in_archive_recall_information_modal(
    selenium: SeleniumDrivers, browser_id: str, info: str, text: str
) -> None:
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
    selenium: SeleniumDrivers, browser_id: str, info: str
) -> None:

    recall_modal = Modals(selenium[browser_id]).archive_recall_information
    information = getattr(recall_modal, transform(info)).split("/")
    error_message = f"There is visible statistics of {info}"
    assert information[0] == "", error_message


@wt(
    parsers.parse(
        'user of {browser_id} waits for status "{status}" in archive '
        "recall information modal"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wait_for_status_in_archive_recall_information_modal(
    selenium: SeleniumDrivers, browser_id: str, status: str
) -> None:
    driver = selenium[browser_id]
    recall_status = Modals(driver).archive_recall_information.status
    for _ in range(100):
        if recall_status == status:
            break
        time.sleep(2)
        recall_status = Modals(driver).archive_recall_information.status
    else:
        error_message = f"Archive status:{recall_status} does not match expected"
        assert recall_status == status, error_message


@wt(
    parsers.parse(
        "user of {browser_id} sees that recall has been {stop} at "
        "the same time or after recall has been {start}"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_recall_duration_in_archive_recall_information_modal(
    selenium: SeleniumDrivers, browser_id: str, start: str, stop: str
) -> None:
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

    error_message = f"Recall start time {begin} is greater than finish time {finish}"
    assert begin <= finish, error_message


@wt(parsers.parse("user of {browser_id} sees that not all {kind} were recalled"))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_not_all_files_were_recalled(
    selenium: SeleniumDrivers,
    browser_id: str,
    kind: str,
) -> None:
    recalled_kind = f"{kind} recalled"

    data_info = getattr(
        Modals(selenium[browser_id]).archive_recall_information,
        transform(recalled_kind),
    )

    recalled_text, all_data_text = data_info.replace("\n", "").split("/", maxsplit=1)
    if kind == "data":
        recalled = parse_size(recalled_text)
        all_data = parse_size(all_data_text)
    else:
        recalled = int(recalled_text)
        all_data = int(all_data_text)

    assert (
        recalled < all_data
    ), f"Number of recalled {kind} is not smaller than all {kind}: {data_info!r}"


@wt(
    parsers.parse(
        "user of {browser_id} sees that number of items failed is greater than 0"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_number_of_item_greater_than_zero(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
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
    selenium: SeleniumDrivers, browser_id: str, option: str, modal: str
) -> None:
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
def wait_for_recalled_status_tag(
    browser_id: str, name: str, tmp_memory: TmpMemory
) -> None:
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
    browser_id: str, selenium: SeleniumDrivers
) -> None:
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

    def condition(index: int = 0) -> None:
        # just pass
        _ = index

    detected_entries = _scroll_and_check_condition(browser_id, selenium, condition)
    error_message = (
        f"number of entries is {len(detected_entries)} is not equal to "
        f"number of items failed {number_of_items_failed}"
    )
    assert len(detected_entries) == number_of_items_failed, error_message


@wt(
    parsers.parse(
        "user of {browser_id} sees that archive recall error logs "
        "table contain only entries with the "
        'file name "{file_name}" or its duplicate names'
    )
)
def assert_entries_with_file_names_in_archive_recall(
    browser_id: str, file_name: str, selenium: SeleniumDrivers
) -> None:
    # this test assumes that original file name does not
    # contain '(' or ')' characters
    driver = selenium[browser_id]
    modal = Modals(driver).archive_recall_information
    file_name_p, file_name_s = file_name.rsplit(".", 1)
    # if we want to scroll cursor need to be somewhere on the
    # table containing error logs
    modal.move_to_error_logs_table(driver)

    def condition(index: int = 0) -> None:
        new_entries_names: List[str] = modal.get_visible_rows_of_single_column(
            "source_file"
        )[index:]
        for entry_name in new_entries_names:
            file_name_p_, file_name_s_ = file_name.rsplit(".", 1)
            file_name_p_ = file_name_p_.split("(")[0]
            error_message = (
                f"file name {entry_name} does not match name or name "
                f"duplicated of {file_name}"
            )
            assert (
                file_name_p == file_name_p_ and file_name_s == file_name_s_
            ), error_message

    _scroll_and_check_condition(browser_id, selenium, condition)


@wt(
    parsers.parse(
        "user of {browser_id} sees that archive recall error "
        "logs table contain only entries with "
        'error message "{message}"'
    )
)
def assert_entries_with_error_messages_in_archive_recall(
    browser_id: str, message: str, selenium: SeleniumDrivers
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).archive_recall_information
    # if we want to scroll cursor need to be somewhere on the
    # table containing error logs
    modal.move_to_error_logs_table(driver)

    def condition(index: int = 0) -> None:
        new_entries_mes: List[str] = modal.get_visible_rows_of_single_column(
            "error_message"
        )

        new_entries_mes = new_entries_mes[index:]
        for entry_mes in new_entries_mes:
            error_message = (
                f"There is visible error message {entry_mes}, but "
                f"expected message is {message}"
            )
            assert entry_mes == message, error_message

    _scroll_and_check_condition(browser_id, selenium, condition)


def _scroll_and_check_condition(
    browser_id: str,
    selenium: SeleniumDrivers,
    condition: Callable[..., None],
    *args: object,
) -> list[str]:
    driver = selenium[browser_id]
    modal = Modals(driver).archive_recall_information
    new_entries: List[str] = modal.get_visible_rows_of_single_column("source_file")
    detected_entries = []
    detected_entries.extend(new_entries)
    index = 0
    while new_entries:
        condition(*args, index=index)

        modal.scroll_by_press_space()
        new_entries = modal.get_visible_rows_of_single_column("source_file")
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
    browser_id: str, selenium: SeleniumDrivers
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).archive_recall_information
    modal.scroll_to_top()
