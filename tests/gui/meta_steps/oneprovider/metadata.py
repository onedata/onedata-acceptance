"""Meta steps for operations for metadata"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2017-2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.steps.modal import (
    wt_wait_for_modal_to_appear, click_modal_button)
from tests.gui.steps.oneprovider.file_browser import (
    click_menu_for_elem_in_file_browser,
    click_option_in_data_row_menu_in_file_browser)
from tests.gui.steps.oneprovider.metadata import *


@wt(parsers.re('user of (?P<browser_id>.*?) opens '
               '"(?P<modal_name>Directory metadata|File metadata)" modal '
               'for "(?P<item_name>.*?)" (directory|file)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def open_metadata_modal(selenium, browser_id, modals, modal_name,
                        item_name, tmp_memory):
    option = 'Metadata'
    click_menu_for_elem_in_file_browser(browser_id, item_name, tmp_memory)
    click_option_in_data_row_menu_in_file_browser(selenium, browser_id, option,
                                                  modals)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)


@wt(parsers.re('user of (?P<browser_id>.*?) adds basic entry with '
               'key "(?P<key_name>.*?)" and value "(?P<value>.*?)" for '
               '(?P<item>file|directory)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_basic_entry(selenium, browser_id, modals, key_name, value, item):
    if item == 'file':
        modal_name = 'File metadata'
    else:
        modal_name = 'Directory metadata'

    type_text_to_attr_input_in_new_basic_entry(selenium, browser_id, key_name,
                                               modal_name, modals)
    type_text_to_val_of_attr_in_new_basic_entry(selenium, browser_id, value,
                                                modal_name, modals,
                                                key_name)


@wt(parsers.re('user of (?P<browser_id>.*?) adds "(?P<text>.*?)" '
               '(?P<input_type>JSON|RDF) metadata '
               'for "(?P<item_name>.*?)" (?P<item>file|directory)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_json_rdf_metadata_for_item(selenium, browser_id, modals, text,
                                   input_type, item, item_name, tmp_memory):
    if item == 'file':
        modal_name = 'File metadata'
    else:
        modal_name = 'Directory metadata'
    button = 'Save all'
    open_metadata_modal(selenium, browser_id, modals, modal_name, item_name,
                        tmp_memory)
    click_on_navigation_tab_in_metadata_panel(selenium, browser_id, input_type,
                                              modal_name, modals)
    type_text_to_metadata_textarea(selenium, browser_id, text, input_type,
                                   modal_name, modals)
    click_modal_button(selenium, browser_id, button, modal_name, modals)


@wt(parsers.re('user of (?P<browser_id>.*?) opens '
               '(?P<tab>JSON|RDF) metadata '
               'tab for "(?P<item_name>.*?)" (?P<item>file|directory)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def open_json_rdf_metadata_for_item(selenium, browser_id, tab, item_name,
                                    item, modals, tmp_memory):
    if item == 'file':
        modal_name = 'File metadata'
    else:
        modal_name = 'Directory metadata'

    open_metadata_modal(selenium, browser_id, modals, modal_name, item_name,
                        tmp_memory)
    click_on_navigation_tab_in_metadata_panel(selenium, browser_id, tab,
                                              modal_name, modals)