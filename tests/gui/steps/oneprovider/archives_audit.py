"""This module contains gherkin steps to run acceptance tests featuring
archives in oneprovider web GUI.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time

from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed
from tests.gui.utils.generic import parse_seq
from datetime import datetime
import re


@wt(parsers.re('user of (?P<browser_id>.*) sees no empty field(s)? '
               '"(?P<fields>( |.)*)" of first (?P<number>.*) files and dirs in'
               ' archive audit log'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_number_of_first_no_empty_options(selenium, modals, browser_id,
                                            fields, number: int):
    driver = selenium[browser_id]
    modal = modals(driver).archive_audit_log
    fields = parse_seq(fields)
    checked_elems = []
    visible_elems = modal.info_of_visible_elems('name')
    new_elems = visible_elems
    elems_count = len(new_elems)
    while new_elems:
        for field in fields:
            elems_to_check = modal.info_of_visible_elems(field)
            for elem in elems_to_check:
                assert elem != '', f'empty {field} field in elem {elem}'
        modal.scroll_by_press_space()
        checked_elems.extend(new_elems)
        visible_elems = modal.info_of_visible_elems('name')
        new_elems = []
        for elem in visible_elems:
            if elem not in checked_elems:
                new_elems.append(elem)
                elems_count += 1
    assert elems_count == number, (f'there are {elems_count} items instead'
                                   f' of {number}')


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
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_top_item_in_archive_audit_log(browser_id, modals,
                                           selenium):
    driver = selenium[browser_id]
    print(modals(driver).archive_audit_log.data)
    modal = modals(driver).archive_audit_log.data[0]
    modal.click()


@wt(parsers.re('user of (?P<browser_id>.*) sees that items? '
               '"(?P<items>( |.)*)" (is|are) visible in archive audit log'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_presence_of_items_in_archive_audit_log(browser_id, items, modals,
                                                  selenium):
    driver = selenium[browser_id]
    visible_items = modals(driver).archive_audit_log.data
    for item in parse_seq(items):
        assert item in visible_items,  (f'item {item} is not visible in archive'
                                        f' audit log')


@wt(parsers.parse('user of {browser_id} sees that {number} items '
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
    modal = modals(driver).details_audit_log
    visible_message = getattr(modal, field_name)
    assert visible_message == message, (f'expected {message} instead of '
                                        f'{visible_message} message, at field '
                                        f'{field_name}')


@wt(parsers.parse('user of {browser_id} closes details in archive audit log'))
@repeat_failed(timeout=WAIT_FRONTEND)
def close_details_in_archive_audit_log(browser_id, modals, selenium):
    driver = selenium[browser_id]
    modals(driver).details_audit_log.close.click()


@wt(parsers.parse('user of {browser_id} sees message type "{mes_type}" at '
                  'field "{field_name}" in archive audit log'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_pattern_at_field_in_archive_audit_log(browser_id, mes_type,
                                                 field_name, modals, selenium):
    driver = selenium[browser_id]
    modal = modals(driver).details_audit_log
    visible_message = getattr(modal, field_name)
    pattern = None
    if mes_type == 'date':
        pattern = re.compile(r"\d\d? [A-Z][a-z][a-z]? \d\d\d\d \d\d:\d\d:\d\d\."
                             r"\d\d\d")
    elif mes_type == 'file_id':
        pattern = re.compile(r"([A-Z]|[0-9])*")
    elif mes_type == 'time_taken':
        pattern = re.compile(r"\d*(\.\d*)?(ms|s|min|h)")
    elif mes_type == "location_path":
        pattern = re.compile(r"/.*")
    else:
        raise Exception('Empty pattern, unknown this message type')
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


@wt(parsers.parse('user of {browser_id} sees decreasing times' 
                  ' in archive audit log'))
def assert_decreasing_creation_times(browser_id, selenium, modals):
    item_name = 'name'
    creation_time = 'time'
    time_taken = 'time_taken'
    driver = selenium[browser_id]
    modal = modals(driver).archive_audit_log
    names = modal.info_of_visible_elems(item_name)
    new_names = names
    checked_names = []
    last_time = 1000000000
    last_dtime = datetime.strptime('1 Dec 9999 1:1:1.1', '%d %b %Y %H:%M:%S.%f')
    while new_names:
        names = modal.info_of_visible_elems(item_name)
        new_names = []
        creation_duration_times = modal.info_of_visible_elems(time_taken)
        creation_end_time = modal.info_of_visible_elems(creation_time)
        for index, name in enumerate(names):
            if name not in checked_names:
                current_time = parse_time(creation_duration_times[index])
                err_msg = (f'time {last_time} following {current_time} is not '
                           f'smaller')
                assert current_time <= last_time, err_msg
                current_dtime = datetime.strptime(creation_end_time[index] +
                                                  '000', '%d %b %Y %H:%M:%S.%f')
                err_msg = (f'date time {last_time} following {current_time} is '
                           f'not smaller')
                assert current_dtime <= last_dtime, err_msg
                last_dtime = current_dtime
                checked_names.append(name)
                new_names.append(name)
                last_time = current_time
        modal.scroll_by_press_space()


@wt(parsers.parse('user of {browser_id} clicks on field '
                  '"{field_name}" in details in archive audit log'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_field_in_details_archive_audit_log(browser_id, field_name,
                                                modals, selenium):
    driver = selenium[browser_id]
    modal = modals(driver).details_audit_log
    elem_to_click = getattr(modal, field_name)
    elem_to_click.click()
