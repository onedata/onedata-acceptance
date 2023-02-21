"""This module contains gherkin steps to run acceptance tests featuring
automation management in onezone web GUI """

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import json
import time

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.utils.generic import upload_file_path
from tests.utils.bdd_utils import wt, parsers
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.utils import repeat_failed
from tests.gui.steps.common.miscellaneous import (
    press_backspace_on_active_element)


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


@wt(parsers.parse('user of {browser_id} uses "Upload (json)" button from menu '
                  'bar to upload workflow "{file_name}" to current dir '
                  'without waiting for upload to finish'))
@repeat_failed(timeout=2 * WAIT_BACKEND)
def upload_workflow_as_json(selenium, browser_id, file_name, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['automation'].upload_workflow(upload_file_path(file_name))


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>does not see|sees) '
               '"(?P<workflow>.*)" in workflows list '
               'in inventory workflows subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_workflow_exists(selenium, browser_id, oz_page, workflow, option):
    page = oz_page(selenium[browser_id])['automation']

    if option == 'does not see':
        assert workflow not in page.workflows_page.elements_list, \
            f'Workflow: {workflow} found '
    else:
        assert workflow in page.workflows_page.elements_list, \
            f'Workflow: {workflow} not found '


@wt(parsers.re('user of (?P<browser_id>.*) uses '
               '"(?P<option>Add new lambda|Add new workflow)" button from '
               'menu bar in (lambdas|workflows) subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_add_new_button_in_menu_bar(selenium, browser_id, oz_page, option):
    driver = selenium[browser_id]
    getattr(oz_page(driver)['automation'].main_page, transform(option)).click()


@wt(parsers.re('user of (?P<browser_id>.*) writes "(?P<text>.*)" into ('
               '?P<text_field>lambda name|docker image) text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def write_text_into_lambda_form(selenium, browser_id,
                                oz_page, text, text_field):
    page = oz_page(selenium[browser_id])['automation']
    label = getattr(page.lambdas_page.form, transform(text_field))
    setattr(label, 'value', text)


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>checks|unchecks) '
               'lambdas "(?P<toggle>Mount space|Read only)" toggle'))
@repeat_failed(timeout=WAIT_FRONTEND)
def switch_toggle_in_lambda_form(selenium, browser_id, oz_page, option, toggle):
    subpage = oz_page(selenium[browser_id])['automation'].lambdas_page.form
    toggle = transform(toggle) + "_toggle"
    getattr(getattr(subpage, toggle), option[:-1])()


@wt(parsers.re('user of (?P<browser_id>.*) confirms (creating new|edition of) '
               '(?P<option>lambda|revision|task) using '
               '"(Create|Modify)" button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_lambda_creation_or_edition(selenium, browser_id, oz_page, option):
    page = oz_page(selenium[browser_id])['automation']

    if option == 'task':
        page.workflows_page.task_form.create_button.click()
    else:
        page.lambdas_page.form.create_button.click()


@wt(parsers.re('user of (?P<browser_id>.*) chooses "(?P<option>.*)" in '
               '(?P<dropdown_name>.*) in "(?P<object_name>.*)" '
               '(?P<object_type>result|argument) in task creation page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_option_in_dropdown_menu_in_task_page(selenium, browser_id, oz_page,
                                                popups, option, object_name,
                                                object_type):
    driver = selenium[browser_id]
    page = oz_page(driver)['automation'].workflows_page.task_form
    if object_type == 'result':
        page.results[object_name + ':'].add_mapping()
        page.results[object_name + ':'].target_store_dropdown.click()
    else:
        page.arguments[object_name + ':'].value_builder_dropdown.click()

    popups(driver).power_select.choose_item(option)


def clean_tab_textarea_in_json_argument_editor(tab, selenium, browser_id):
    tab.click()
    while tab.text_area:
        press_backspace_on_active_element(selenium, browser_id)
    time.sleep(0.5)


@wt(parsers.re('user of (?P<browser_id>.*) writes "(?P<input_value>.*)" into'
               ' json editor bracket in "(?P<object_name>.*)" '
               '(?P<object_type>result|argument) in task creation page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def write_text_into_editor_bracket(selenium, browser_id, oz_page, input_value,
                                   object_name, object_type):
    driver = selenium[browser_id]
    page = oz_page(driver)['automation'].workflows_page.task_form
    if object_type == 'result':
        page.results[object_name + ':'].json_editor = input_value
    else:
        tab = page.arguments[object_name + ':']
        if tab.data_type == 'STRING':
            tab.string_editor = input_value
        elif tab.data_type == 'OBJECT':
            clean_tab_textarea_in_json_argument_editor(tab.json, selenium,
                                                       browser_id)
            tab.json.text_area = json.dumps(input_value)


@wt(parsers.parse('user of {browser_id} sees "{lambda_name}" in lambdas list '
                  'in inventory lambdas subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_lambda_exists(selenium, browser_id, oz_page, lambda_name):
    page = oz_page(selenium[browser_id])['automation']

    assert lambda_name in page.lambdas_page.elements_list, \
        f'Lambda: {lambda_name} not found '


@wt(parsers.parse('user of {browser_id} clicks on "Create new revision" '
                  'in "{lambda_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_create_new_revision_button(selenium, browser_id, oz_page,
                                        lambda_name):
    page = oz_page(selenium[browser_id])['automation']
    page.lambdas_page.elements_list[lambda_name].create_new_revision.click()


def collapse_revision_list(subpage):
    subpage.show_revisions_button.click()


def get_lambda_or_workflow_bracket(selenium, browser_id, oz_page, page,
                                   object_name):
    page_name = page + 's_page'
    subpage = getattr(oz_page(selenium[browser_id])['automation'], page_name)

    object = subpage.elements_list[object_name]

    try:
        collapse_revision_list(object)
    except (RuntimeError, AttributeError):
        pass

    return object


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>does not see|sees) that '
               '(?P<ordinal>1st|2nd|3rd|4th) revision of '
               '"(?P<object_name>.*)" (?P<page>lambda|workflow) '
               'is described "(?P<description>.*)"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_revision_description_in_object_bracket(selenium, browser_id, oz_page,
                                                  ordinal, option, object_name,
                                                  page, description):
    object = get_lambda_or_workflow_bracket(selenium, browser_id, oz_page,
                                            page, object_name)

    revision = object.revision_list[ordinal[:-2]]

    if option == 'does not see':
        assert revision.name != description, \
            f'Revision: {object_name} found'
    else:
        assert revision.name == description, \
            f'Revision: {object_name} not found'


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>does not see|sees) '
               '(?P<ordinal>1st|2nd|3rd|4th) revision of '
               '"(?P<object_name>.*)" (?P<page>lambda|workflow)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_revision_of_object(selenium, browser_id, oz_page,
                              ordinal, option, object_name,
                              page):
    object = get_lambda_or_workflow_bracket(selenium, browser_id, oz_page,
                                            page, object_name)

    if option == 'does not see':
        assert ordinal[:-2] not in object.revision_list, \
            f'{ordinal} revision found'
    else:
        assert ordinal[:-2] in object.revision_list, \
            f'{ordinal} revision not found'


@wt(parsers.re('user of (?P<browser_id>.*) clicks on "(?P<option>Redesign as '
               'new revision|Duplicate to...|Download \(json\)|Remove)" button '
               'from (?P<ordinal>1st|2nd|3rd|4th) revision of '
               '"(?P<object_name>.*)" (?P<page>lambda|workflow) menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_revision_menu_button(selenium, browser_id, oz_page, option,
                                         object_name, ordinal, popups,
                                         page):
    object = get_lambda_or_workflow_bracket(selenium, browser_id, oz_page,
                                            page, object_name)

    revision = object.revision_list[ordinal[:-2]]
    object.revision_list[ordinal[:-2]].menu_button.click()

    popups(selenium[browser_id]).menu_popup_with_label.menu[option].click()


@wt(parsers.parse('user of {browser_id} writes "{text}" into workflow name '
                  'text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def write_text_into_workflow_name_on_main_workflows_page(selenium, browser_id,
                                                         oz_page, text):
    page = oz_page(selenium[browser_id])['automation']
    page.workflows_page.workflow_creator.workflow_name.value = text


@wt(parsers.parse('user of {browser_id} confirms creating new workflow using '
                  '"Create" button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_workflow_creation(selenium, browser_id, oz_page):
    page = oz_page(selenium[browser_id])['automation']
    page.workflows_page.workflow_creator.create_button.click()


@wt(parsers.parse('user of {browser_id} clicks "Add store" button '
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


@wt(parsers.re('user of (?P<browser_id>.*?) clicks on create lane button '
               '(?P<option>in the middle|on the right side of latest created'
               ' lane) of workflow visualizer'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_add_lane_button_in_workflow_visualizer(selenium, browser_id, oz_page,
                                                 option):
    page = oz_page(selenium[browser_id])['automation']
    if "right" in option:
        page.workflows_page.workflow_visualiser.create_lane_button[-1].click()
    else:
        page.workflows_page.workflow_visualiser.create_lane_button[0].click()


@wt(parsers.parse('user of {browser_id} sees "{lane_name}" lane in workflow '
                  'visualizer'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_lane_in_workflow_visualizer(selenium, browser_id, oz_page,
                                       lane_name):
    page = oz_page(selenium[browser_id])['automation']
    workflow_visualizer = page.workflows_page.workflow_visualiser.workflow_lanes

    assert lane_name in workflow_visualizer, f'Lane: {lane_name} not found'


@wt(parsers.parse('user of {browser_id} clicks on "Add parallel box" button in '
                  'the middle of "{lane_name}" lane'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_parallel_box_to_lane(selenium, browser_id, oz_page, lane_name):
    page = oz_page(selenium[browser_id])['automation']
    workflow_visualiser = page.workflows_page.workflow_visualiser
    workflow_visualiser.workflow_lanes[
        lane_name].add_parallel_box_button.click()


@wt(parsers.parse('user of {browser_id} clicks "Create task" button in empty '
                  'parallel box in "{lane_name}" lane'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_task_to_empty_parallel_box(selenium, browser_id, oz_page, lane_name):
    page = oz_page(selenium[browser_id])['automation']
    lane = page.workflows_page.workflow_visualiser.workflow_lanes[lane_name]
    lane.empty_parallel_box.add_task_button.click()


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>does not see|sees) task '
               'named "(?P<task_name>.*)" in "(?P<lane_name>.*)" lane'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_task_in_lane_in_workflow(selenium, browser_id, oz_page, lane_name,
                                    task_name, option):
    page = oz_page(selenium[browser_id])['automation']
    workflow_visualiser = page.workflows_page.workflow_visualiser
    task = workflow_visualiser.workflow_lanes[lane_name].parallel_box.task_list

    if option == 'does not see':
        assert task_name not in task, f'Task: {task_name} found'
    else:
        assert task_name in task, f'Task: {task_name} not found'


@wt(parsers.re('user of (?P<browser_id>.*) writes "(?P<task_name>.*)" '
               'into name text field in task (creation|edition) subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def write_task_name_in_task_edition_text_field(selenium, browser_id,
                                               oz_page, task_name):
    page = oz_page(selenium[browser_id])['automation']
    page.workflows_page.task_form.task_name.value = task_name


@wt(parsers.parse('user of {browser_id} clicks on "{option}" button in task '
                  '"{task_name}" menu in "{lane_name}" lane '
                  'in workflow visualizer'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_task_menu_button(selenium, browser_id, oz_page, lane_name,
                                     task_name, option, popups):
    driver = selenium[browser_id]
    page = oz_page(driver)['automation']
    workflow_visualiser = page.workflows_page.workflow_visualiser
    box = workflow_visualiser.workflow_lanes[lane_name].parallel_box
    box.task_list[task_name].menu_button.click()

    popups(driver).menu_popup_with_label.menu[option].click()


@wt(parsers.parse('user of {browser_id} clicks on "{option}" button in '
                  'workflow "{workflow}" menu in workflows subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_workflow_menu_button(selenium, browser_id, oz_page,
                                         workflow, option, popups):
    page = oz_page(selenium[browser_id])['automation']
    page.workflows_page.elements_list[workflow].menu_button.click()
    popups(selenium[browser_id]).menu_popup_with_label.menu[option].click()


@wt(parsers.parse('user of {browser_id} writes "{text}" in name textfield of '
                  'selected workflow'))
@repeat_failed(timeout=WAIT_FRONTEND)
def insert_text_in_textfield_of_workflow(selenium, browser_id, oz_page, text):
    page = oz_page(selenium[browser_id])['automation']
    page.workflows_page.workflow_name_input.value = text


@wt(parsers.parse('user of {browser_id} confirms edition of selected workflow '
                  'details using "Save" button'))
@wt(parsers.parse('user of {browser_id} saves workflow edition by clicking '
                  '"Save" button from menu bar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_in_workflow(selenium, browser_id, oz_page):
    page = oz_page(selenium[browser_id])['automation']
    page.workflows_page.workflow_save_button.click()


@wt(parsers.parse('user of {browser_id} sees that "{file_name}" '
                  'has been downloaded'))
@repeat_failed(timeout=WAIT_FRONTEND)
def has_downloaded_workflow_file_content(browser_id, tmpdir, file_name):
    downloaded_file = tmpdir.join(browser_id, 'download', file_name)
    assert downloaded_file.exists(), f'file {file_name} has not been downloaded'


@wt(parsers.parse('user of {browser_id} changes workflow view to '
                  '"{tab_name}" tab'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_navigation_tab_in_workflow(selenium, browser_id, oz_page, tab_name):
    page = oz_page(selenium[browser_id])['automation']
    page.workflows_page.navigation_tab[tab_name].click()


@wt(parsers.parse('user of {browser_id} writes "{text}" in description '
                  'textfield in workflow Details tab'))
@repeat_failed(timeout=WAIT_FRONTEND)
def insert_text_in_description_of_revision(selenium, browser_id, oz_page, text):
    page = oz_page(selenium[browser_id])['automation']
    page.workflows_page.revision_details.description = text


@wt(parsers.re('user of (?P<browser_id>.*?) chooses '
               '(?P<ordinal>1st|2nd|3rd|4th) revision of '
               '"(?P<lambda_name>.*?)" lambda to add to workflow'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_lambda_revision_to_workflow(selenium, browser_id, oz_page, lambda_name,
                                    ordinal):
    subpage = oz_page(selenium[browser_id])['automation'].lambdas_page
    object = subpage.elements_list[lambda_name]
    revision = object.revision_list[ordinal[:-2]]

    try:
        collapse_revision_list(object)
    except (RuntimeError, AttributeError):
        pass

    revision.add_to_workflow.click()


@wt(parsers.re('user of (?P<browser_id>.*?) clicks on "Add parallel box" button'
               ' (?P<position>below|above) Parallel box'
               ' in "(?P<lane_name>.*?)" lane'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_another_parallel_box_to_lane(selenium, browser_id, oz_page, lane_name,
                                     position):
    page = oz_page(selenium[browser_id])['automation']
    workflow_visualiser = page.workflows_page.workflow_visualiser
    lane = workflow_visualiser.workflow_lanes[lane_name]

    if position == 'below':
        lane.add_parallel_box_below.click()
    else:
        lane.add_parallel_box_above.click()
