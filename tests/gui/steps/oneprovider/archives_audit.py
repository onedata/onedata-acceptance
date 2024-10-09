"""This module contains gherkin steps to run acceptance tests featuring
archives audit logs in oneprovider web GUI.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

import re
from datetime import datetime

import yaml
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) sees non-empty "
        "(?P<fields>( |.)*) field(s)? of first (?P<number>.*) files and "
        "directories in archive audit log"
    )
)
def assert_number_of_first_non_empty_column_content(
    selenium, modals, fields, browser_id, number: int
):
    driver = selenium[browser_id]
    modal = modals(driver).archive_audit_log
    fields = parse_seq(fields)
    # Because files` names repeat, files` names must be first loaded in order to
    # add annotations to them

    def condition(index=0):
        pass

    _scroll_and_check_condition(browser_id, selenium, modals, condition)
    scroll_to_top_in_archive_audit_log(browser_id, selenium, modals)

    def condition(index=0):
        for field in fields:
            elems_to_check = modal.get_rows_of_column(field)[index:]
            for elem in elems_to_check:
                assert (
                    elem != ""
                ), f"there is empty {field} field: {elem} in archive audit log"

    checked_elems = _scroll_and_check_condition(
        browser_id, selenium, modals, condition
    )
    assert len(checked_elems) == number, (
        f"there is {len(checked_elems)} entries instead of {number} in archive "
        "audit log"
    )


@wt(
    parsers.parse(
        "user of {browser_id} sees entries ordered from shortest to "
        'longest times in column "{column_name}" in archive '
        "audit log"
    )
)
@wt(
    parsers.parse(
        "user of {browser_id} sees entries ordered from latest to "
        'oldest in column "{column_name}" in archive audit log'
    )
)
def assert_decreasing_creation_times_in_archives_audit_log(
    browser_id, column_name, selenium, modals
):
    driver = selenium[browser_id]
    modal = modals(driver).archive_audit_log
    start_value = None
    if column_name == "Time":
        start_value = datetime.strptime(
            "1 Dec 9999 1:1:1.1", "%d %b %Y %H:%M:%S.%f"
        )
    elif column_name == "Time taken":
        start_value = 1000000000

    def condition(last, index=0):
        currents = modal.get_rows_of_column(column_name)[index:]
        for current in currents:
            current_ = None
            if column_name == "Time":
                current_ = datetime.strptime(
                    current + "000", "%d %b %Y %H:%M:%S.%f"
                )
                err_msg = f"time {current_} following {last} is not smaller"
                assert current_ <= last, err_msg
            elif column_name == "Time taken":
                current_ = parse_time(current)
                err_msg = f"time {current_} following {last} is not smaller"
                assert current_ <= last, err_msg
            last = current_

    _scroll_and_check_condition(
        browser_id, selenium, modals, condition, start_value
    )


@wt(
    parsers.parse(
        "user of {browser_id} sees logs about directories or files "
        "ordered ascendingly by name index with prefix dir_ or file_ "
        "in archive audit log"
    )
)
def assert_ascending_file_or_dir_names(browser_id, selenium, modals):
    driver = selenium[browser_id]
    modal = modals(driver).archive_audit_log
    start_value = -1

    def condition(last, index=0):
        currents = modal.get_rows_of_column("File")[index:]
        for current in currents:
            current_ = int(current.strip("dirfile_"))
            err_msg = f"index {current_} following {last} is not bigger"
            assert current_ > last, err_msg
            last = current_

    _scroll_and_check_condition(
        browser_id, selenium, modals, condition, start_value
    )


@wt(
    parsers.parse(
        "user of {browser_id} sees that {number} first logs contain "
        "events about finished archivisation of files, directories "
        "or symbolic links in archive audit log"
    )
)
def assert_n_logs_about_archivisation_finished(
    browser_id, number: int, modals, selenium
):
    driver = selenium[browser_id]
    modal = modals(driver).archive_audit_log
    expected_events = [
        "Directory archivisation finished.",
        "Symbolic link archivisation finished.",
        "Regular file archivisation finished.",
    ]

    def condition(index=0):
        visible_events = modal.get_rows_of_column("Event")[index:]
        for event in visible_events:
            err_msg = f"visible event {event} is not expected"
            assert event in expected_events, err_msg

    checked_elems = _scroll_and_check_condition(
        browser_id, selenium, modals, condition
    )
    assert len(checked_elems) == number, (
        f"there are {len(checked_elems)} items instead of {number} in archive "
        "audit log"
    )


def _scroll_and_check_condition(browser_id, selenium, modals, condition, *args):
    driver = selenium[browser_id]
    modal = modals(driver).archive_audit_log
    checked_elems = []
    visible_elems = modal.get_rows_of_column("File")
    new_elems = visible_elems
    index = 0
    while new_elems:
        condition(*args, index=index)

        modal.scroll_by_press_space()
        checked_elems.extend(new_elems)
        visible_elems = modal.get_rows_of_column("File")
        index = 0
        for elem in visible_elems:
            if elem not in checked_elems:
                break
            index += 1
        new_elems = visible_elems[index:]
    return checked_elems


@wt(
    parsers.parse(
        "user of {browser_id} sees that entries in archive audit log "
        "contain following File and Event data:\n{config}"
    )
)
def check_entries_in_archive_audit_log(browser_id, config, selenium, modals):
    """
    There are only checked visible entries (without scrolling)
    There can be more entries than given (no error)
    Config format given in yaml:
        File: Event
    Example:
        file1: Regular file archivisation finished.
        dir1: Directory archivisation finished.
    """
    _check_entries_in_archive_audit_log(browser_id, config, selenium, modals)


def _check_entries_in_archive_audit_log(browser_id, config, selenium, modals):
    driver = selenium[browser_id]
    modal = modals(driver).archive_audit_log
    visible_logs = modal.data_row
    data = yaml.load(config, yaml.Loader)
    for item in data.keys():
        err_msg = (
            f"there is no visible log: {item}: {data[item]} in archive "
            "audit log"
        )
        assert (
            item in visible_logs and data[item] == visible_logs[item].event
        ), err_msg


@wt(
    parsers.parse(
        'user of {browser_id} clicks on item "{item_name}" in archive audit log'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_item_in_archive_audit_log(browser_id, item_name, modals, selenium):
    driver = selenium[browser_id]
    modal = modals(driver).archive_audit_log.data_row[item_name]
    modal.click()


@wt(
    parsers.parse(
        "user of {browser_id} clicks on top item in archive audit log"
    )
)
def click_on_top_item_in_archive_audit_log(browser_id, modals, selenium):
    click_on_item_in_archive_audit_log(browser_id, 0, modals, selenium)


@wt(
    parsers.parse(
        "user of {browser_id} sees that exactly {number} items "
        "are visible in archive audit log"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_number_of_items_in_archive_audit_log(
    browser_id, number: int, modals, selenium
):
    driver = selenium[browser_id]
    visible_items = modals(driver).archive_audit_log.get_rows_of_column("File")
    assert number == len(visible_items), (
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
    browser_id, field_name, modals, message, selenium
):
    driver = selenium[browser_id]
    modal = modals(driver).audit_log_entry_details
    visible_message = getattr(modal, transform(field_name))
    assert visible_message == message, (
        f"expected {message} instead of "
        f"{visible_message} message, at field "
        f"{field_name}"
    )


@wt(
    parsers.parse(
        "user of {browser_id} sees that details for archived "
        "item in archive audit log are as follow:\n{config}"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def check_details_for_archived_item(browser_id, config, modals, selenium):
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
    _check_details_for_archived_item(browser_id, config, modals, selenium)


def _check_details_for_archived_item(browser_id, config, modals, selenium):
    data = yaml.load(config, yaml.Loader)

    for field in data.keys():
        if isinstance(data[field], dict):
            mes_type = data[field]["type"]
            assert_pattern_at_field_in_archive_audit_log(
                browser_id, mes_type, transform(field), modals, selenium
            )
        else:
            message = data[field]
            assert_message_at_field_in_archive_audit_log(
                browser_id, transform(field), modals, message, selenium
            )


@wt(
    parsers.parse(
        'user of {browser_id} sees message type "{mes_type}" at '
        'field "{field_name}" in archive audit log'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_pattern_at_field_in_archive_audit_log(
    browser_id, mes_type, field_name, modals, selenium
):
    driver = selenium[browser_id]
    modal = modals(driver).audit_log_entry_details
    visible_message = getattr(modal, field_name)
    patterns = {
        "date": re.compile(
            r"\d\d? [A-Z][a-z][a-z]? \d\d\d\d \d\d?:" r"\d\d:\d\d\.\d\d\d"
        ),
        "file_id": re.compile(r"([A-Z]|[0-9])*"),
        "time_taken": re.compile(r"\d*(\.\d*)?(ms|s|min|h)"),
        "location_path": re.compile(r"/.*"),
    }
    if mes_type not in patterns:
        raise Exception("Empty pattern, unknown this message type")
    pattern = patterns[mes_type]
    err_msg = (
        f"message at field is {visible_message}, which does not"
        f" correspond to the type {mes_type}"
    )
    assert pattern.fullmatch(visible_message), err_msg


def parse_time(str_time):
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
    browser_id, field_name, modals, selenium
):
    driver = selenium[browser_id]
    modal = modals(driver).audit_log_entry_details
    elem_to_click = getattr(modal, transform(field_name))
    elem_to_click.click()


@wt(parsers.parse("user of {browser_id} scrolls to top in archive audit log"))
@repeat_failed(timeout=WAIT_FRONTEND)
def scroll_to_top_in_archive_audit_log(browser_id, selenium, modals):
    driver = selenium[browser_id]
    modal = modals(driver).archive_audit_log
    modal.scroll_to_top()
