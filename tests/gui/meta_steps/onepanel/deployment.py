"""This module contains gherkin meta steps to run acceptance tests featuring
deployment management in onezone web GUI.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import re
import time
from typing import Any, Tuple

import yaml

from tests.gui.meta_steps.onezone.provider import send_copied_invite_token_in_oz_gui
from tests.gui.steps.common.login import login_using_basic_auth
from tests.gui.steps.common.notifies import notify_visible_with_text
from tests.gui.steps.onepanel.deployment import (
    wt_assert_begin_of_cluster_deployment,
    wt_check_host_options_list_in_deployment_step1,
    wt_click_on_add_btn_in_storage_add_form,
    wt_click_on_btn_in_deployment_step,
    wt_click_perform_check_in_dns_setup_step,
    wt_click_proceed_in_dns_setup_step,
    wt_click_yes_in_warning_modal_in_dns_setup_step,
    wt_select_storage_type_in_deployment_step5,
    wt_type_property_to_in_box_in_deployment_step,
    wt_type_text_to_in_box_in_deployment_step,
    wt_type_text_to_in_box_in_deployment_step5,
)
from tests.gui.steps.onepanel.provider import deactivate_request_subdomain_toggle
from tests.utils.bdd_utils import parsers, wt


@wt(
    parsers.parse(
        "user of {browser_id} sets options for {host_regexp} host in "
        "step 1 of deployment process with following "
        "configuration:\n{config}"
    )
)
def setup_step1(
    selenium: Any, browser_id: Any, host_regexp: Any, config: Any, hosts: Any
) -> Any:
    """
    config:

    zone name: <name of onezone> where only "onezone" property is taken
    zone domain: <domain of onezone> where only "onezone" property is taken
    options:
     - Database
     - Cluster Worker
     - Cluster Manager
     - Primary Cluster Manager
    """
    _setup_step1(selenium, browser_id, host_regexp, config, hosts)


def _setup_step1(
    selenium: Any, browser_id: Any, host_regexp: Any, configuration: Any, hosts: Any
) -> Any:
    config = yaml.load(configuration, yaml.Loader)
    options = config.get("options", [])
    step = "step 1"
    btn = "Deploy"

    wt_check_host_options_list_in_deployment_step1(
        selenium, browser_id, options, host_regexp
    )
    if "onezone" in host_regexp:
        zone_for_name, zone_for_domain = _parse_zone_data(
            config["zone name"], config["zone domain"]
        )
        _setup_onezone_in_step1(
            selenium,
            browser_id,
            zone_for_name,
            zone_for_domain,
            hosts,
        )
        wt_click_on_btn_in_deployment_step(selenium, browser_id, btn, step)
        wt_assert_begin_of_cluster_deployment(selenium, browser_id)
    else:
        wt_click_on_btn_in_deployment_step(selenium, browser_id, btn, step)


def _parse_zone_data(zone_name: str, zone_domain: str) -> Tuple[str, str]:
    match_name = re.match(r"/name of (.+)/", zone_name)
    if match_name is None:
        raise ValueError(f"Cannot parse zone name from: {zone_name}")
    zone_from_name = match_name.group(1)

    match_domain = re.match(r"/domain of (.+)/", zone_domain)
    if match_domain is None:
        raise ValueError(f"Cannot parse zone domain from: {zone_domain}")
    zone_from_domain = match_domain.group(1)

    return zone_from_name, zone_from_domain


def _setup_onezone_in_step1(
    selenium: Any, browser_id: Any, zone_for_name: Any, zone_for_domain: Any, hosts: Any
) -> Any:
    step = "step 1"

    name_property = "name"
    name_input_box = "Zone name"
    wt_type_property_to_in_box_in_deployment_step(
        selenium,
        browser_id,
        zone_for_name,
        name_property,
        name_input_box,
        step,
        hosts,
    )
    hostname_property = "hostname"
    hostname_input_box = "Zone domain name"
    wt_type_property_to_in_box_in_deployment_step(
        selenium,
        browser_id,
        zone_for_domain,
        hostname_property,
        hostname_input_box,
        step,
        hosts,
    )


@wt(
    parsers.parse(
        "user of {browser_id} performs DNS check in deployment "
        "setup DNS step and proceeds"
    )
)
def setup_dns(selenium: Any, browser_id: Any) -> Any:
    wt_click_perform_check_in_dns_setup_step(selenium, browser_id)
    wt_click_proceed_in_dns_setup_step(selenium, browser_id)
    wt_click_yes_in_warning_modal_in_dns_setup_step(selenium, browser_id)


@wt(
    parsers.parse(
        "user of {browser_id} logs as {user_login}, copies "
        "provider cluster registration "
        "token and sends it to user of {browser_id2}"
    )
)
def enable_provider_cluster_registration_for_user(
    selenium: Any,
    browser_id: Any,
    user_login: Any,
    browser_id2: Any,
    users: Any,
    tmp_memory: Any,
    displays: Any,
    clipboard: Any,
) -> Any:
    last_step_btn = "Manage cluster via onezone"
    last_step = "last step"
    wt_click_on_btn_in_deployment_step(selenium, browser_id, last_step_btn, last_step)
    service = "Onezone"
    login_using_basic_auth(selenium, browser_id, user_login, users, service)
    send_copied_invite_token_in_oz_gui(
        selenium,
        browser_id,
        browser_id2,
        tmp_memory,
        displays,
        clipboard,
    )


@wt(
    parsers.parse(
        "user of {browser_id} registers provider in step 2 of "
        "deployment process in Onepanel with following config:\n"
        "{config}"
    )
)
def setup_step2(selenium: Any, browser_id: Any, hosts: Any, config: Any) -> Any:
    """
    provider: provider_name
    request a subdomain: True/False
    email: email@email.email
    """
    _setup_step2(selenium, browser_id, hosts, config)
    time.sleep(5)


def _setup_step2(selenium: Any, browser_id: Any, hosts: Any, configuration: Any) -> Any:
    config = yaml.load(configuration, yaml.Loader)
    provider_for_name, provider_for_domain = _parse_provider(
        config["name"], config["domain"]
    )
    request_a_subdomain = config.get("request a subdomain", False)
    email = config["email"]
    step = "step 2"

    name_property = "name"
    name_input_box = "Provider name"
    wt_type_property_to_in_box_in_deployment_step(
        selenium,
        browser_id,
        provider_for_name,
        name_property,
        name_input_box,
        step,
        hosts,
    )

    if not request_a_subdomain:
        deactivate_request_subdomain_toggle(selenium, browser_id)

    hostname_property = "hostname"
    hostname_input_box = "domain"
    wt_type_property_to_in_box_in_deployment_step(
        selenium,
        browser_id,
        provider_for_domain,
        hostname_property,
        hostname_input_box,
        step,
        hosts,
    )

    email_input_box = "admin email"
    wt_type_text_to_in_box_in_deployment_step(
        selenium, browser_id, email, email_input_box, step
    )

    register_button = "Register"
    wt_click_on_btn_in_deployment_step(selenium, browser_id, register_button, step)


def _parse_provider(provider_name: str, provider_domain: str) -> Tuple[str, str]:
    match_name = re.match(r"/name of (.+)/", provider_name)
    if match_name is None:
        raise ValueError(f"Cannot parse provider name from: {provider_name}")
    provider_for_name = match_name.group(1)

    match_domain = re.match(r"/domain of (.+)/", provider_domain)
    if match_domain is None:
        raise ValueError(f"Cannot parse provider domain from: {provider_domain}")
    provider_for_domain = match_domain.group(1)

    return provider_for_name, provider_for_domain


@wt(
    parsers.parse(
        "user of {browser_id} adds storage in step 5 of deployment "
        "process in Onepanel with following config:\n{config}"
    )
)
def add_storage_in_step5(selenium: Any, browser_id: Any, config: Any) -> Any:
    """
    storage type: type of storage
    storage name: name of storage
    """
    _add_storage_in_step5(selenium, browser_id, config)


def _add_storage_in_step5(selenium: Any, browser_id: Any, configuration: Any) -> Any:
    config = yaml.load(configuration, yaml.Loader)
    storage_type = config["storage type"]
    name = config["name"]
    name_box = "Storage name"
    notify_type = "info"
    text_regexp = ".*[Ss]torage.*added.*"

    wt_select_storage_type_in_deployment_step5(selenium, browser_id, storage_type)
    wt_type_text_to_in_box_in_deployment_step5(
        selenium, browser_id, name, storage_type, name_box
    )
    wt_click_on_add_btn_in_storage_add_form(selenium, browser_id)
    notify_visible_with_text(selenium, browser_id, notify_type, text_regexp)
