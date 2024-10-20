"""Meta steps for operations for quality of service"""

__author__ = "Michal Dronka"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

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
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


def _add_qos_requirement_in_modal(
    selenium,
    browser_id,
    modals,
    item_name,
    tmp_memory,
    expression,
    popups,
    replicas_number,
):
    qos_option = "Quality of Service"
    panel = "qos"
    add_button = "Add Requirement"
    save_button = "Save"
    close_button = "X"
    replicas_field = "Replicas number"
    expression_field = "expression"
    details_modal = "Details modal"

    choose_option_for_file_from_selection_menu(
        browser_id, selenium, qos_option, popups, tmp_memory, item_name
    )
    click_panel_button(selenium, browser_id, add_button, panel, modals)
    click_enter_as_text_link(selenium, browser_id, modals)
    write_name_into_text_field_in_panel(
        selenium, browser_id, expression, panel, modals, expression_field
    )
    confirm_entering_text(selenium, browser_id, modals)
    if replicas_number != 1:
        write_name_into_text_field_in_panel(
            selenium, browser_id, replicas_number, panel, modals, replicas_field
        )
    click_panel_button(selenium, browser_id, save_button, panel, modals)
    click_modal_button(selenium, browser_id, close_button, details_modal, modals)


@wt(
    parsers.parse(
        'user of {browser_id} creates "{expression}" QoS requirement '
        'for "{item_name}" in space "{space_name}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def add_qos_requirement_in_modal(
    selenium,
    browser_id,
    modals,
    item_name,
    tmp_memory,
    expression,
    oz_page,
    op_container,
    popups,
    space_name,
):
    replicas_number = 1

    go_to_filebrowser(
        selenium, browser_id, oz_page, op_container, tmp_memory, space_name
    )
    _add_qos_requirement_in_modal(
        selenium,
        browser_id,
        modals,
        item_name,
        tmp_memory,
        expression,
        popups,
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
    selenium,
    browser_id,
    modals,
    item_name,
    tmp_memory,
    expression,
    oz_page,
    space_name,
    op_container,
    popups,
    replicas_number,
):
    go_to_filebrowser(
        selenium, browser_id, oz_page, op_container, tmp_memory, space_name
    )
    _add_qos_requirement_in_modal(
        selenium,
        browser_id,
        modals,
        item_name,
        tmp_memory,
        expression,
        popups,
        replicas_number,
    )


@wt(
    parsers.parse(
        "user of {browser_id} creates QoS requirement with copied "
        'storageId for "{item_name}" from file browser'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def add_id_qos_requirement_in_modal(
    selenium,
    browser_id,
    modals,
    item_name,
    tmp_memory,
    popups,
    clipboard,
    displays,
):
    expression = "storageId=" + clipboard.paste(display=displays[browser_id])
    replicas_number = 1

    _add_qos_requirement_in_modal(
        selenium,
        browser_id,
        modals,
        item_name,
        tmp_memory,
        expression,
        popups,
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
    selenium,
    browser_id,
    modals,
    item_name,
    tmp_memory,
    popups,
    clipboard,
    displays,
):
    expression = r"anyStorage \ storageId=" + clipboard.paste(
        display=displays[browser_id]
    )
    replicas_number = 1

    _add_qos_requirement_in_modal(
        selenium,
        browser_id,
        modals,
        item_name,
        tmp_memory,
        expression,
        popups,
        replicas_number,
    )


def assert_qos_file_status_in_op_gui(
    user,
    file_name,
    space_name,
    tmp_memory,
    selenium,
    oz_page,
    op_container,
    option,
):
    option_of_space = "Files"
    status_type = "QoS"
    click_on_option_of_space_on_left_sidebar_menu(
        selenium, user, space_name, option_of_space, oz_page
    )
    assert_browser_in_tab_in_op(selenium, user, op_container, tmp_memory)
    if option == "has some":
        assert_status_tag_for_file_in_browser(user, status_type, file_name, tmp_memory)
    else:
        assert_not_status_tag_for_file_in_browser(
            user, status_type, file_name, tmp_memory
        )


def delete_qos_requirement_in_op_gui(
    selenium,
    user,
    space_name,
    oz_page,
    modals,
    popups,
    file_name,
    tmp_memory,
    op_container,
):
    option1 = "Files"
    status_type = "QoS"
    button = "X"
    modal = "Details modal"
    click_on_option_of_space_on_left_sidebar_menu(
        selenium, user, space_name, option1, oz_page
    )
    assert_browser_in_tab_in_op(selenium, user, op_container, tmp_memory)
    click_on_status_tag_for_file_in_file_browser(
        user, status_type, file_name, tmp_memory
    )
    delete_all_qualities_of_service(selenium, user, modals, popups)
    click_modal_button(selenium, user, button, modal, modals)
