"""This module contains meta steps for operations on provider in Onepanel
using web GUI
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


import yaml

from tests.gui.steps.onepanel.common import *
from tests.gui.steps.onepanel.provider import *
from tests.gui.steps.common.notifies import *
from tests.gui.steps.common.miscellaneous import *
from tests.gui.steps.onepanel.deployment import *
from tests.gui.steps.common.url import *
from tests.gui.steps.onepanel.provider import (
    wt_click_on_discard_btn_in_domain_change_modal
)


def modify_provider_with_given_name_in_op_panel_using_gui(selenium, user,
                                                          onepanel,
                                                          provider_name,
                                                          new_provider_name,
                                                          new_domain,
                                                          panel_login_page,
                                                          users, hosts,
                                                          browser_id, modals):
    sidebar = 'CLUSTERS'
    sub_item = 'Provider'
    button = 'Modify provider details'
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
    wt_click_on_btn_in_modify_provider_detail_form(selenium, user, onepanel)
    notify_visible_with_text(selenium, user, notify_type, notify_text_regexp)
    wt_click_on_discard_btn_in_domain_change_modal(selenium, browser_id, onepanel,
                                                   modals)
    wt_assert_value_of_provider_attribute(selenium, user, prov_name_attr,
                                          new_provider_name, onepanel)
    wt_assert_value_of_provider_attribute(selenium, user, red_point_attr,
                                          new_domain, onepanel)


def deregister_provider_in_op_panel_using_gui(selenium, user, provider_name,
                                              onepanel, popups, hosts):
    sidebar = 'CLUSTERS'
    sub_item = 'Provider'
    content = 'provider'
    popup = 'Deregister provider'

    wt_click_on_subitem_for_item(selenium, user, sidebar, sub_item,
                                 provider_name, onepanel, hosts)
    wt_click_on_btn_in_content(selenium, user, 'Deregister provider', content,
                               onepanel)
    wt_click_on_btn_in_popup(selenium, user, 'Yes, deregister', popup, popups)
    notify_visible_with_text(selenium, user, 'info',
                             '.*[Pp]rovider.*deregistered.*')


def register_provider_in_op_using_gui(selenium, user, onepanel, hosts, config, modals):
    sidebar = 'CLUSTERS'
    record = 'New cluster'
    step2 = 'step 2'
    step3 = 'step 3'
    webcertstep = 'web cert step'
    step5 = 'step 5'
    storage_type_attr = 'Storage type'
    mount_point_attr = 'Mount point'
    last_step = 'last step'
    notify_type = 'info'
    notify_text_regexp = '.*registered.*successfully.*'

    options = yaml.load(config)

    # step2
    wt_click_on_sidebar_item(selenium, user, sidebar, record, onepanel)
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
        onezone = options['zone domain']['of zone']
    except KeyError:
        wt_type_text_to_in_box_in_deployment_step(
            selenium, user, options['zone domain'], 'Onezone domain', step2,
            onepanel)
    else:
        wt_type_property_to_in_box_in_deployment_step(
            selenium, user, onezone, 'hostname', 'Onezone domain', step2,
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
    notify_visible_with_text(selenium, user, notify_type,
                             notify_text_regexp)

    #step3
    wt_click_setup_ip_in_deployment_setup_ip(selenium, user, onepanel)

    # dns setup
    wt_click_perform_check_in_dns_setup_step(selenium, user, onepanel)
    wt_click_proceed_in_dns_setup_step(selenium, user, onepanel)

    # web cert step
    wt_deactivate_lets_encrypt_toggle_in_deployment_step4(selenium, user, onepanel)
    wt_click_on_btn_in_deployment_step(selenium, user, 'Next step', webcertstep, 
                                       onepanel)

    #step5
    for storage_name, storage_options in options['storages'].items():
        storage_type = storage_options['type']
        mount_point = storage_options['mount point']
        wt_expand_storage_item_in_deployment_step5(selenium, user, storage_name,
                                                   onepanel)
        wt_assert_storage_attr_in_deployment_step5(selenium, user, storage_name,
                                                   storage_type_attr,
                                                   storage_type, onepanel)
        wt_assert_storage_attr_in_deployment_step5(selenium, user, storage_name,
                                                   mount_point_attr,
                                                   mount_point, onepanel)
    wt_click_on_btn_in_deployment_step(selenium, user, 'Finish', step5,
                                       onepanel)
    wt_click_on_btn_in_deployment_step(selenium, user, 'Manage the cluster',
                                       last_step, onepanel)


@given(parsers.re('provider name set to name of "(?P<provider>.+?)" '
                  '(?P<by>by user of|by) (?P<browser_id>.+?) in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_provider_name_if_name_is_different_than_given(selenium, browser_id,
                                                         provider, hosts,
                                                         onepanel,
                                                         login_page,
                                                         users, modals):
    sub_item = 'Provider'
    record = 1
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
