"""Steps implementation for permissions GUI tests."""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from typing import Optional

from selenium.common.exceptions import StaleElementReferenceException

from tests.gui.conftest import WAIT_BACKEND
from tests.gui.meta_steps.oneprovider.data import (
    _click_menu_for_elem_somewhere_in_file_browser,
    assert_browser_in_tab_in_op,
    choose_option_from_selection_menu,
)
from tests.gui.steps.modals.details_modal import (
    assert_posix_tab_in_panel,
    assert_tab_in_modal,
)
from tests.gui.steps.modals.modal import (
    assert_there_is_no_button_in_panel,
    check_warning_modal,
    click_modal_button,
    click_panel_button,
)
from tests.gui.steps.oneprovider.browser import click_option_in_data_row_menu_in_browser
from tests.gui.steps.oneprovider.data_tab import (
    choose_option_for_file_from_selection_menu,
)
from tests.gui.steps.oneprovider.file_browser import (
    select_files_from_file_list_using_ctrl,
)
from tests.gui.steps.oneprovider.permissions import (
    assert_acl_subject,
    assert_fail_to_select_acl_option,
    assert_set_acl_privileges,
    check_permission,
    check_permission_denied_alert_in_edit_permissions_modal,
    check_permissions_list_in_edit_permissions_modal,
    click_on_record_header_in_edit_permissions_modal,
    expand_subject_record_in_edit_permissions_modal,
    fail_to_set_posix_permission,
    get_unknown_user_id_from_acl_entry,
    select_acl_options,
    select_acl_subject,
    select_permission_type,
    set_posix_permission,
)
from tests.gui.steps.onezone.spaces import (
    _click_on_option_in_the_sidebar,
    click_element_on_lists_on_left_sidebar_menu,
    click_on_option_of_space_on_left_sidebar_menu,
)
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils import Modals
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    parse_elements_sequence,
    parse_seq,
)
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.user_utils import Users
from tests.utils.utils import repeat_failed


def open_permission_modal(
    selenium: SeleniumDrivers,
    browser_id: str,
    path: str,
    space: str,
    tmp_memory: TmpMemory,
    permission_type: str,
) -> None:
    option = "Permissions"
    modal_name = "Details modal"

    _click_menu_for_elem_somewhere_in_file_browser(
        selenium, browser_id, path, space, tmp_memory
    )
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option)
    assert_tab_in_modal(selenium, browser_id, option, modal_name)

    try:
        select_permission_type(selenium, browser_id, permission_type)
    except RuntimeError as err:
        if permission_type == "posix":
            assert_posix_tab_in_panel(selenium, browser_id, modal_name)
        else:
            raise err


def _assert_posix_permissions(
    selenium: SeleniumDrivers,
    browser_id: str,
    space: str,
    path: str,
    perm: str,
    tmp_memory: TmpMemory,
) -> None:
    modal_name = "Details modal"
    close_button = "X"
    open_permission_modal(
        selenium,
        browser_id,
        path,
        space,
        tmp_memory,
        "posix",
    )
    check_permission(selenium, browser_id, perm)
    click_modal_button(selenium, browser_id, close_button, modal_name)


@repeat_failed(timeout=WAIT_BACKEND)
def assert_posix_permissions_in_op_gui(
    selenium: SeleniumDrivers,
    browser_id: str,
    space: str,
    path: str,
    perm: str,
    tmp_memory: TmpMemory,
) -> None:
    modal_name = "Details modal"
    close_button = "X"
    try:
        click_modal_button(selenium, browser_id, close_button, modal_name)
        _assert_posix_permissions(
            selenium,
            browser_id,
            space,
            path,
            perm,
            tmp_memory,
        )
    except (AttributeError, StaleElementReferenceException, RuntimeError):
        _assert_posix_permissions(
            selenium,
            browser_id,
            space,
            path,
            perm,
            tmp_memory,
        )


@wt(
    parsers.re(
        r"user of (?P<browser_id>\w+) sets (?P<path>.*) POSIX "
        r'(?P<perm>.*) privileges in "(?P<space>.*)"'
    )
)
def set_posix_permissions_in_op_gui(
    selenium: SeleniumDrivers,
    browser_id: str,
    space: str,
    path: str,
    perm: str,
    tmp_memory: TmpMemory,
) -> None:
    modal_name = "Details modal"
    button = "Save"
    close_button = "X"
    panel = "Edit permissions"

    open_permission_modal(
        selenium,
        browser_id,
        path,
        space,
        tmp_memory,
        "posix",
    )
    set_posix_permission(selenium, browser_id, perm)

    click_panel_button(selenium, browser_id, button, panel)
    click_modal_button(selenium, browser_id, close_button, modal_name)


def fail_to_set_posix_permissions_in_op_gui(
    selenium: SeleniumDrivers,
    browser_id: str,
    space: str,
    path: str,
    perm: str,
    tmp_memory: TmpMemory,
) -> None:
    button = "Save"
    panel = "Edit permissions"
    details_modal = "Details modal"
    x_button = "X"

    open_permission_modal(
        selenium,
        browser_id,
        path,
        space,
        tmp_memory,
        "posix",
    )
    fail_to_set_posix_permission(selenium, browser_id, perm)
    assert_there_is_no_button_in_panel(selenium, browser_id, button, panel)
    click_modal_button(selenium, browser_id, x_button, details_modal)


@wt(
    parsers.re(
        r"user of (?P<browser_id>\w+) adds ACE with (?P<privileges>.*) "
        r"privileges? set for (?P<type>.*?) (?P<name>.*)"
    )
)
def set_acl_entry_in_op_gui(
    selenium: SeleniumDrivers, browser_id: str, privileges: str, name: str
) -> None:
    permission_type = "acl"

    select_permission_type(selenium, browser_id, permission_type)
    select_acl_subject(selenium, browser_id, name)
    expand_subject_record_in_edit_permissions_modal(selenium, browser_id, name)
    select_acl_options(selenium, browser_id, privileges, name)
    click_on_record_header_in_edit_permissions_modal(selenium, browser_id, name)


def _set_acl_privileges_for_selected(
    browser_id: str,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    privileges: str,
    name: str,
    path: Optional[str] = None,
) -> None:
    option = "Permissions"
    modal_name = "Details modal"
    button = "Save"
    close_button = "X"
    panel = "Edit permissions"
    warning_modal = "warning"
    proceed_button = "proceed"
    parsed_path = parse_seq(path) if path is not None else []

    if parsed_path and len(parsed_path) == 1:
        choose_option_for_file_from_selection_menu(
            browser_id, selenium, option, tmp_memory, parsed_path[0]
        )
    else:
        choose_option_from_selection_menu(browser_id, selenium, option, tmp_memory)
    assert_tab_in_modal(selenium, browser_id, option, modal_name)

    set_acl_entry_in_op_gui(selenium, browser_id, privileges, name)
    click_panel_button(selenium, browser_id, button, panel)
    if check_warning_modal(selenium, browser_id):
        click_modal_button(selenium, browser_id, proceed_button, warning_modal)
    click_modal_button(selenium, browser_id, close_button, modal_name)


@wt(
    parsers.re(
        r'user of (?P<browser_id>\w+) sets "(?P<item_name>.*)" '
        r"(directory|file) ACL (?P<privileges>.*) privileges for"
        r" (?P<type>.*) (?P<name>.*)"
    )
)
def grant_acl_privileges_to_selected_in_filebrowser(
    selenium: SeleniumDrivers,
    browser_id: str,
    privileges: str,
    name: str,
    tmp_memory: TmpMemory,
    item_name: str,
) -> None:
    assert_browser_in_tab_in_op(selenium, browser_id, tmp_memory, "file browser")
    _set_acl_privileges_for_selected(
        browser_id,
        selenium,
        tmp_memory,
        privileges,
        name,
        item_name,
    )


@wt(
    parsers.re(
        rf"user of (?P<browser_id>\w+) sets (?P<item_list>{ELEMENTS_SEQUENCE_PATTERN})"
        r" ACL "
        r"(?P<privileges>.*) privileges for (?P<type>.*) (?P<name>.*) "
        r'in "(?P<space>.*)"'
    ),
    converters={"item_list": parse_elements_sequence},
)
def grant_acl_privileges_in_op_gui(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_list: str | list[str],
    privileges: str,
    name: str,
    tmp_memory: TmpMemory,
    space: str,
) -> None:
    option_in_menu = "Data"
    option = "spaces"
    option_in_submenu = "Files"
    _click_on_option_in_the_sidebar(selenium, browser_id, option_in_menu)
    click_element_on_lists_on_left_sidebar_menu(selenium, browser_id, option, space)
    click_on_option_of_space_on_left_sidebar_menu(
        selenium, browser_id, space, option_in_submenu
    )
    assert_browser_in_tab_in_op(selenium, browser_id, tmp_memory, "file browser")
    if isinstance(item_list, str):
        item_list = parse_elements_sequence(item_list)
    select_files_from_file_list_using_ctrl(browser_id, item_list, tmp_memory)
    selected_path = item_list[0] if len(item_list) == 1 else None
    _set_acl_privileges_for_selected(
        browser_id,
        selenium,
        tmp_memory,
        privileges,
        name,
        selected_path,
    )


@wt(
    parsers.re(
        r'user of (?P<browser_id>\w+) (?P<res>.*) to read "(?P<path>.*)"'
        r' ACL in "(?P<space>.*)"'
    )
)
def read_items_acl(
    selenium: SeleniumDrivers,
    browser_id: str,
    path: str,
    tmp_memory: TmpMemory,
    res: str,
    space: str,
) -> None:
    modal_name = "Details modal"
    close_button = "X"
    open_permission_modal(selenium, browser_id, path, space, tmp_memory, "acl")

    if res == "fails":
        check_permission_denied_alert_in_edit_permissions_modal(selenium, browser_id)
    else:
        check_permissions_list_in_edit_permissions_modal(selenium, browser_id)

    click_modal_button(selenium, browser_id, close_button, modal_name)


@wt(
    parsers.re(
        r"user of (?P<browser_id>\w+) sees that (?P<path>.*?) in space "
        r'"(?P<space>\w+)" (has|have) (?P<privileges>.*) privileges? set for '
        r"(?P<acl_type>.*?) (?P<name>.*) in (?P<num>.*) ACL record"
    )
)
def assert_ace_in_op_gui(
    selenium: SeleniumDrivers,
    browser_id: str,
    privileges: str,
    acl_type: str,
    name: str,
    num: str,
    space: str,
    path: str,
    tmp_memory: TmpMemory,
    numerals: dict[str, int],
) -> None:
    modal_name = "Details modal"
    close_button = "X"
    open_permission_modal(
        selenium,
        browser_id,
        path,
        space,
        tmp_memory,
        "acl",
    )
    if acl_type != "unknown":
        assert_acl_subject(selenium, browser_id, num, numerals, acl_type, name)
        assert_set_acl_privileges(selenium, browser_id, num, numerals, privileges)
    click_modal_button(selenium, browser_id, close_button, modal_name)


@wt(
    parsers.re(
        r"user of (?P<browser_id>\w+) sees that (?P<path>.*?) in space "
        r'"(?P<space>\w+)" contains id of user "(?P<name>.*)" in '
        r"(?P<num>.*) ACL record"
    )
)
def assert_user_id_in_ace_in_op_gui(
    selenium: SeleniumDrivers,
    browser_id: str,
    name: str,
    num: str,
    space: str,
    path: str,
    tmp_memory: TmpMemory,
    numerals: dict[str, int],
    users: Users,
) -> None:
    modal_name = "Details modal"
    close_button = "X"
    open_permission_modal(
        selenium,
        browser_id,
        path,
        space,
        tmp_memory,
        "acl",
    )
    visible_id = get_unknown_user_id_from_acl_entry(selenium, browser_id, num, numerals)
    user_id = users[name].user_id
    error_message = (
        f"id in acl entry: {visible_id} differs from actual user id: {user_id}"
    )
    assert visible_id == user_id, error_message
    click_modal_button(selenium, browser_id, close_button, modal_name)


@wt(
    parsers.re(
        r"user of (?P<browser_id>\w+) (?P<res>.*) to change "
        r'"(?P<path>.*)" ACL for (?P<name>.*) in "(?P<space>.*)"'
    )
)
def change_acl_privileges(
    selenium: SeleniumDrivers,
    browser_id: str,
    path: str,
    tmp_memory: TmpMemory,
    res: str,
    space: str,
    name: str,
) -> None:
    privileges_option_list = "[attributes]" if res == "succeeds" else "[acl:change acl]"
    button_save = "Save"
    button_close = "Close"
    panel = "Edit permissions"

    open_permission_modal(
        selenium,
        browser_id,
        path,
        space,
        tmp_memory,
        "acl",
    )
    expand_subject_record_in_edit_permissions_modal(selenium, browser_id, name)

    if res == "fails":
        assert_fail_to_select_acl_option(
            selenium,
            browser_id,
            parse_elements_sequence(privileges_option_list),
            name,
        )

    else:
        select_acl_options(selenium, browser_id, privileges_option_list, name)
        click_panel_button(selenium, browser_id, button_save, panel)
        click_panel_button(selenium, browser_id, button_close, panel)
        open_permission_modal(
            selenium,
            browser_id,
            path,
            space,
            tmp_memory,
            "acl",
        )
        check_permissions_list_in_edit_permissions_modal(selenium, browser_id)


@wt(
    parsers.re(
        r'user of (?P<browser_id>\w+) sees the following warning: "(?P<text>.*)"'
        r" in ACL Edit Permissions tab"
    )
)
def assert_warning_in_details_modal_in_edit_permimssions_tab(
    selenium: SeleniumDrivers, browser_id: str, text: str
) -> None:
    driver = selenium[browser_id]
    acl = Modals(driver).details_modal.edit_permissions.acl
    warn_priv = acl.limited_privileges_warning
    assert (
        text == warn_priv.text
    ), f"Warning from modal: {warn_priv.text} is not equal to given: {text}"
