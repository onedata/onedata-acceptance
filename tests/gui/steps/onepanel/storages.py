"""This module contains gherkin steps to run acceptance tests featuring
storages management in onepanel web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from functools import partial

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.utils.common.constants import CONFLICT_NAME_SEPARATOR
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        "user of {browser_id} selects {storage_type} from storage "
        "selector in storages page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_select_storage_type_in_storage_page_op_panel(
    selenium, browser_id, storage_type, onepanel, popups
):
    storage_selector = onepanel(
        selenium[browser_id]
    ).content.storages.form.storage_selector
    storage_selector.expand()
    storage_selector_list = popups(selenium[browser_id]).dropdown

    for storage in storage_selector_list.options:
        if storage.text.lower() == storage_type.lower():
            storage_selector_list.options[storage.text].click()
            return
    raise RuntimeError(f"storage {storage_type} not found")


@wt(
    parsers.re(
        'user of (?P<browser_id>.*?) types "(?P<text>.*?)" to '
        "(?P<input_box>.*?) field in (?P<form>.*?) form "
        "in storages page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_text_to_in_box_in_storages_page_op_panel(
    selenium, browser_id, text, form, onepanel, input_box
):
    form = getattr(
        onepanel(selenium[browser_id]).content.storages.form, transform(form)
    )
    setattr(form, transform(input_box), text)


@wt(
    parsers.re(
        'user of (?P<browser_id>.*?) checks "(?P<option>.*?)" in '
        "Storage path type field in (?P<form>.*?) form "
        "in storages page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_check_option_in_box_in_storages_page_op_panel(
    selenium, browser_id, option, form, onepanel
):
    form = getattr(
        onepanel(selenium[browser_id]).content.storages.form, transform(form)
    )
    getattr(form.storage_path_type, option).click()


def enable_import_in_add_storage_form(selenium, browser_id, onepanel):
    form = onepanel(selenium[browser_id]).content.storages.form
    form.posix.imported_storage.check()


@wt(
    parsers.parse(
        "user of {browser_id} clicks on Add button in add storage "
        "form in storages page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_add_btn_in_storage_add_form_in_storage_page(
    selenium, browser_id, onepanel
):
    onepanel(selenium[browser_id]).content.storages.form.add()


@wt(
    parsers.parse(
        'user of {browser_id} expands "{storage}" record on '
        "storages list in storages page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def wt_expand_storage_item_in_storages_page_op_panel(
    selenium, browser_id, storage, onepanel
):
    storage_item = onepanel(selenium[browser_id]).content.storages.storages[storage]
    storage_item.expand()

    if not storage_item.is_expanded():
        raise RuntimeError(f"did not manage to expand storage {storage}")


@wt(
    parsers.re(
        'user of (?P<browser_id>.*?) sees that "(?P<storage>.*?)" '
        "(?P<attr>.*?) is (?P<val>.*?) "
        "in storages page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def wt_assert_storage_attr_in_storages_page_op_panel(
    selenium, browser_id, storage, attr, val, onepanel
):
    storages = onepanel(selenium[browser_id]).content.storages.storages
    displayed_val = getattr(storages[storage], transform(attr)).lower()
    assert (
        displayed_val == val.lower()
    ), f"got {displayed_val} as storage's {attr} instead of expected {val}"


@wt(
    parsers.parse(
        'user of {browser_id} expands toolbar for "{name}" storage '
        "record in Storages page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def wt_expands_toolbar_for_storage_in_onepanel(selenium, browser_id, name, onepanel):
    driver = selenium[browser_id]
    onepanel(driver).content.storages.storages[name].expand_menu(driver)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) clicks on "
        r"(?P<option>Remove storage backend) "
        r"option in storage's toolbar in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_btn_in_storage_toolbar_in_panel(selenium, browser_id, option, popups):
    toolbar = popups(selenium[browser_id]).toolbar
    if toolbar.is_displayed():
        toolbar.options[option].click()
    else:
        raise RuntimeError("no storage toolbar found in Onepanel")


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "Modify" button for '
        '"{name}" storage record in Storages page in Onepanel'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def click_modify_storage_in_onepanel(selenium, browser_id, name, onepanel):
    driver = selenium[browser_id]
    onepanel(driver).content.storages.storages[name].click()
    onepanel(driver).content.storages.storages[name].modify()


@wt(
    parsers.parse(
        'user of {browser_id} types "{in_value}" into last key in '
        "posix QoS parameters form in storage edit page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def type_key_in_posix_storage_edit_page(selenium, browser_id, key, onepanel):
    driver = selenium[browser_id]
    storage_posix = onepanel(driver).content.storages.storages["posix"]
    storage_posix.edit_form.posix_editor.params.set_last_key(key)


@wt(
    parsers.parse(
        "user of {browser_id} clicks value of modified record in "
        "QoS parameters form in posix storage edit page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_value_in_posix_storage_edit_page(selenium, browser_id, onepanel):
    driver = selenium[browser_id]
    storage_posix = onepanel(driver).content.storages.storages["posix"]
    storage_posix.edit_form.posix_editor.params.click_value_in_modified_record()


@wt(
    parsers.parse(
        "user of {browser_id} deletes first additional param "
        "in QoS parameters form in posix storage edit page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def delete_additional_param_in_posix_storage_edit_page(selenium, browser_id, onepanel):
    driver = selenium[browser_id]
    storage_posix = onepanel(driver).content.storages.storages["posix"]
    storage_posix.edit_form.posix_editor.params.delete_first_additional_param()


@wt(parsers.parse("user of {browser_id} saves changes in posix storage edit page"))
@repeat_failed(timeout=WAIT_FRONTEND)
def save_changes_in_posix_storage_edit_page(selenium, browser_id, onepanel):
    driver = selenium[browser_id]
    storage = onepanel(driver).content.storages.storages["posix"]
    storage.edit_form.posix_editor.save_button.click()


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{name}" has disappeared from the storages list'
    )
)
@wt(parsers.parse('user of {browser_id} does not see "{name}" on the storages list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_storage_disappeared_from_list(selenium, browser_id, name, onepanel):
    driver = selenium[browser_id]
    storages_list = onepanel(driver).content.storages.storages
    assert name not in storages_list, f"found {name} on storages list"


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{name}" is visible on the storages list'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_storage_on_storage_list(selenium, browser_id, name, onepanel):
    assert is_storage_on_storage_list(
        selenium, browser_id, name, onepanel
    ), f"{name} not visible on storages list"


def is_storage_on_storage_list(selenium, browser_id, name, onepanel):
    driver = selenium[browser_id]
    storages_list = onepanel(driver).content.storages.storages
    return name in storages_list


# if there are repeated ids, set will be shorter than list
def check_ids_different(id_list):
    ids_set = set(id_list)
    return len(ids_set) == len(id_list)


@wt(
    parsers.parse(
        'user of {browser_id} types "{name}" to {input_box} field '
        'in {storage_type} edit form for "{storage}" storage in Onepanel'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def type_name_to_form_in_storages_page(
    selenium, browser_id, name, input_box, onepanel, storage_type, storage
):
    driver = selenium[browser_id]
    form = getattr(
        onepanel(driver).content.storages.storages[storage].edit_form,
        f"{storage_type.lower()}_editor",
    )
    # breakpoint()
    setattr(form, transform(input_box), name)


@wt(
    parsers.parse(
        "user of {browser_id} clicks on {name} button in edit form "
        'for "{storage}" storage in Onepanel'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_button_in_edit_form(selenium, browser_id, name, onepanel, storage):
    driver = selenium[browser_id]
    button = name.lower() + "_button"
    getattr(
        onepanel(driver).content.storages.storages[storage].edit_form.posix_editor,
        button,
    )()


@wt(
    parsers.parse(
        'user of {browser_id} copies id of "{storage_name}" storage '
        "to clipboard via copy button"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_storage_id_to_clipboard(selenium, browser_id, storage_name, onepanel):
    driver = selenium[browser_id]
    onepanel(driver).content.storages.storages[storage_name].copy_id_button()


def scroll_and_call_and_assert(selenium, browser_id, onepanel, inner_func, assert_func):
    driver = selenium[browser_id]
    seen_rows_names = set()
    stop_scrolling_flag = False

    while not stop_scrolling_flag:

        new_storages_list = onepanel(driver).content.storages.storages
        new_storages_names = [storage.name for storage in new_storages_list]

        not_yet_seen_rows = [
            storage
            for storage in new_storages_list
            if storage.name not in seen_rows_names
        ]
        stop_scrolling_flag = len(not_yet_seen_rows) == 0

        output_inner_function = inner_func(new_rows=not_yet_seen_rows)
        if output_inner_function:
            return

        seen_rows_names.update(new_storages_names)
        onepanel(driver).content.storages.scroll_by_press_space()

    assert_func(rows_names_set=seen_rows_names)


@wt(
    parsers.parse(
        "user of {browser_id} collapses first expanded storage backend with name"
        ' "{name}" in Storages page in Onepanel'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_storage(selenium, browser_id, name, onepanel):

    def get_rows_with_name_and_collapse_first(name, new_rows):
        rows_with_name = [
            row
            for row in new_rows
            if row.name.split(CONFLICT_NAME_SEPARATOR)[0] == name
        ]
        for row in rows_with_name:
            if row.is_expanded():
                row.click_toggle()
                return True
        return False

    def assert_no_rows_with_name(name: str, rows_names_set: set):
        raise AssertionError(f"No row with name '{name}' found")

    call_func = partial(get_rows_with_name_and_collapse_first, name=name)
    assert_func = partial(assert_no_rows_with_name, name=name)
    scroll_and_call_and_assert(selenium, browser_id, onepanel, call_func, assert_func)


@wt(
    parsers.parse(
        'user of {browser_id} sees {number} storages named "{name}" '
        "with different IDs on the storages list"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_number_storages_with_same_name(
    selenium, browser_id, name, onepanel, number: int
):
    def help_func(new_rows):
        return (
            len(new_rows) < 0
        )  # For the static analyzer to pass, always returns False

    def assert_number_entries_with_name(name: str, number: int, rows_names_set: set):
        rows_with_name = [
            row_name
            for row_name in list(rows_names_set)
            if row_name.split(CONFLICT_NAME_SEPARATOR)[0] == name
        ]
        ids = [
            row_name.split(CONFLICT_NAME_SEPARATOR)[1] for row_name in rows_with_name
        ]

        assert (
            len(rows_with_name) == number
        ), f"{name} not visible {number} times on storages list"
        assert check_ids_different(ids), f"IDs are not unique, {ids}"

    assert_func = partial(assert_number_entries_with_name, name=name, number=number)
    scroll_and_call_and_assert(selenium, browser_id, onepanel, help_func, assert_func)
