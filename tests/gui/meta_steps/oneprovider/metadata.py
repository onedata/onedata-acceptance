"""Meta steps for operations for metadata"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2017-2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time
from typing import Any

from tests.conftest import SeleniumDrivers
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.meta_steps.oneprovider.data import (
    go_to_filebrowser,
    open_modal_for_file_browser_item,
)
from tests.gui.steps.modals.details_modal import (
    assert_tab_in_modal,
    click_on_context_menu_item,
    click_on_navigation_tab_in_panel,
)
from tests.gui.steps.modals.modal import (
    assert_error_modal_with_text_appeared,
    click_modal_button,
    click_panel_button,
)
from tests.gui.steps.oneprovider.browser import assert_status_tag_for_file_in_browser
from tests.gui.steps.oneprovider.metadata import (
    assert_no_xattrs_metadata_for_item,
    assert_textarea_contains_record,
    assert_textarea_is_empty_for_metadata,
    assert_textarea_not_contain_record,
    assert_there_is_no_such_meta_record,
    assert_there_is_such_xattr_meta_record,
    clean_tab_textarea_in_metadata_modal,
    click_on_del_metadata_record_button,
    type_text_to_attr_input_in_new_xattr_entry,
    type_text_to_metadata_textarea,
    type_text_to_val_of_attr_in_new_xattr_entry,
)
from tests.gui.utils import Modals
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.re(
        "user of (?P<browser_id>.*?) adds xattr entry with "
        'key "(?P<key_name>.*?)" and value "(?P<value>.*?)"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def add_xattr_entry(
    selenium: SeleniumDrivers, browser_id: Any, key_name: Any, value: Any
) -> Any:
    type_text_to_attr_input_in_new_xattr_entry(selenium, browser_id, key_name)
    type_text_to_val_of_attr_in_new_xattr_entry(selenium, browser_id, value, key_name)


def get_modal_name_from_item_name(item_name: Any) -> Any:
    if "file" in item_name:
        return "File details"
    return "Directory details"


@wt(
    parsers.re(
        "user of (?P<browser_id>.*?) adds and saves '(?P<text>.*?)' "
        "(?P<input_type>JSON|RDF) metadata "
        'for "(?P<item_name>.*?)"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def add_json_rdf_metadata_for_item(
    selenium: SeleniumDrivers,
    browser_id: Any,
    text: Any,
    input_type: Any,
    item_name: Any,
    tmp_memory: Any,
) -> Any:

    modal_name = get_modal_name_from_item_name(item_name.lower())
    button = "Save"
    panel = "Metadata"
    close_button = "X"

    click_on_context_menu_item(selenium, browser_id, item_name, tmp_memory, panel)
    assert_tab_in_modal(selenium, browser_id, panel, modal_name)
    click_on_navigation_tab_in_panel(selenium, browser_id, input_type, panel)
    type_text_to_metadata_textarea(selenium, browser_id, text, input_type)
    click_panel_button(selenium, browser_id, button, panel)
    click_modal_button(selenium, browser_id, close_button, modal_name)


@wt(
    parsers.re(
        "user of (?P<browser_id>.*?) opens metadata panel on "
        "(?P<tab>JSON|RDF) "
        'tab for "(?P<item_name>.*?)"(?P<dir> directory|)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def open_json_rdf_metadata_for_item(
    selenium: SeleniumDrivers,
    browser_id: Any,
    tab: Any,
    item_name: Any,
    tmp_memory: Any,
) -> Any:
    modal_name = get_modal_name_from_item_name(item_name.lower())
    option = "Metadata"
    click_on_context_menu_item(selenium, browser_id, item_name, tmp_memory, option)
    assert_tab_in_modal(selenium, browser_id, option, modal_name)
    click_on_navigation_tab_in_panel(selenium, browser_id, tab, option)


@wt(
    parsers.re(
        "user of (?P<browser_id>.*?) (?P<res>.*) to write "
        '"(?P<path>.*)" (?P<item>file|directory)'
        " (?P<tab_name>xattrs|JSON|RDF) metadata: ('|\")(?P<val>.*)('|\")"
        ' in "(?P<space>.*)"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def set_metadata_in_op_gui(
    selenium: SeleniumDrivers,
    browser_id: Any,
    path: Any,
    tmp_memory: Any,
    res: Any,
    space: Any,
    tab_name: Any,
    val: Any,
    item: Any,
) -> Any:
    modal_name = get_modal_name_from_item_name(item)
    option = "Metadata"
    button = "Save"
    close_button = "X"
    text = "Updating metadata failed"
    status_type = "metadata"

    open_modal_for_file_browser_item(
        selenium,
        browser_id,
        modal_name,
        path,
        tmp_memory,
        option,
        space,
    )
    if tab_name == "xattrs":
        attr, val = val.split("=")
        type_text_to_attr_input_in_new_xattr_entry(selenium, browser_id, attr)
        type_text_to_val_of_attr_in_new_xattr_entry(selenium, browser_id, val, attr)
    else:
        click_on_navigation_tab_in_panel(selenium, browser_id, tab_name, option)
        type_text_to_metadata_textarea(selenium, browser_id, val, tab_name)
    click_panel_button(selenium, browser_id, button, option)

    if res == "fails":
        assert_error_modal_with_text_appeared(selenium, browser_id, text)
    else:
        assert_status_tag_for_file_in_browser(browser_id, status_type, path, tmp_memory)

    click_modal_button(selenium, browser_id, close_button, modal_name)


def _assert_metadata_loading_alert(selenium: SeleniumDrivers, browser_id: Any) -> Any:
    modal = Modals(selenium[browser_id]).details_modal.metadata
    assert "Insufficient privileges" in modal.loading_alert, "resource loaded"


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) (?P<res>.*) to read "
        '"(?P<path>.*)" (?P<item>file|directory) '
        "(?P<tab_name>xattrs|JSON|RDF) "
        'metadata: "(?P<val>.*)"'
        ' in "(?P<space>.*)"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_metadata_in_op_gui(
    selenium: SeleniumDrivers,
    browser_id: Any,
    path: Any,
    tmp_memory: Any,
    res: Any,
    space: Any,
    tab_name: Any,
    val: Any,
    item: Any,
) -> Any:
    modal_name = get_modal_name_from_item_name(item)
    option = "Metadata"
    close_button = "X"

    open_modal_for_file_browser_item(
        selenium,
        browser_id,
        modal_name,
        path,
        tmp_memory,
        option,
        space,
    )
    if res == "fails":
        _assert_metadata_loading_alert(selenium, browser_id)
    else:
        if tab_name == "xattrs":
            attr, val = val.split("=")
            assert_there_is_such_xattr_meta_record(selenium, browser_id, attr, val)
        else:
            click_on_navigation_tab_in_panel(selenium, browser_id, tab_name, option)
            assert_textarea_contains_record(selenium, browser_id, val, tab_name)
    click_modal_button(selenium, browser_id, close_button, modal_name)


def assert_such_metadata_not_exist_in_op_gui(
    selenium: SeleniumDrivers,
    browser_id: Any,
    path: Any,
    tmp_memory: Any,
    space: Any,
    tab_name: Any,
    val: Any,
    item: Any,
) -> Any:
    modal_name = get_modal_name_from_item_name(item)
    option = "Metadata"
    details_modal = "Details modal"
    x_button = "X"

    open_modal_for_file_browser_item(
        selenium,
        browser_id,
        modal_name,
        path,
        tmp_memory,
        option,
        space,
    )

    if tab_name == "xattrs":
        attr, val = val.split("=")
        assert_there_is_no_such_meta_record(selenium, browser_id, attr)
    else:
        click_on_navigation_tab_in_panel(selenium, browser_id, tab_name, option)
        assert_textarea_not_contain_record(selenium, browser_id, val, tab_name)
    click_modal_button(selenium, browser_id, x_button, details_modal)


def remove_all_xattrs_metadata(selenium: SeleniumDrivers, browser_id: Any) -> Any:
    button = "Save"
    panel = "Metadata"
    modal = Modals(selenium[browser_id]).details_modal.metadata
    if len(modal.xattrs.entries) > 0:
        while len(modal.xattrs.entries) > 0:
            modal.xattrs.entries[0].remove()
            time.sleep(0.5)

        click_panel_button(selenium, browser_id, button, panel)


def remove_all_metadata_in_op_gui(
    selenium: SeleniumDrivers,
    browser_id: Any,
    space: Any,
    tmp_memory: Any,
    path: Any,
    item: Any,
) -> Any:
    modal_name = get_modal_name_from_item_name(item)
    option = "Metadata"

    open_modal_for_file_browser_item(
        selenium,
        browser_id,
        modal_name,
        path,
        tmp_memory,
        option,
        space,
    )
    click_on_navigation_tab_in_panel(selenium, browser_id, "xattrs", option)
    remove_all_xattrs_metadata(selenium, browser_id)

    click_on_navigation_tab_in_panel(selenium, browser_id, "JSON", option)
    clean_tab_textarea_in_metadata_modal(selenium, browser_id, "JSON")

    click_save_button_metadata(selenium, browser_id)

    click_on_navigation_tab_in_panel(selenium, browser_id, "RDF", option)
    clean_tab_textarea_in_metadata_modal(selenium, browser_id, "RDF")
    click_save_button_metadata(selenium, browser_id)


def click_save_button_metadata(selenium: SeleniumDrivers, browser_id: Any) -> Any:
    button = "Save"
    panel = "Metadata"
    try:
        click_panel_button(selenium, browser_id, button, panel)
    except RuntimeError:
        pass


@wt(
    parsers.parse(
        "user of {browser_id} sees that there is no metadata in metadata panel"
    )
)
def assert_no_metadata_in_modal(selenium: SeleniumDrivers, browser_id: Any) -> Any:
    panel = "Metadata"

    assert_no_xattrs_metadata_for_item(selenium, browser_id)
    click_on_navigation_tab_in_panel(selenium, browser_id, "JSON", panel)
    assert_textarea_is_empty_for_metadata(selenium, browser_id, "JSON")
    click_on_navigation_tab_in_panel(selenium, browser_id, "RDF", panel)
    assert_textarea_is_empty_for_metadata(selenium, browser_id, "RDF")


@wt(
    parsers.parse(
        "user of {browser_id} removes xattr metadata entry with key "
        '"{key}" for "{path}" file in "{space}" space'
    )
)
def open_filebrowser_and_remove_meta(
    selenium: SeleniumDrivers,
    browser_id: Any,
    key: Any,
    path: Any,
    space: Any,
    tmp_memory: Any,
) -> Any:
    modal_name = "File details"
    button = "Save"
    option = "Metadata"

    go_to_filebrowser(selenium, browser_id, tmp_memory, space)
    open_modal_for_file_browser_item(
        selenium,
        browser_id,
        modal_name,
        path,
        tmp_memory,
        option,
        space,
    )
    click_on_del_metadata_record_button(selenium, browser_id, key)
    click_panel_button(selenium, browser_id, button, option)
