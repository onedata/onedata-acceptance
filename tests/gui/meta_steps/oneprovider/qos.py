"""Meta steps for operations for quality of service"""

__author__ = "Michal Dronka"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.meta_steps.oneprovider.data import go_to_filebrowser
from tests.gui.steps.modal import write_name_into_text_field_in_modal
from tests.gui.steps.oneprovider.data_tab import (
    choose_option_from_selection_menu)
from tests.gui.steps.oneprovider.file_browser import (
    click_on_item_in_file_browser)
from tests.gui.steps.oneprovider.metadata import *


def _create_qos_modal(selenium, browser_id, modals, item_name, tmp_memory,
                      expression, oz_page, op_container, popups,
                      replicas_number):
    qos_option = modal = 'Quality of Service'
    add_button = 'Add Requirement'
    save_button = 'Save'
    close_button = 'Close'
    replicas_field = 'Replicas number'

    click_on_item_in_file_browser(browser_id, item_name, tmp_memory)
    choose_option_from_selection_menu(browser_id, selenium, qos_option, popups,
                                      tmp_memory)
    click_modal_button(selenium, browser_id, add_button, modal, modals)
    write_name_into_text_field_in_modal(selenium, browser_id, expression,
                                        modal, modals)
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
    _create_qos_modal(selenium, browser_id, modals, item_name, tmp_memory,
                      expression, oz_page, op_container, popups,
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
    _create_qos_modal(selenium, browser_id, modals, item_name, tmp_memory,
                      expression, oz_page, op_container, popups,
                      replicas_number)


@wt(parsers.parse('user of {browser_id} creates QoS requirement with copied '
                  'storageId for "{item_name}" from file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_id_qos_requirement_in_modal(selenium, browser_id, modals, item_name,
                                    tmp_memory, oz_page, op_container, popups,
                                    clipboard, displays):
    expression = 'storageId=' + clipboard.paste(display=displays[browser_id])
    replicas_number = 1

    _create_qos_modal(selenium, browser_id, modals, item_name, tmp_memory,
                      expression, oz_page, op_container, popups,
                      replicas_number)


@wt(parsers.parse('user of {browser_id} creates "anyStorage - storageId=" QoS '
                  'requirement and pastes storage id from clipboard for '
                  '"{item_name}" from file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_no_id_qos_requirement_in_modal(selenium, browser_id, modals, item_name,
                                       tmp_memory, oz_page, op_container,
                                       popups, clipboard, displays):
    expression = 'anyStorage - storageId=' +\
                 clipboard.paste(display=displays[browser_id])
    replicas_number = 1

    _create_qos_modal(selenium, browser_id, modals, item_name, tmp_memory,
                      expression, oz_page, op_container, popups,
                      replicas_number)
