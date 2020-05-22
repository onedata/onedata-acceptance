"""This module contains meta steps for operations on storages in Onepanel
using web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import re

import yaml
from pytest_bdd import parsers

from tests.gui.meta_steps.onezone.common import wt_visit_op
from tests.gui.steps.oneprovider.data_tab import \
    assert_file_browser_in_data_tab_in_op
from tests.utils.acceptance_utils import wt
from tests.gui.steps.onepanel.storages import (
    wt_expands_toolbar_for_storage_in_onepanel,
    wt_clicks_on_btn_in_storage_toolbar_in_panel,
    assert_storage_disappeared_from_list,
    wt_select_storage_type_in_storage_page_op_panel,
    wt_type_text_to_in_box_in_storages_page_op_panel,
    wt_click_on_add_btn_in_storage_add_form_in_storage_page,
    enable_import_in_add_storage_form,
    wt_assert_storage_attr_in_storages_page_op_panel,
    assert_storage_on_storage_list, is_storage_on_storage_list)
from tests.gui.steps.modal import click_modal_button
from tests.gui.steps.onezone.spaces import (
    click_on_option_in_the_sidebar, click_element_on_lists_on_left_sidebar_menu,
    click_on_option_of_space_on_left_sidebar_menu,
    assert_providers_list_contains_provider)
from tests.gui.steps.onezone.clusters import click_on_record_in_clusters_menu
from tests.gui.steps.onepanel.common import (
    wt_click_on_subitem_for_item, wt_click_on_btn_in_content)
from tests.gui.steps.common.notifies import notify_visible_with_text
from tests.utils.bdd_utils import given


@wt(parsers.parse('user of {browser_id} removes "{name}" storage '
                  'in Onepanel page'))
def remove_storage_in_op_panel_using_gui(selenium, browser_id, name, onepanel,
                                         popups, modals):
    option = 'Remove storage'
    button = 'Remove'
    modal = 'REMOVE STORAGE'

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

        Config format given in yaml is as follow:

            storage type: storage_type             --> required
            mount point: mount_point               --> required
            imported storage: true                 --> optional
    """
    _go_to_storage_view_in_clusters(selenium, browser_id, provider_name,
                                    oz_page, hosts, onepanel)
    _add_storage_in_op_panel_using_gui(selenium, browser_id, config, onepanel,
                                       name)


@given(parsers.parse('there is "{storage_name}" storage in '
                     '"{provider_name}" Oneprovider panel service used by user '
                     'of {browser_id} with following configuration:\n{config}'))
def create_storage_if_necessary(storage_name, provider_name, browser_id, config,
                                oz_page, hosts, selenium, onepanel):
    _go_to_storage_view_in_clusters(selenium, browser_id, provider_name,
                                    oz_page, hosts, onepanel)
    if not is_storage_on_storage_list(selenium, browser_id, storage_name,
                                      onepanel):
        _add_storage_in_op_panel_using_gui(selenium, browser_id, config,
                                           onepanel, storage_name)


def _go_to_storage_view_in_clusters(selenium, browser_id, provider_name,
                                    oz_page, hosts, onepanel):
    driver = selenium[browser_id]
    onezone_url_pattern = 'https?://[^/]*/ozw/.*'
    sidebar = 'Clusters'
    sub_item = 'Storages'

    if re.match(onezone_url_pattern, driver.current_url):
        click_on_option_in_the_sidebar(selenium, browser_id, sidebar, oz_page)
        click_on_record_in_clusters_menu(selenium, browser_id, oz_page,
                                         provider_name, hosts)

    wt_click_on_subitem_for_item(selenium, browser_id, sidebar, sub_item,
                                 provider_name, onepanel, hosts)


def _add_storage_in_op_panel_using_gui(selenium, browser_id, config, onepanel,
                                       storage_name):
    content = 'storages'
    btn = 'Add storage'
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

