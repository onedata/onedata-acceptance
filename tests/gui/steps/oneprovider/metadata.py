"""This module contains gherkin steps to run acceptance tests featuring
files metadata in oneprovider web GUI.
"""

__author__ = "Bartosz Walkowicz, Natalia Organek"
__copyright__ = "Copyright (C) 2017-2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
import time

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import press_tab_on_active_element
from tests.gui.utils import Modals
from tests.gui.utils.common.modals.files_modals.tabs_in_details_modal.metadata_tab import (
    XattrMetadataEntry,
)
from tests.gui.utils.generic import parse_elements_sequence
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        "user of {browser_id} sees that all metadata tabs are marked as empty"
    )
)
def assert_all_metadata_tabs_marked_empty(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    modal = Modals(selenium[browser_id]).details_modal.metadata
    tabs = modal.navigation
    for tab in tabs:
        assert tab.is_empty(), f"{tab} metadata tab is not empty"


@wt(
    parsers.parse(
        "user of {browser_id} sees {tab_list:ElementsSequence} navigation tabs in"
        " metadata panel",
        extra_types={"ElementsSequence": parse_elements_sequence},
    ),
)
@repeat_failed(timeout=WAIT_FRONTEND)
def are_nav_tabs_for_metadata_panel_displayed(
    selenium: SeleniumDrivers, browser_id: str, tab_list: list[str]
) -> None:
    modal = Modals(selenium[browser_id]).details_modal.metadata
    nav = modal.navigation
    for tab in tab_list:
        assert nav[tab] is not None, f"no navigation tab {tab} found"


@wt(parsers.re(r"user of (?P<browser_id>.*?) sees that there is no xattrs metadata"))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_no_xattrs_metadata_for_item(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    modal = Modals(selenium[browser_id]).details_modal.metadata
    assert (
        len(modal.xattrs.entries) == 0
    ), "There is xattrs metadata while should not be"


@wt(
    parsers.parse(
        'user of {browser_id} types "{text}" to key input '
        "box of new metadata xattr entry"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_to_attr_input_in_new_xattr_entry(
    selenium: SeleniumDrivers, browser_id: str, text: str
) -> None:
    modal = Modals(selenium[browser_id]).details_modal.metadata
    modal.xattrs.new_entry.key = text
    press_tab_on_active_element(selenium, browser_id)


@wt(
    parsers.parse(
        'user of {browser_id} types "{text}" to value input '
        "box of new metadata xattr entry"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_to_val_input_in_new_xattr_entry(
    selenium: SeleniumDrivers, browser_id: str, text: str
) -> None:
    modal = Modals(selenium[browser_id]).details_modal.metadata
    modal.xattrs.new_entry.value = text


@wt(
    parsers.parse(
        'user of {browser_id} types "{text}" to value input box of '
        'attribute "{attribute_name}" metadata xattr entry'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_to_val_of_attr_in_new_xattr_entry(
    selenium: SeleniumDrivers, browser_id: str, text: str, attribute_name: str
) -> None:
    modal = Modals(selenium[browser_id]).details_modal.metadata
    modal.xattrs.entries[attribute_name].value = text


@wt(
    parsers.parse(
        "user of {browser_id} sees xattr metadata entry "
        'with key "{attr_key}" and value "{attribute_value}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_there_is_such_xattr_meta_record(
    selenium: SeleniumDrivers, browser_id: str, attr_key: str, attribute_value: str
) -> None:
    attribute_value = attribute_value.lower()
    modal = Modals(selenium[browser_id]).details_modal.metadata
    error_message = (
        f'no metadata entry "{attr_key}" with value "{attribute_value}" found'
    )
    assert (
        modal.xattrs.entries[attr_key].value.lower() == attribute_value
    ), error_message


@wt(
    parsers.parse(
        'user of {browser_id} does not see xattr metadata entry with key "{key_name}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_there_is_no_such_meta_record(
    selenium: SeleniumDrivers, browser_id: str, key_name: str
) -> None:
    modal = Modals(selenium[browser_id]).details_modal.metadata
    error_message = f"metadata entry {key_name} found while should not be"
    assert key_name not in modal.xattrs.entries, error_message


@wt(
    parsers.parse(
        "user of {browser_id} clicks on delete "
        "icon for xattr metadata entry with key "
        '"{attr_name}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_del_metadata_record_button(
    selenium: SeleniumDrivers, browser_id: str, attr_name: str
) -> None:
    modal = Modals(selenium[browser_id]).details_modal.metadata
    entry = modal.xattrs.entries[attr_name]
    entry.remove()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) types '(?P<text>.+?)' "
        r"to (?P<tab_name>JSON|RDF) textarea in metadata panel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_to_metadata_textarea(
    selenium: SeleniumDrivers, browser_id: str, text: str, tab_name: str
) -> None:
    modal = Modals(selenium[browser_id]).details_modal.metadata
    tab = getattr(modal, tab_name.lower())
    tab.text_area = text


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that (?P<tab_name>JSON|RDF) "
        r"textarea in metadata panel "
        r"contains '(?P<expected_metadata>.*)'"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_textarea_contains_record(
    selenium: SeleniumDrivers,
    browser_id: str,
    expected_metadata: str,
    tab_name: str,
) -> None:
    modal = Modals(selenium[browser_id]).details_modal.metadata
    tab = getattr(modal, tab_name.lower())
    if tab_name.lower() == "json":
        parsed_expected_metadata = json.loads(expected_metadata)
        metadata = json.loads(tab.text_area)
        error_message = f"got {metadata} instead of expected {parsed_expected_metadata}"
        assert all(
            metadata.get(key, None) == value
            for key, value in parsed_expected_metadata.items()
        ), error_message
    else:
        error_message = (
            f"text in textarea: {tab.text_area} does not contain "
            f"{expected_metadata} but {tab.text_area}"
        )
        assert expected_metadata in tab.text_area, error_message


def assert_textarea_not_contain_record(
    selenium: SeleniumDrivers,
    browser_id: str,
    expected_metadata: str,
    tab_name: str,
) -> None:
    modal = Modals(selenium[browser_id]).details_modal.metadata
    tab = getattr(modal, tab_name.lower())
    assert expected_metadata not in tab.text_area


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that (?P<tab_name>JSON|RDF) "
        r"textarea in metadata panel is empty"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_textarea_is_empty_for_metadata(
    selenium: SeleniumDrivers, browser_id: str, tab_name: str
) -> None:
    modal = Modals(selenium[browser_id]).details_modal.metadata
    tab = getattr(modal, tab_name.lower())
    error_message = f"{tab_name} textarea is not empty"
    assert tab.text_area == "", error_message


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) cleans (?P<tab_name>JSON|RDF) "
        r"textarea in metadata panel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def clean_tab_textarea_in_metadata_modal(
    selenium: SeleniumDrivers, browser_id: str, tab_name: str
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).details_modal.metadata
    tab = getattr(modal, tab_name.lower())
    tab.clear_editor(tab_name.lower())


@wt(parsers.parse('user of {browser_id} sees "{text}" label in metadata panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def see_editor_disabled_label(
    browser_id: str, selenium: SeleniumDrivers, text: str
) -> None:
    driver = selenium[browser_id]
    item_status = Modals(driver).details_modal.metadata.editor_disabled
    assert item_status == text, f"{item_status} does not match expected {text}"


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) modifies (?P<entry_elem>key|value)"
        r' field by typing "(?P<new_text>.*)" for exisiting'
        r' xattr metadata entry with "(?P<attr_name>.*)" key'
    )
)
def modify_existing_xattr_entry(
    selenium: SeleniumDrivers,
    browser_id: str,
    entry_elem: str,
    new_text: str,
    attr_name: str,
) -> None:
    driver = selenium[browser_id]
    modal = Modals(driver).details_modal.metadata
    entry_elem = entry_elem.lower()
    entry = modal.xattrs.entries[attr_name]

    if entry_elem == "key":
        edit_xattr_entry_key(entry, new_text)
    elif entry_elem == "value":
        entry.value = new_text

    modal.xattrs.click_on_background_in_xattrs_panel()


def edit_xattr_entry_key(entry: XattrMetadataEntry, new_key: str) -> None:
    entry.edit_existing_key.click()
    time.sleep(0.5)
    # this sleep is necessary, because there is small delay between
    # clicking edit icon and user being able to write new key
    entry.press_backspace_to_delete_selected()
    entry.edit_key = new_key
