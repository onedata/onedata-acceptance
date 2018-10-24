"""This module contains meta steps for operations on spaces in Onepanel
using web GUI
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from tests.gui.steps.onepanel.common import *
from tests.gui.steps.common.notifies import *
from tests.gui.steps.onepanel.spaces import *
import yaml


def support_space_in_op_panel_using_gui(selenium, user, config, onepanel,
                                        tmp_memory, space_name, provider_name,
                                        hosts):
    sidebar = 'Clusters'
    sub_item = 'Spaces'
    input_box = 'Size'
    button = 'MiB'
    sync_type = 'IMPORT'
    notify_type = 'info'
    notify_text_regexp = '.*[Aa]dded.*support.*space.*'

    options = yaml.load(config)

    wt_click_on_subitem_for_item(selenium, user, sidebar, sub_item,
                                 provider_name, onepanel, hosts)
    wt_click_on_support_space_btn_on_condition(selenium, user, onepanel)
    wt_select_storage_in_support_space_form(selenium, user, options['storage'],
                                            onepanel)
    wt_type_received_token_to_support_token_field(selenium, user, onepanel,
                                                  tmp_memory)
    wt_type_text_to_input_box_in_space_support_form(
        selenium, user, str(options['size']), input_box, onepanel)
    wt_select_unit_in_space_support_add_form(selenium, user, button,
                                             onepanel)
    if options.get('mount in root', False):
        wt_enable_option_box_in_space_support_form(selenium, user,
                                                   'Mount in root', onepanel)
    if options.get('storage import', False):
        storage_import_options = options.get('storage import', None)
        wt_enable_option_box_in_space_support_form(
            selenium, user, 'Import storage data', onepanel)
        wt_select_strategy_in_conf_in_support_space_form(
            selenium, user, storage_import_options['strategy'], sync_type,
            onepanel)
        if 'max depth' in storage_import_options:
            wt_type_text_to_input_box_in_conf_in_space_support_form(
                selenium, user, str(storage_import_options['max depth']),
                'Max depth', sync_type, onepanel)

    wt_click_on_btn_in_space_support_add_form(selenium, user, onepanel)
    notify_visible_with_text(selenium, user, notify_type,
                             notify_text_regexp)
    wt_assert_existence_of_space_support_record(selenium, user, space_name,
                                                onepanel)


def revoke_space_support_in_op_panel_using_gui(selenium, user, provider_name,
                                               onepanel, space_name, popups,
                                               modals, hosts):
    sidebar = 'Clusters'
    sub_item = 'Spaces'
    option = 'Revoke space support'
    button = 'Yes, revoke'
    notify_type = 'info'
    notify_text_regexp = '.*[Ss]upport.*revoked.*'

    wt_click_on_subitem_for_item(selenium, user, sidebar, sub_item,
                                 provider_name, onepanel, hosts)
    wt_expands_toolbar_icon_for_space_in_onepanel(selenium, user, space_name,
                                                  onepanel)
    wt_clicks_on_btn_in_space_toolbar_in_panel(selenium, user, option, popups)
    wt_clicks_on_btn_in_revoke_space_support(selenium, user, button, modals)
    notify_visible_with_text(selenium, user, notify_type, notify_text_regexp)


def configure_sync_parameters_for_space_in_op_panel_gui(selenium, user, space,
                                                        onepanel, popups,
                                                        config, sync_type):
    notify_type = 'info'
    notify_text_regexp = '.*[Cc]onfiguration.*space.*support.*changed.*'

    wt_expands_toolbar_icon_for_space_in_onepanel(selenium, user, space,
                                                  onepanel)
    wt_clicks_on_btn_in_space_toolbar_in_panel(selenium, user,
                                               'Configure data synchronization',
                                               popups)
    options = yaml.load(config)
    storage_import = options['{} strategy'.format(sync_type.capitalize())]
    wt_select_strategy_in_conf_in_space_record(selenium, user, storage_import,
                                               sync_type, space, onepanel)

    if storage_import.lower() == 'disabled':
        wt_clicks_on_save_config_btn_in_space_record(selenium, user, space,
                                                     onepanel)
        return

    for field, input_box in zip(('Max depth', 'Scan interval [s]'),
                                ('Max depth', 'Scan interval')):
        val = str(options.get(field, None))
        if val:
            wt_type_text_to_input_box_in_conf_in_space_record(
                selenium, user, val, input_box, sync_type, space, onepanel)

    for field in ('Write once', 'Delete enabled'):
        val = options.get(field, None)
        if val:
            wt_enable_option_box_in_conf_in_space_record(
                selenium, user, field, space, onepanel)

    wt_clicks_on_save_config_btn_in_space_record(selenium, user, space,
                                                 onepanel)
    notify_visible_with_text(selenium, user, notify_type, notify_text_regexp)


def copy_id_of_space_gui(selenium, user, space_name, onepanel, tmp_memory):
    wt_expand_space_item_in_spaces_page_op_panel(selenium, user, space_name,
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
    wt_expand_space_item_in_spaces_page_op_panel(selenium, user, space,
                                                 onepanel)
    wt_assert_proper_space_configuration_in_panel(selenium, user, sync_type,
                                                  space, conf, onepanel)


@given(parsers.parse('user of {browser_id} revokes all spaces supports'))
@repeat_failed(timeout=WAIT_FRONTEND)
def revoke_all_space_supports(selenium, browser_id, onepanel, popups, modals):
    spaces_list = onepanel(selenium[browser_id]).content.spaces.spaces
    option = 'Revoke space support'
    button = 'Yes, revoke'

    for space in spaces_list:
        space.toolbar.click()
        wt_clicks_on_btn_in_space_toolbar_in_panel(selenium, browser_id,
                                                   option, popups)
        wt_clicks_on_btn_in_revoke_space_support(selenium, browser_id,
                                                 button, modals)
