"""This module contains gherkin steps to run acceptance tests featuring
automation management in onezone web GUI """

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.utils.generic import (upload_file_path, upload_workflow_path,
                                     transform)
from tests.utils.bdd_utils import wt, parsers
from tests.gui.utils.generic import parse_seq
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} clicks on Create automation inventory '
                  'button in automation sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_automation_button_in_sidebar(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['automation'].create_automation()


def get_oz_workflow_visualizer(oz_page, driver):
    return oz_page(driver)['automation'].workflows_page.workflow_visualiser


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
    page.elements_list[0].edit_box.value = text


@wt(parsers.re('user of (?P<browser_id>.*) confirms inventory rename with '
               'confirmation button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_rename_the_inventory(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id]
            )['automation'].elements_list[0].edit_box.confirm()


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
@repeat_failed(timeout=WAIT_BACKEND)
def go_to_inventory_subpage(selenium, browser_id, inventory, subpage, oz_page,
                            tmp_memory):
    try:
        page = tmp_memory[browser_id]['oz_page']
    except KeyError:
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


@repeat_failed(timeout=2 * WAIT_BACKEND)
def upload_workflow_from_repository(selenium, browser_id, workflow_name,
                                    oz_page):
    driver = selenium[browser_id]
    workflows_in_directories = [
        'detect-file-formats', 'detect-file-mime-formats', 'download-files',
        'bagit-uploader']

    workflow_name = (workflow_name + '.json'
                     ) if workflow_name not in workflows_in_directories else (
            workflow_name + '/' + workflow_name + '.json')
    automation_page = oz_page(driver)['automation']
    automation_page.upload_workflow(upload_workflow_path(workflow_name))


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


@wt(parsers.parse('user of {browser_id} sees "{lambda_name}" in lambdas list '
                  'in inventory lambdas subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_lambda_exists(selenium, browser_id, oz_page, lambda_name):
    page = oz_page(selenium[browser_id])['automation']

    assert lambda_name in page.lambdas_page.elements_list, \
        f'Lambda: {lambda_name} not found '


@wt(parsers.parse('user of {browser_id} sees there are {number} lambdas '
                  'in lambdas list in inventory lambdas subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_number_of_lambdas(selenium, browser_id, oz_page, number: int):
    page = oz_page(selenium[browser_id])['automation']
    lambdas_number = len(page.lambdas_page.elements_list)
    err_msg = f'number of lambdas is {lambdas_number} instead of {number}'
    assert lambdas_number == number, err_msg


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


@wt(parsers.parse('user of {browser_id} clicks on "{option}" button in '
                  'workflow "{workflow}" menu in workflows subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_workflow_menu_button(selenium, browser_id, oz_page,
                                         workflow, option, popups):
    page = oz_page(selenium[browser_id])['automation']
    page.workflows_page.elements_list[workflow].menu_button.click()
    popups(selenium[browser_id]).menu_popup_with_label.menu[option].click()


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


def click_on_option_of_inventory_on_left_sidebar_menu(selenium, browser_id,
                                                      inventory_name, option,
                                                      oz_page):
    driver = selenium[browser_id]
    getattr(oz_page(driver)['automation'].elements_list[inventory_name],
            transform(option)).click()
