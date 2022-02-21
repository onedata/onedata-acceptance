"""This module contains gherkin steps to run acceptance tests featuring
automation management in onezone web GUI """

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.utils.generic import transform, upload_file_path
from tests.utils.bdd_utils import wt, parsers
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.utils import repeat_failed
from tests.gui.steps.common.miscellaneous import press_enter_on_active_element


@wt(parsers.parse('user of {browser_id} clicks on Create automation inventory '
                  'button in automation sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_automation_button_in_sidebar(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['automation'].create_automation()


@wt(parsers.parse('user of {browser_id} writes "{text}" into inventory name '
                  'text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def input_name_into_input_box_on_main_automation_page(selenium, browser_id,
                                                      text, oz_page):
    oz_page(selenium[browser_id])['automation'].input_box.value = text


@wt(parsers.parse('user of {browser_id} clicks on confirmation button on '
                  'automation page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_name_input_on_main_automation_page(selenium, browser_id,
                                               oz_page):
    oz_page(selenium[browser_id])['automation'].input_box.confirm()


@wt(parsers.re('user of (?P<browser_id>.*) clicks on '
               '"(?P<option>Rename|Leave|Remove)" '
               'button in inventory "(?P<inventory>.*)" menu in the '
               'sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_inventory_menu(selenium, browser_id, option, inventory,
                                   oz_page, popups):
    driver = selenium[browser_id]
    page = oz_page(driver)['automation']
    page.elements_list[inventory]()
    page.elements_list[inventory].menu()
    popups(driver).menu_popup_with_text.menu[option]()


@wt(parsers.parse('user of {browser_id} writes '
                  '"{text}" into rename inventory text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def input_new_inventory_name_into_rename_inventory_input_box(selenium,
                                                             browser_id, text,
                                                             oz_page):
    page = oz_page(selenium[browser_id])['automation']
    page.elements_list[''].edit_box.value = text


@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_confirmation_button_to_rename_inventory(selenium, browser_id,
                                                     oz_page):
    oz_page(selenium[browser_id])['automation'].elements_list[
        ''].edit_box.confirm()


@wt(parsers.re('user of (?P<browser_id>.*) confirms inventory rename with '
               'confirmation button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_rename_the_inventory(selenium, browser_id, oz_page):
    click_on_confirmation_button_to_rename_inventory(selenium, browser_id,
                                                     oz_page)


@wt(parsers.re('users? of (?P<browser_ids>.*) (?P<option>does not see|sees) '
               'inventory "(?P<inventory>.*)" on inventory list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_inventory_exists(selenium, browser_ids, option, inventory, oz_page):
    for browser_id in parse_seq(browser_ids):
        elem_list = oz_page(selenium[browser_id])['automation'].elements_list

        if option == 'does not see':
            assert inventory not in elem_list, f'inventory: {inventory} found'
        else:
            assert inventory in elem_list, f'inventory: {inventory} not found'


@wt(parsers.re('user of (?P<browser_id>.*) opens inventory "(?P<inventory>.*)" '
               '(?P<subpage>workflows|lambdas|members|main) subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def go_to_inventory_subpage(selenium, browser_id, inventory, subpage, oz_page):
    page = oz_page(selenium[browser_id])['automation']
    page.elements_list[inventory]()
    if subpage != 'main':
        getattr(page.elements_list[inventory], subpage)()


@wt(parsers.parse('user of {browser_ids} sees "{text}" label in "{inventory}" '
                  'main page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_inventory_exists(selenium, browser_ids, oz_page, text):
    for browser_id in parse_seq(browser_ids):
        err_msg = oz_page(selenium[browser_id])['automation'].privileges_err_msg

        assert text in err_msg, f'Error message: {text} not found'


@wt(parsers.parse('user of {browser_id} uses Upload (json) button from menu '
                  'bar to upload workflow "{file_name}" to current dir '
                  'without waiting for upload to finish'))
@repeat_failed(timeout=2 * WAIT_BACKEND)
def upload_workflow_as_json(selenium, browser_id, file_name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['automation'].upload_workflow(upload_file_path(file_name))


@wt(parsers.parse('user of {browser_id} sees "{workflow}" in workflows list '
                  'in inventory workflows subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_workflow_exists(selenium, browser_id, oz_page, workflow):
    page = oz_page(selenium[browser_id])['automation']

    assert workflow in page.workflows_page.elements_list, \
        f'Workflow: {workflow} not found '


@wt(parsers.re('user of (?P<browser_id>.*) uses Add new '
               '(?P<option>lambda|workflow) button from menu bar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_add_new_button_in_menu_bar(selenium, browser_id, oz_page, option):
    driver = selenium[browser_id]
    if option == "lambda":
        oz_page(driver)['automation'].main_page.add_new_lambda.click()
    else:
        oz_page(driver)['automation'].main_page.add_new_workflow.click()


@wt(parsers.re('user of (?P<browser_id>.*) writes "(?P<text>.*)" into ('
               '?P<text_field>lambda name|docker image) text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def write_lambda_name_in_lambda_text_field(selenium, browser_id,
                                                   oz_page, text, text_field):
    page = oz_page(selenium[browser_id])['automation']
    label = getattr(page.lambdas_page.form, transform(text_field))
    setattr(label, 'value', text)


@wt(parsers.re('user of (?P<browser_id>.*) confirms '
               '(?P<option>lambda|revision|task) (creation|edition) by clicking'
               ' (Create|Modify) button'))
@wt(parsers.re('user of (?P<browser_id>.*) confirms create new '
               '(lambda|revision) using Create button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_lambda_creation(selenium, browser_id, oz_page, option):
    page = oz_page(selenium[browser_id])['automation']

    if option == 'task':
        page.workflows_page.task_form.create_button.click()
    else:
        page.lambdas_page.form.create_button.click()


@wt(parsers.parse('user of {browser_id} sees "{lambda_name}" in lambdas list '
                  'in inventory lambdas subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_lambda_exists(selenium, browser_id, oz_page, lambda_name):
    page = oz_page(selenium[browser_id])['automation']

    assert lambda_name in page.lambdas_page.elements_list, \
        f'Lambda: {lambda_name} not found '


@wt(parsers.parse('user of {browser_id} clicks on Create new revision '
                  'in "{lambda_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_create_new_revision_button(selenium, browser_id, oz_page,
                                        lambda_name):
    page = oz_page(selenium[browser_id])['automation']
    page.lambdas_page.elements_list[lambda_name].create_new_revision.click()


def collapse_revision_list_in_lambda(selenium, browser_id, oz_page,
                                     lambda_name):
    page = oz_page(selenium[browser_id])['automation']
    lambda_box = page.lambdas_page.elements_list[lambda_name]
    lambda_box.show_revisions_button.click()


@wt(parsers.parse('user of {browser_id} sees "{revision_name}" in lambdas '
                  'revision list of "{lambda_name}" in '
                  'inventory lambdas subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_revision_in_lambda_bracket(selenium, browser_id, oz_page,
                                      lambda_name, revision_name):
    page = oz_page(selenium[browser_id])['automation']
    lambda_box = page.lambdas_page.elements_list[lambda_name]
    try:
        collapse_revision_list_in_lambda(selenium, browser_id, oz_page,
                                         lambda_name)
    finally:
        assert revision_name in lambda_box.revision_list, \
            f'Lambda revision: {revision_name} not found'


@wt(parsers.re('user of (?P<browser_id>.*) clicks on "(?P<option>Redesign as '
               'new revision)" button in revision "(?P<revision_name>.*)" '
               'menu in the "(?P<lambda_name>.*)" revision list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_revision_menu_button(selenium, browser_id, oz_page, option,
                                         lambda_name, revision_name, popups):
    page = oz_page(selenium[browser_id])['automation']
    lambda_box = page.lambdas_page.elements_list[lambda_name]
    try:
        collapse_revision_list_in_lambda(selenium, browser_id, oz_page,
                                         lambda_name)
        lambda_box.revision_list[revision_name].menu_button.click()
    except BaseException:
        lambda_box.revision_list[revision_name].menu_button.click()

    popups(selenium[browser_id]).menu_popup_with_label.menu[option].click()


@wt(parsers.parse('user of {browser_id} writes "{text}" into workflow name '
                  'text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def input_name_into_input_box_on_main_workflows_page(selenium, browser_id,
                                                     oz_page, text):
    page = oz_page(selenium[browser_id])['automation']
    page.workflows_page.workflow_name.value = text


@wt(parsers.parse('user of {browser_id} confirms create new workflow using '
                  'Create button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_workflow_creation(selenium, browser_id, oz_page):
    page = oz_page(selenium[browser_id])['automation']
    page.workflows_page.create_button.click()


@wt(parsers.parse('user of {browser_id} clicks Add store button '
                  'in workflow visualizer'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_add_store_button(selenium, browser_id, oz_page):
    page = oz_page(selenium[browser_id])['automation']
    page.workflows_page.workflow_visualiser.add_store_button.click()


@wt(parsers.parse('user of {browser_id} sees "{store_name}" in the stores '
                  'list in workflow visualizer'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_store_in_store_list(selenium, browser_id, oz_page, store_name):
    page = oz_page(selenium[browser_id])['automation']
    stores_list = page.workflows_page.workflow_visualiser.stores_list

    assert store_name in stores_list, f'Store: {store_name} not found'


@wt(parsers.parse('user of {browser_id} clicks on create lane button in the '
                  'middle of workflow visualizer'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_add_lane_button_in_store(selenium, browser_id, oz_page):
    page = oz_page(selenium[browser_id])['automation']
    page.workflows_page.workflow_visualiser.create_lane_button.click()


@wt(parsers.parse('user of {browser_id} sees "{lane_name}" in workflow '
                  'visualizer'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_lane_in_workflow_visualizer(selenium, browser_id, oz_page,
                                       lane_name):
    page = oz_page(selenium[browser_id])['automation']
    workflow_visualizer = page.workflows_page.workflow_visualiser.workflow_lanes

    assert lane_name in workflow_visualizer, f'Lane: {lane_name} not found'


@wt(parsers.parse('user of {browser_id} clicks on add parallel box button in '
                  'the middle of "{lane_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_parallel_box_to_lane(selenium, browser_id, oz_page, lane_name):
   page = oz_page(selenium[browser_id])['automation']
   workflow_visualiser = page.workflows_page.workflow_visualiser
   workflow_visualiser.workflow_lanes[lane_name].add_parallel_box_button.click()


@wt(parsers.parse('user of {browser_id} clicks create task button in empty '
                  'parallel box in "{lane_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_task_to_empty_parallel_box(selenium, browser_id, oz_page, lane_name):
    page = oz_page(selenium[browser_id])['automation']
    lane = page.workflows_page.workflow_visualiser.workflow_lanes[lane_name]
    lane.parallel_box.add_task_button.click()


@wt(parsers.parse('user of {browser_id} sees task named '
                  '"{task_name}" in "{lane_name}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_task_in_lane_in_workflow(selenium, browser_id, oz_page, lane_name, task_name):
    page = oz_page(selenium[browser_id])['automation']
    workflow_visualiser = page.workflows_page.workflow_visualiser
    task = workflow_visualiser.workflow_lanes[lane_name].parallel_box.task

    assert task_name in task, f'Task: {task_name} not found'


@wt(parsers.parse('user of {browser_id} writes "{task_name}" '
                  'into name text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def write_task_name_in_task_edition_text_field(selenium, browser_id,
                                               oz_page, text):
    page = oz_page(selenium[browser_id])['automation']
    page.workflows_page.task_page.task_name.value = text


@wt(parsers.parse('user of {browser_id} clicks on "{option}" button in task '
                  '"{task_name}" menu in "{lane_name}" in workflow visualizer'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_task_menu_button(selenium, browser_id, oz_page, lane_name, task_name, option, popups):
    page = oz_page(selenium[browser_id])['automation']
    lane = page.workflows_page.workflow_visualiser.workflow_lanes[lane_name]
    lane.parallel_box.task.menu_button.click()

    popups(selenium[browser_id]).menu_popup_with_label.menu[option].click()



