"""Meta steps for operations for quality of service"""

__author__ = "Michal Dronka"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.conftest import SeleniumDrivers
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.meta_steps.oneprovider.data import go_to_filebrowser
from tests.gui.steps.modals.modal import (
    click_modal_button,
    click_panel_button,
    write_name_into_text_field_in_panel,
)
from tests.gui.steps.oneprovider.browser import (
    assert_not_status_tag_for_file_in_browser,
    assert_status_tag_for_file_in_browser,
)
from tests.gui.steps.oneprovider.data_tab import (
    assert_browser_in_tab_in_op,
    choose_option_for_file_from_selection_menu,
)
from tests.gui.steps.oneprovider.file_browser import (
    click_on_status_tag_for_file_in_file_browser,
)
from tests.gui.steps.oneprovider.qos import (
    click_enter_as_text_link,
    confirm_entering_text,
    delete_all_qualities_of_service,
)
from tests.gui.steps.onezone.spaces import click_on_option_of_space_on_left_sidebar_menu
from tests.gui.types import Clipboard, DisplayMap, TmpMemory
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


def _add_qos_requirement_in_modal(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_name: str,
    tmp_memory: TmpMemory,
    expression: str,
    replicas_number: int,
) -> None:
    qos_option = "Quality of Service"
    panel = "qos"
    add_button = "Add Requirement"
    save_button = "Save"
    close_button = "X"
    replicas_field = "Replicas number"
    expression_field = "expression"
    details_modal = "Details modal"

    choose_option_for_file_from_selection_menu(
        browser_id, selenium, qos_option, tmp_memory, item_name
    )
    click_panel_button(selenium, browser_id, add_button, panel)
    click_enter_as_text_link(selenium, browser_id)
    write_name_into_text_field_in_panel(
        selenium, browser_id, expression, panel, expression_field
    )
    confirm_entering_text(selenium, browser_id)
    if replicas_number != 1:
        write_name_into_text_field_in_panel(
            selenium, browser_id, str(replicas_number), panel, replicas_field
        )
    click_panel_button(selenium, browser_id, save_button, panel)
    click_modal_button(selenium, browser_id, close_button, details_modal)


@wt(
    parsers.parse(
        'user of {browser_id} creates "{expression}" QoS requirement '
        'for "{item_name}" in space "{space_name}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def add_qos_requirement_in_modal(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_name: str,
    tmp_memory: TmpMemory,
    expression: str,
    space_name: str,
) -> None:
    replicas_number = 1

    go_to_filebrowser(selenium, browser_id, tmp_memory, space_name)
    _add_qos_requirement_in_modal(
        selenium,
        browser_id,
        item_name,
        tmp_memory,
        expression,
        replicas_number,
    )


@wt(
    parsers.parse(
        "user of {browser_id} creates {replicas_number} replicas of "
        '"{expression}" QoS requirement for "{item_name}" in space '
        '"{space_name}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def add_qos_requirement_in_modal_with_replicas(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_name: str,
    tmp_memory: TmpMemory,
    expression: str,
    space_name: str,
    replicas_number: str,
) -> None:
    go_to_filebrowser(selenium, browser_id, tmp_memory, space_name)
    _add_qos_requirement_in_modal(
        selenium,
        browser_id,
        item_name,
        tmp_memory,
        expression,
        int(replicas_number),
    )


@wt(
    parsers.parse(
        "user of {browser_id} creates QoS requirement with copied "
        'storageId for "{item_name}" from file browser'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def add_id_qos_requirement_in_modal(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_name: str,
    tmp_memory: TmpMemory,
    clipboard: Clipboard,
    displays: DisplayMap,
) -> None:
    expression = "storageId=" + clipboard.paste(display=displays[browser_id])
    replicas_number = 1

    _add_qos_requirement_in_modal(
        selenium,
        browser_id,
        item_name,
        tmp_memory,
        expression,
        replicas_number,
    )


@wt(
    parsers.parse(
        'user of {browser_id} creates "anyStorage \\ storageId=" QoS '
        "requirement and pastes storage id from clipboard for "
        '"{item_name}" from file browser'
    )
)
def add_no_id_qos_requirement_in_modal(
    selenium: SeleniumDrivers,
    browser_id: str,
    item_name: str,
    tmp_memory: TmpMemory,
    clipboard: Clipboard,
    displays: DisplayMap,
) -> None:
    expression = r"anyStorage \ storageId=" + clipboard.paste(
        display=displays[browser_id]
    )
    replicas_number = 1

    _add_qos_requirement_in_modal(
        selenium,
        browser_id,
        item_name,
        tmp_memory,
        expression,
        replicas_number,
    )


def assert_qos_file_status_in_op_gui(
    user: str,
    file_name: str,
    space_name: str,
    tmp_memory: TmpMemory,
    selenium: SeleniumDrivers,
    option: str,
) -> None:
    option_of_space = "Files"
    status_type = "QoS"
    click_on_option_of_space_on_left_sidebar_menu(
        selenium, user, space_name, option_of_space
    )
    assert_browser_in_tab_in_op(selenium, user, tmp_memory, "file browser")
    if option == "has some":
        assert_status_tag_for_file_in_browser(user, status_type, file_name, tmp_memory)
    else:
        assert_not_status_tag_for_file_in_browser(
            user, status_type, file_name, tmp_memory
        )


def delete_qos_requirement_in_op_gui(
    selenium: SeleniumDrivers,
    user: str,
    space_name: str,
    file_name: str,
    tmp_memory: TmpMemory,
) -> None:
    option1 = "Files"
    status_type = "QoS"
    button = "X"
    modal = "Details modal"
    click_on_option_of_space_on_left_sidebar_menu(selenium, user, space_name, option1)
    assert_browser_in_tab_in_op(selenium, user, tmp_memory, "file browser")
    click_on_status_tag_for_file_in_file_browser(
        user, status_type, file_name, tmp_memory
    )
    delete_all_qualities_of_service(selenium, user)
    click_modal_button(selenium, user, button, modal)
