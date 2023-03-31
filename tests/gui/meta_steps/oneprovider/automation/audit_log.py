"""This module contains meta steps for operations on automation page checking
audit logs in Oneprovider using web GUI
"""
__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import json
import time

from tests import GUI_LOGDIR
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.meta_steps.oneprovider.automation.run_workflow import (
    get_store_content)
from tests.gui.meta_steps.oneprovider.data import get_file_id_from_details_modal
from tests.gui.steps.oneprovider.archives import from_ordinal_number_to_int
from tests.gui.steps.oneprovider.automation.automation_basic import (
    check_if_task_is_opened, switch_to_automation_page)
from tests.gui.steps.oneprovider.automation.workflow_results_modals import (
    get_modal_and_logs_for_task, get_audit_log_json_and_write_to_file,
    close_modal_and_task, click_on_task_audit_log)
from tests.gui.utils.generic import parse_seq
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_FRONTEND)
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
    act_status = page.workflow_visualiser.status
    driver = selenium[browser_id]
    if act_status == exp_status:
        lanes = page.workflow_visualiser.workflow_lanes
        path = GUI_LOGDIR + '/audit_logs.txt'
        get_audit_logs_from_every_task_in_workflow(
            lanes, modals, driver, clipboard, path, displays, browser_id,
            exp_status)


@wt(parsers.parse('user of {browser_id} sees file_id, checksum and algorithm '
                  'information in audit log in "{store_name}" store details'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_audit_log_in_store(browser_id, selenium, op_container, store_name,
                              modals, clipboard, displays, tmp_memory):

    driver = selenium[browser_id]
    store_type = 'object'

    page = op_container(driver).automation_page.workflow_visualiser
    store_details = json.loads(get_store_content(
        browser_id, driver, page, modals, clipboard, displays, store_name,
        store_type))

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
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_number_of_elements_in_store_details(selenium, browser_id, modals,
                                               store_name, op_container,
                                               number):
    driver = selenium[browser_id]
    page = op_container(driver).automation_page.workflow_visualiser
    page.stores_list[store_name].click()
    modal = modals(driver).store_details
    time.sleep(0.25)
    actual_number = len(modal.store_content_object)
    err_msg = (f'Expected number of elements {number} is not equal to actual '
               f'number {actual_number} in "{store_name}" store details modal')

    assert actual_number == int(number), err_msg


@wt(parsers.re('user of (?P<browser_id>.*?) sees that (each element with |)'
               '"file_id" in "(?P<store_name>.*?)" store details modal '
               '(corresponds to id of file from|is id of) "(?P<file_list>.*?)"'
               ' in "(?P<space_name>.*?)" space'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_file_id_in_store_details(browser_id, selenium, op_container,
                                    store_name, modals, clipboard, displays,
                                    tmp_memory, file_list, popups, oz_page,
                                    space_name):

    driver = selenium[browser_id]

    page = op_container(driver).automation_page.workflow_visualiser
    store_type = 'object'
    files = parse_seq(file_list)

    elem_num = len(modals(driver).store_details.store_content_object)
    storage_file_ids = [
        json.loads(get_store_content(browser_id, driver, page, modals,
                                     clipboard, displays, store_name,
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

    assert len(storage_file_ids) == len(file_ids), (
        f'Number of elements in "{store_name}" store details modal does not'
        f' match number of files given to check id')








