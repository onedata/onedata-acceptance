"""This module contains meta steps for operations on storages in Onepanel
using web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
import re

import pytest
import yaml
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
)

from tests import PANEL_REST_PORT
from tests.gui.conftest import WAIT_BACKEND
from tests.gui.meta_steps.rest.storages import (
    get_storage_ids_by_name,
    remove_multiple_storages_in_op_panel_using_rest,
    restore_config_and_remove_storage_by_id,
    storage_data_from_config,
)
from tests.gui.steps.common.miscellaneous import type_string_into_active_element
from tests.gui.steps.common.notifies import notify_visible_with_text
from tests.gui.steps.modals.modal import (
    click_modal_button,
    wait_for_named_modal_to_disappear,
)
from tests.gui.steps.onepanel.common import (
    wt_click_on_btn_in_content,
    wt_click_on_subitem_for_item,
)
from tests.gui.steps.onepanel.storages import (
    assert_storage_disappeared_from_list,
    click_modify_storage_in_onepanel,
    click_value_in_posix_storage_edit_page,
    delete_additional_param_in_posix_storage_edit_page,
    enable_import_in_add_storage_form,
    save_changes_in_posix_storage_edit_page,
    type_key_in_posix_storage_edit_page,
    wt_click_on_add_btn_in_storage_add_form_in_storage_page,
    wt_clicks_on_btn_in_storage_toolbar_in_panel,
    wt_expands_toolbar_for_storage_in_onepanel,
    wt_select_storage_type_in_storage_page_op_panel,
    wt_type_text_to_in_box_in_storages_page_op_panel,
)
from tests.gui.steps.onezone.clusters import click_on_record_in_clusters_menu
from tests.gui.steps.onezone.spaces import click_on_option_in_the_sidebar
from tests.gui.utils import Onepanel
from tests.gui.utils.common.popups.generic import AlertPopup
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.rest_utils import get_panel_rest_path, http_post
from tests.utils.user_utils import User
from tests.utils.utils import repeat_failed


def _register_storage_finalizer(
    request: pytest.FixtureRequest,
    provider: str,
    hosts: Hosts,
    onepanel_credentials: User,
    storage_id: str,
    storage_name: str,
    config: str,
) -> None:
    request.addfinalizer(
        lambda: restore_config_and_remove_storage_by_id(
            hosts[provider]["hostname"],
            onepanel_credentials.username,
            onepanel_credentials.password,
            storage_id,
            storage_name,
            config,
        )
    )


@wt(parsers.parse('user of {browser_id} removes "{name}" storage in Onepanel page'))
def remove_storage_in_op_panel_using_gui(
    selenium: SeleniumDrivers, browser_id: str, name: str
) -> None:
    option = "Remove storage backend"
    button = "Remove"
    modal = "REMOVE STORAGE BACKEND"

    wt_expands_toolbar_for_storage_in_onepanel(selenium, browser_id, name)
    wt_clicks_on_btn_in_storage_toolbar_in_panel(selenium, browser_id, option)
    click_modal_button(selenium, browser_id, button, modal)
    assert_storage_disappeared_from_list(selenium, browser_id, name)


@wt(
    parsers.re(
        r'user of (?P<browser_id>.+?) adds "(?P<name>.*)" storage '
        r'in "(?P<provider_name>.+?)" Oneprovider panel service '
        r"with following configuration:\n(?P<config>(.|\s)*)"
    )
)
def add_storage_in_op_panel_using_gui(
    selenium: SeleniumDrivers,
    browser_id: str,
    name: str,
    provider_name: str,
    config: str,
    hosts: Hosts,
) -> None:
    """Create storage according to given config.

    Config format given in yaml is as follows:

        storage type: storage_type             --> required
        mount point: mount_point               --> required
        imported storage: true                 --> optional
    """
    _go_to_storage_view_in_clusters(selenium, browser_id, provider_name, hosts)
    _add_storage_in_op_panel_using_gui(selenium, browser_id, config, name)


def _go_to_storage_view_in_clusters(
    selenium: SeleniumDrivers, browser_id: str, provider_name: str, hosts: Hosts
) -> None:
    driver = selenium[browser_id]
    onezone_url_pattern = "https?://[^/]*/ozw/.*"
    sidebar = "Clusters"
    sub_item = "Storage backends"

    if re.match(onezone_url_pattern, driver.current_url):
        click_on_option_in_the_sidebar(selenium, browser_id, sidebar)
        click_on_record_in_clusters_menu(selenium, browser_id, provider_name, hosts)

    wt_click_on_subitem_for_item(
        selenium, [browser_id], sidebar, sub_item, provider_name, hosts
    )


def _add_storage_in_op_panel_using_gui(
    selenium: SeleniumDrivers, browser_id: str, config: str, storage_name: str
) -> None:
    content = "storages"
    btn = "Add storage backend"
    form = "POSIX"
    input_box = "Storage name"
    mount_point_option = "mount point"
    options = yaml.load(config, yaml.Loader)

    try:
        wt_click_on_btn_in_content(selenium, [browser_id], btn, content)
    except (ElementNotInteractableException, NoSuchElementException):
        pass

    storage_type = options["storage type"]
    wt_select_storage_type_in_storage_page_op_panel(selenium, browser_id, storage_type)
    wt_type_text_to_in_box_in_storages_page_op_panel(
        selenium, browser_id, storage_name, form, input_box
    )
    mount_point = options[mount_point_option]
    wt_type_text_to_in_box_in_storages_page_op_panel(
        selenium, browser_id, mount_point, form, mount_point_option
    )
    if options.get("imported storage", False):
        enable_import_in_add_storage_form(selenium, browser_id)
    wt_click_on_add_btn_in_storage_add_form_in_storage_page(selenium, browser_id)
    notify_visible_with_text(selenium, browser_id, AlertPopup.STORAGE_ADDED)


@given(
    parsers.parse(
        '"{storage_name}" storage backend in "{provider}" '
        "Oneprovider panel service used by "
        "{user} with following configuration:\n{config}"
    )
)
def safely_create_storage_rest(
    storage_name: str,
    provider: str,
    config: str,
    hosts: Hosts,
    onepanel_credentials: User,
    request: pytest.FixtureRequest,
) -> None:
    """Create storage according to given config.

    Config format given in yaml is as follows:

        storage type: storage_type             --> required
        mount point: mount_point               --> required
        imported storage: true                 --> optional
        LUMA feed: local                       --> optional, 'auto' by
                                                   default
    """
    remove_multiple_storages_in_op_panel_using_rest(
        storage_name, provider, hosts, onepanel_credentials
    )
    storage_id = _add_storage_in_op_panel_using_rest(
        config, storage_name, provider, hosts, onepanel_credentials
    )
    _register_storage_finalizer(
        request,
        provider,
        hosts,
        onepanel_credentials,
        storage_id,
        storage_name,
        config,
    )


@given(
    parsers.parse(
        'there is no "{storage_name}" storage in "{provider}" Oneprovider panel service'
    )
)
def remove_all_storages_named(
    storage_name: str, provider: str, hosts: Hosts, onepanel_credentials: User
) -> None:
    remove_multiple_storages_in_op_panel_using_rest(
        storage_name, provider, hosts, onepanel_credentials
    )


@given(parsers.parse('there is no "{name}" storage in "{provider}" Oneprovider panel'))
def remove_storage_in_op_panel_rest(
    onepanel_credentials: User, hosts: Hosts, provider: str, name: str
) -> None:
    remove_multiple_storages_in_op_panel_using_rest(
        name, provider, hosts, onepanel_credentials
    )


def get_first_storage_id_by_name(
    storage_name: str, provider: str, hosts: Hosts, onepanel_credentials: User
) -> str:
    ids = get_storage_ids_by_name(storage_name, provider, hosts, onepanel_credentials)
    return ids[0]


@repeat_failed(timeout=WAIT_BACKEND)
def _add_storage_in_op_panel_using_rest(
    config: str,
    storage_name: str,
    provider: str,
    hosts: Hosts,
    onepanel_credentials: User,
) -> str:
    storage_data = storage_data_from_config(config, storage_name)

    provider_hostname = hosts[provider]["hostname"]
    onepanel_username = onepanel_credentials.username
    onepanel_password = onepanel_credentials.password

    response = http_post(
        ip=provider_hostname,
        port=PANEL_REST_PORT,
        path=get_panel_rest_path("provider", "storages"),
        auth=(onepanel_username, onepanel_password),
        data=json.dumps(storage_data),
    )

    storage_id = response.json()[storage_name]["id"]

    if not isinstance(storage_id, str):
        raise TypeError("Storage creation response contains an invalid storage ID")
    return storage_id


@wt(
    parsers.parse(
        'user of {browser_id} adds key="{key}" value="{val}" in '
        "QoS parameters form in storage edit page"
    )
)
def add_key_value_in_storage_page(
    selenium: SeleniumDrivers, browser_id: str, key: str, val: str
) -> None:

    type_key_in_posix_storage_edit_page(selenium, browser_id, key)
    click_value_in_posix_storage_edit_page(selenium, browser_id)
    type_string_into_active_element(selenium, browser_id, val)
    save_changes_in_posix_storage_edit_page(selenium, browser_id)
    confirm_changes_in_modify_storage_modal(selenium, browser_id)


@wt(parsers.parse("user of {browser_id} deletes additional param in storage edit page"))
def delete_additional_param_in_storage_page(
    selenium: SeleniumDrivers, browser_id: str
) -> None:

    delete_additional_param_in_posix_storage_edit_page(selenium, browser_id)
    save_changes_in_posix_storage_edit_page(selenium, browser_id)
    _try_confirm_changes_in_modify_storage_modal(selenium, browser_id)


def _delete_all_additional_params_in_storage_page(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    deleted = False
    name = "posix"

    while not deleted:
        click_modify_storage_in_onepanel(selenium, browser_id, name)
        driver = selenium[browser_id]
        storage = Onepanel(driver).content.storages.storages["posix"]
        if storage.edit_form.posix_editor.params.get_key_values_count() == 2:
            deleted = True
        if not deleted:
            delete_additional_param_in_posix_storage_edit_page(selenium, browser_id)
        save_changes_in_posix_storage_edit_page(selenium, browser_id)
        _try_confirm_changes_in_modify_storage_modal(selenium, browser_id)


@given(
    parsers.parse(
        "there are no additional params in QoS parameters form "
        "in storage edit page used by {browser_id}"
    )
)
def g_delete_all_additional_params_in_storage_page(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    _delete_all_additional_params_in_storage_page(selenium, browser_id)


@wt(
    parsers.parse(
        "user of {browser_id} deletes all additional params in "
        "QoS parameters form in storage edit page"
    )
)
def wt_delete_all_additional_params_in_storage_page(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    _delete_all_additional_params_in_storage_page(selenium, browser_id)


def _try_confirm_changes_in_modify_storage_modal(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    button = "Proceed"
    checkbox = "Understand checkbox"
    modal = "Modify Storage"
    # if modal will not appear
    try:
        click_modal_button(selenium, browser_id, checkbox, modal)
        click_modal_button(selenium, browser_id, button, modal)
        wait_for_named_modal_to_disappear(
            selenium, browser_id, modal, wait_time=WAIT_BACKEND * 5
        )
    except NoSuchElementException:
        pass


@wt(
    parsers.parse(
        'user of {browser_id} confirms committed changes in modal "Modify Storage"'
    )
)
def confirm_changes_in_modify_storage_modal(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    _try_confirm_changes_in_modify_storage_modal(selenium, browser_id)
