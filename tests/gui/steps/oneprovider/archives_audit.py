"""This module contains gherkin steps to run acceptance tests featuring
archives audit logs in oneprovider web GUI.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import re
from collections import Counter
from collections.abc import Callable
from datetime import datetime
from typing import cast

import yaml

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.common import scroll_and_get_columns
from tests.gui.utils import Modals
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    parse_elements_sequence,
    parse_indexed_path_sequence,
    transform,
)
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees non-empty "
        rf"(?P<fields>{ELEMENTS_SEQUENCE_PATTERN}) field(s)? of first "
        r"(?P<number>.*) files and "
        r"directories in archive audit log"
    ),
    converters={
        "fields": parse_elements_sequence,
    },
)
def assert_number_of_first_non_empty_column_content(
    selenium: SeleniumDrivers, fields: list[str], browser_id: str, number: str
) -> None:
    expected_number = int(number)
    driver = selenium[browser_id]
    columns_names = [transform(field) for field in fields]

    # Because files names repeat, files names must be first loaded in order to
    # add annotations to them
    modal = Modals(driver).archive_audit_log
    _ = scroll_and_get_columns(modal, columns_names)
    scroll_to_top_in_archive_audit_log(browser_id, selenium)

    checked_elems = scroll_and_get_columns(modal, columns_names)
    elems_counter = Counter(checked_elems)
    non_unique_elems = [elem for elem in elems_counter if elems_counter[elem] > 1]

    assert len(checked_elems) == expected_number, (
        f"There are {len(checked_elems)} entries instead of {number} "
        "in archive audit log.\n\n"
        f"Number of non unique entries: {len(non_unique_elems)}\n\n"
        f"Entries: {sorted(checked_elems)}\n\n"
        f"Non Unique entries: {sorted(non_unique_elems)}"
    )


@wt(
    parsers.parse(
        "user of {browser_id} sees entries ordered from shortest to "
        'longest times in column "{column_name}" in archive audit log'
    )
)
@wt(
    parsers.parse(
        "user of {browser_id} sees entries ordered from latest to "
        'oldest in column "{column_name}" in archive audit log'
    )
)
def assert_decreasing_creation_times_in_archives_audit_log(
    browser_id: str, column_name: str, selenium: SeleniumDrivers
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).archive_audit_log
    start_value: datetime | int
    column_name = transform(column_name)
    if column_name == "time":
        start_value = datetime.strptime("1 Dec 9999 1:1:1.1", "%d %b %Y %H:%M:%S.%f")
    elif column_name == "time_taken":
        start_value = 1000000000
    else:
        raise ValueError(f"Unknown column: {column_name}")

    @repeat_failed(timeout=WAIT_FRONTEND)
    def condition(last: datetime | int, index: int = 0) -> None:
        rows_of_columns: dict[str, list[str]] = modal.get_visible_rows_of_columns(
            [column_name]
        )
        currents = rows_of_columns[column_name][index:]
        for current in currents:
            if column_name == "time":
                current_time = datetime.strptime(
                    current + "000", "%d %b %Y %H:%M:%S.%f"
                )
                error_message = f"time {current_time} following {last} is not smaller"
                assert current_time <= cast(datetime, last), error_message
                last = current_time
            elif column_name == "time_taken":
                current_duration = parse_time(current)
                error_message = (
                    f"time {current_duration} following {last} is not smaller"
                )
                assert current_duration <= cast(int | float, last), error_message
                last = cast(int, current_duration)

    _scroll_and_check_condition(browser_id, selenium, condition, start_value)


@wt(
    parsers.parse(
        "user of {browser_id} sees logs about directories or files "
        "ordered ascendingly by name index with prefix dir_ or "
        "file_ in archive audit log"
    )
)
def assert_ascending_file_or_dir_names(
    browser_id: str, selenium: SeleniumDrivers
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).archive_audit_log
    start_value = -1

    @repeat_failed(timeout=WAIT_FRONTEND)
    def condition(last: int, index: int = 0) -> None:
        currents = modal.get_visible_rows_of_single_column("file")[index:]
        for current in currents:
            current_ = int(current.strip("dirfile_"))
            error_message = f"index {current_} following {last} is not bigger"
            assert current_ > last, error_message
            last = current_

    _scroll_and_check_condition(browser_id, selenium, condition, start_value)


@wt(
    parsers.parse(
        "user of {browser_id} sees that {number} first logs contain "
        "events about finished archivisation of files, directories "
        "or symbolic links in archive audit log"
    )
)
def assert_n_logs_about_archivisation_finished(
    browser_id: str, number: str, selenium: SeleniumDrivers
) -> None:
    expected_number = int(number)
    driver = selenium[browser_id]
    modal = Modals(driver).archive_audit_log
    expected_events = [
        "Directory archivisation finished.",
        "Symbolic link archivisation finished.",
        "Regular file archivisation finished.",
    ]

    @repeat_failed(timeout=WAIT_FRONTEND)
    def condition(index: int = 0) -> None:
        visible_events: list[str] = modal.get_visible_rows_of_single_column("event")[
            index:
        ]
        for event in visible_events:
            error_message = f"visible event {event} is not expected"
            assert event in expected_events, error_message

    checked_elems = _scroll_and_check_condition(browser_id, selenium, condition)
    assert (
        len(checked_elems) == expected_number
    ), f"there are {len(checked_elems)} items instead of {number} in archive audit log"


def _scroll_and_check_condition(
    browser_id: str,
    selenium: SeleniumDrivers,
    condition: Callable[..., None],
    *args: object,
) -> list[str]:
    driver = selenium[browser_id]
    modal = Modals(driver).archive_audit_log
    checked_elems = []
    visible_elems = modal.get_visible_rows_of_single_column("file")
    new_elems = visible_elems
    last_index = 0

    while new_elems:
        condition(*args, index=last_index)
        checked_elems.extend(new_elems)
        driver.execute_script(
            "arguments[0].scrollIntoView();",
            modal.data_row[new_elems[-1]].clickable_field,
        )
        visible_elems = modal.get_visible_rows_of_single_column("file")
        for index, elem in enumerate(visible_elems):
            if elem not in checked_elems:
                last_index = index
                break
        else:
            last_index = len(visible_elems)
        new_elems = visible_elems[last_index:]
    return checked_elems


@wt(
    parsers.parse(
        "user of {browser_id} sees that entries in archive audit log "
        "contain following File and Event data:\n{config}"
    )
)
def check_entries_in_archive_audit_log(
    browser_id: str, config: str, selenium: SeleniumDrivers
) -> None:
    """
    There are only checked visible entries (without scrolling)
    There can be more entries than given (no error)
    Config format given in yaml:
        File: Event
    Example:
        file1: Regular file archivisation finished.
        dir1: Directory archivisation finished.
    """
    _check_entries_in_archive_audit_log(browser_id, config, selenium)


@repeat_failed(timeout=WAIT_FRONTEND)
def _check_entries_in_archive_audit_log(
    browser_id: str, config: str, selenium: SeleniumDrivers
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).archive_audit_log
    visible_logs = modal.data_row
    data = yaml.load(config, yaml.Loader)
    for item in data.keys():
        error_message = (
            f"there is no visible log: {item}: {data[item]} in archive audit log"
        )
        assert (
            item in visible_logs and data[item] == visible_logs[item].event
        ), error_message


@wt(
    parsers.parse(
        'user of {browser_id} clicks on item "{item_name}" in archive audit log'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_item_in_archive_audit_log(
    browser_id: str, item_name: str | int, selenium: SeleniumDrivers
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).archive_audit_log.data_row[item_name]
    modal.click()


@wt(
    parsers.parse(
        'user of {browser_id} clicks on item "{file_name}" using '
        "scroll in archive audit log"
    )
)
def click_on_entry_with_file_name_using_scroll_in_archive_audit_log(
    browser_id: str, file_name: str, selenium: SeleniumDrivers
) -> None:

    driver = selenium[browser_id]
    modal = Modals(driver).archive_audit_log

    seen_rows = set()
    stop_scrolling_flag = False
    while not stop_scrolling_flag:
        new_rows_names = modal.get_visible_rows_of_single_column("file")

        if file_name in new_rows_names:
            driver.execute_script(
                "arguments[0].scrollIntoView();",
                modal.data_row[file_name].clickable_field,
            )
            modal.data_row[file_name].clickable_field.click()
            return

        stop_scrolling_flag = not any(el not in seen_rows for el in new_rows_names)
        seen_rows.update(new_rows_names)

        driver.execute_script(
            "arguments[0].scrollIntoView();",
            modal.data_row[new_rows_names[-1]].clickable_field,
        )

    raise AssertionError(f"entry {file_name} not found in archive audit log")


@wt(parsers.parse("user of {browser_id} clicks on top item in archive audit log"))
def click_on_top_item_in_archive_audit_log(
    browser_id: str, selenium: SeleniumDrivers
) -> None:
    click_on_item_in_archive_audit_log(browser_id, 0, selenium)


@wt(
    parsers.parse(
        "user of {browser_id} sees that exactly {number} items "
        "are visible in archive audit log"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_number_of_items_in_archive_audit_log(
    browser_id: str, number: str, selenium: SeleniumDrivers
) -> None:
    driver = selenium[browser_id]
    visible_items: list[str] = Modals(
        driver
    ).archive_audit_log.get_visible_rows_of_single_column("file")
    assert int(number) == len(visible_items), (
        f"there are {len(visible_items)} "
        f"items visible instead of {number} "
        "in archive audit log"
    )


@wt(
    parsers.parse(
        'user of {browser_id} sees message "{message}" at field '
        '"{field_name}" in archive audit log'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_message_at_field_in_archive_audit_log(
    browser_id: str, field_name: str, message: str, selenium: SeleniumDrivers
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).audit_log_entry_details
    visible_message = getattr(modal, transform(field_name))
    assert (
        visible_message == message
    ), f"expected {message} instead of {visible_message} message, at field {field_name}"


@wt(
    parsers.parse(
        "user of {browser_id} sees that details for archived "
        "item in archive audit log are as follow:\n{config}"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def check_details_for_archived_item(
    browser_id: str, config: str, selenium: SeleniumDrivers
) -> None:
    """
    Config format given in yaml:
    Possible fields, each of them is optional
        Event
        Relative location
        Started at
        Finished at
        Time taken
        Archived item absolute location
        File ID
        Source item absolute location
    Configuration to each field can be passed in 2 ways:
        Specific message to be matched
        [field name]: text
        or
        Pattern of message to be matched
        [field name]:
          type: date/file_id/time_taken/location_path

    Example:
    Event: Directory archivisation finished.
    Started at:
      type: date
    Finished at:
      type: date
    """
    _check_details_for_archived_item(browser_id, config, selenium)


def _check_details_for_archived_item(
    browser_id: str, config: str, selenium: SeleniumDrivers
) -> None:
    data = yaml.load(config, yaml.Loader)

    for field in data.keys():
        if isinstance(data[field], dict):
            mes_type = data[field]["type"]
            assert_pattern_at_field_in_archive_audit_log(
                browser_id, mes_type, transform(field), selenium
            )
        else:
            message = data[field]
            assert_message_at_field_in_archive_audit_log(
                browser_id, transform(field), message, selenium
            )


@wt(
    parsers.parse(
        'user of {browser_id} sees message type "{mes_type}" at '
        'field "{field_name}" in archive audit log'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_pattern_at_field_in_archive_audit_log(
    browser_id: str, mes_type: str, field_name: str, selenium: SeleniumDrivers
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).audit_log_entry_details
    visible_message = getattr(modal, field_name)
    patterns = {
        "date": re.compile(r"\d\d? [A-Z][a-z][a-z]? \d\d\d\d \d\d?:\d\d:\d\d\.\d\d\d"),
        "file_id": re.compile(r"([A-Z]|[0-9])*"),
        "time_taken": re.compile(r"\d*(\.\d*)?(ms|s|min|h)"),
        "location_path": re.compile(r"/.*"),
    }
    if mes_type not in patterns:
        raise AssertionError("Empty pattern, unknown this message type")
    pattern = patterns[mes_type]
    error_message = (
        f"message at field is {visible_message}, which does not"
        f" correspond to the type {mes_type}"
    )
    assert pattern.fullmatch(visible_message), error_message


def parse_time(str_time: str) -> int | float:
    n = len(str_time)
    if str_time[n - 2 : n] == "ms":
        return int(str_time[: n - 2])
    if str_time[n - 1] == "s":
        return float(str_time[: n - 1]) * 1000
    raise ValueError("wrong time unit")


@wt(
    parsers.parse(
        "user of {browser_id} clicks on link for field "
        '"{field_name}" in details in archive audit log'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_field_in_details_archive_audit_log(
    browser_id: str, field_name: str, selenium: SeleniumDrivers
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).audit_log_entry_details
    elem_to_click = getattr(modal, transform(field_name))
    elem_to_click.click()


@wt(parsers.parse("user of {browser_id} scrolls to top in archive audit log"))
@repeat_failed(timeout=WAIT_FRONTEND)
def scroll_to_top_in_archive_audit_log(
    browser_id: str, selenium: SeleniumDrivers
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).archive_audit_log
    modal.scroll_to_top()


@wt(
    parsers.parse(
        "user of {browser_id} sees that path in Entry Details in archive audit log is:"
        ' "{path}" and displayed archive name is correct'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_archived_file_path_and_archive_name(
    browser_id: str, selenium: SeleniumDrivers, path: str
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).archive_audit_log
    modal_details = Modals(driver).audit_log_entry_details
    separator = "›"

    # Example shortened path:
    # 'long-directory_0\n›\n25 Aug 2026 21:21\n/\n...\n/\nlong-directory_19\n/\nvery-long-file_20'
    details_file_path = modal_details.file_path.replace("\n", "")

    # Depending on window size, the archive name may not be present.
    if separator in details_file_path:
        splitted_file_path = details_file_path.split("/")
        details_archive_info = splitted_file_path[0]

        details_archive_name = details_archive_info.partition(separator)[2]
        assert modal.archive_name == details_archive_name, (
            f"name of archive in archive audit log modal: {modal.archive_name} is"
            f" different than shown in audit log entry details:  {details_archive_name}"
        )
        path_without_archive_name = "/".join(splitted_file_path[1:])
    else:
        path_without_archive_name = details_file_path

    details_path_params = parse_indexed_path_sequence(path_without_archive_name)
    expected_path_params = parse_indexed_path_sequence(path)

    assert details_path_params == expected_path_params, (
        f"given path: {path_without_archive_name} is different than actual file path:"
        f" {path}"
    )


@wt(
    parsers.parse(
        'user of {browser_id} sees that all entries with filename: "{file_name}"'
        ' have different hashes and sees exactly "{number}" of them'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_unique_hashes_and_number_of_logs(
    browser_id: str, selenium: SeleniumDrivers, file_name: str, number: str
) -> None:
    driver = selenium[browser_id]
    logs = Modals(driver).archive_audit_log.data_row
    hashes = []
    for log in logs:
        if log.file == file_name:
            log_hash = log.duplicated_name_hash
            assert (
                log_hash not in hashes
            ), f"There are at least two identical hashes: {log_hash}"
            hashes.append(log_hash)

    assert len(hashes) == int(
        number
    ), f"Expected number of logs: {number} is different than actual: {len(hashes)}"
