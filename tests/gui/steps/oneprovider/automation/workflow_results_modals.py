"""This module contains gherkin steps to run acceptance tests featuring
workflow results modals in oneprovider web GUI """

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import json
from datetime import datetime
import time

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.steps.common.miscellaneous import switch_to_iframe
from tests.gui.steps.common.url import _open_url
from tests.gui.steps.oneprovider.automation.automation_basic import (
    check_if_task_is_opened, get_op_workflow_visualizer_page)
from tests.gui.utils.generic import parse_seq
from tests.utils.bdd_utils import wt, parsers
from tests.utils.path_utils import append_log_to_file
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} sees that chart with processing '
                  'stats exist'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_processing_chart(browser_id, selenium, modals):
    switch_to_iframe(selenium, browser_id)
    modal = modals(selenium[browser_id]).task_time_series
    assert modal.chart, 'chart with processing stats is not visible'


@wt(parsers.parse('user of {browser_id} sees that time in right corner of chart'
                  ' with processing stats is around actual time'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_time_on_lower_right_corner_of_chart_is_around_actual_time(
        browser_id, selenium, modals):
    switch_to_iframe(selenium, browser_id)
    modal = modals(selenium[browser_id]).task_time_series
    chart_time_in_right_corner = modal.get_time_from_chart()[-1]
    now = datetime.now()
    ts = datetime.timestamp(now)
    assert abs(chart_time_in_right_corner - ts) < 420, (
        'Difference between actual time and time on chart is greater than 420s')


@wt(parsers.parse('user of {browser_id} sees that value of last column on chart'
                  ' with processing stats is greater than zero'))
def assert_value_of_last_column_is_bigger_than_zero(browser_id, selenium,
                                                    modals):
    switch_to_iframe(selenium, browser_id)
    modal = modals(selenium[browser_id]).task_time_series
    values = modal.get_last_column_value()
    err_msg = (f'Last column {values[0][1]} is {values[0][0]} and'
               f' {values[1][1]} is {values[1][0]} when one of them should be '
               f'bigger than zero')
    assert (values[0][0] > 0 or values[1][0] > 0), err_msg


@wt(parsers.parse('user of {browser_id} chooses "{resolution}" resolution from'
                  ' time resolution list in modal "{modal}"'))
def choose_time_resolution(selenium, browser_id, popups, resolution, modal):
    driver = selenium[browser_id]
    for option in popups(driver).time_resolutions_list:
        if option.text == resolution:
            option.click()
            break
    else:
        raise Exception(f'There is no {resolution} in time resolution'
                        f' list in modal "{modal}".')


@wt(parsers.parse('user of {browser_id} sees "{message}" message on chart '
                  'with processing stats'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_no_data_message_processing_chart(browser_id, selenium, modals,
                                            message):
    switch_to_iframe(selenium, browser_id)
    actual_message = modals(selenium[browser_id]).task_time_series.no_data_message
    err_msg = (f'Actual message: "{actual_message}" on chart with processing'
               f' stats is not "{message}" as expected')
    assert actual_message == message, err_msg


@wt(parsers.parse('user of {browser_id} sees that {option} processing speed'
                  ' is greater or equal {number} per second on chart with'
                  ' processing stats'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_number_of_proceeded_files(browser_id, selenium, modals, option,
                                     number):
    switch_to_iframe(selenium, browser_id)
    modal = modals(selenium[browser_id]).task_time_series
    values = modal.get_last_column_value()
    for value in values:
        if option in value[1].lower():
            err_msg = (f'Processing speed is {value[0]} {option} per second '
                       f'and is lower than expected {number} per second.')
            assert value[0] >= int(number), err_msg
            break
    else:
        raise Exception(f'There is no {option} processing speed on chart with'
                        f' processing stat.')


@repeat_failed(timeout=WAIT_BACKEND)
def click_on_task_audit_log(task):
    if not check_if_task_is_opened(task):
        task.drag_handle.click()
    task.audit_log()


def get_modal_and_logs_for_task(path, task, modals, driver):
    append_log_to_file(path, task.name)
    click_on_task_audit_log(task)
    # wait a moment for audit log modal to appear
    time.sleep(1)
    modal = modals(driver).audit_log
    logs = modal.logs_entry
    return modal, logs


def close_modal_and_task(modal, task):
    modal.x()
    task.drag_handle.click()
    # wait for task to close
    time.sleep(1)


@repeat_failed(timeout=WAIT_FRONTEND)
def get_audit_log_json_and_write_to_file(log, modal, clipboard, displays,
                                         browser_id, path):
    log.click()
    modal.copy_json()
    audit_log = clipboard.paste(display=displays[browser_id])
    append_log_to_file(path, audit_log)


@wt(parsers.parse('user of {browser_id} opens "{store_name}" store details '
                  'modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def open_store_details_modal(selenium, browser_id, op_container, modals,
                             store_name):
    driver = selenium[browser_id]
    page = get_op_workflow_visualizer_page(op_container, driver)
    page.stores_list[store_name].click()
    time.sleep(0.25)
    return modals(driver).store_details


@repeat_failed(timeout=WAIT_BACKEND)
def compare_datasets_in_store_details_modal(item_list, modal, store_name):
    item_list = parse_seq(item_list)
    actual_items = [elem.name for elem in modal.store_content_list]
    for item in item_list:
        err_msg = f'{item} is not in Store details modal for {store_name} store'
        assert item in actual_items, err_msg


@repeat_failed(timeout=WAIT_BACKEND)
def compare_booleans_in_store_details_modal(item_list, modal):
    actual = [elem.value for elem in modal.store_content_list]
    err_msg = (f'Actual boolean list {actual} does not match '
               f'expected {item_list}')
    assert (actual.count('true') == item_list.count(True) and
            actual.count('false') == item_list.count(False)), err_msg


@repeat_failed(timeout=WAIT_BACKEND)
def compare_string_in_store_details_modal(item, modal, variable_type,
                                          store_name):
    actual = modal.raw_view.replace('"', '')
    err_msg = (f'expected {variable_type} {item} does not contain'
               f' {actual} in {store_name} store details modal')
    assert actual == str(item), err_msg


@repeat_failed(timeout=WAIT_BACKEND)
def compare_array_in_store_details_modal(modal, item_list):
    item_list = json.loads(item_list)
    expected_num = str(len(item_list))
    actual_num = modal.array_view.header.replace(')', '').split(' (')[1]

    assert expected_num == actual_num, (f'expected number: {expected_num}'
                                        f' of element in array does not'
                                        f' match actual: {actual_num}')
    for i in range(len(item_list)):
        actual_elem = modal.array_view.items[i].text
        assert str(item_list[i]) == actual_elem, (
            f'element {item_list[i]} does not match actual element '
            f'{actual_elem} on {i} position in array in store details '
            f'modal')


@repeat_failed(timeout=WAIT_BACKEND)
def open_raw_view_for_elem(store_content_list, index, modal):
    for _ in range(10):
        store_content_list[index].click()
        try:
            if modal.raw_view != '':
                break
        except AttributeError:
            if modal.single_file_container.name != '':
                break
    else:
        raise Exception(f'Did not manage to open raw view for '
                        f'{index} element in store content list')


@repeat_failed(timeout=WAIT_BACKEND)
def get_store_content(modal, store_type, index, clipboard, displays,
                      browser_id):
    store_content_type = 'store_content_' + store_type
    store_content_list = getattr(modal, store_content_type)
    try:
        open_raw_view_for_elem(store_content_list, index, modal)
    except RuntimeError:
        # this closes the successful copy alert
        modal.name_header.click()
        open_raw_view_for_elem(store_content_list, index, modal)
    modal.copy_button()
    return clipboard.paste(display=displays[browser_id])


@wt(parsers.parse('user of {browser_id} opens "{option}" URL from '
                  '"{store_name}" store in browser\'s location bar'))
def open_url_from_store_content(browser_id, option, store_name, selenium,
                                modals, op_container, clipboard, displays):

    modal = open_store_details_modal(selenium, browser_id, op_container,
                                     modals, store_name)
    modal.store_content_list[0].click()
    modal.copy_button()
    items = json.loads(clipboard.paste(display=displays[browser_id]))
    modal.close()

    url = items[option]
    _open_url(selenium, browser_id, url)


@repeat_failed(timeout=WAIT_FRONTEND)
def check_number_of_elements_in_store_details_modal(modal, number, store_name):
    actual_number = len(modal.store_content_object)
    err_msg = (f'Expected number of elements {number} is not equal to actual '
               f'number {actual_number} in "{store_name}" store details modal')

    assert actual_number == int(number), err_msg
