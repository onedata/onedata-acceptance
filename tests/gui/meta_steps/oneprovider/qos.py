"""Meta steps for operations for quality of service"""

__author__ = "Michal Dronka"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.steps.modal import write_name_into_text_field_in_modal
from tests.gui.steps.oneprovider.data_tab import \
    assert_file_browser_in_data_tab_in_op, choose_option_from_selection_menu
from tests.gui.steps.oneprovider.file_browser import \
    click_on_item_in_file_browser
from tests.gui.steps.oneprovider.metadata import *
from tests.gui.steps.onezone.spaces import \
    click_element_on_lists_on_left_sidebar_menu, \
    click_on_option_of_space_on_left_sidebar_menu


@wt(parsers.parse('user of {browser_id} creates "{expression}" quality of '
                  'service for "{item_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_qos_modal(selenium, browser_id, modals, item_name, tmp_memory,
                     expression, oz_page, op_container, popups):
    option = 'spaces'
    space_name = 'space1'
    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id, option,
                                                space_name, oz_page)
    option = 'Data'
    click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                  space_name, option, oz_page)
    item_browser = 'file browser'
    assert_file_browser_in_data_tab_in_op(selenium, browser_id, op_container,
                                          tmp_memory, item_browser)
    click_on_item_in_file_browser(browser_id, item_name, tmp_memory)
    option = modal = 'Quality of Service'
    choose_option_from_selection_menu(browser_id, selenium, option, popups,
                                      tmp_memory)
    button = 'Add Requirement'
    click_modal_button(selenium, browser_id, button, modal, modals)
    write_name_into_text_field_in_modal(selenium, browser_id, expression,
                                        modal, modals)
    button = 'Save'
    click_modal_button(selenium, browser_id, button, modal, modals)
    button = 'CLose'
    click_modal_button(selenium, browser_id, button, modal, modals)


@wt(parsers.parse('user of {browser_id} creates {replicas_number} replicas of '
                  '"{expression}" quality of service for "{item_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_qos_modal_with_replicas(selenium, browser_id, modals, item_name,
                                   tmp_memory, expression, oz_page,
                                   op_container, popups, replicas_number):
    option = 'spaces'
    space_name = 'space1'
    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id, option,
                                                space_name, oz_page)
    option = 'Data'
    click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                  space_name, option, oz_page)
    item_browser = 'file browser'
    assert_file_browser_in_data_tab_in_op(selenium, browser_id, op_container,
                                          tmp_memory, item_browser)
    click_on_item_in_file_browser(browser_id, item_name, tmp_memory)
    option = modal = 'Quality of Service'
    choose_option_from_selection_menu(browser_id, selenium, option, popups,
                                      tmp_memory)
    button = 'Add Requirement'
    click_modal_button(selenium, browser_id, button, modal, modals)
    write_name_into_text_field_in_modal(selenium, browser_id, expression,
                                        modal, modals)
    text_area = 'Replicas number'
    write_name_into_text_field_in_modal(selenium, browser_id, replicas_number,
                                        modal, modals, text_area)
    button = 'Save'
    click_modal_button(selenium, browser_id, button, modal, modals)
    button = 'CLose'
    click_modal_button(selenium, browser_id, button, modal, modals)


@wt(parsers.parse('user of {browser_id} copies storageId quality of service '
                  'from clipboard for "{item_name}" from file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_qos_modal(selenium, browser_id, modals, item_name, tmp_memory,
                     oz_page, op_container, popups, clipboard, displays):
    click_on_item_in_file_browser(browser_id, item_name, tmp_memory)
    option = modal = 'Quality of Service'
    choose_option_from_selection_menu(browser_id, selenium, option, popups,
                                      tmp_memory)
    button = 'Add Requirement'
    click_modal_button(selenium, browser_id, button, modal, modals)
    expression = 'storageId=' + clipboard.paste(display=displays[browser_id])
    write_name_into_text_field_in_modal(selenium, browser_id, expression,
                                        modal, modals)
    button = 'Save'
    click_modal_button(selenium, browser_id, button, modal, modals)
    button = 'CLose'
    click_modal_button(selenium, browser_id, button, modal, modals)


@wt(parsers.parse('user of {browser_id} creates anyStorage quality of service '
                  'excluding storage from clipboard for "{item_name}" '
                  'from file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_qos_modal(selenium, browser_id, modals, item_name, tmp_memory,
                     oz_page, op_container, popups, clipboard, displays):
    click_on_item_in_file_browser(browser_id, item_name, tmp_memory)
    option = modal = 'Quality of Service'
    choose_option_from_selection_menu(browser_id, selenium, option, popups,
                                      tmp_memory)
    button = 'Add Requirement'
    click_modal_button(selenium, browser_id, button, modal, modals)
    expression = 'anyStorage - storageId=' +\
                 clipboard.paste(display=displays[browser_id])
    write_name_into_text_field_in_modal(selenium, browser_id, expression,
                                        modal, modals)
    button = 'Save'
    click_modal_button(selenium, browser_id, button, modal, modals)
    button = 'CLose'
    click_modal_button(selenium, browser_id, button, modal, modals)