"""This module contains gherkin steps to run acceptance tests featuring
storages management in onepanel web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.utils import Onepanel, Popups
from tests.gui.utils.common.constants import CONFLICT_NAME_SEPARATOR
from tests.gui.utils.generic import transform
from tests.type_definitions import SeleniumDrivers
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
    selenium: SeleniumDrivers, browser_id: str, storage_type: str
) -> None:
    storage_selector = Onepanel(
        selenium[browser_id]
    ).content.storages.form.storage_selector
    storage_selector.expand()
    storage_selector_list = Popups(selenium[browser_id]).dropdown

    for storage in storage_selector_list.options:
        if storage.text.lower() == storage_type.lower():
            storage_selector_list.options[storage.text].click()
            return
    raise RuntimeError(f"storage {storage_type} not found")


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) types "(?P<text>.*?)" to '
        r"(?P<input_box>.*?) field in (?P<form>.*?) form "
        r"in storages page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_text_to_in_box_in_storages_page_op_panel(
    selenium: SeleniumDrivers,
    browser_id: str,
    text: str,
    form: str,
    input_box: str,
) -> None:
    form = getattr(
        Onepanel(selenium[browser_id]).content.storages.form, transform(form)
    )
    setattr(form, transform(input_box), text)


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) checks "(?P<option>.*?)" in '
        r"Storage path type field in (?P<form>.*?) form "
        r"in storages page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_check_option_in_box_in_storages_page_op_panel(
    selenium: SeleniumDrivers, browser_id: str, option: str, form: str
) -> None:
    storage_form = getattr(
        Onepanel(selenium[browser_id]).content.storages.form, transform(form)
    )
    getattr(storage_form.storage_path_type, option).click()


def enable_import_in_add_storage_form(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    form = Onepanel(selenium[browser_id]).content.storages.form
    form.posix.imported_storage.check()


@wt(
    parsers.parse(
        "user of {browser_id} clicks on Add button in add storage "
        "form in storages page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_add_btn_in_storage_add_form_in_storage_page(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    Onepanel(selenium[browser_id]).content.storages.form.add()


@wt(
    parsers.parse(
        'user of {browser_id} expands "{storage}" record on '
        "storages list in storages page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def wt_expand_storage_item_in_storages_page_op_panel(
    selenium: SeleniumDrivers, browser_id: str, storage: str
) -> None:
    storage_item = Onepanel(selenium[browser_id]).content.storages.storages[storage]
    storage_item.expand()

    if not storage_item.is_expanded():
        raise RuntimeError(f"did not manage to expand storage {storage}")


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) sees that "(?P<storage>.*?)" '
        r"(?P<attribute>.*?) is (?P<val>.*?) "
        r"in storages page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def wt_assert_storage_attr_in_storages_page_op_panel(
    selenium: SeleniumDrivers,
    browser_id: str,
    storage: str,
    attribute: str,
    val: str,
) -> None:
    storages = Onepanel(selenium[browser_id]).content.storages.storages
    displayed_val = getattr(storages[storage], transform(attribute)).lower()
    assert (
        displayed_val == val.lower()
    ), f"got {displayed_val} as storage's {attribute} instead of expected {val}"


@wt(
    parsers.parse(
        'user of {browser_id} expands toolbar for "{name}" storage '
        "record in Storages page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def wt_expands_toolbar_for_storage_in_onepanel(
    selenium: SeleniumDrivers, browser_id: str, name: str
) -> None:
    driver = selenium[browser_id]
    Onepanel(driver).content.storages.storages[name].expand_menu()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) clicks on "
        r"(?P<option>Remove storage backend) "
        r"option in storage's toolbar in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_btn_in_storage_toolbar_in_panel(
    selenium: SeleniumDrivers, browser_id: str, option: str
) -> None:
    toolbar = Popups(selenium[browser_id]).toolbar
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
def click_modify_storage_in_onepanel(
    selenium: SeleniumDrivers, browser_id: str, name: str
) -> None:
    driver = selenium[browser_id]
    Onepanel(driver).content.storages.storages[name].click()
    Onepanel(driver).content.storages.storages[name].modify()


@wt(
    parsers.parse(
        'user of {browser_id} types "{in_value}" into last key in '
        "posix QoS parameters form in storage edit page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def type_key_in_posix_storage_edit_page(
    selenium: SeleniumDrivers, browser_id: str, key: str
) -> None:
    driver = selenium[browser_id]
    storage_posix = Onepanel(driver).content.storages.storages["posix"]
    storage_posix.edit_form.posix_editor.params.set_last_key(key)


@wt(
    parsers.parse(
        "user of {browser_id} clicks value of modified record in "
        "QoS parameters form in posix storage edit page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_value_in_posix_storage_edit_page(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    storage_posix = Onepanel(driver).content.storages.storages["posix"]
    storage_posix.edit_form.posix_editor.params.click_value_in_modified_record()


@wt(
    parsers.parse(
        "user of {browser_id} deletes first additional param "
        "in QoS parameters form in posix storage edit page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def delete_additional_param_in_posix_storage_edit_page(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    storage_posix = Onepanel(driver).content.storages.storages["posix"]
    storage_posix.edit_form.posix_editor.params.delete_first_additional_param()


@wt(parsers.parse("user of {browser_id} saves changes in posix storage edit page"))
@repeat_failed(timeout=WAIT_FRONTEND)
def save_changes_in_posix_storage_edit_page(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    storage = Onepanel(driver).content.storages.storages["posix"]
    storage.edit_form.posix_editor.save_button.click()


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{name}" has disappeared from the storages list'
    )
)
@wt(parsers.parse('user of {browser_id} does not see "{name}" on the storages list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_storage_disappeared_from_list(
    selenium: SeleniumDrivers, browser_id: str, name: str
) -> None:
    driver = selenium[browser_id]
    storages_list = Onepanel(driver).content.storages.storages
    assert name not in storages_list, f"found {name} on storages list"


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{name}" is visible on the storages list'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_storage_on_storage_list(
    selenium: SeleniumDrivers, browser_id: str, name: str
) -> None:
    assert is_storage_on_storage_list(
        selenium, browser_id, name
    ), f"{name} not visible on storages list"


def is_storage_on_storage_list(
    selenium: SeleniumDrivers, browser_id: str, name: str
) -> bool:
    driver = selenium[browser_id]
    storages_list = Onepanel(driver).content.storages.storages
    return name in storages_list


# if there are repeated ids, set will be shorter than list
def check_ids_different(id_list: list[str]) -> bool:
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
    selenium: SeleniumDrivers,
    browser_id: str,
    name: str,
    input_box: str,
    storage_type: str,
    storage: str,
) -> None:
    driver = selenium[browser_id]
    form = getattr(
        Onepanel(driver).content.storages.storages[storage].edit_form,
        f"{storage_type.lower()}_editor",
    )

    input_box = transform(input_box)
    form.change_field_in_editor(driver, input_box, name)


@wt(
    parsers.parse(
        "user of {browser_id} clicks on {name} button in edit form "
        'for "{storage}" storage in Onepanel'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_button_in_edit_form(
    selenium: SeleniumDrivers, browser_id: str, name: str, storage: str
) -> None:
    driver = selenium[browser_id]
    button = name.lower() + "_button"
    getattr(
        Onepanel(driver).content.storages.storages[storage].edit_form.posix_editor,
        button,
    )()


@wt(
    parsers.parse(
        'user of {browser_id} copies id of "{storage_name}" storage '
        "to clipboard via copy button"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_storage_id_to_clipboard(
    selenium: SeleniumDrivers, browser_id: str, storage_name: str
) -> None:
    driver = selenium[browser_id]
    Onepanel(driver).content.storages.storages[storage_name].copy_id_button()


def close_all_expanded_storages(
    browser_id: str, selenium: SeleniumDrivers
) -> list[str]:
    driver = selenium[browser_id]
    storages_list = Onepanel(driver).content.storages.storages

    for storage in storages_list:
        if storage.is_expanded():
            storage.click_toggle()

    return [storage.name for storage in storages_list]


@wt(
    parsers.parse(
        'user of {browser_id} sees {number} storages named "{name}" '
        "with different IDs on the storages list"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_number_storages_with_same_name(
    selenium: SeleniumDrivers, browser_id: str, name: str, number: str
) -> None:
    storages_names = close_all_expanded_storages(browser_id, selenium)

    rows_with_name = [
        row_name
        for row_name in storages_names
        if row_name.split(CONFLICT_NAME_SEPARATOR)[0] == name
    ]
    ids = [row_name.split(CONFLICT_NAME_SEPARATOR)[1] for row_name in rows_with_name]

    assert len(rows_with_name) == int(
        number
    ), f"{name} not visible {number} times on storages list"
    assert check_ids_different(ids), f"IDs are not unique, {ids}"
