"""This module contains gherkin steps to run acceptance tests featuring
archives in oneprovider web GUI.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.steps.oneprovider.data_tab import assert_browser_in_tab_in_op
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed
from tests.gui.utils.generic import transform, parse_seq
import re


@wt(parsers.parse('user of {browser_id} sees no empty "{options}" info of '
                  'first "{number}" files and dirs in archive audit log'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_number_of_first_no_empty_options(selenium, modals, browser_id,
                                            options, number):
    driver = selenium[browser_id]
    modal = modals(driver).archive_audit_log
    options = parse_seq(options)
    checked_elems = []
    visible_elems = modal.info_of_visible_elems('name')
    new_elems = visible_elems
    elems_count = len(new_elems)
    while new_elems:
        for option in options:
            elems_to_check = modal.info_of_visible_elems(option)
            for elem in elems_to_check:
                assert elem != '', f'empty {option} field in elem {elem}'
        modal.scroll_by_press_space()
        checked_elems.extend(new_elems)
        visible_elems = modal.info_of_visible_elems('name')
        new_elems = []
        for elem in visible_elems:
            if elem not in checked_elems:
                new_elems.append(elem)
                elems_count += 1
    assert elems_count == int(number), f"checked first {elems_count} instead " \
                                       f"of {number}"


@wt(parsers.parse('user of {browser_id} clicks on item "{item_name}" in '
                  'archive audit log'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_item_in_archive_audit_log(browser_id, item_name, modals,
                                       selenium):
    driver = selenium[browser_id]
    modal = modals(driver).archive_audit_log.data[item_name]
    modal.click()


@wt(parsers.parse('user of {browser_id} sees "{message}" in field '
                  '"{field_name}" in archive audit log'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_message_at_field_in_archive_audit_log(browser_id, field_name,
                                                 modals, message, selenium):
    driver = selenium[browser_id]
    modal = modals(driver).details_audit_log
    actual_message = getattr(modal, field_name)
    assert actual_message == message, f"expected {message} instead of  " \
                                      f"{actual_message} message"


@wt(parsers.parse('user of {browser_id} closes details in archive audit log'))
@repeat_failed(timeout=WAIT_FRONTEND)
def close_details_in_archive_audit_log(browser_id, modals, selenium):
    driver = selenium[browser_id]
    modals(driver).details_audit_log.close.click()


@wt(parsers.parse('user of {browser_id} sees message pattern "{option}" in '
                  'field "{field_name}" in archive audit log'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_date_at_field_in_archive_audit_log(browser_id, option, field_name,
                                              modals, selenium):
    driver = selenium[browser_id]
    modal = modals(driver).details_audit_log
    actual_message = getattr(modal, field_name)
    pattern = None
    if option == 'date':
        pattern = re.compile(r"\d\d? [A-Z][a-z][a-z]? \d\d\d\d \d\d:\d\d:\d\d\."
                             r"\d\d\d")
    elif option == 'file_id':
        pattern = re.compile(r"([A-Z]|[0-9])*")
    elif option == 'time_taken':
        pattern = re.compile(r"\d*(\.\d*)?(ms|s|min|h)")
    elif option == "location_path":
        pattern = re.compile(r"/.*")
    else:
        raise Exception('Empty pattern')
    assert pattern.fullmatch(actual_message), f"message at field is" \
                                              f" {actual_message}"