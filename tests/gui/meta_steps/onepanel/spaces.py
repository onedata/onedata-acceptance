"""This module contains meta steps for operations on spaces in Onepanel
using web GUI
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.steps.modal import assert_error_modal_with_text_appeared
from tests.gui.steps.onepanel.common import *
from tests.gui.steps.common.notifies import *
from tests.gui.steps.onepanel.spaces import *
from tests.gui.steps.onezone.clusters import click_on_record_in_clusters_menu
from tests.gui.steps.onezone.spaces import click_on_option_in_the_sidebar
from tests import OP_REST_PORT
from tests.utils.rest_utils import http_get, get_panel_rest_path, http_delete


@wt(parsers.re('user of (?P<user>.+?) supports "(?P<space_name>.*)" space '
               'in "(?P<provider_name>.+?)" Oneprovider panel service '
               'with following configuration:\n'
               '(?P<config>(.|\s)*)'))
def support_space_in_op_panel_using_gui(selenium, user, config, onepanel,
                                        tmp_memory, space_name, provider_name,
                                        hosts):
    result = 'succeeds'

    result_to_support_space_in_op_panel_using_gui(selenium, user, config,
                                                  result, onepanel, tmp_memory,
                                                  space_name, provider_name,
                                                  hosts)


@wt(parsers.parse('user of {user} {result} to support "{space_name}" space '
                  'in "{provider_name}" Oneprovider panel service with '
                  'following configuration:\n{config}'))
def result_to_support_space_in_op_panel_using_gui(selenium, user, config,
                                                  result, onepanel, tmp_memory,
                                                  space_name, provider_name,
                                                  hosts):
    notify_type = 'info'
    notify_text_regexp = '.*[Aa]dded.*support.*space.*'

    _support_space_in_op_panel_using_gui(selenium, user, config, onepanel,
                                         tmp_memory, space_name, provider_name,
                                         hosts)
    if result == 'succeeds':
        notify_visible_with_text(selenium, user, notify_type, notify_text_regexp)
        wt_assert_existence_of_space_support_record(selenium, user, space_name,
                                                    onepanel)
    else:
        text = 'Space supporting failed'
        assert_error_modal_with_text_appeared(selenium, user, text)


def _support_space_in_op_panel_using_gui(selenium, user, config, onepanel,
                                        tmp_memory, space_name, provider_name,
                                        hosts):
    sidebar = 'Clusters'
    sub_item = 'Spaces'
    input_box = 'Size'
    sync_type_import = 'IMPORT'
    sync_type_update = 'UPDATE'

    options = yaml.load(config)
    unit = options.get('unit', 'MiB')

    wt_click_on_subitem_for_item(selenium, user, sidebar, sub_item,
                                 provider_name, onepanel, hosts)
    wt_click_on_support_space_btn_on_condition(selenium, user, onepanel)
    wt_select_storage_in_support_space_form(selenium, user, options['storage'],
                                            onepanel)
    wt_type_received_token_to_support_token_field(selenium, user, onepanel,
                                                  tmp_memory)
    wt_type_text_to_input_box_in_space_support_form(selenium, user,
        str(options['size']), input_box, onepanel)
    wt_select_unit_in_space_support_add_form(selenium, user, unit, onepanel)

    if options.get('storage import', False):
        storage_import_options = options.get('storage import', None)
        wt_enable_option_box_in_space_support_form(selenium, user,
            'Import storage data', onepanel)
        wt_select_strategy_in_conf_in_support_space_form(selenium, user,
            storage_import_options['strategy'], sync_type_import, onepanel)
        if 'max depth' in storage_import_options:
            wt_type_text_to_input_box_in_conf_in_space_support_form(selenium,
                user, str(storage_import_options['max depth']), 'Max depth',
                sync_type_import, onepanel)

        if options.get('storage update', False):
            storage_update_options = options.get('storage update', None)
            wt_select_strategy_in_conf_in_support_space_form(selenium, user,
                storage_update_options['strategy'], sync_type_update, onepanel)
            if 'max depth' in storage_update_options:
                wt_type_text_to_input_box_in_conf_in_space_support_form(
                    selenium, user, str(storage_update_options['max depth']),
                    'Max depth', sync_type_update, onepanel)
            if 'scan interval [s]' in storage_update_options:
                wt_type_text_to_input_box_in_conf_in_space_support_form(
                    selenium, user,
                    str(storage_update_options['scan interval [s]']),
                    'Scan interval', sync_type_update, onepanel)

    wt_click_on_btn_in_space_support_add_form(selenium, user, onepanel)


@wt(parsers.parse('user of {browser_id} sets update configuration in '
                  'Storage synchronization tab as following:\n{config}'))
def set_update_configuration_in_storage_sync(selenium, browser_id, config,
                                             onepanel):
    sync_type_update = 'UPDATE'
    options = yaml.load(config)

    if options.get('storage update', False):
        storage_update_options = options.get('storage update', None)
        wt_select_strategy_in_conf_in_space_record(selenium, browser_id,
            storage_update_options['strategy'], sync_type_update, onepanel)
        if 'max depth' in storage_update_options:
            wt_type_text_to_input_box_in_conf_in_space_record(selenium,
                browser_id, str(storage_update_options['max depth']),
                'Max depth', sync_type_update, onepanel)
        if 'scan interval [s]' in storage_update_options:
            wt_type_text_to_input_box_in_conf_in_space_record(selenium,
                browser_id, str(storage_update_options['scan interval [s]']),
                'Scan interval', sync_type_update, onepanel)
        if storage_update_options.get('delete enabled', False):
            wt_enable_option_box_in_conf_in_space_record(selenium, browser_id,
                'delete enabled', onepanel)
        if storage_update_options.get('write once', False):
            wt_enable_option_box_in_conf_in_space_record(selenium, browser_id,
                'write once', onepanel)

    button = 'Save configuration'
    notify_type = 'info'
    text_regexp = '.*[Cc]onfiguration.*space.*support.*changed.*'
    wt_clicks_on_button_in_space_record(selenium, browser_id, onepanel, button)
    notify_visible_with_text(selenium, browser_id, notify_type, text_regexp)


@wt(parsers.parse('user of {user} revokes "{space_name}" space support '
                  'in "{provider_name}" provider in Onepanel'))
def revoke_space_support_in_op_panel_using_gui(selenium, user, provider_name,
                                               onepanel, space_name, popups,
                                               modals, hosts):
    sidebar = 'Clusters'
    sub_item = 'Spaces'
    option = 'Revoke space support'
    button = 'Cease support'
    notify_type = 'info'
    notify_text_regexp = 'Ceased.*[Ss]upport.*'

    wt_click_on_subitem_for_item(selenium, user, sidebar, sub_item,
                                 provider_name, onepanel, hosts)
    wt_expands_toolbar_icon_for_space_in_onepanel(selenium, user, space_name,
                                                  onepanel)
    wt_clicks_on_btn_in_space_toolbar_in_panel(selenium, user, option, popups)
    wt_clicks_on_understand_risk_in_cease_support_modal(selenium, user, modals)
    wt_clicks_on_btn_in_cease_support_modal(selenium, user, button, modals)
    notify_visible_with_text(selenium, user, notify_type, notify_text_regexp)


def configure_sync_parameters_for_space_in_op_panel_gui(selenium, user, space,
                                                        onepanel, popups,
                                                        config, sync_type):
    tab_name = 'Storage synchronization'
    notify_type = 'info'
    notify_text_regexp = '.*[Cc]onfiguration.*space.*support.*changed.*'
    configure_button = 'Configure'
    button = ('Start synchronization' if sync_type == 'IMPORT'
              else 'Save configuration')

    click_on_navigation_tab_in_space(user, tab_name, onepanel, selenium)

    if sync_type == 'IMPORT':
        wt_clicks_on_button_in_space_record(selenium, user, onepanel,
                                            configure_button)
    else:
        wt_clicks_on_option_in_spaces_page(selenium, user, onepanel)

    options = yaml.load(config)
    storage_import = options['{} strategy'.format(sync_type.capitalize())]
    wt_select_strategy_in_conf_in_space_record(selenium, user, storage_import,
                                               sync_type, onepanel)

    if storage_import.lower() == 'disabled':
        wt_clicks_on_button_in_space_record(selenium, user, onepanel, button)
        return

    for field, input_box in zip(('Max depth', 'Scan interval [s]'),
                                ('Max depth', 'Scan interval')):
        val = str(options.get(field, None))
        if val:
            wt_type_text_to_input_box_in_conf_in_space_record(
                selenium, user, val, input_box, sync_type, onepanel)

    for field in ('Write once', 'Delete enabled'):
        val = options.get(field, None)
        if val:
            wt_enable_option_box_in_conf_in_space_record(
                selenium, user, field, onepanel)

    wt_clicks_on_button_in_space_record(selenium, user, onepanel, button)
    notify_visible_with_text(selenium, user, notify_type, notify_text_regexp)


def copy_id_of_space_gui(selenium, user, space_name, onepanel, tmp_memory):
    wt_open_space_item_in_spaces_page_op_panel(selenium, user, space_name,
                                                 onepanel)
    wt_copy_space_id_in_spaces_page_in_onepanel(selenium, user, space_name,
                                                onepanel, tmp_memory)


def assert_proper_space_configuration_in_op_panel_gui(selenium, user, space,
                                                      onepanel, sync_type,
                                                      conf, provider_name, hosts):
    sidebar = 'Clusters'
    sub_item = 'Spaces'
    wt_click_on_subitem_for_item(selenium, user, sidebar, sub_item,
                                 provider_name, onepanel, hosts)
    wt_open_space_item_in_spaces_page_op_panel(selenium, user, space,
                                                 onepanel)
    wt_assert_proper_space_configuration_in_panel(selenium, user, sync_type,
                                                  space, conf, onepanel)


@given(parsers.parse('there are no spaces supported in Onepanel used '
                     'by user of {browser_id}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def revoke_all_space_supports(selenium, browser_id, onepanel, popups,
                              modals, hosts, oz_page):
    sidebar = 'CLUSTERS'
    sub_item = 'Spaces'
    record = 'oneprovider-1'

    option = 'Revoke space support'
    button = 'Cease support'

    click_on_option_in_the_sidebar(selenium, browser_id, sidebar, oz_page)
    click_on_record_in_clusters_menu(selenium, browser_id, oz_page, record,
                                     hosts)
    # wait for load cluster
    time.sleep(5)
    wt_click_on_subitem_for_item(selenium, browser_id, sidebar, sub_item,
                                 record, onepanel, hosts)
    # wait for load spaces list
    time.sleep(1)
    spaces_list = onepanel(selenium[browser_id]).content.spaces.spaces

    while len(spaces_list) > 0:
        space = spaces_list[0]
        wt_expands_toolbar_icon_for_space_in_onepanel(selenium, browser_id,
                                                      space.name, onepanel)
        wt_clicks_on_btn_in_space_toolbar_in_panel(selenium, browser_id,
                                                   option, popups)
        wt_clicks_on_understand_risk_in_cease_support_modal(selenium,
                                                            browser_id,
                                                            modals)
        wt_clicks_on_btn_in_cease_support_modal(selenium, browser_id,
                                                button, modals)
        # wait for update spaces list
        time.sleep(1)
        spaces_list = onepanel(selenium[browser_id]).content.spaces.spaces
    selenium[browser_id].refresh()


@given(parsers.parse('there are no spaces supported by {provider_host} '
                     'in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def revoke_all_space_supports_using_rest(selenium, hosts, users, provider_host):
    user = 'onepanel'

    provider_hostname = hosts[provider_host]['hostname']

    spaces_list = http_get(ip=provider_hostname, port=OP_REST_PORT,
                           path=get_panel_rest_path('provider', 'spaces'),
                           auth=(user, users[user].password)).json()

    for space in spaces_list['ids']:
        http_delete(ip=provider_hostname, port=OP_REST_PORT,
                    path=get_panel_rest_path('provider', 'spaces', space),
                    auth=(user, users[user].password))


@wt(parsers.parse('{provider_host} revokes all spaces support in Onepanel '
                  'using REST'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_revoke_all_space_supports_using_rest(hosts, users, provider_host):
    user = 'onepanel'

    provider_hostname = hosts[provider_host]['hostname']

    spaces_list = http_get(ip=provider_hostname, port=OP_REST_PORT,
                           path=get_panel_rest_path('provider', 'spaces'),
                           auth=(user, users[user].password)).json()

    for space in spaces_list['ids']:
        http_delete(ip=provider_hostname, port=OP_REST_PORT,
                    path=get_panel_rest_path('provider', 'spaces', space),
                    auth=(user, users[user].password))


@wt(parsers.parse('user of {browser_id} sets {quota} quota to {value} value '
                  'in auto-cleaning tab in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def set_quota_in_auto_cleaning(selenium, browser_id, quota, value, onepanel):
    click_change_quota_button(selenium, browser_id, quota, onepanel)
    type_value_to_quota_input(selenium, browser_id, quota, value, onepanel)
    confirm_quota_value_change(selenium, browser_id, quota, onepanel)
