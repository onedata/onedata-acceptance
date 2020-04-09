"""This module contains gherkin steps to run acceptance tests featuring
files metadata in oneprovider web GUI.
"""

__author__ = "Bartosz Walkowicz, Natalia Organek"
__copyright__ = "Copyright (C) 2017-2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import json

from tests.gui.steps.common.miscellaneous import (
    press_tab_on_active_element, press_backspace_on_active_element)
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import wt, parsers

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.generic import parse_seq
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} sees {tab_list} navigation tabs in '
                  '"{modal_name}" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def are_nav_tabs_for_metadata_panel_displayed(selenium, browser_id, tab_list,
                                              modal_name, modals):
    modal = getattr(modals(selenium[browser_id]), transform(modal_name))
    nav = modal.navigation
    for tab in parse_seq(tab_list):
        assert getattr(nav, tab.lower()) is not None, (
            f'no navigation tab {tab} found')


@wt(parsers.re('user of (?P<browser_id>.*?) sees that there is no basic '
               'metadata for (?P<item>file|directory)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def no_basic_metadata_for_item(selenium, browser_id, item, modals):
    if item == 'file':
        modal_name = 'File metadata'
    else:
        modal_name = 'Directory metadata'

    modal = getattr(modals(selenium[browser_id]), transform(modal_name))
    assert len(modal.basic.entries) == 0, ('There is basic metadata while'
                                           ' should not be')


@wt(parsers.parse('user of {browser_id} types "{text}" to key input '
                  'box of new metadata basic entry in "{modal_name}" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_to_attr_input_in_new_basic_entry(selenium, browser_id, text,
                                               modal_name, modals):
    modal = getattr(modals(selenium[browser_id]), transform(modal_name))
    modal.basic.new_entry.key = text
    press_tab_on_active_element(selenium, browser_id)


@wt(parsers.parse('user of {browser_id} types "{text}" to value input '
                  'box of new metadata basic entry in "{modal_name}" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_to_val_input_in_new_basic_entry(selenium, browser_id, text,
                                              modal_name, modals):
    modal = getattr(modals(selenium[browser_id]), transform(modal_name))
    modal.basic.new_entry.value = text


@wt(parsers.parse('user of browser types "{text}" to value input box of '
                  'attribute "{attribute_name}" metadata basic entry in'
                  ' "{modal_name}" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_to_val_of_attr_in_new_basic_entry(selenium, browser_id, text,
                                                modal_name, modals,
                                                attribute_name):
    modal = getattr(modals(selenium[browser_id]), transform(modal_name))
    modal.basic.entries[attribute_name].value = text


@wt(parsers.parse('user of {browser_id} sees basic metadata entry '
                  'with attribute named "{attr_name}" and value "{attr_val}" '
                  'in "{modal_name}" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_there_is_such_basic_meta_record(selenium, browser_id, attr_name,
                                           attr_val, modal_name, modals):
    modal = getattr(modals(selenium[browser_id]), transform(modal_name))
    err_msg = f'no metadata entry "{attr_name}" with value "{attr_val}" found'
    assert modal.basic.entries[attr_name].value == attr_val, err_msg


@wt(parsers.parse('user of {browser_id} does not see basic metadata entry '
                  'with attribute named "{attribute_name}" in '
                  '"{modal_name}" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_there_is_no_such_meta_record(selenium, browser_id, attribute_name,
                                        modal_name, modals):
    modal = getattr(modals(selenium[browser_id]), transform(modal_name))
    err_msg = f'metadata entry {attribute_name} found while should not be'
    assert attribute_name not in modal.basic.entries, err_msg


@wt(parsers.parse('user of {browser_id} clicks on delete basic metadata entry '
                  'icon for basic metadata entry with attribute named '
                  '"{attr_name}" in "{modal_name}" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_del_metadata_record_button(selenium, browser_id, attr_name,
                                        modal_name, modals):
    modal = getattr(modals(selenium[browser_id]), transform(modal_name))
    entry = modal.basic.entries[attr_name]
    entry.remove()


@wt(parsers.parse('user of {browser_id} clicks on {tab_name} navigation '
                  'tab in "{modal_name}" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_navigation_tab_in_metadata_panel(selenium, browser_id, tab_name,
                                              modal_name, modals):
    modal = getattr(modals(selenium[browser_id]), transform(modal_name))
    tab = getattr(modal.navigation, tab_name.lower())
    tab()


@wt(parsers.re('user of (?P<browser_id>.+?) types "(?P<text>.+?)" '
               'to (?P<tab>JSON|RDF) textarea in "(?P<modal_name>.+?)" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_to_metadata_textarea(selenium, browser_id, text, tab, modal_name,
                                   modals):
    modal = getattr(modals(selenium[browser_id]), transform(modal_name))
    tab = getattr(modal, tab.lower())
    tab.text_area = text


@wt(parsers.re('user of (?P<browser_id>.+?) sees that (?P<tab_name>JSON|RDF) '
               'textarea in "(?P<modal_name>.+?)" modal '
               'contains (?P<expected_metadata>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_textarea_contains_record(selenium, browser_id, expected_metadata,
                                    tab_name, modal_name, modals):
    modal = getattr(modals(selenium[browser_id]), transform(modal_name))
    tab = getattr(modal, tab_name.lower())
    if tab_name.lower() == 'json':
        expected_metadata = json.loads(expected_metadata)
        metadata = json.loads(tab.text_area)
        err_msg = f'got {metadata} instead of expected {expected_metadata}'
        assert all(metadata.get(key, None) == value for key, value in
                   expected_metadata.items()), err_msg
    else:
        err_msg = (f'text in textarea: {tab.text_area} does not contain '
                   f'{expected_metadata}')
        assert expected_metadata in tab.text_area, err_msg


@wt(parsers.re('user of (?P<browser_id>.+?) sees that (?P<tab_name>JSON|RDF) '
               'textarea in "(?P<modal_name>.+?)" modal is empty'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_textarea_is_empty_for_metadata(selenium, browser_id, tab_name,
                                          modal_name, modals):
    modal = getattr(modals(selenium[browser_id]), transform(modal_name))
    tab = getattr(modal, tab_name.lower())
    err_msg = f'{tab_name} textarea is not empty'
    assert tab.text_area == '', err_msg


@wt(parsers.re('user of (?P<browser_id>.+?) cleans (?P<tab_name>JSON|RDF) '
               'textarea in "(?P<modal_name>.+?)" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def clean_tab_textarea_in_metadata_modal(selenium, browser_id, tab_name,
                                         modal_name, modals):
    modal = getattr(modals(selenium[browser_id]), transform(modal_name))
    tab = getattr(modal, tab_name.lower())
    tab.text_area = ' '
    press_backspace_on_active_element(selenium, browser_id)


@wt(parsers.parse('user of {browser_id} sees that "{button_name}" button '
                  'in "{modal_name}" modal is disabled'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_btn_disabled_in_metadata_footer(selenium, browser_id, button_name,
                                           modal_name, modals):
    modal = getattr(modals(selenium[browser_id]), transform(modal_name))
    btn = getattr(modal, button_name.lower().replace(' ', '_'))
    assert not btn.is_enabled()


@wt(parsers.re('user of (?P<browser_id>.+?) sees that (?P<tab_name>JSON|RDF) '
               'textarea is highlighted as invalid '
               'in "(?P<modal_name>.+?)" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_entered_json_rdf_is_invalid(selenium, browser_id, modals, modal_name,
                                       tab_name):
    modal = getattr(modals(selenium[browser_id]), transform(modal_name))
    entry = getattr(modal, transform(tab_name))
    assert entry.is_invalid(), 'Entry is valid but should not be'
