"""This module contains meta steps for operations on provider in Onepanel
using web GUI
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


import yaml

from tests.gui.steps.onepanel.common import (
    wt_click_on_subitem_for_item_with_name, wt_click_on_btn_in_content,
    wt_click_on_subitem_for_item)
from tests.gui.steps.onepanel.provider import *
from tests.gui.steps.common.notifies import *
from tests.gui.steps.common.miscellaneous import *
from tests.gui.steps.onepanel.deployment import *
from tests.gui.steps.common.url import *
from tests.gui.steps.onepanel.provider import (
    wt_click_on_discard_btn_in_domain_change_modal)
from tests.utils.bdd_utils import given


def modify_provider_with_given_name_in_op_panel_using_gui(selenium, user,
                                                          onepanel,
                                                          provider_name,
                                                          new_provider_name,
                                                          new_domain,
                                                          panel_login_page,
                                                          users, hosts,
                                                          browser_id, modals):
    sidebar = 'CLUSTERS'
    sub_item = 'Provider configuration'
    button = 'Edit settings'
    content = 'provider'
    prov_name_attr = 'Provider name'
    red_point_attr = 'Domain'
    notify_type = 'info'
    notify_text_regexp = '.*[Pp]rovider.*data.*modified.*'

    wt_click_on_subitem_for_item_with_name(selenium, user, sidebar, sub_item,
                                           provider_name, onepanel)

    wt_click_on_btn_in_content(selenium, user, button, content, onepanel)
    wt_type_val_to_in_box_in_provider_details_form(selenium, user,
                                                   new_provider_name,
                                                   prov_name_attr, onepanel)
    wt_type_val_to_in_box_in_provider_details_form(selenium, user,
                                                   new_domain,
                                                   red_point_attr, onepanel)
    wt_save_changes_in_modify_provider_detail_form(selenium, user, onepanel)
    notify_visible_with_text(selenium, user, notify_type, notify_text_regexp)
    wt_click_on_discard_btn_in_domain_change_modal(selenium, browser_id, modals)
    wt_assert_value_of_provider_attribute(selenium, user, prov_name_attr,
                                          new_provider_name, onepanel)
    wt_assert_value_of_provider_attribute(selenium, user, red_point_attr,
                                          new_domain, onepanel)


@wt(parsers.re('user of (?P<browser_id>.*?) deregisters '
               'provider in "(?P<provider_name>.+?)" Oneprovider panel '
               'service'))
def deregister_provider_in_op_panel_using_gui(selenium, browser_id,
                                              provider_name, onepanel, popups,
                                              hosts):
    sidebar = 'CLUSTERS'
    sub_item = 'Provider configuration'
    content = 'provider'
    popup = 'Deregister provider'

    wt_click_on_subitem_for_item(selenium, browser_id, sidebar, sub_item,
                                 provider_name, onepanel, hosts)
    wt_click_on_btn_in_content(selenium, browser_id, 'Deregister provider',
                               content, onepanel)
    wt_click_on_btn_in_popup(selenium, browser_id, 'Yes, deregister', popup,
                             popups)
    notify_visible_with_text(selenium, browser_id, 'info',
                             '.*[Pp]rovider.*deregistered.*')


def register_provider_in_op_using_gui(selenium, user, onepanel, hosts, config,
                                      tmp_memory):
    step2 = 'step 2'
    options = yaml.load(config)

    wt_type_registration_token_in_step2(selenium, user, onepanel,
                                        tmp_memory)
    wt_click_proceed_button_in_step2(selenium, user, onepanel)

    time.sleep(1)
    deactivate_request_subdomain_toggle(selenium, user, onepanel)

    try:
        provider_name = options['provider name']['of provider']
    except KeyError:
        wt_type_text_to_in_box_in_deployment_step(
            selenium, user, options['provider name'], 'Provider name', step2,
            onepanel)
    else:
        wt_type_property_to_in_box_in_deployment_step(
            selenium, user, provider_name, 'name', 'Provider name', step2,
            onepanel, hosts)
    try:
        provider_name = options['domain']['of provider']
    except KeyError:
        wt_type_text_to_in_box_in_deployment_step(
            selenium, user, options['domain'], 'Domain', step2, onepanel)
    else:
        wt_type_property_to_in_box_in_deployment_step(
            selenium, user, provider_name, 'hostname', 'Domain', step2,
            onepanel, hosts)

    wt_type_text_to_in_box_in_deployment_step(selenium, user, 
                                              options['admin email'], 
                                              'Admin email', step2, onepanel)

    wt_click_on_btn_in_deployment_step(selenium, user, 'Register', step2,
                                       onepanel)


@given(parsers.re('provider name set to name of "(?P<provider>.+?)" '
                  '(?P<by>by user of|by) (?P<browser_id>.+?) in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_provider_name_if_name_is_different_than_given(selenium, browser_id,
                                                         provider, hosts,
                                                         onepanel,  login_page,
                                                         users, modals):
    sub_item = 'Provider configuration'
    record = 0
    sidebar = 'CLUSTERS'

    wt_click_on_subitem_for_item_with_name(selenium, browser_id, sidebar,
                                           sub_item, record, onepanel)

    current_provider = (onepanel(selenium[browser_id])
                        .content
                        .provider
                        .details
                        .provider_name)
    domain = hosts[provider]['hostname']
    provider = hosts[provider]['name']
    if current_provider != provider:
        modify_provider_with_given_name_in_op_panel_using_gui(selenium,
                                                              browser_id,
                                                              onepanel,
                                                              current_provider,
                                                              provider, domain,
                                                              login_page,
                                                              users, hosts,
                                                              browser_id, modals)
