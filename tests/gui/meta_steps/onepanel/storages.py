"""This module contains meta steps for operations on storages in Onepanel
using web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import json
import re

import yaml

from tests import PANEL_REST_PORT
from tests.gui.conftest import WAIT_BACKEND
from tests.gui.steps.common.miscellaneous import type_string_into_active_element
from tests.gui.steps.common.notifies import notify_visible_with_text
from tests.gui.steps.modals.modal import click_modal_button
from tests.gui.steps.onepanel.common import (
    wt_click_on_subitem_for_item, wt_click_on_btn_in_content)
from tests.gui.steps.onepanel.storages import (
    wt_expands_toolbar_for_storage_in_onepanel,
    wt_clicks_on_btn_in_storage_toolbar_in_panel,
    assert_storage_disappeared_from_list,
    wt_select_storage_type_in_storage_page_op_panel,
    wt_type_text_to_in_box_in_storages_page_op_panel,
    wt_click_on_add_btn_in_storage_add_form_in_storage_page,
    enable_import_in_add_storage_form, save_changes_in_posix_storage_edit_page,
    click_value_in_posix_storage_edit_page,
    delete_additional_param_in_posix_storage_edit_page,
    type_key_in_posix_storage_edit_page, click_modify_storage_in_onepanel)
from tests.gui.steps.onezone.clusters import click_on_record_in_clusters_menu
from tests.gui.steps.onezone.spaces import (
    click_on_option_in_the_sidebar)
from tests.utils.bdd_utils import given, wt, parsers
from tests.utils.rest_utils import (
    http_post, get_panel_rest_path, http_get, http_delete)
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} removes "{name}" storage '
                  'in Onepanel page'))
def remove_storage_in_op_panel_using_gui(selenium, browser_id, name, onepanel,
                                         popups, modals):
    option = 'Remove storage backend'
    button = 'Remove'
    modal = 'REMOVE STORAGE BACKEND'

    wt_expands_toolbar_for_storage_in_onepanel(selenium, browser_id, name,
                                               onepanel)
    wt_clicks_on_btn_in_storage_toolbar_in_panel(selenium, browser_id, option,
                                                 popups)
    click_modal_button(selenium, browser_id, button, modal, modals)
    assert_storage_disappeared_from_list(selenium, browser_id, name, onepanel)


@wt(parsers.re('user of (?P<browser_id>.+?) adds "(?P<name>.*)" storage '
               'in "(?P<provider_name>.+?)" Oneprovider panel service '
               'with following configuration:\n'
               '(?P<config>(.|\s)*)'))
def add_storage_in_op_panel_using_gui(selenium, browser_id, name, provider_name,
                                      config, oz_page, hosts, onepanel):
    """ Create storage according to given config.

        Config format given in yaml is as follows:

            storage type: storage_type             --> required
            mount point: mount_point               --> required
            imported storage: true                 --> optional
    """
    _go_to_storage_view_in_clusters(selenium, browser_id, provider_name,
                                    oz_page, hosts, onepanel)
    _add_storage_in_op_panel_using_gui(selenium, browser_id, config, onepanel,
                                       name)


def _go_to_storage_view_in_clusters(selenium, browser_id, provider_name,
                                    oz_page, hosts, onepanel):
    driver = selenium[browser_id]
    onezone_url_pattern = 'https?://[^/]*/ozw/.*'
    sidebar = 'Clusters'
    sub_item = 'Storage backends'

    if re.match(onezone_url_pattern, driver.current_url):
        click_on_option_in_the_sidebar(selenium, browser_id, sidebar, oz_page)
        click_on_record_in_clusters_menu(selenium, browser_id, oz_page,
                                         provider_name, hosts)

    wt_click_on_subitem_for_item(selenium, browser_id, sidebar, sub_item,
                                 provider_name, onepanel, hosts)


def _add_storage_in_op_panel_using_gui(selenium, browser_id, config, onepanel,
                                       storage_name):
    content = 'storages'
    btn = 'Add storage backend'
    form = 'POSIX'
    input_box = 'Storage name'
    mount_point_option = 'mount point'
    notify_type = 'info'
    text_regexp = '.*[Ss]torage.*added.*'

    options = yaml.load(config)

    wt_click_on_btn_in_content(selenium, browser_id, btn, content, onepanel)

    storage_type = options['storage type']
    wt_select_storage_type_in_storage_page_op_panel(selenium, browser_id,
                                                    storage_type, onepanel)
    wt_type_text_to_in_box_in_storages_page_op_panel(selenium, browser_id,
                                                     storage_name, form,
                                                     onepanel, input_box)
    mount_point = options[mount_point_option]
    wt_type_text_to_in_box_in_storages_page_op_panel(selenium, browser_id,
                                                     mount_point, form,
                                                     onepanel,
                                                     mount_point_option)
    if options.get('imported storage', False):
        enable_import_in_add_storage_form(selenium, browser_id, onepanel)

    wt_click_on_add_btn_in_storage_add_form_in_storage_page(selenium,
                                                            browser_id,
                                                            onepanel)
    notify_visible_with_text(selenium, browser_id, notify_type, text_regexp)


@given(parsers.parse('there is "{storage_name}" storage in "{provider}" '
                     'Oneprovider panel service used by '
                     '{user} with following configuration:\n{config}'))
def safely_create_storage_rest(storage_name, provider, config,
                               hosts, onepanel_credentials):
    """ Create storage according to given config.

            Config format given in yaml is as follows:

                storage type: storage_type             --> required
                mount point: mount_point               --> required
                imported storage: true                 --> optional
                LUMA feed: local                       --> optional, 'auto' by
                                                           default
        """
    _remove_storage_in_op_panel_using_rest(storage_name, provider, hosts,
                                           onepanel_credentials)
    _add_storage_in_op_panel_using_rest(config, storage_name, provider, hosts,
                                        onepanel_credentials)


@given(parsers.parse('there is no "{storage_name}" storage in "{provider}" '
                     'Oneprovider panel service'))
def remove_all_storages_named(storage_name, provider, hosts,
                              onepanel_credentials):
    _remove_storage_in_op_panel_using_rest(storage_name, provider, hosts,
                                           onepanel_credentials)


@repeat_failed(timeout=WAIT_BACKEND)
def _remove_storage_in_op_panel_using_rest(storage_name, provider, hosts,
                                           onepanel_credentials):
    provider_hostname = hosts[provider]['hostname']
    onepanel_username = onepanel_credentials.username
    onepanel_password = onepanel_credentials.password

    storage_ids = _get_storage_id_list_by_name(storage_name, provider, hosts,
                                               onepanel_credentials)
    for storage_id in storage_ids:
        _remove_storage_by_id(provider_hostname, onepanel_username,
                              onepanel_password, storage_id)


def _remove_storage_by_id(provider_hostname, onepanel_username,
                          onepanel_password, storage_id):
    http_delete(ip=provider_hostname, port=PANEL_REST_PORT,
                path=get_panel_rest_path('provider', 'storages', storage_id),
                auth=(onepanel_username, onepanel_password))


@given(parsers.parse('there is no "{name}" storage in "{provider}" '
                     'Oneprovider panel'))
def remove_storage_in_op_panel_rest(onepanel_credentials, hosts, provider,
                                    name):
    _remove_storage_in_op_panel_using_rest(name, provider, hosts,
                                           onepanel_credentials)


def _get_storages_ids(provider_hostname, onepanel_username, onepanel_password):
    return http_get(ip=provider_hostname, port=PANEL_REST_PORT,
                    path=get_panel_rest_path('provider', 'storages'),
                    auth=(onepanel_username, onepanel_password)).json()['ids']


def _get_storage_id_list_by_name(storage_name, provider, hosts,
                                 onepanel_credentials):
    provider_hostname = hosts[provider]['hostname']
    onepanel_username = onepanel_credentials.username
    onepanel_password = onepanel_credentials.password

    storage_ids = _get_storages_ids(provider_hostname, onepanel_username,
                                    onepanel_password)
    selected_ids = []
    for storage_id in storage_ids:
        response = http_get(ip=provider_hostname, port=PANEL_REST_PORT,
                            path=get_panel_rest_path('provider', 'storages',
                                                     storage_id),
                            auth=(onepanel_username, onepanel_password)).json()
        if storage_name == response['name']:
            selected_ids.append(storage_id)
    return selected_ids


def get_first_storage_id_by_name(storage_name, provider, hosts,
                                 onepanel_credentials):
    return _get_storage_id_list_by_name(storage_name, provider, hosts,
                                        onepanel_credentials)[0]


@repeat_failed(timeout=WAIT_BACKEND)
def _add_storage_in_op_panel_using_rest(config, storage_name, provider, hosts,
                                        onepanel_credentials):
    storage_config = {}
    options = yaml.load(config)

    storage_config['type'] = options['storage type'].lower()
    if options.get('imported storage', False):
        storage_config['importedStorage'] = True
    storage_config['mountPoint'] = options['mount point']
    luma_feed = options.get('LUMA feed')
    if luma_feed:
        storage_config['lumaFeed'] = luma_feed

    provider_hostname = hosts[provider]['hostname']
    onepanel_username = onepanel_credentials.username
    onepanel_password = onepanel_credentials.password

    storage_data = {storage_name: storage_config}

    http_post(ip=provider_hostname, port=PANEL_REST_PORT,
              path=get_panel_rest_path('provider', 'storages'),
              auth=(onepanel_username, onepanel_password),
              data=json.dumps(storage_data))


@wt(parsers.parse('user of {browser_id} adds key="{key}" value="{val}" in '
                  'QoS parameters form in storage edit page'))
def add_key_value_in_storage_page(selenium, browser_id, key,
                                  val, onepanel, modals):
    button = 'Proceed'
    modal = 'Modify Storage'

    type_key_in_posix_storage_edit_page(selenium, browser_id, key, onepanel)
    click_value_in_posix_storage_edit_page(selenium, browser_id, onepanel)
    type_string_into_active_element(selenium, browser_id, val)
    save_changes_in_posix_storage_edit_page(selenium, browser_id, onepanel)
    click_modal_button(selenium, browser_id, button, modal, modals)


@wt(parsers.parse('user of {browser_id} deletes additional param in storage '
                  'edit page'))
def delete_additional_param_in_storage_page(selenium, browser_id,
                                            onepanel, modals):
    button = 'Proceed'
    modal = 'Modify Storage'

    delete_additional_param_in_posix_storage_edit_page(selenium, browser_id,
                                                       onepanel)
    save_changes_in_posix_storage_edit_page(selenium, browser_id, onepanel)
    click_modal_button(selenium, browser_id, button, modal, modals)


def _delete_all_additional_params_in_storage_page(selenium, browser_id,
                                                  onepanel, modals):
    deleted = False
    name = 'posix'
    button = 'Proceed'
    modal = 'Modify Storage'

    while not deleted:
        click_modify_storage_in_onepanel(selenium, browser_id, name,
                                         onepanel)
        driver = selenium[browser_id]
        storage = onepanel(driver).content.storages.storages['posix']
        if storage.edit_form.posix_editor.params.get_key_values_count() == 2:
            deleted = True
        if not deleted:
            delete_additional_param_in_posix_storage_edit_page(selenium,
                                                               browser_id,
                                                               onepanel)
        save_changes_in_posix_storage_edit_page(selenium, browser_id, onepanel)
        click_modal_button(selenium, browser_id, button, modal, modals)


@given(parsers.parse('there are no additional params in QoS parameters form '
                     'in storage edit page used by {browser_id}'))
def g_delete_all_additional_params_in_storage_page(selenium, browser_id,
                                                   onepanel, modals):
    _delete_all_additional_params_in_storage_page(selenium, browser_id,
                                                  onepanel, modals)


@wt(parsers.parse('user of {browser_id} deletes all additional params in '
                  'QoS parameters form in storage edit page'))
def wt_delete_all_additional_params_in_storage_page(selenium, browser_id,
                                                    onepanel, modals):
    _delete_all_additional_params_in_storage_page(selenium, browser_id,
                                                  onepanel, modals)
