"""This module contains gherkin meta steps to run acceptance tests featuring
deployment management in onezone web GUI.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import yaml

from tests.gui.meta_steps.onezone.provider import (
    send_copied_invite_token_in_oz_gui)
from tests.gui.steps.common.login import wt_login_using_basic_auth
from tests.gui.steps.common.notifies import notify_visible_with_text
from tests.gui.steps.onepanel.deployment import *
from tests.gui.steps.onepanel.provider import (
    deactivate_request_subdomain_toggle)
from tests.utils.bdd_utils import wt, parsers


@wt(parsers.parse('user of {browser_id} sets options for {host_regexp} host in '
                  'step 1 of deployment process with following '
                  'configuration:\n{config}'))
def setup_step1(selenium, browser_id, onepanel, host_regexp, config, hosts,
                modals):
    """
    config:

    zone name: <name of onezone> where only "onezone" property is taken
    zone domain: <domain of onezone> where only "onezone" property is taken
    options:
     - Database
     - Cluster Worker
     - Cluster Manager
     - Primary Cluster Manager
     - Ceph
    """
    _setup_step1(selenium, browser_id, onepanel, host_regexp, config, hosts,
                 modals)


def _setup_step1(selenium, browser_id, onepanel, host_regexp, configuration,
                 hosts, modals):
    config = yaml.load(configuration)
    options = config.get('options', [])
    step = 'step 1'
    btn = 'Deploy'

    wt_check_host_options_list_in_deployment_step1(selenium, browser_id,
                                                   options, host_regexp,
                                                   onepanel)
    if 'onezone' in host_regexp:
        zone_for_name, zone_for_domain = _parse_zone_data(
            config['zone name'], config['zone domain'])
        _setup_onezone_in_step1(selenium, browser_id, zone_for_name,
                                zone_for_domain, onepanel,
                                hosts)
        wt_click_on_btn_in_deployment_step(selenium, browser_id, btn, step,
                                           onepanel)
        wt_assert_begin_of_cluster_deployment(selenium, browser_id, modals)
    else:
        wt_click_on_btn_in_deployment_step(selenium, browser_id, btn, step,
                                           onepanel)


def _parse_zone_data(zone_name, zone_domain):
    zone_from_name = re.match(r'/name of (.+)/', zone_name).group(1)
    zone_from_domain = re.match(r'/domain of (.+)/', zone_domain).group(1)
    return zone_from_name, zone_from_domain


def _setup_onezone_in_step1(selenium, browser_id, zone_for_name,
                            zone_for_domain, onepanel, hosts):
    step = 'step 1'

    name_property = 'name'
    name_input_box = 'Zone name'
    wt_type_property_to_in_box_in_deployment_step(selenium, browser_id,
                                                  zone_for_name, name_property,
                                                  name_input_box, step,
                                                  onepanel, hosts)
    hostname_property = 'hostname'
    hostname_input_box = 'Zone domain name'
    wt_type_property_to_in_box_in_deployment_step(selenium, browser_id,
                                                  zone_for_domain,
                                                  hostname_property,
                                                  hostname_input_box, step,
                                                  onepanel, hosts)


@wt(parsers.parse('user of {browser_id} performs DNS check in deployment '
                  'setup DNS step and proceeds'))
def setup_dns(selenium, browser_id, onepanel, modals):
    wt_click_perform_check_in_dns_setup_step(selenium, browser_id, onepanel)
    wt_click_proceed_in_dns_setup_step(selenium, browser_id, onepanel)
    wt_click_yes_in_warning_modal_in_dns_setup_step(selenium, browser_id,
                                                    modals)


@wt(parsers.parse('user of {browser_id} logs as {user_login}, copies '
                  'provider cluster registration '
                  'token and sends it to user of {browser_id2}'))
def enable_provider_cluster_registration_for_user(selenium, browser_id,
                                                  user_login,
                                                  browser_id2, onepanel,
                                                  login_page, users, oz_page,
                                                  tmp_memory, displays,
                                                  clipboard):
    last_step_btn = 'Manage cluster via onezone'
    last_step = 'last step'
    wt_click_on_btn_in_deployment_step(selenium, browser_id, last_step_btn,
                                       last_step, onepanel)
    service = 'Onezone'
    wt_login_using_basic_auth(selenium, browser_id, user_login, login_page,
                              users, service)
    send_copied_invite_token_in_oz_gui(selenium, browser_id, oz_page,
                                       browser_id2, tmp_memory, displays,
                                       clipboard)


@wt(parsers.parse('user of {browser_id} registers provider in step 2 of '
                  'deployment process in Onepanel with following config:\n'
                  '{config}'))
def setup_step2(selenium, browser_id, onepanel, hosts, config):
    """
        provider: provider_name
        request a subdomain: True/False
        email: email@email.email
    """
    _setup_step2(selenium, browser_id, onepanel, hosts, config)
    time.sleep(5)


def _setup_step2(selenium, browser_id, onepanel, hosts, configuration):
    config = yaml.load(configuration)
    provider_for_name, provider_for_domain = _parse_provider(config['name'],
                                                             config['domain'])
    request_a_subdomain = config.get('request a subdomain', False)
    email = config['email']
    step = 'step 2'

    name_property = 'name'
    name_input_box = 'Provider name'
    wt_type_property_to_in_box_in_deployment_step(selenium, browser_id,
                                                  provider_for_name,
                                                  name_property,
                                                  name_input_box, step,
                                                  onepanel, hosts)

    if not request_a_subdomain:
        deactivate_request_subdomain_toggle(selenium, browser_id, onepanel)

    hostname_property = 'hostname'
    hostname_input_box = 'domain'
    wt_type_property_to_in_box_in_deployment_step(selenium, browser_id,
                                                  provider_for_domain,
                                                  hostname_property,
                                                  hostname_input_box, step,
                                                  onepanel, hosts)

    email_input_box = 'admin email'
    wt_type_text_to_in_box_in_deployment_step(selenium, browser_id, email,
                                              email_input_box, step, onepanel)

    register_button = 'Register'
    wt_click_on_btn_in_deployment_step(selenium, browser_id, register_button,
                                       step, onepanel)


def _parse_provider(provider_name, provider_domain):
    provider_for_name = re.match(r'/name of (.+)/', provider_name).group(1)
    provider_for_domain = re.match(r'/domain of (.+)/',
                                   provider_domain).group(1)
    return provider_for_name, provider_for_domain


@wt(parsers.parse('user of {brwoser_id} deploys Ceph with following '
                  'configuration:\n{config}'))
def setup_ceph_config(selenium, browser_id, onepanel, config, modals):
    """
    Manager And Monitor: True/False
    OSDs:          - only with Manager&Monitor enabled
      - 1.5 GiB
      - 2 GiB      - takes one or two OSDs
    """
    _setup_ceph_config(selenium, browser_id, onepanel, config, modals)


def _setup_ceph_config(selenium, browser_id, onepanel, configuration, modals):
    config = yaml.load(configuration)
    manager_and_monitor = config.get('Manager And Monitor', False)
    if manager_and_monitor:
        enable_manager_and_monitor_toggle_in_ceph_config_step(selenium,
                                                              browser_id,
                                                              onepanel)
        osds = config['OSDs']
        osd1, osd2 = _unpack_osds(osds)
        first_number = 'first'
        _set_osd_of_number(selenium, browser_id, osd1, first_number, onepanel,
                           modals)
        if osd2:
            second_number = 'second'
            _set_osd_of_number(selenium, browser_id, osd2, second_number,
                               onepanel, modals)
    deploy_button = 'Deploy'
    step = 'Ceph configuration step'
    wt_click_on_btn_in_deployment_step(selenium, browser_id, deploy_button,
                                       step, onepanel)
    wt_assert_begin_of_cluster_deployment(selenium, browser_id, modals)


def _unpack_osds(osds):
    if len(osds) == 1:
        return osds[0], None
    return osds[0], osds[1]


def _set_osd_of_number(selenium, browser_id, size, number, onepanel, modals):
    osd_button = 'Add OSD'
    step = 'Ceph configuration step'
    wt_click_on_btn_in_deployment_step(selenium, browser_id, osd_button, step,
                                       onepanel)
    [size_number, size_unit] = size.split()
    type_osd_size_to_input(selenium, number, size_number, browser_id, onepanel)
    choose_osd_unit(selenium, number, size_unit, browser_id, onepanel, modals)


@wt(parsers.parse('user of {browser_id} adds storage in step 5 of deployment '
                  'process in Onepanel with following config:\n{config}'))
def add_storage_in_step5(selenium, browser_id, onepanel, config):
    """
        storage type: type of storage
        storage name: name of storage
    """
    _add_storage_in_step5(selenium, browser_id, onepanel, config)


def _add_storage_in_step5(selenium, browser_id, onepanel, configuration):
    config = yaml.load(configuration)
    storage_type = config['storage type']
    name = config['name']
    name_box = 'Storage name'
    notify_type = 'info'
    text_regexp = '.*[Ss]torage.*added.*'

    wt_select_storage_type_in_deployment_step5(selenium, browser_id,
                                               storage_type, onepanel)
    wt_type_text_to_in_box_in_deployment_step5(selenium, browser_id, name,
                                               storage_type, onepanel,
                                               name_box)
    wt_click_on_add_btn_in_storage_add_form(selenium, browser_id, onepanel)
    notify_visible_with_text(selenium, browser_id, notify_type, text_regexp)

