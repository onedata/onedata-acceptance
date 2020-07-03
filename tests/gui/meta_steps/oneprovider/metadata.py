"""Meta steps for operations for metadata"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2017-2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.meta_steps.oneprovider.data import (
    open_modal_for_file_browser_item)
from tests.gui.steps.modal import (
    wt_wait_for_modal_to_appear, assert_error_modal_with_text_appeared)
from tests.gui.steps.oneprovider.file_browser import (
    click_menu_for_elem_in_file_browser,
    click_option_in_data_row_menu_in_file_browser,
    assert_status_tag_for_file_in_file_browser)
from tests.gui.steps.oneprovider.metadata import *


@wt(parsers.parse('user of {browser_id} opens "{modal_name}" metadata modal '
                  'for "{item_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def open_metadata_modal(selenium, browser_id, modals, modal_name, item_name,
                        tmp_memory):
    option = 'Metadata'

    click_menu_for_elem_in_file_browser(browser_id, item_name, tmp_memory)
    click_option_in_data_row_menu_in_file_browser(selenium, browser_id, option,
                                                  modals)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)


@wt(parsers.re('user of (?P<browser_id>.*?) adds basic entry with '
               'key "(?P<key_name>.*?)" and value "(?P<value>.*?)"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_basic_entry(selenium, browser_id, modals, key_name, value):
    type_text_to_attr_input_in_new_basic_entry(selenium, browser_id, key_name,
                                               modals)
    type_text_to_val_of_attr_in_new_basic_entry(selenium, browser_id, value,
                                                modals, key_name)


@wt(parsers.re('user of (?P<browser_id>.*?) adds and saves \'(?P<text>.*?)\' '
               '(?P<input_type>JSON|RDF) metadata '
               'for "(?P<item_name>.*?)"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_json_rdf_metadata_for_item(selenium, browser_id, modals, text,
                                   input_type, item_name, tmp_memory):
    if 'file' in item_name.lower():
        modal_name = 'File metadata'
    else:
        modal_name = 'Directory metadata'
    button = 'Save all'

    open_metadata_modal(selenium, browser_id, modals, modal_name, item_name,
                        tmp_memory)
    click_on_navigation_tab_in_metadata_modal(selenium, browser_id, input_type,
                                              modals)
    type_text_to_metadata_textarea(selenium, browser_id, text, input_type,
                                   modals)
    click_metadata_modal_button(selenium, browser_id, button, modals)


@wt(parsers.re('user of (?P<browser_id>.*?) opens metadata modal on '
               '(?P<tab>JSON|RDF) '
               'tab for "(?P<item_name>.*?)"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def open_json_rdf_metadata_for_item(selenium, browser_id, tab, item_name,
                                    modals, tmp_memory):
    if 'file' in item_name.lower():
        modal_name = 'File metadata'
    else:
        modal_name = 'Directory metadata'

    open_metadata_modal(selenium, browser_id, modals, modal_name, item_name,
                        tmp_memory)
    click_on_navigation_tab_in_metadata_modal(selenium, browser_id, tab, modals)


@wt(parsers.re('user of (?P<browser_id>.*?) (?P<res>.*) to write '
               '"(?P<path>.*)" (?P<item>file|directory)'
               ' (?P<tab_name>basic|JSON|RDF) metadata: "(?P<val>.*)"'
               ' in "(?P<space>.*)"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def set_metadata_in_op_gui(selenium, browser_id, path, tmp_memory, op_container,
                           res, space, tab_name, val, modals, oz_page, item):
    if item == 'file':
        modal_name = 'File metadata'
    else:
        modal_name = 'Directory metadata'

    option = 'Metadata'
    button = 'Save all'
    text = 'Updating metadata failed'
    status_type = 'metadata'

    open_modal_for_file_browser_item(selenium, browser_id, modals, modal_name,
                                     path, tmp_memory, option, space, oz_page,
                                     op_container)
    if tab_name == "basic":
        attr, val = val.split('=')
        type_text_to_attr_input_in_new_basic_entry(selenium, browser_id, attr,
                                                   modals)
        type_text_to_val_of_attr_in_new_basic_entry(selenium, browser_id, val,
                                                    modals, attr)
    else:
        click_on_navigation_tab_in_metadata_modal(selenium, browser_id,
                                                  tab_name, modals)
        type_text_to_metadata_textarea(selenium, browser_id, val, tab_name,
                                       modals)
    click_metadata_modal_button(selenium, browser_id, button, modals)

    if res == 'fails':
        assert_error_modal_with_text_appeared(selenium, browser_id, text)
    else:
        assert_status_tag_for_file_in_file_browser(browser_id, status_type,
                                                   path, tmp_memory)


def _assert_metadata_loading_alert(selenium, browser_id, modals):
    modal = modals(selenium[browser_id]).metadata
    assert 'Insufficient permissions' in modal.loading_alert, (
        "resource loaded")


@wt(parsers.re('user of (?P<browser_id>.*) (?P<res>.*) to read '
               '"(?P<path>.*)" (?P<item>file|directory) '
               '(?P<tab_name>basic|JSON|RDF) '
               'metadata: "(?P<val>.*)"'
               ' in "(?P<space>.*)"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_metadata_in_op_gui(selenium, browser_id, path, tmp_memory,
                              op_container, res, space, tab_name, val, modals,
                              oz_page, item):
    if item == 'file':
        modal_name = 'File metadata'
    else:
        modal_name = 'Directory metadata'

    option = 'Metadata'

    open_modal_for_file_browser_item(selenium, browser_id, modals, modal_name,
                                     path, tmp_memory, option, space, oz_page,
                                     op_container)
    if res == 'fails':
        _assert_metadata_loading_alert(selenium, browser_id, modals)
    else:
        if tab_name == 'basic':
            attr, val = val.split('=')
            assert_there_is_such_basic_meta_record(selenium, browser_id, attr,
                                                   val, modals)
        else:
            click_on_navigation_tab_in_metadata_modal(selenium, browser_id,
                                                      tab_name,
                                                      modals)
            assert_textarea_contains_record(selenium, browser_id, val, tab_name,
                                            modals)
    click_metadata_modal_button(selenium, browser_id, 'Close', modals)


def assert_such_metadata_not_exist_in_op_gui(selenium, browser_id, path, tmp_memory,
                                             op_container, space, tab_name, val, modals,
                                             oz_page, item):
    if item == 'file':
        modal_name = 'File metadata'
    else:
        modal_name = 'Directory metadata'

    option = 'Metadata'

    open_modal_for_file_browser_item(selenium, browser_id, modals, modal_name,
                                     path, tmp_memory, option, space, oz_page,
                                     op_container)

    if tab_name == 'basic':
        attr, val = val.split('=')
        assert_there_is_no_such_meta_record(selenium, browser_id, attr,
                                            modals)
    else:
        click_on_navigation_tab_in_metadata_modal(selenium, browser_id, tab_name,
                                                  modals)
        assert_textarea_not_contain_record(selenium, browser_id, val,
                                           tab_name, modals)
    click_metadata_modal_button(selenium, browser_id, 'Close', modals)


def remove_all_basic_metadata(selenium, browser_id, modals):
    modal = modals(selenium[browser_id]).metadata
    while len(modal.basic.entries) > 0:
        modal.basic.entries[0].remove()


def remove_all_metadata_in_op_gui(selenium, browser_id, space, op_container,
                                  tmp_memory, path, oz_page, modals, item):
    if item == 'file':
        modal_name = 'File metadata'
    else:
        modal_name = 'Directory metadata'

    option = 'Metadata'
    button = 'Save all'

    open_modal_for_file_browser_item(selenium, browser_id, modals, modal_name,
                                     path, tmp_memory, option, space, oz_page,
                                     op_container)
    click_on_navigation_tab_in_metadata_modal(selenium, browser_id, 'Basic',
                                              modals)
    remove_all_basic_metadata(selenium, browser_id, modals)
    click_on_navigation_tab_in_metadata_modal(selenium, browser_id, 'JSON',
                                              modals)
    clean_tab_textarea_in_metadata_modal(selenium, browser_id, 'JSON', modals)
    click_on_navigation_tab_in_metadata_modal(selenium, browser_id, 'RDF',
                                              modals)
    clean_tab_textarea_in_metadata_modal(selenium, browser_id, 'RDF', modals)
    click_metadata_modal_button(selenium, browser_id, button, modals)


@wt(parsers.parse('user of {browser_id} sees that there is no metadata '
                  'in metadata modal'))
def assert_no_metadata_in_modal(selenium, browser_id, modals):
    assert_no_basic_metadata_for_item(selenium, browser_id, modals)
    click_on_navigation_tab_in_metadata_modal(selenium, browser_id, 'JSON',
                                              modals)
    assert_textarea_is_empty_for_metadata(selenium, browser_id, 'JSON', modals)
    click_on_navigation_tab_in_metadata_modal(selenium, browser_id, 'RDF',
                                              modals)
    assert_textarea_is_empty_for_metadata(selenium, browser_id, 'RDF', modals)
