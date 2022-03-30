"""Meta steps for operations for quality of service"""

__author__ = "Michal Dronka"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.meta_steps.oneprovider.data import go_to_filebrowser
from tests.gui.steps.modal import (
    write_name_into_text_field_in_modal, wt_wait_for_modal_to_appear)
from tests.gui.steps.oneprovider.data_tab import (
    choose_option_from_selection_menu, assert_browser_in_tab_in_op)
from tests.gui.steps.oneprovider.file_browser import (
    click_on_item_in_file_browser, click_on_status_tag_for_file_in_file_browser)
from tests.gui.steps.oneprovider.browser import (
    click_option_in_data_row_menu_in_browser, click_menu_for_elem_in_browser,
    assert_status_tag_for_file_in_browser,
    assert_not_status_tag_for_file_in_browser)
from tests.gui.steps.oneprovider.metadata import *
from tests.gui.steps.oneprovider.qos import (
    click_enter_as_text_link, confirm_entering_text,
    delete_all_qualities_of_service)
from tests.gui.steps.onezone.spaces import (
    click_on_option_of_space_on_left_sidebar_menu)


def _add_qos_requirement_in_modal(selenium, browser_id, modals, item_name,
                                  tmp_memory, expression, popups,
                                  replicas_number):
    qos_option = modal = 'Quality of Service'
    add_button = 'Add Requirement'
    save_button = 'Save'
    close_button = 'Close'
    replicas_field = 'Replicas number'
    expression_field = 'expression'

    click_on_item_in_file_browser(browser_id, item_name, tmp_memory)
    choose_option_from_selection_menu(browser_id, selenium, qos_option, popups,
                                      tmp_memory)
    click_modal_button(selenium, browser_id, add_button, modal, modals)
    click_enter_as_text_link(selenium, browser_id, modals)
    write_name_into_text_field_in_modal(selenium, browser_id, expression,
                                        modal, modals, expression_field)
    confirm_entering_text(selenium, browser_id, modals)
    if replicas_number != 1:
        write_name_into_text_field_in_modal(selenium, browser_id,
                                            replicas_number,
                                            modal, modals, replicas_field)
    click_modal_button(selenium, browser_id, save_button, modal, modals)
    click_modal_button(selenium, browser_id, close_button, modal, modals)


@wt(parsers.parse('user of {browser_id} creates "{expression}" QoS requirement '
                  'for "{item_name}" in space "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_qos_requirement_in_modal(selenium, browser_id, modals, item_name,
                                 tmp_memory, expression, oz_page, op_container,
                                 popups, space_name):
    replicas_number = 1

    go_to_filebrowser(selenium, browser_id, oz_page, op_container,
                      tmp_memory, space_name)
    _add_qos_requirement_in_modal(selenium, browser_id, modals, item_name,
                                  tmp_memory, expression, popups,
                                  replicas_number)


@wt(parsers.parse('user of {browser_id} creates {replicas_number} replicas of '
                  '"{expression}" QoS requirement for "{item_name}" in space '
                  '"{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_qos_requirement_in_modal_with_replicas(selenium, browser_id, modals,
                                               item_name, tmp_memory,
                                               expression, oz_page, space_name,
                                               op_container, popups,
                                               replicas_number):
    go_to_filebrowser(selenium, browser_id, oz_page, op_container,
                      tmp_memory, space_name)
    _add_qos_requirement_in_modal(selenium, browser_id, modals, item_name,
                                  tmp_memory, expression, popups,
                                  replicas_number)


@wt(parsers.parse('user of {browser_id} creates QoS requirement with copied '
                  'storageId for "{item_name}" from file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_id_qos_requirement_in_modal(selenium, browser_id, modals, item_name,
                                    tmp_memory, popups, clipboard, displays):
    expression = 'storageId=' + clipboard.paste(display=displays[browser_id])
    replicas_number = 1

    _add_qos_requirement_in_modal(selenium, browser_id, modals, item_name,
                                  tmp_memory, expression, popups,
                                  replicas_number)


@wt(parsers.parse('user of {browser_id} creates "anyStorage \ storageId=" QoS '
                  'requirement and pastes storage id from clipboard for '
                  '"{item_name}" from file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_no_id_qos_requirement_in_modal(selenium, browser_id, modals, item_name,
                                       tmp_memory, popups, clipboard, displays):
    expression = ('anyStorage \ storageId=' +
                  clipboard.paste(display=displays[browser_id]))
    replicas_number = 1

    _add_qos_requirement_in_modal(selenium, browser_id, modals, item_name,
                                  tmp_memory, expression, popups,
                                  replicas_number)


@wt(parsers.parse('user of {browser_id} opens "Quality of Service" modal for '
                  '"{filename}" file'))
def open_qos_modal_for_file(selenium, browser_id, filename, popups, tmp_memory):
    qos = 'Quality of Service'

    click_menu_for_elem_in_browser(browser_id, filename, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, qos, popups)
    wt_wait_for_modal_to_appear(selenium, browser_id, qos, tmp_memory)


def assert_qos_file_status_in_op_gui(user, file_name, space_name, tmp_memory,
                                     selenium, oz_page, op_container, option):
    option_of_space = 'Files'
    status_type = 'QoS'
    click_on_option_of_space_on_left_sidebar_menu(selenium, user,
                                                  space_name, option_of_space,
                                                  oz_page)
    assert_browser_in_tab_in_op(selenium, user, op_container, tmp_memory)
    if option == 'has some':
        assert_status_tag_for_file_in_browser(user, status_type,
                                              file_name, tmp_memory)
    else:
        assert_not_status_tag_for_file_in_browser(user, status_type,
                                                  file_name, tmp_memory)


def delete_qos_requirement_in_op_gui(selenium, user, space_name, oz_page,
                                     modals, popups, file_name, tmp_memory,
                                     op_container):
    option1 = 'Files'
    status_type = 'QoS'
    button = 'Close'
    modal = 'Quality of Service'
    click_on_option_of_space_on_left_sidebar_menu(selenium, user,
                                                  space_name, option1,
                                                  oz_page)
    assert_browser_in_tab_in_op(selenium, user, op_container, tmp_memory)
    click_on_status_tag_for_file_in_file_browser(user, status_type,
                                                 file_name, tmp_memory)
    delete_all_qualities_of_service(selenium, user, modals, popups)
    click_modal_button(selenium, user, button, modal, modals)

