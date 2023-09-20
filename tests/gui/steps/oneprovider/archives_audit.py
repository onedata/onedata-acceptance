"""This module contains gherkin steps to run acceptance tests featuring
archives audit logs in oneprovider web GUI.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import yaml
import re

from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed
from tests.gui.utils.generic import parse_seq, transform
from datetime import datetime


@wt(parsers.re('user of (?P<browser_id>.*) sees no empty '
               '(?P<fields>( |.)*) field(s)? of first (?P<number>.*) files and '
               'directories in archive audit log'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_number_of_first_no_empty_column_content(selenium, modals, fields,
                                                   browser_id, number: int):
    driver = selenium[browser_id]
    modal = modals(driver).archive_audit_log
    fields = parse_seq(fields)
    checked_elems = []
    visible_elems = modal.info_of_visible_elems('File')
    new_elems = visible_elems
    elems_count = len(new_elems)
    while new_elems:
        for field in fields:
            elems_to_check = modal.info_of_visible_elems(field)
            for elem in elems_to_check:
                assert elem != '', f'empty {field} field in elem {elem}'
        modal.scroll_by_press_space()
        checked_elems.extend(new_elems)
        visible_elems = modal.info_of_visible_elems('File')
        new_elems = []
        for elem in visible_elems:
            if elem not in checked_elems:
                new_elems.append(elem)
                elems_count += 1
    assert elems_count == number, (f'there are {elems_count} items instead'
                                   f' of {number}')


@wt(parsers.parse('user of {browser_id} sees that {number} first logs contain '
                  'events about archivisation finished of files, directories '
                  'or symbolic links in archive audit log'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_n_logs_about_archivisation_finished(browser_id, number: int, modals,
                                               selenium):
    driver = selenium[browser_id]
    modal = modals(driver).archive_audit_log
    visible_items = modal.info_of_visible_elems('File')
    expected_events = ['Directory archivisation finished.',
                       'Symbolic link archivisation finished.',
                       'Regular file archivisation finished.']
    new_elems = visible_items
    checked_elems = []
    log_count = 0
    while new_elems:
        visible_items = modal.info_of_visible_elems('File')
        visible_events = modal.info_of_visible_elems('Event')
        for index, event in enumerate(visible_events):
            err_msg = f'visible event {event} is not expected'
            assert event in expected_events, err_msg
            checked_elems.append(visible_items[index])
            log_count += 1
            if log_count >= number:
                break
        if log_count >= number:
            break
        modal.scroll_by_press_space()
        new_elems = []
        for elem in modal.info_of_visible_elems('File'):
            if elem not in checked_elems:
                new_elems.append(elem)
    assert log_count == number


@wt(parsers.parse('user of {browser_id} clicks on item "{item_name}" in '
                  'archive audit log'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_item_in_archive_audit_log(browser_id, item_name, modals,
                                       selenium):
    driver = selenium[browser_id]
    modal = modals(driver).archive_audit_log.data[item_name]
    modal.click()


@wt(parsers.parse('user of {browser_id} clicks on top item in '
                  'archive audit log'))
def click_on_top_item_in_archive_audit_log(browser_id, modals,
                                           selenium):
    click_on_item_in_archive_audit_log(browser_id, 0, modals, selenium)


@wt(parsers.re('user of (?P<browser_id>.*) sees that items? '
               '(?P<items>( |.)*) (is|are) visible in archive audit log'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_presence_of_items_in_archive_audit_log(browser_id, items, modals,
                                                  selenium):
    driver = selenium[browser_id]
    visible_items = modals(driver).archive_audit_log.data
    for item in parse_seq(items):
        assert item in visible_items,  (f'item {item} is not visible in archive'
                                        f' audit log')


@wt(parsers.parse('user of {browser_id} sees that exactly {number} items '
                  'are visible in archive audit log'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_number_of_items_in_archive_audit_log(browser_id, number: int, modals,
                                                selenium):
    driver = selenium[browser_id]
    visible_items = modals(driver).archive_audit_log.data
    assert number == len(visible_items), (f'there are {len(visible_items)} '
                                          f'items visible instead of {number} '
                                          f'in archive audit log')


@wt(parsers.parse('user of {browser_id} sees message "{message}" at field '
                  '"{field_name}" in archive audit log'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_message_at_field_in_archive_audit_log(browser_id, field_name,
                                                 modals, message, selenium):
    driver = selenium[browser_id]
    modal = modals(driver).details_archive_audit_log
    visible_message = getattr(modal, transform(field_name))
    assert visible_message == message, (f'expected {message} instead of '
                                        f'{visible_message} message, at field '
                                        f'{field_name}')


@wt(parsers.parse('user of {browser_id} sees that details for archived '
                  'item in archive audit log are as follow:\n{config}'))
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
    data = yaml.load(config)

    for field in data.keys():
        if isinstance(data[field], dict):
            mes_type = data[field]['type']
            assert_pattern_at_field_in_archive_audit_log(browser_id, mes_type,
                                                         transform(field),
                                                         modals, selenium)
        else:
            message = data[field]
            assert_message_at_field_in_archive_audit_log(browser_id,
                                                         transform(field),
                                                         modals, message,
                                                         selenium)


@wt(parsers.parse('user of {browser_id} sees message type "{mes_type}" at '
                  'field "{field_name}" in archive audit log'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_pattern_at_field_in_archive_audit_log(browser_id, mes_type,
                                                 field_name, modals, selenium):
    driver = selenium[browser_id]
    modal = modals(driver).details_archive_audit_log
    visible_message = getattr(modal, field_name)
    patterns = {'date': re.compile(r"\d\d? [A-Z][a-z][a-z]? \d\d\d\d \d\d?:"
                                   r"\d\d:\d\d\.\d\d\d"),
                'file_id': re.compile(r"([A-Z]|[0-9])*"),
                'time_taken': re.compile(r"\d*(\.\d*)?(ms|s|min|h)"),
                'location_path': re.compile(r"/.*")
                }
    if mes_type not in patterns:
        raise Exception('Empty pattern, unknown this message type')
    pattern = patterns[mes_type]
    err_msg = (f'message at field is {visible_message}, which does not'
               f' correspond to the type {mes_type}')
    assert pattern.fullmatch(visible_message), err_msg


def parse_time(str_time):
    n = len(str_time)
    if str_time[n-2:n] == 'ms':
        return int(str_time[:n-2])
    elif str_time[n-1] == 's':
        return float(str_time[:n-1]) * 1000
    else:
        raise Exception('wrong time unit')


@wt(parsers.parse('user of {browser_id} sees entries ordered from newest to'
                  ' oldest in column "{column_name}" in archive audit log'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_decreasing_creation_times_in_archives_audit_log(browser_id,
                                                           column_name,
                                                           selenium, modals):
    err_msg = (f'column name {column_name} is expected to be Time or Time '
               f'taken')
    assert column_name in ['Time', 'Time taken'], err_msg
    item_name = 'File'
    driver = selenium[browser_id]
    modal = modals(driver).archive_audit_log
    names = modal.info_of_visible_elems(item_name)
    new_names = names
    checked_names = []
    last = None
    if column_name == "Time":
        last = datetime.strptime('1 Dec 9999 1:1:1.1', '%d %b %Y %H:%M:%S.%f')
    elif column_name == "Time taken":
        last = 1000000000
    while new_names:
        names = modal.info_of_visible_elems(item_name)
        new_names = []
        currents = modal.info_of_visible_elems(column_name)
        for index, name in enumerate(names):
            if name not in checked_names:
                current = currents[index]
                current_ = None
                if column_name == 'Time':
                    current_ = datetime.strptime(current + '000',
                                                 '%d %b %Y %H:%M:%S.%f')
                    err_msg = (
                        f'time {current_} following {last} is not smaller')
                    assert current_ <= last, err_msg
                elif column_name == "Time taken":
                    current_ = parse_time(current)
                    err_msg = (
                        f'time {current_} following {last} is not smaller')
                    assert current_ <= last, err_msg
                checked_names.append(name)
                new_names.append(name)
                last = current_
        modal.scroll_by_press_space()


@wt(parsers.parse('user of {browser_id} sees logs about directories or files '
                  'ordered ascendingly by name index with prefix dir_ or file_ '
                  'in archive audit log'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_ascending_file_or_dir_names(browser_id, selenium, modals):
    item_name = 'File'
    driver = selenium[browser_id]
    modal = modals(driver).archive_audit_log
    names = modal.info_of_visible_elems(item_name)
    new_names = names
    checked_names = []
    last = -1
    while new_names:
        names = modal.info_of_visible_elems(item_name)
        new_names = []
        currents = modal.info_of_visible_elems(item_name)
        for index, name in enumerate(names):
            if name not in checked_names:
                current = currents[index]
                current_ = int(current.strip('dirfile_'))
                err_msg = (
                    f'index {current_} following {last} is not bigger')
                assert current_ > last, err_msg
                checked_names.append(name)
                new_names.append(name)
                last = current_
        modal.scroll_by_press_space()


@wt(parsers.parse('user of {browser_id} clicks on field '
                  '"{field_name}" in details in archive audit log'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_field_in_details_archive_audit_log(browser_id, field_name,
                                                modals, selenium):
    driver = selenium[browser_id]
    modal = modals(driver).details_archive_audit_log
    elem_to_click = getattr(modal, transform(field_name))
    elem_to_click.click()
