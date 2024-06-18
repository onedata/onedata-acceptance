"""This module contains meta steps for operations on automation page checking
audit logs in Oneprovider using web GUI
"""
__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import json
import time
import os
from datetime import date

import yaml
from selenium.common.exceptions import StaleElementReferenceException

from tests import GUI_LOGDIR
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.meta_steps.oneprovider.automation.workflow_results import (
    get_store_details_json, open_modal_and_get_store_content)
from tests.gui.meta_steps.oneprovider.data import get_file_id_from_details_modal
from tests.gui.steps.common.url import switch_to_last_tab
from tests.gui.steps.oneprovider.archives import from_ordinal_number_to_int
from tests.gui.steps.oneprovider.automation.automation_basic import (
    check_if_task_is_opened, switch_to_automation_page,
    get_op_workflow_visualizer_page, click_on_task_in_lane,
    click_on_link_in_task_box)
from tests.gui.steps.oneprovider.automation.automation_statuses import (
    get_status_from_workflow_visualizer)
from tests.gui.steps.oneprovider.automation.workflow_results_modals import (
    get_modal_and_logs_for_task, get_audit_log_json_and_write_to_file,
    close_modal_and_task, click_on_task_audit_log, open_store_details_modal,
    compare_datasets_in_store_details_modal,
    compare_booleans_in_store_details_modal,
    compare_string_in_store_details_modal, compare_array_in_store_details_modal,
    check_number_of_elements_in_store_details_modal, get_store_content)
from tests.gui.steps.oneprovider.data_tab import assert_browser_in_tab_in_op
from tests.gui.steps.modals.modal import wt_wait_for_modal_to_appear
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.bdd_utils import wt, parsers
from tests.utils.path_utils import append_log_to_file
from tests.utils.utils import repeat_failed


def write_audit_logs_for_task_to_file(task, modals, driver, clipboard, path,
                                      displays, browser_id, exp_status):
    task.drag_handle.click()
    # wait for task to open
    time.sleep(1)
    if not check_if_task_is_opened(task):
        task.drag_handle.click()
    if task.status == exp_status:
        modal, logs = get_modal_and_logs_for_task(
            path, task, modals, driver)
        for log in logs:
            if log.severity != 'Info':
                get_audit_log_json_and_write_to_file(log, modal, clipboard,
                                                     displays, browser_id, path)
                modal.close_details()
                append_log_to_file(path, '\n')

        close_modal_and_task(modal, task)


def get_audit_logs_from_every_task_in_workflow(lanes, modals, driver, clipboard,
                                               path, displays, browser_id,
                                               exp_status):
    for lane in lanes:
        for parallel_box in lane.parallel_boxes:
            for task in parallel_box.task_list:
                write_audit_logs_for_task_to_file(task, modals, driver,
                                                  clipboard, path,
                                                  displays, browser_id,
                                                  exp_status)


@wt(parsers.parse('if workflow status is "{exp_status}" {user} of {browser_id}'
                  ' saves audit logs for all tasks to logs'))
def save_audit_logs_to_logs(selenium, browser_id, op_container, exp_status,
                            modals, clipboard, displays):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    act_status = get_status_from_workflow_visualizer(page)
    driver = selenium[browser_id]
    if act_status == exp_status:
        lanes = page.workflow_visualiser.workflow_lanes
        path = GUI_LOGDIR + '/audit_logs.txt'
        get_audit_logs_from_every_task_in_workflow(
            lanes, modals, driver, clipboard, path, displays, browser_id,
            exp_status)


@wt(parsers.parse('user of {browser_id} sees file_id, checksum and algorithm '
                  'information in audit log in "{store_name}" store details'))
def assert_audit_log_in_store(browser_id, selenium, op_container, store_name,
                              modals, clipboard, displays, tmp_memory):

    driver = selenium[browser_id]
    store_type = 'object'
    store_details = get_store_details_json(op_container, driver, browser_id,
                                           modals, clipboard, displays,
                                           store_name,  store_type)

    err_msg = (f'There is no information about algorithm, checksum or file id '
               f'in audit log in {store_name} store details')
    assert (store_details['algorithm'] and store_details['checksum']
            and store_details['fileId']), err_msg

    tmp_memory[f'{store_name}_store_log'] = store_details


@wt(parsers.parse('user of {browser_id} sees destination path, size and '
                  'source URL information in audit log in "{store_name}" store'
                  ' details and they are as follow:\n{content}'))
def assert_content_in_audit_log_in_store(browser_id, selenium, op_container,
                                         store_name, modals, clipboard,
                                         displays, content):
    driver = selenium[browser_id]
    store_type = 'object'
    expected_data = yaml.load(content)
    store_details = get_store_details_json(op_container, driver, browser_id,
                                           modals, clipboard, displays,
                                           store_name,  store_type)

    err_msg1 = (f'There is no information about destination path, size or '
                f'source URL in audit log in {store_name} store details')
    assert (store_details['destinationPath'] and store_details['sourceUrl']
            and store_details['size']), err_msg1

    actual_expected = {'sourceUrl': 'source URL', 'size': 'size',
                       'destinationPath': 'destination path'}

    for actual, expected in actual_expected.items():
        actual_elem = (store_details[actual].split(
            '/')[-1] if actual == 'destinationPath' else store_details[actual])
        expected_elem = expected_data[expected]
        err_msg2 = (f'Actual {actual} {actual_elem} is not the same '
                    f'as expected {expected_elem}')
        assert actual_elem == expected_elem, err_msg2


def get_store_audit_log(browser_id, selenium, op_container, store_name, modals,
                        clipboard, displays, tmp_memory, store_key):
    if store_key not in tmp_memory.keys():
        assert_audit_log_in_store(browser_id, selenium, op_container,
                                  store_name, modals, clipboard, displays,
                                  tmp_memory)

    return tmp_memory[store_key]


def compare_audit_log_to_store_log(modals, driver, clipboard, displays,
                                   browser_id, elem_name, elem_type,
                                   store_name, selenium, op_container,
                                   tmp_memory):
    store_key = f'{store_name}_store_log'
    store_audit_log = get_store_audit_log(browser_id, selenium, op_container,
                                          store_name, modals, clipboard,
                                          displays, tmp_memory, store_key)

    modal = modals(driver).audit_log

    modal.user_log.click()
    modal.copy_json()
    audit_log = json.loads(clipboard.paste(display=displays[browser_id]))

    err_msg = (f'Audit logs for {elem_type} "{elem_name}" does not contain '
               f'audit log for {store_name} store')
    assert store_audit_log == audit_log['content'], err_msg


@wt(parsers.parse('user of {browser_id} sees that audit log in task '
                  '"{task_name}" in {ordinal} parallel box in lane '
                  '"{lane_name}" contains same entries like audit log in'
                  ' "{store_name}" store details'))
def assert_task_audit_log_is_like_store_audit_log(
        selenium, browser_id, op_container, lane_name, task_name, ordinal,
        modals, clipboard, displays, tmp_memory, store_name):
    elem_type = 'task'
    driver = selenium[browser_id]
    number = from_ordinal_number_to_int(ordinal) - 1
    page = switch_to_automation_page(selenium, browser_id, op_container)

    task = page.workflow_visualiser.workflow_lanes[
        lane_name].parallel_boxes[number].task_list[task_name]

    click_on_task_audit_log(task)
    # wait a moment for audit log modal to appear
    time.sleep(1)

    compare_audit_log_to_store_log(modals, driver, clipboard, displays,
                                   browser_id, task_name, elem_type,
                                   store_name, selenium,
                                   op_container, tmp_memory)
    modal = modals(driver).audit_log
    close_modal_and_task(modal, task)


@wt(parsers.parse('user of {browser_id} sees that audit log for "{workflow}"'
                  ' workflow contains the same entries like audit log in'
                  ' "{store_name}" store details'))
def assert_workflow_audit_log_contains_store_audit_log_info(
        selenium, browser_id, op_container, modals, store_name, clipboard,
        displays, tmp_memory, workflow):
    elem_type = 'workflow'
    page = switch_to_automation_page(selenium, browser_id, op_container)
    page.workflow_visualiser.audit_log()
    driver = selenium[browser_id]

    compare_audit_log_to_store_log(modals, driver, clipboard, displays,
                                   browser_id, workflow, elem_type, store_name,
                                   selenium, op_container, tmp_memory)
    modals(driver).audit_log.x()


@wt(parsers.parse('user of {browser_id} sees that number of elements in the '
                  'content of the "{store_name}" store details modal'
                  ' is {number}'))
def assert_number_of_elements_in_store_details(selenium, browser_id, modals,
                                               store_name, op_container,
                                               number):
    modal = open_store_details_modal(selenium, browser_id, op_container,
                                     modals, store_name)
    check_number_of_elements_in_store_details_modal(modal, number, store_name)


@wt(parsers.re('user of (?P<browser_id>.*?) sees that each element from list '
               '"(?P<file_list>.*?)" in "(?P<space_name>.*?)" '
               '(?P<option>corresponds to two) instances of the element with '
               '"file_id" in "(?P<store_name>.*?)" store'))
@wt(parsers.re('user of (?P<browser_id>.*?) sees that (each element with |)'
               '"file_id" in "(?P<store_name>.*?)" store details modal '
               '(?P<option>corresponds to id of file from|is id of) '
               '"(?P<file_list>.*?)" in "(?P<space_name>.*?)" space'))
def assert_file_id_in_store_details(browser_id, selenium, op_container,
                                    store_name, modals, clipboard, displays,
                                    tmp_memory, file_list, popups, oz_page,
                                    space_name, option):
    driver = selenium[browser_id]

    page = get_op_workflow_visualizer_page(op_container, driver)
    store_type = 'object'
    files = parse_seq(file_list)

    elem_num = len(modals(driver).store_details.store_content_object)
    storage_file_ids = [
        json.loads(open_modal_and_get_store_content(
            browser_id, driver, page, modals, clipboard, displays, store_name,
            store_type, i))['fileId']
        for i in range(elem_num)]

    file_ids = [get_file_id_from_details_modal(selenium, browser_id, oz_page,
                                               space_name, op_container,
                                               tmp_memory, file, popups, modals,
                                               clipboard, displays)
                for file in files]

    for storage_file_id in storage_file_ids:
        err_msg = (f'"file_id" in "{store_name}" store details modal is not '
                   f'id of "{files}" from "{space_name}" space')

        assert storage_file_id in file_ids, err_msg

    if 'two' in option:
        assert len(storage_file_ids) == 2*len(file_ids), (
            f'Number of elements in "{store_name}" store details modal does not'
            f' match twice number of files given to check id')
    else:
        assert len(storage_file_ids) == len(file_ids), (
            f'Number of elements in "{store_name}" store details modal does not'
            f' match number of files given to check id')


@wt(parsers.parse('user of {browser_id} sees that element in the content of the'
                  ' "{store_name}" store details modal contains following '
                  '{option}:\n{content}'))
@wt(parsers.parse('user of {browser_id} sees that each element in the content '
                  'of the "{store_name}" store details modal contains one of '
                  'following {option}:\n{content}'))
def assert_each_element_contains_some_information(
        browser_id, selenium, store_name, content, op_container, modals,
        clipboard, displays, option):
    driver = selenium[browser_id]
    store_type = 'object'
    expected_data = yaml.load(content)
    actual_data = []
    get_op_workflow_visualizer_page(op_container, driver)
    modal = modals(driver).store_details
    elem_num = len(modal.store_content_object)
    for i in range(elem_num):
        store_content = json.loads(get_store_content(modal, store_type, i,
                                                     clipboard, displays,
                                                     browser_id))
        modal.close_details()
        file_path = (store_content if option == 'file names' else store_content[
            option.split(' ')[0] + option.split(' ')[-1].capitalize()])
        actual_data.append(file_path.split('/')[-1])
    assert len(actual_data) == len(expected_data), (
        f'Actual and expected number of elements in {store_name} differ')
    for elem in actual_data:
        assert elem in expected_data, (
            f'Expected data does not contain {elem} file name in'
            f' {store_name} store details modal')


@wt(parsers.parse('user of {browser_id} sees that each element in the '
                  'content of the "{store_name}" store details modal contains '
                  'following information:\n{content}'))
def assert_each_element_checksum_content_in_store(
        browser_id, selenium, store_name, content, op_container, modals,
        clipboard, displays):
    driver = selenium[browser_id]
    store_type = 'object'
    expected_data = yaml.load(content)
    get_op_workflow_visualizer_page(op_container, driver)
    modal = modals(driver).store_details
    elem_num = len(modal.store_content_object)
    for i in range(elem_num):
        store_content = json.loads(get_store_content(modal, store_type, i,
                                                     clipboard, displays,
                                                     browser_id))
        modal.close_details()
        expected_sha256 = expected_data['checksums']['sha256']['status']
        actual_sha256 = store_content['checksums']['sha256']['status']
        err_msg = (f'expected sha256 status {expected_sha256} does not match '
                   f'actual {actual_sha256} for {i} element in {store_name}'
                   f' details modal')
        assert (expected_sha256 == actual_sha256), err_msg
        expected_md5 = expected_data['checksums']['md5']['status']
        actual_md5 = store_content['checksums']['md5']['status']
        err_msg = (f'expected md5 status {expected_md5} does not match '
                   f'actual {actual_md5} for {i} element in {store_name}'
                   f' details modal')
        assert (expected_md5 == actual_md5), err_msg


def check_visual_in_store_details_modal(modal, variable_type, item_list,
                                        store_name):
    if variable_type == 'booleans':
        item_list = json.loads(item_list)
        compare_booleans_in_store_details_modal(item_list, modal)
    elif variable_type == 'boolean':
        err_msg = (f'{modal.raw_view} in store details modal does not match'
                   f' expected {item_list}')
        assert modal.raw_view == item_list, err_msg
    else:
        item_list = eval(item_list) if variable_type != 'files' else parse_seq(
            item_list)
        for elem in modal.store_content_list:
            if variable_type == 'ranges':
                expected = {'start': int(elem.range_start),
                            'end': int(elem.range_end),
                            'step': int(elem.range_step)}
            elif variable_type == 'range_objects':
                expected = {'start': int(elem.objects_sequence[1].text),
                            'end': int(elem.objects_sequence[0].text),
                            'step': int(elem.objects_sequence[2].text)}
            elif variable_type == 'files':
                expected = elem.path
            elif variable_type == 'strings' or variable_type == 'numbers':
                expected = eval(elem.value)
            else:
                raise Exception(f'this {variable_type} is not handled in this'
                                f' function')

            err_msg = (f'expected {variable_type} {item_list} does not '
                       f'contain {expected} in {store_name} store details'
                       f' modal')
            assert expected in item_list, err_msg


@wt(parsers.re('user of (?P<browser_id>.*?) sees following '
               '(?P<variable_type>.*?) represented by "(?P<item_list>.*?)" in '
               'content in "(?P<store_name>.*?)" store details modal'))
def assert_elements_in_store_details_modal(browser_id, selenium, op_container,
                                           item_list, store_name, modals,
                                           variable_type):
    modal = open_store_details_modal(selenium, browser_id, op_container,
                                     modals, store_name)

    if variable_type == 'string':
        compare_string_in_store_details_modal(item_list, modal, variable_type,
                                              store_name)
    elif variable_type == 'array':
        compare_array_in_store_details_modal(modal, item_list)

    else:
        check_visual_in_store_details_modal(modal, variable_type, item_list,
                                            store_name)


@wt(parsers.parse('user of {browser_id} sees {item_list} datasets in '
                  'Store details modal for "{store_name}" store'))
def assert_datasets_in_store_details(selenium, browser_id, op_container,
                                     modals, store_name, item_list):
    modal = open_store_details_modal(selenium, browser_id, op_container,
                                     modals, store_name)
    compare_datasets_in_store_details_modal(item_list, modal, store_name)
    modal.close()


@wt(parsers.parse('user of {browser_id} sees "{file}" file in '
                  'Store details modal for "{store_name}" store'))
def assert_file_in_store_details(selenium, browser_id, op_container, modals,
                                 store_name, file):
    modal = open_store_details_modal(selenium, browser_id, op_container,
                                     modals, store_name)
    actual_file = modal.single_file_container.name

    err_msg = f'{file} is not in Store details modal for {store_name} store'
    assert file == actual_file, err_msg
    modal.close()


@wt(parsers.parse('user of {browser_id} clicks on "{name}" {option} link in '
                  'Store details modal for "{store_name}" store'))
def click_on_elem_in_store_details_modal(browser_id, selenium, op_container,
                                         name, store_name, modals, option=''):
    modal = open_store_details_modal(selenium, browser_id, op_container,
                                     modals, store_name)
    if option == 'archive':
        modal.store_content_list[name].file_name.click()
    elif option == 'dataset':
        modal.store_content_list[name].dataset_name.click()
    else:
        modal.single_file_container.clickable_name()

    # wait a moment to open a tab
    time.sleep(1)


@repeat_failed(timeout=WAIT_FRONTEND)
def check_if_element_is_selected(tmp_memory, browser_id, name, which_browser):
    err_msg = f'Element {name} is not selected in {which_browser}'
    browser = tmp_memory[browser_id][transform(which_browser)]
    if_selected = browser.data[name].is_selected()
    assert if_selected, err_msg


@wt(parsers.parse('user of {browser_id} sees "{name}" item selected in the'
                  ' {which_browser} opened in new web browser tab'))
def assert_element_selected_in_new_browser_tab(
        browser_id, selenium, op_container, name, tmp_memory, which_browser):
    switch_to_last_tab(selenium, browser_id)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container, tmp_memory,
                                which_browser)
    check_if_element_is_selected(tmp_memory, browser_id, name, which_browser)


def compare_to_expected_if_element_exist_for_store(
        elem, items, option, store_name, selenium, browser_id, oz_page,
        op_container, tmp_memory, popups, modals, clipboard, displays):
    if elem:
        if option == 'fileId':
            file_info = elem.split(' ')[1].replace(')', '').split('/')
            elem = get_file_id_from_details_modal(
                selenium, browser_id, oz_page, file_info[0], op_container,
                tmp_memory, file_info[1], popups, modals, clipboard,
                displays)

        assert elem == items[option], (
            f"{option}: {items[option]} in store {store_name} does not"
            f" match expected {elem}")


@wt(parsers.parse('user of {browser_id} sees that content of "{store_name}"'
                  ' store is:\n{config}'))
def assert_content_of_store(selenium, browser_id, op_container, modals,
                            store_name, config, clipboard, displays, oz_page,
                            tmp_memory, popups):

    options_to_check = ['mimeType', 'formatName', 'isExtensionMatchingFormat',
                        'fileName', 'extensions', 'sourceUrl', 'fileId']
    data = yaml.load(config)
    modal = open_store_details_modal(selenium, browser_id, op_container,
                                     modals, store_name)

    if len(modal.store_content_list) == 0:
        modal.copy_button()
        item = json.loads(clipboard.paste(display=displays[browser_id]))
        err_msg = 'expected value: {} differs from actual one: {}'
        assert data[0] == item, err_msg.format(data[0], item)
    else:
        modal.store_content_list[0].click()
        modal.copy_button()
        items = json.loads(clipboard.paste(display=displays[browser_id]))

        for option in options_to_check:
            elem = data.get(option, False)
            compare_to_expected_if_element_exist_for_store(
                elem, items, option, store_name, selenium, browser_id, oz_page,
                op_container, tmp_memory, popups, modals, clipboard, displays)
    try:
        modal.close()
    except StaleElementReferenceException:
        pass


def compare_to_expected_if_elem_exist_audit_log(data, label, actual_items,
                                                task_name):
    expected = data.get(label, False)
    if expected:
        actual = actual_items[label]
        if label == 'timestamp':
            expected = date.today()
            actual = date.fromtimestamp(actual_items['timestamp'] / 1000)
        expected = expected.lower() if label == 'severity' else expected
        assert_elements_of_task_audit_log_are_the_same(expected, actual, label,
                                                       task_name)


def assert_elements_of_task_audit_log_are_the_same(expected, actual, label,
                                                   task_name):
    assert expected == actual, (
        f'{label} "{actual}" in audit log for "{task_name}" task is '
        f'not "{expected}" as expected')


def compare_content_reason_of_task_audit_log(
        reason, actual_reason, selenium, browser_id, oz_page, op_container,
        tmp_memory, popups, modals, clipboard, displays, task_name):
    err_msg = (f'Reason: "{reason}" in audit log for "{task_name}" '
               f'task does not contain "{actual_reason}" as expected')
    if 'contains' in reason:
        reason_data = yaml.load(
            reason.split('contains ')[1].replace('])', ']'))
        for reason_elem in reason_data:
            assert reason_elem in actual_reason, err_msg
    elif 'file checksum' in reason:
        assert reason == actual_reason.replace(':', ''), err_msg
    else:
        if not isinstance(reason, str):
            placeholder_file_id = reason['details'][
                'specificError']['details']['value']['fileId']
            placeholder_file_id = placeholder_file_id.split(
                ' ')[1].replace(')', '').split('/')
            reason['details']['specificError']['details']['value'][
                'fileId'] = get_file_id_from_details_modal(
                selenium, browser_id, oz_page, placeholder_file_id[0],
                op_container, tmp_memory, placeholder_file_id[1],
                popups, modals, clipboard, displays)
        assert_elements_of_task_audit_log_are_the_same(reason, actual_reason,
                                                       'Reason', task_name)


def compare_content_of_task_audit_log(
        content, actual_content, task_name, selenium, browser_id, oz_page,
        op_container, tmp_memory, popups, modals, clipboard, displays):
    expected_identical = ['status', 'fetchFileName', 'description']
    actual_details = actual_content.get('details', False)
    details = content.get('details', False)
    reason = details.get('reason', False) if details else False
    item = details.get('item', False) if details else False

    for label in expected_identical:
        compare_to_expected_if_elem_exist_audit_log(content, label,
                                                    actual_content, task_name)
    if reason:
        compare_content_reason_of_task_audit_log(
            reason, actual_details['reason'], selenium, browser_id,
            oz_page, op_container, tmp_memory, popups, modals, clipboard,
            displays, task_name)
    if item:
        file_id = item['fileId'].split(' ')[1].replace(
            ')', '').split('/')
        item['fileId'] = get_file_id_from_details_modal(
            selenium, browser_id, oz_page, file_id[0],
            op_container, tmp_memory, file_id[1], popups, modals,
            clipboard, displays)
        assert_elements_of_task_audit_log_are_the_same(
            item, actual_details['item']['value'], 'Item', task_name)


@wt(parsers.parse('user of {browser_id} sees that audit log in task '
                  '"{task_name}" in {ordinal} parallel box in lane '
                  '"{lane_name}" doesn\'t contain user\'s entry'))
def assert_content_of_user_task_audit_log(selenium, browser_id, op_container,
                                          lane_name, task_name, ordinal, modals):
    click = 'click'
    close = 'closes'
    link = 'Audit log'
    driver = selenium[browser_id]

    click_on_task_in_lane(selenium, browser_id, op_container, lane_name,
                          task_name, ordinal, click)
    click_on_link_in_task_box(selenium, browser_id, op_container, lane_name,
                              task_name, link, ordinal)
    # wait a moment for modal to open
    time.sleep(1)
    modal = modals(driver).audit_log
    try:
        modal.user_log
        raise Exception(f'Audit log in task "{task_name}" in lane'
                        f' "{lane_name}" contains user\'s entry')
    except RuntimeError:
        pass
    modal.x()
    click_on_task_in_lane(selenium, browser_id, op_container, lane_name,
                          task_name, ordinal, close)


@wt(parsers.parse('user of {browser_id} sees expected exception for '
                  '{file_name} in "{element}" content of audit log in task '
                  '"{task_name}" in {ordinal} parallel box '
                  'in lane "{lane_name}"'))
def assert_exception_in_element_content_in_task_audit_log(
        file_name, element, selenium, browser_id, op_container, lane_name,
        task_name, ordinal, modals, clipboard, displays, tmp_memory):
    file_name = file_name.replace('"', '')
    expected_data = tmp_memory['exceptions'][file_name]
    expected_data = list(map(lambda x: x.lower(), expected_data))
    assert_element_content_in_task_audit_log(
        expected_data, element, selenium, browser_id, op_container,
        lane_name, task_name, ordinal, modals, clipboard, displays)


@wt(parsers.parse('user of {browser_id} sees that "{element}" content of audit'
                  ' log in task "{task_name}" in {ordinal} parallel box in lane'
                  ' "{lane_name}" is {expected_data}'))
def assert_element_content_in_task_audit_log(
        expected_data, element, selenium, browser_id, op_container, lane_name,
        task_name, ordinal, modals, clipboard, displays):
    click = 'click'
    link = 'Audit log'
    close = 'closes'
    if isinstance(expected_data, list):
        expected_data = list(map(lambda x: x.replace('"', ''), expected_data))
        expected_data = list(map(lambda x: x.replace("\\n", "\n"), expected_data))
    else:
        expected_data = expected_data.replace('"', '')
        expected_data = expected_data.replace("\\n", "\n")
    driver = selenium[browser_id]
    click_on_task_in_lane(selenium, browser_id, op_container, lane_name,
                          task_name, ordinal, click)
    click_on_link_in_task_box(selenium, browser_id, op_container, lane_name,
                              task_name, link, ordinal)
    # wait a moment for modal to open
    time.sleep(1)
    modal = modals(driver).audit_log
    modal.user_log.click()
    modal.copy_json()
    actual_items = json.loads(clipboard.paste(display=displays[browser_id]))
    actual_data = actual_items['content'][element]
    # this is done because of very specific problem with passing (data/)
    # as expected_data
    actual_data = actual_data.replace("(data/) ", "")
    actual_data = actual_data.lower()
    if isinstance(expected_data, list):
        err_msg = (
            f'actual {element} content for task:\n "{actual_data}"\n is not '
            f'in expected cases:\n "{expected_data}"')
        assert actual_data in expected_data, err_msg
    else:
        err_msg = (
            f'actual {element} content for task:\n "{actual_data}"\n is not '
            f'as expected:\n "{expected_data}"')
        assert actual_data == expected_data, err_msg
    modal.x()
    click_on_task_in_lane(selenium, browser_id, op_container, lane_name,
                          task_name, ordinal, close)


@wt(parsers.parse('user of {browser_id} sees that audit log in task'
                  ' "{task_name}" in {ordinal} parallel box in lane '
                  '"{lane_name}" contains following entry:\n{config}'))
def assert_content_of_task_audit_log(config, selenium, browser_id,
                                     op_container, lane_name, task_name,
                                     ordinal, modals, clipboard, displays,
                                     popups, tmp_memory, oz_page):
    expected_identical = ['source', 'severity', 'timestamp']
    click = 'click'
    link = 'Audit log'
    driver = selenium[browser_id]
    data = yaml.load(config)
    content = data.get('content', False)
    severity = data.get('severity', False)
    source = data.get('source', False)
    close = 'closes'
    # wait a second for workflow to open
    time.sleep(1)
    click_on_task_in_lane(selenium, browser_id, op_container, lane_name,
                          task_name, ordinal, click)
    click_on_link_in_task_box(selenium, browser_id, op_container, lane_name,
                              task_name, link, ordinal)
    # wait a moment for modal to open
    time.sleep(1)
    modal = modals(driver).audit_log
    if severity == 'Error' or severity == 'Debug':
        modal.logs_entry[severity].click()
    elif source == 'user':
        modal.user_log.click()
    else:
        modal.logs_entry[0].click()
    modal.copy_json()
    actual_items = json.loads(clipboard.paste(display=displays[browser_id]))

    for label in expected_identical:
        compare_to_expected_if_elem_exist_audit_log(data, label, actual_items,
                                                    task_name)

    if content:
        compare_content_of_task_audit_log(
            content, actual_items['content'], task_name, selenium,
            browser_id, oz_page, op_container, tmp_memory, popups, modals,
            clipboard, displays)

    try:
        modal.x()
        click_on_task_in_lane(selenium, browser_id, op_container, lane_name,
                              task_name, ordinal, close)
    except StaleElementReferenceException:
        pass


@wt(parsers.parse('user of {browser_id} sees that recent downloaded json '
                  'file contains audit log which has the same entries as the '
                  'workflow audit log in GUI'))
def assert_log_entries_in_json_same_as_visible_in_workflow_audit_log(
        browser_id, tmpdir, modals, selenium, clipboard, displays):
    driver = selenium[browser_id]
    modal = modals(driver).audit_log
    path = tmpdir.join(browser_id, 'download')
    file_name = os.listdir(path)[-1]
    file_path = tmpdir.join(browser_id, 'download', file_name)
    if file_path.isfile():
        with open(file_path) as f:
            data = json.load(f)
            log_entries = len(modal.logs_entry)
            err_msg = (f'there is different number of log entries in file '
                       f'{len(data)} and visible {log_entries}')
            assert len(data) == log_entries, err_msg
            for i in range(log_entries):
                file_log = data[i]
                idx = log_entries - i - 1
                modal.logs_entry[idx].click()
                modal.copy_json()
                visible_log = json.loads(
                    clipboard.paste(display=displays[browser_id]))
                # remove 'source' from dict
                visible_log.pop('source')
                err_msg = (f'logs in file: {file_log} and visible {visible_log}'
                           f'are different')
                assert file_log == visible_log, err_msg
                modal.close_details.click()
    else:
        raise RuntimeError('file {} has not been downloaded'.format(file_name))


@wt(parsers.parse('user of {browser_id} sees that workflow audit log contains '
                  'following system debug entries with description:\n{config}'))
def assert_workflow_audit_log_contains_entries(selenium, browser_id, modals,
                                               tmpdir, tmp_memory, config):
    _assert_workflow_audit_log_contains_entries(selenium, browser_id, modals,
                                                tmpdir, tmp_memory, config)


def _assert_workflow_audit_log_contains_entries(
        selenium, browser_id, modals, tmpdir, tmp_memory, config):
    data = yaml.load(config)
    driver = selenium[browser_id]
    modal = modals(driver).audit_log
    file_path = _get_workflow_audit_log(browser_id, selenium, tmp_memory,
                                        modals, tmpdir)

    f = open(file_path)
    data_file = json.load(f)
    for expected_entry in data:
        if assert_expected_in_entries(expected_entry, data_file):
            continue
        err_msg = f'there is no entry {expected_entry} in workflow audit log'
        raise RuntimeError(err_msg)
    modal.x()


def assert_expected_in_entries(expected_entry, entries):
    for actual_entry in entries:
        if compare_audit_log_debug_entries(actual_entry, expected_entry):
            return True
    return False


def compare_audit_log_debug_entries(actual_entry, expected_entry):
    return expected_entry in actual_entry['content']['description'] and (
            actual_entry['severity'] == 'debug')


@wt(parsers.parse('user of {browser_id} sees that workflow audit log contains '
                  'entry with info only about file attributes {item_list}'))
def assert_workflow_audit_log_contains_entry(
        selenium, browser_id, modals, tmpdir, tmp_memory, item_list):
    file_path = _get_workflow_audit_log(browser_id, selenium, tmp_memory,
                                        modals, tmpdir)
    f = open(file_path)
    data_file = json.load(f)
    item_list = parse_seq(item_list)
    for entry in data_file:
        try:
            content = entry['content']
            if _assert_all_items_in_json(item_list, content) and (
                    len(item_list) == len(content)):
                return True
        except KeyError:
            pass
    err_msg = (f'there is no entry containing data about {item_list} '
               f'in workflow audit log')
    raise RuntimeError(err_msg)


def _assert_all_items_in_json(item_list, data):
    for item in item_list:
        if not data.get(item, False):
            return False
    return True


@wt(parsers.parse('user of {browser_id} sees that workflow audit log does '
                  'not contain any system debug entry'))
def assert_no_debug_entry_in_workflow_audit_log(browser_id, selenium,
                                                tmp_memory, modals, tmpdir):
    file_path = _get_workflow_audit_log(browser_id, selenium, tmp_memory,
                                        modals, tmpdir)
    with open(file_path) as f:
        data_file = json.load(f)
        err_msg = 'workflow audit log contains debug entry'
        assert not any(filter(lambda x: x.get('severity', None) == 'debug',
                              data_file)), err_msg


def _get_workflow_audit_log(browser_id, selenium, tmp_memory, modals, tmpdir):
    driver = selenium[browser_id]
    modal_name = 'Workflow audit log'
    # wait for modal to appear
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    modal = modals(driver).audit_log
    modal.download_as_json()
    # wait a while for file to download
    time.sleep(0.5)
    path = tmpdir.join(browser_id, 'download')
    file_path = os.listdir(path)[-1]
    file_path = tmpdir.join(browser_id, 'download', file_path)
    return file_path
