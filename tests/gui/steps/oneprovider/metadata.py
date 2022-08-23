"""This module contains gherkin steps to run acceptance tests featuring
files metadata in oneprovider web GUI.
"""

__author__ = "Bartosz Walkowicz, Natalia Organek"
__copyright__ = "Copyright (C) 2017-2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import json
import time

from tests.gui.steps.common.miscellaneous import (
    press_tab_on_active_element, press_backspace_on_active_element)
from tests.gui.steps.modals.modal import click_modal_button
from tests.utils.bdd_utils import wt, parsers

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.generic import parse_seq
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} sees that all metadata tabs '
                  'are marked as empty'))
def assert_all_metadata_tabs_marked_empty(selenium, browser_id, modals):
    modal = modals(selenium[browser_id]).metadata
    tabs = modal.navigation
    for tab in tabs:
        assert tab.is_empty(), f'{tab} metadata tab is not empty'


@wt(parsers.parse('user of {browser_id} sees {tab_list} navigation tabs in '
                  'metadata modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def are_nav_tabs_for_metadata_panel_displayed(selenium, browser_id, tab_list,
                                              modals):
    modal = modals(selenium[browser_id]).metadata
    nav = modal.navigation
    for tab in parse_seq(tab_list):
        assert nav[tab] is not None, (
            f'no navigation tab {tab} found')


@wt(parsers.re('user of (?P<browser_id>.*?) sees that there is no basic '
               'metadata'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_no_basic_metadata_for_item(selenium, browser_id, modals):
    modal = modals(selenium[browser_id]).metadata
    assert len(modal.basic.entries) == 0, ('There is basic metadata while'
                                           ' should not be')


@wt(parsers.parse('user of {browser_id} types "{text}" to key input '
                  'box of new metadata basic entry'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_to_attr_input_in_new_basic_entry(selenium, browser_id, text,
                                               modals):
    modal = modals(selenium[browser_id]).metadata
    modal.basic.new_entry.key = text
    press_tab_on_active_element(selenium, browser_id)


@wt(parsers.parse('user of {browser_id} types "{text}" to value input '
                  'box of new metadata basic entry'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_to_val_input_in_new_basic_entry(selenium, browser_id, text,
                                              modals):
    modal = modals(selenium[browser_id]).metadata
    modal.basic.new_entry.value = text


@wt(parsers.parse('user of browser types "{text}" to value input box of '
                  'attribute "{attribute_name}" metadata basic entry'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_to_val_of_attr_in_new_basic_entry(selenium, browser_id, text,
                                                modals, attribute_name):
    modal = modals(selenium[browser_id]).metadata
    modal.basic.entries[attribute_name].value = text


@wt(parsers.parse('user of {browser_id} sees basic metadata entry '
                  'with attribute named "{attr_name}" and value "{attr_val}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_there_is_such_basic_meta_record(selenium, browser_id, attr_name,
                                           attr_val, modals):
    modal = modals(selenium[browser_id]).metadata
    err_msg = f'no metadata entry "{attr_name}" with value "{attr_val}" found'
    assert modal.basic.entries[attr_name].value == attr_val, err_msg


@wt(parsers.parse('user of {browser_id} does not see basic metadata entry '
                  'with attribute named "{attribute_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_there_is_no_such_meta_record(selenium, browser_id, attribute_name,
                                        modals):
    modal = modals(selenium[browser_id]).metadata
    err_msg = f'metadata entry {attribute_name} found while should not be'
    assert attribute_name not in modal.basic.entries, err_msg


@wt(parsers.parse('user of {browser_id} clicks on delete '
                  'icon for basic metadata entry with attribute named '
                  '"{attr_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_del_metadata_record_button(selenium, browser_id, attr_name,
                                        modals):
    modal = modals(selenium[browser_id]).metadata
    entry = modal.basic.entries[attr_name]
    entry.remove()


@wt(parsers.re('user of (?P<browser_id>.+?) types \'(?P<text>.+?)\' '
               'to (?P<tab_name>JSON|RDF) textarea in metadata modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_to_metadata_textarea(selenium, browser_id, text, tab_name,
                                   modals):
    modal = modals(selenium[browser_id]).metadata
    tab = getattr(modal, tab_name.lower())
    tab.text_area = text


@wt(parsers.re('user of (?P<browser_id>.+?) sees that (?P<tab_name>JSON|RDF) '
               'textarea in metadata modal '
               'contains \'(?P<expected_metadata>.*)\''))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_textarea_contains_record(selenium, browser_id, expected_metadata,
                                    tab_name, modals):
    modal = modals(selenium[browser_id]).metadata
    tab = getattr(modal, tab_name.lower())
    if tab_name.lower() == 'json':
        expected_metadata = json.loads(expected_metadata)
        metadata = json.loads(tab.text_area)
        err_msg = f'got {metadata} instead of expected {expected_metadata}'
        assert all(metadata.get(key, None) == value for key, value in
                   expected_metadata.items()), err_msg
    else:
        err_msg = (f'text in textarea: {tab.text_area} does not contain '
                   f'{expected_metadata} but {tab.text_area}')
        assert expected_metadata in tab.text_area, err_msg


def assert_textarea_not_contain_record(selenium, browser_id, expected_metadata,
                                       tab_name, modals):
    modal = modals(selenium[browser_id]).metadata
    tab = getattr(modal, tab_name.lower())
    assert expected_metadata not in tab.text_area


@wt(parsers.re('user of (?P<browser_id>.+?) sees that (?P<tab_name>JSON|RDF) '
               'textarea in metadata modal is empty'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_textarea_is_empty_for_metadata(selenium, browser_id, tab_name,
                                          modals):
    modal = modals(selenium[browser_id]).metadata
    tab = getattr(modal, tab_name.lower())
    err_msg = f'{tab_name} textarea is not empty'
    assert tab.text_area == '', err_msg


@wt(parsers.re('user of (?P<browser_id>.+?) cleans (?P<tab_name>JSON|RDF) '
               'textarea in metadata modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def clean_tab_textarea_in_metadata_modal(selenium, browser_id, tab_name,
                                         modals):
    modal = modals(selenium[browser_id]).metadata
    tab = getattr(modal, tab_name.lower())
    button = 'Save'
    if tab.text_area or len(tab.lines) > 1:
        while tab.text_area or len(tab.lines) > 1:
            tab.area.click()
            with tab.select_lines() as selector:
                selector.backspace_down()
                selector.backspace_down()

        # when deleting all text with backspace button does not activate
        # so the trick is that last sign is deleted after a moment
        tab.text_area = ' '
        time.sleep(0.5)
        tab.area.click()
        press_backspace_on_active_element(selenium, browser_id)
        click_metadata_modal_button(selenium, browser_id, button, modals)


@wt(parsers.parse('user of {browser_id} clicks on "{button}" button in '
                  'metadata modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_metadata_modal_button(selenium, browser_id, button, modals):
    modal_name = "Metadata"
    click_modal_button(selenium, browser_id, button, modal_name, modals)


@wt(parsers.parse('user of {browser_id} sees "{text}" label in Metadata modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def see_editor_disabled_label(browser_id, selenium, modals, text):
    driver = selenium[browser_id]
    item_status = modals(driver).metadata.editor_disabled
    assert item_status == text, f'{item_status} does not match expected {text}'

