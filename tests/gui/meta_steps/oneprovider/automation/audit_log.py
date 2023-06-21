"""This module contains meta steps for operations on automation page checking
audit logs in Oneprovider using web GUI
"""
__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import json
import time
from datetime import date

import yaml
from selenium.common.exceptions import StaleElementReferenceException

from tests import GUI_LOGDIR
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
    compare_string_in_store_details_modal, compare_array_in_store_details_modal)
from tests.gui.steps.oneprovider.data_tab import assert_browser_in_tab_in_op
from tests.gui.utils.generic import parse_seq
from tests.utils.bdd_utils import wt, parsers
from tests.utils.path_utils import append_log_to_file


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
            and store_details['file_id']), err_msg

    tmp_memory[f'{store_name}_store_log'] = store_details


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


@wt(parsers.parse('user of {browser_id} sees that audit logs in task '
                  '"{task_name}" in {ordinal} parallel box in lane '
                  '"{lane_name}" contains same information like audit log in'
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


@wt(parsers.parse('user of {browser_id} sees that audit logs for "{workflow}"'
                  ' workflow contains the same information like audit log in'
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


@wt(parsers.parse('user of {browser_id} sees that number of elements in '
                  'content in "{store_name}" store details modal is {number}'))
def assert_number_of_elements_in_store_details(selenium, browser_id, modals,
                                               store_name, op_container,
                                               number):
    modal = open_store_details_modal(selenium, browser_id, op_container,
                                     modals, store_name)
    actual_number = len(modal.store_content_object)
    err_msg = (f'Expected number of elements {number} is not equal to actual '
               f'number {actual_number} in "{store_name}" store details modal')

    assert actual_number == int(number), err_msg


@wt(parsers.re('user of (?P<browser_id>.*?) sees that each element from list '
               '"(?P<file_list>.*?)" in "(?P<space_name>.*?)" space '
               '(?P<option>corresponds to two) instances of the element with '
               '"file_id" in "(?P<store_name>.*?)" store details modal'))
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
            store_type, i))['file_id']
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


@wt(parsers.parse('user of {browser_id} sees "{item_list}" datasets in '
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


@wt(parsers.parse('user of {browser_id} sees {browser} after clicking '
                  '"{name}" in Store details modal for "{store_name}"'
                  ' store'))
def assert_browser_after_clicking_on_item_in_details_modal(
        browser_id, selenium, op_container, name, store_name, modals,
        tmp_memory, browser):
    modal = open_store_details_modal(selenium, browser_id, op_container,
                                     modals, store_name)
    if 'file' in browser:
        modal.single_file_container.clickable_name()
    else:
        modal.store_content_list[name].dataset_name.click()
    switch_to_last_tab(selenium, browser_id)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container, tmp_memory,
                                browser)


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
    if 'contains' in reason:
        reason_data = yaml.load(
            reason.split('contains ')[1].replace('])', ']'))
        for reason_elem in reason_data:
            assert reason_elem in actual_reason, (
                f'Reason: "{reason}" in audit log for "{task_name}" '
                f'task does not contain "{actual_reason}" as expected')
    else:
        if not isinstance(reason, str):
            placeholder_file_id = reason['details'][
                'specificError']['details']['value']['file_id']
            placeholder_file_id = placeholder_file_id.split(
                ' ')[1].replace(')', '').split('/')
            reason['details']['specificError']['details']['value'][
                'file_id'] = get_file_id_from_details_modal(
                selenium, browser_id, oz_page, placeholder_file_id[0],
                op_container, tmp_memory, placeholder_file_id[1],
                popups, modals, clipboard, displays)
        assert_elements_of_task_audit_log_are_the_same(reason, actual_reason,
                                                       'Reason', task_name)


def compare_content_of_task_audit_log(
        content, actual_content, task_name, selenium, browser_id, oz_page,
        op_container, tmp_memory, popups, modals, clipboard, displays):
    expected_identical = ['status', 'fetchFileName', 'description']
    reason = content.get('reason', False)
    item = content.get('item', False)

    for label in expected_identical:
        compare_to_expected_if_elem_exist_audit_log(content, label,
                                                    actual_content, task_name)
    if reason:
        compare_content_reason_of_task_audit_log(
            reason, actual_content['reason'], selenium, browser_id,
            oz_page, op_container, tmp_memory, popups, modals, clipboard,
            displays, task_name)
    if item:
        file_id = item['file_id'].split(' ')[1].replace(
            ')', '').split('/')
        item['file_id'] = get_file_id_from_details_modal(
            selenium, browser_id, oz_page, file_id[0],
            op_container, tmp_memory, file_id[1], popups, modals,
            clipboard, displays)
        assert_elements_of_task_audit_log_are_the_same(
            item, actual_content['item'], 'Item', task_name)


@wt(parsers.parse('user of {browser_id} sees that audit logs in task'
                  ' "{task_name}" in {ordinal} parallel box in lane '
                  '"{lane_name}" contains following information:\n{config}'))
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

    click_on_task_in_lane(selenium, browser_id, op_container, lane_name,
                          task_name, ordinal, click)
    click_on_link_in_task_box(selenium, browser_id, op_container, lane_name,
                              task_name, link, ordinal)
    # wait a moment for modal to open
    time.sleep(1)
    modal = modals(driver).audit_log
    modal.logs_entry[0].click()
    modal.copy_json()
    actual_items = json.loads(clipboard.paste(display=displays[browser_id]))

    for label in expected_identical:
        compare_to_expected_if_elem_exist_audit_log(data, label, actual_items,
                                                    task_name)

    if content:
        compare_content_of_task_audit_log(
            content, actual_items['content'], task_name, selenium, browser_id,
            oz_page, op_container, tmp_memory, popups, modals, clipboard,
            displays)

    try:
        modal.x()
    except StaleElementReferenceException:
        pass
