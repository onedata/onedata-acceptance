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

from tests.utils.acceptance_utils import wt
from tests.gui.steps.onepanel.storages import (
    wt_expands_toolbar_icon_for_storage_in_onepanel,
    wt_clicks_on_btn_in_storage_toolbar_in_panel,
    assert_storage_disappeared_from_list,
    wt_select_storage_type_in_storage_page_op_panel,
    wt_type_text_to_in_box_in_storages_page_op_panel,
    wt_click_on_add_btn_in_storage_add_form_in_storage_page)
from tests.gui.steps.modal import click_modal_button
from tests.gui.steps.onezone.spaces import click_on_option_in_the_sidebar
from tests.gui.steps.onezone.clusters import click_on_record_in_clusters_menu
from tests.gui.steps.onepanel.common import (wt_click_on_subitem_for_item,
                                             wt_click_on_btn_in_content)
from tests.gui.steps.common.notifies import notify_visible_with_text


@wt(parsers.parse('user of {browser_id} removes "{name}" storage '
                  'in Onepanel page'))
def remove_storage_in_op_panel_using_gui(selenium, browser_id, name,
                                         onepanel, popups):
    option = 'Remove storage'
    button = 'Remove'
    modal = 'REMOVE STORAGE'

    wt_expands_toolbar_icon_for_storage_in_onepanel(selenium, browser_id,
                                                    name, onepanel)
    wt_clicks_on_btn_in_storage_toolbar_in_panel(selenium, browser_id,
                                                 option, popups)
    click_modal_button(selenium, browser_id, button, modal)
    assert_storage_disappeared_from_list(selenium, browser_id, name,
                                         onepanel)


@wt(parsers.re('user of (?P<browser_id>.+?) creates "(?P<name>.*)" storage '
               'in "(?P<provider_name>.+?)" Oneprovider panel service '
               'with following configuration:\n'
               '(?P<config>(.|\s)*)'))
def create_storage_in_op_panel_using_gui(selenium, browser_id, name,
                                         provider_name, config, oz_page,
                                         hosts, onepanel):
    """ Create storage according to given config.

        Config format given in yaml is as follow:

            storage type: storage_type             --> required
            mount point: mount_point               --> required

    """

    sidebar = 'Clusters'
    sub_item = 'Storages'
    content = 'storages'
    btn = 'Add storage'
    form = 'POSIX'
    input_box = 'Storage name'
    mount_point_option = 'mount point'
    notify_type = 'info'
    text_regexp = '.*[Ss]torage.*added.*'

    options = yaml.load(config)
    driver = selenium[browser_id]
    onezone_url_pattern = 'https?://[^/]*/ozw/.*'

    if re.match(onezone_url_pattern, driver.current_url):
        click_on_option_in_the_sidebar(selenium, browser_id, sidebar, oz_page)
        click_on_record_in_clusters_menu(selenium, browser_id, oz_page,
                                         provider_name, hosts)

    wt_click_on_subitem_for_item(selenium, browser_id, sidebar,
                                 sub_item, provider_name, onepanel, hosts)
    wt_click_on_btn_in_content(selenium, browser_id, btn, content, onepanel)

    storage_type = options['storage type']
    wt_select_storage_type_in_storage_page_op_panel(selenium, browser_id,
                                                    storage_type, onepanel)
    wt_type_text_to_in_box_in_storages_page_op_panel(selenium, browser_id,
                                                     name, form, onepanel,
                                                     input_box)
    mount_point = options[mount_point_option]
    wt_type_text_to_in_box_in_storages_page_op_panel(selenium, browser_id,
                                                     mount_point, form, onepanel,
                                                     mount_point_option)
    wt_click_on_add_btn_in_storage_add_form_in_storage_page(selenium,
                                                            browser_id,
                                                            onepanel)
    notify_visible_with_text(selenium, browser_id, notify_type, text_regexp)

