"""This module contains meta steps for operations on automation page in Onezone
using web GUI
"""
__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import yaml
import json

from tests import GUI_LOGDIR
from tests.gui.meta_steps.oneprovider.automation import (
    choose_file_as_initial_workflow_value,
    wait_for_workflows_in_automation_subpage)
from tests.gui.steps.modals.modal import (
    _wait_for_modal_to_appear, click_modal_button,
    write_name_into_text_field_in_modal, switch_toggle_in_modal,
    choose_option_in_dropdown_menu_in_modal)
from tests.gui.steps.oneprovider.automation import (
    click_button_in_navigation_tab, choose_workflow_revision_to_run,
    confirm_workflow_to_execute, expand_first_executed_workflow_record,
    switch_to_automation_page, check_if_task_is_opened)
from tests.gui.steps.onezone.automation import *
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.onezone.spaces import (
    click_on_option_in_the_sidebar, click_element_on_lists_on_left_sidebar_menu,
    click_on_option_of_space_on_left_sidebar_menu)
from tests.gui.utils.core import scroll_to_css_selector
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} creates workflow "{workflow_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_workflow_using_gui(selenium, browser_id, oz_page, workflow_name):
    click_add_new_button_in_menu_bar(selenium, browser_id,
                                     oz_page, 'Add new workflow')
    write_text_into_workflow_name_on_main_workflows_page(selenium, browser_id,
                                                         oz_page, workflow_name)

    confirm_workflow_creation(selenium, browser_id, oz_page)


@wt(parsers.parse('user of {browser_id} uploads "{workflow}" workflow from '
                  '"{file_name}" file to "{inventory}" inventory'))
def upload_and_assert_workflow_to_inventory_using_gui(selenium, browser_id,
                                                      oz_page, modals,
                                                      inventory, workflow,
                                                      file_name, tmp_memory):
    driver = selenium[browser_id]
    click_on_option_in_the_sidebar(selenium, browser_id, 'Automation', oz_page)
    go_to_inventory_subpage(selenium, browser_id, inventory,
                            'workflows', oz_page)
    upload_workflow_as_json(selenium, browser_id, file_name, oz_page)
    _wait_for_modal_to_appear(driver, browser_id, 'Upload workflow', tmp_memory)
    click_modal_button(selenium, browser_id, 'Apply', 'Upload workflow', modals)
    go_to_inventory_subpage(selenium, browser_id, inventory,
                            'workflows', oz_page)

    assert_workflow_exists(selenium, browser_id, oz_page, workflow, 'sees')


@wt(parsers.parse('user of {browser_id} creates lambda with following '
                  'configuration:\n{config}'))
def create_lambda_manually(browser_id, config, selenium, oz_page, popups):

    """Create lambda according to given config.

        Config format given in yaml is as follow:
            name: lambda_name
            docker image: docker image
            mount space: True/False                 ---> optional
            read-only: True/False                   ---> optional
            arguments:
              - name: argument_name
                type: argument_type
              - name: 2nd_argument_name             ---> optional
                type: 2nd_argument_type
            results:                                ---> optional
              - name: result_name
                type: result_type


        Example configuration:

            name: "checksum-counting-oneclient"
            docker image: "docker.onedata.org/checksum-counting-oneclient:v8"
            read-only: False
            arguments:
              - name: "file"
                type: File
              - name: "metadata_key"
                type: String
              - name: "algorithm"
                type: String
            results:
              - name: "result"
                type: Object
    """
    _create_lambda_manually(browser_id, config, selenium, oz_page, popups)


def _create_lambda_manually(browser_id, config, selenium, oz_page, popups):

    button = 'Add new lambda'
    name_field = 'lambda name'
    docker_field = 'docker image'
    read_only_toggle = 'Read only'
    mount_space_toggle = 'Mount space'
    argument_option = 'argument'
    conf_param_option = 'configuration parameters'
    result_option = 'result'
    option = 'lambda'

    data = yaml.load(config)
    name = data['name']
    docker_image = data['docker image']
    read_only = data.get('read-only', True)
    mount_space = data.get('mount space', True)
    arguments = data.get('arguments', False)
    results = data.get('results', False)
    configuration_parameters = data.get('configuration parameters', False)

    read_only_option = 'checks' if read_only else 'unchecks'
    mount_space_option = 'checks' if mount_space else 'unchecks'

    click_add_new_button_in_menu_bar(selenium, browser_id, oz_page, button)
    write_text_into_lambda_form(selenium, browser_id, oz_page, name, name_field)
    write_text_into_lambda_form(selenium, browser_id, oz_page, docker_image,
                                docker_field)
    switch_toggle_in_lambda_form(selenium, browser_id, oz_page,
                                 read_only_option, read_only_toggle)
    switch_toggle_in_lambda_form(selenium, browser_id, oz_page,
                                 mount_space_option, mount_space_toggle)

    def ordinal(n):
        return "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n
                                       % 10::4])

    if configuration_parameters:
        for i, config_param in enumerate(configuration_parameters):
            add_parameter_into_lambda_form(
                selenium, browser_id, oz_page, popups, conf_param_option,
                config_param['name'], config_param['type'], ordinal(i + 1))


    if arguments:
        for i, args in enumerate(arguments):
            add_parameter_into_lambda_form(
                selenium, browser_id, oz_page, popups, argument_option,
                args['name'], args['type'], ordinal(i+1))

    if results:
        for i, res in enumerate(results):
            add_parameter_into_lambda_form(
                selenium, browser_id, oz_page, popups, result_option,
                res['name'], res['type'], ordinal(i+1))

    confirm_lambda_creation_or_edition(selenium, browser_id, oz_page, option)


@wt(parsers.re('user of (?P<browser_id>.*) creates (input|output) store for '
               'workflow "(?P<workflow>.*)" with following configuration:'
               r'\n(?P<config>(.|\s)*)'))
def create_store_for_workflow(browser_id, config, selenium, oz_page, modals,
                              popups):
    """Create store according to given config.

        Config format given in yaml is as follow:
            name: store_name
            type dropdown: type                     ---> optional
            data type dropdown: data_type
            user input: True/False                  ---> optional

        Example configuration:

            name: "output"
            type dropdown: List
            data type dropdown: Object
    """
    _create_store_for_workflow(browser_id, config, selenium, oz_page, modals,
                               popups)


def _create_store_for_workflow(browser_id, config, selenium, oz_page, modals,
                               popups):
    data = yaml.load(config)
    name = data['name']

    type_dropdown = data['type dropdown']
    data_type_dropdown = data['data type dropdown']
    user_input = data.get('user input', False)

    name_textfield = 'store name'
    modal_name = 'Create new store'
    type_dropdown_menu = 'type dropdown menu'
    data_type_dropdown_menu = 'data type dropdown menu'
    toggle_name = 'User input'
    option = 'checks' if user_input else 'unchecks'
    button = 'Create'

    click_add_store_button(selenium, browser_id, oz_page)
    write_name_into_text_field_in_modal(selenium, browser_id, name, modal_name,
                                        modals, name_textfield)
    choose_option_in_dropdown_menu_in_modal(selenium, browser_id, modals,
                                            type_dropdown_menu, popups,
                                            type_dropdown, modal_name)
    choose_option_in_dropdown_menu_in_modal(selenium, browser_id, modals,
                                            data_type_dropdown_menu, popups,
                                            data_type_dropdown, modal_name)
    switch_toggle_in_modal(selenium, browser_id, modals, toggle_name,
                           option, modal_name)
    click_modal_button(selenium, browser_id, button, modal_name, modals)


@wt(parsers.re('user of (?P<browser_id>.*) creates (?P<which>|another )task '
               'using (?P<ordinal>1st|2nd|3rd|4th) revision of '
               '"(?P<lambda_name>.*)" lambda in "(?P<lane_name>.*)" lane with '
               r'following configuration:\n(?P<config>(.|\s)*)'))
def create_task_using_previously_created_lambda(browser_id, config, selenium,
                                                oz_page, lane_name,
                                                lambda_name, ordinal, popups,
                                                which):

    """Create task using lambda according to given config.

        Config format given in yaml is as follow:
        where parallel box: "below"/"above"         ---> optional
        task name: task_name                        ---> optional
        arguments:                                  ---> optional
            task_arguments
        results:                                    ---> optional
            task_results


        Example configuration:

            where parallel box: "below"
            task name: "Second lambda task"
            arguments:
                file:
                  value builder: "Iterated item"
                metadata_key:
                  value builder: "Constant value"
                  value: "sha256_key"
                algorithm:
                  value builder: "Constant value"
                  value: "sha256"
            results:
                result:
                  target store: "output-store"
    """

    _create_task_using_previously_created_lambda(browser_id, config, selenium,
                                                 oz_page, lane_name,
                                                 lambda_name, ordinal, popups,
                                                 which)


def _create_task_using_previously_created_lambda(browser_id, config, selenium,
                                                 oz_page, lane_name,
                                                 lambda_name, ordinal, popups,
                                                 which):
    arg_type = 'argument'
    res_type = 'result'
    conf_param_option = 'configuration parameters'
    option = 'task'
    data = yaml.load(config)
    arguments = data.get('arguments', False)
    results = data.get('results', False)
    task_name = data.get('task name', False)
    configuration_parameters = data.get('configuration parameters', False)

    if 'another' in which:
        position = data['where parallel box']
        add_another_parallel_box_to_lane(selenium, browser_id, oz_page,
                                         lane_name, position)
    else:
        add_parallel_box_to_lane(selenium, browser_id, oz_page, lane_name)

    add_task_to_empty_parallel_box(selenium, browser_id, oz_page, lane_name)
    add_lambda_revision_to_workflow(selenium, browser_id, oz_page, lambda_name,
                                    ordinal)

    if task_name:
        write_task_name_in_task_edition_text_field(selenium, browser_id,
                                                   oz_page, task_name)

    if configuration_parameters:
        for param_name, param in configuration_parameters.items():
            choose_option_in_dropdown_menu_in_task_page(
                selenium, browser_id, oz_page, popups, param['value builder'],
                param_name, conf_param_option)
            write_text_into_editor_bracket(selenium, browser_id, oz_page,
                                           param['value'], param_name,
                                           conf_param_option)

    if arguments:
        for arg_name, arg in arguments.items():
            choose_option_in_dropdown_menu_in_task_page(
                selenium, browser_id, oz_page, popups, arg['value builder'],
                arg_name, arg_type)
            if 'value' in arg:
                write_text_into_editor_bracket(selenium, browser_id, oz_page,
                                               arg['value'], arg_name, arg_type)

    if results:
        for res_name, res in results.items():
            choose_option_in_dropdown_menu_in_task_page(
                selenium, browser_id, oz_page, popups, res['target store'],
                res_name, res_type)

    confirm_lambda_creation_or_edition(selenium, browser_id, oz_page, option)


@wt(parsers.parse('user of {browser_id} executes {ordinal} revision of '
                  '"{workflow}", using "{item_list}" as initial value, in '
                  '"{space}" space'))
def execute_workflow(browser_id, selenium, oz_page, space, op_container,
                     ordinal, workflow, modals, item_list, popups):
    spaces = 'spaces'
    automation_workflows = 'Automation Workflows'
    tab_name = 'Run workflow'

    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id, spaces,
                                                space, oz_page)
    click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id, space,
                                                  automation_workflows, oz_page)
    click_button_in_navigation_tab(selenium, browser_id, op_container,
                                   tab_name)
    choose_workflow_revision_to_run(selenium, browser_id, op_container,
                                    ordinal, workflow)
    choose_file_as_initial_workflow_value(selenium, browser_id, item_list, modals,
                                          op_container, popups)
    confirm_workflow_to_execute(selenium, browser_id, op_container)


@wt(parsers.parse('user of {browser_id} executes {ordinal} revision of '
                  '"{workflow}", using "{item}" as initial value, in '
                  '"{space}" space and waits extended time for workflow to '
                  'finish'))
def execute_workflow_and_wait(browser_id, selenium, oz_page, space,
                              op_container, ordinal, workflow, modals, item,
                              popups):
    start = 'start'
    finish = 'finish'
    execute_workflow(browser_id, selenium, oz_page, space, op_container,
                     ordinal, workflow, modals, item, popups)
    wait_for_workflows_in_automation_subpage(selenium, browser_id, op_container,
                                             start)
    wait_for_workflows_in_automation_subpage(selenium, browser_id, op_container,
                                             finish)
    expand_first_executed_workflow_record(selenium, browser_id, op_container)


@wt(parsers.parse('user of {browser_id} creates "{lambda_name}" lambda from '
                  '"{docker_image}" docker image in "{inventory}" inventory'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_lambda_using_gui(selenium, browser_id, oz_page, lambda_name,
                            docker_image, inventory):
    click_on_option_in_the_sidebar(selenium, browser_id, 'Automation', oz_page)
    go_to_inventory_subpage(selenium, browser_id, inventory,
                            'lambdas', oz_page)
    click_add_new_button_in_menu_bar(selenium, browser_id, oz_page,
                                     'Add new lambda')
    write_text_into_lambda_form(selenium, browser_id, oz_page,
                                lambda_name, 'lambda name')
    write_text_into_lambda_form(selenium, browser_id, oz_page,
                                docker_image, 'docker image')

    confirm_lambda_creation_or_edition(selenium, browser_id, oz_page, 'lambda')

    go_to_inventory_subpage(selenium, browser_id, inventory,
                            'lambdas', oz_page)

    assert_lambda_exists(selenium, browser_id, oz_page, lambda_name)


@wt(parsers.re('user of (?P<browser_id>.*) adds '
               '(?P<ordinal>|1st |2nd |3rd |4th )(?P<option>argument|result'
               '|configuration parameters) named "(?P<name>.*)" '
               'of "(?P<type>.*)" type'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_parameter_into_lambda_form(selenium, browser_id, oz_page, popups,
                                   option, name, type, ordinal):
    driver = selenium[browser_id]
    page = oz_page(driver)['automation'].lambdas_page.form

    subpage = getattr(page, transform(option))
    subpage.add_button()
    ordinal = '1st' if not ordinal else ordinal
    bracket_name = 'bracket_' + ordinal.strip()
    object_bracket = getattr(subpage, bracket_name)

    name_input = object_bracket.name
    css_sel = '#' + name_input.web_elem.get_attribute('id')
    scroll_to_css_selector(driver, css_sel)
    name_input.value = name

    object_bracket.type_dropdown.click()
    popups(driver).power_select.choose_item(type)


def write(path, text):
    import os
    with open(path, 'a') as f:
        f.write(f'{text}\n\n')
        os.utime(path, None)


@repeat_failed(timeout=WAIT_BACKEND)
def click_on_task_audit_log(task):
        if not check_if_task_is_opened(task):
            task.drag_handle.click()
        task.audit_log()


def get_modal_and_logs_for_task(path, task, modals, driver):
    write(path, task.name)
    time.sleep(2)
    click_on_task_audit_log(task)
    time.sleep(2)
    modal = modals(driver).task_audit_log
    logs = modal.logs_entry
    return modal, logs


def close_modal_and_task(modal, task):
    time.sleep(2)
    modal.x()
    task.drag_handle.click()


def get_audit_log_json_and_write_to_file(log, modal, clipboard, displays,
                                         browser_id, path):
    log.click()
    modal.copy_json()
    audit_log = clipboard.paste(display=displays[browser_id])
    write(path, audit_log)
    modal.close_details()
    write(path, '\n')


@repeat_failed(timeout=WAIT_FRONTEND)
def write_audit_logs_for_task_to_file(task, modals, driver, clipboard, path,
                                      displays, browser_id):
    task.drag_handle.click()
    time.sleep(2)
    if not check_if_task_is_opened(task):
        task.drag_handle.click()
    if task.status == 'Failed':
        modal, logs = get_modal_and_logs_for_task(
            path, task, modals, driver)
        for log in logs:
            if log.severity != 'Info':
                get_audit_log_json_and_write_to_file(log, modal, clipboard,
                                                     displays, browser_id, path)
        close_modal_and_task(modal, task)


def get_audit_logs_from_every_task_in_workflow(lanes, modals, driver, clipboard,
                                               path, displays, browser_id):
    for lane in lanes:
        boxes = lane.parallel_box
        for box in boxes:
            tasks = box.task_list
            for task in tasks:
                time.sleep(0.5)
                write_audit_logs_for_task_to_file(task, modals, driver,
                                                  clipboard, path,
                                                  displays, browser_id)


@wt(parsers.parse('if workflow status is "{exp_status}" {user} of {browser_id}'
                  ' saves audit logs for all tasks to logs'))
def save_audit_logs_to_logs(selenium, browser_id, op_container, exp_status,
                            modals, clipboard, displays):
    page = switch_to_automation_page(selenium, browser_id, op_container)
    time.sleep(2)
    act_status = page.workflow_visualiser.status
    driver = selenium[browser_id]
    if act_status == exp_status:
        lanes = page.workflow_visualiser.workflow_lanes
        path = GUI_LOGDIR + '/audit_logs.txt'
        get_audit_logs_from_every_task_in_workflow(
            lanes, modals, driver, clipboard, path, displays, browser_id)
