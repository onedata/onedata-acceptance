"""This module contains meta steps for operations on provider in Onepanel
using web GUI
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import time

import yaml

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import wt_click_on_btn_in_popup
from tests.gui.steps.common.notifies import notify_visible_with_text
from tests.gui.steps.onepanel.common import (
    wt_click_on_btn_in_content,
    wt_click_on_subitem_for_item,
    wt_click_on_subitem_for_item_with_name,
)
from tests.gui.steps.onepanel.deployment import (
    wt_click_on_btn_in_deployment_step,
    wt_click_proceed_button_in_step2,
    wt_type_property_to_in_box_in_deployment_step,
    wt_type_registration_token_in_step2,
    wt_type_text_to_in_box_in_deployment_step,
)
from tests.gui.steps.onepanel.provider import (
    deactivate_request_subdomain_toggle,
    wt_assert_value_of_provider_attribute,
    wt_click_on_discard_btn_in_domain_change_modal,
    wt_save_changes_in_modify_provider_detail_form,
    wt_type_val_to_in_box_in_provider_details_form,
)
from tests.gui.steps.rest.provider import (
    add_provider_service_node,
    get_provider_service_nodes_statuses,
    start_stop_provider_service_node,
)
from tests.gui.utils import Onepanel
from tests.gui.utils.generic import OnedataService
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.utils import repeat_failed


def modify_provider_with_given_name_in_op_panel_using_gui(
    selenium,
    user,
    provider_name,
    new_provider_name,
    new_domain,
    browser_id,
):
    sidebar = "CLUSTERS"
    sub_item = "Provider configuration"
    button = "Edit settings"
    content = "provider"
    prov_name_attr = "Provider name"
    red_point_attr = "Domain"
    notify_type = "info"
    notify_text_regexp = ".*[Pp]rovider.*data.*modified.*"

    wt_click_on_subitem_for_item_with_name(
        selenium, user, sidebar, sub_item, provider_name
    )

    wt_click_on_btn_in_content(selenium, user, button, content)
    wt_type_val_to_in_box_in_provider_details_form(
        selenium, user, new_provider_name, prov_name_attr
    )
    wt_type_val_to_in_box_in_provider_details_form(
        selenium, user, new_domain, red_point_attr
    )
    wt_save_changes_in_modify_provider_detail_form(selenium, user)
    notify_visible_with_text(selenium, user, notify_type, notify_text_regexp)
    wt_click_on_discard_btn_in_domain_change_modal(selenium, browser_id)
    wt_assert_value_of_provider_attribute(
        selenium, user, prov_name_attr, new_provider_name
    )
    wt_assert_value_of_provider_attribute(selenium, user, red_point_attr, new_domain)


@wt(
    parsers.re(
        "user of (?P<browser_id>.*?) deregisters "
        'provider in "(?P<provider_name>.+?)" Oneprovider panel '
        "service"
    )
)
def deregister_provider_in_op_panel_using_gui(
    selenium, browser_id, provider_name, hosts
):
    sidebar = "CLUSTERS"
    sub_item = "Provider configuration"
    content = "provider"
    popup = "Deregister provider"

    wt_click_on_subitem_for_item(
        selenium, browser_id, sidebar, sub_item, provider_name, hosts
    )
    wt_click_on_btn_in_content(selenium, browser_id, "Deregister provider", content)
    wt_click_on_btn_in_popup(selenium, browser_id, "Yes, deregister", popup)
    notify_visible_with_text(
        selenium, browser_id, "info", ".*[Pp]rovider.*deregistered.*"
    )


def register_provider_in_op_using_gui(selenium, user, hosts, config, tmp_memory):
    step2 = "step 2"
    options = yaml.load(config, yaml.Loader)

    wt_type_registration_token_in_step2(selenium, user, tmp_memory)
    wt_click_proceed_button_in_step2(selenium, user)

    time.sleep(1)
    deactivate_request_subdomain_toggle(selenium, user)

    try:
        provider_name = options["provider name"]["of provider"]
    except KeyError:
        wt_type_text_to_in_box_in_deployment_step(
            selenium,
            user,
            options["provider name"],
            "Provider name",
            step2,
        )
    else:
        wt_type_property_to_in_box_in_deployment_step(
            selenium,
            user,
            provider_name,
            "name",
            "Provider name",
            step2,
            hosts,
        )
    try:
        provider_name = options["domain"]["of provider"]
    except KeyError:
        wt_type_text_to_in_box_in_deployment_step(
            selenium, user, options["domain"], "Domain", step2
        )
    else:
        wt_type_property_to_in_box_in_deployment_step(
            selenium,
            user,
            provider_name,
            "hostname",
            "Domain",
            step2,
            hosts,
        )

    wt_type_text_to_in_box_in_deployment_step(
        selenium, user, options["admin email"], "Admin email", step2
    )

    wt_click_on_btn_in_deployment_step(selenium, user, "Register", step2)


@given(
    parsers.re(
        'provider name set to name of "(?P<provider>.+?)" '
        "(?P<by>by user of|by) (?P<browser_id>.+?) in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def change_provider_name_if_name_is_different_than_given(
    selenium, browser_id, provider, hosts
):
    sub_item = "Provider configuration"
    record = 0
    sidebar = "CLUSTERS"

    wt_click_on_subitem_for_item_with_name(
        selenium, browser_id, sidebar, sub_item, record
    )

    current_provider = Onepanel(
        selenium[browser_id]
    ).content.provider.details.provider_name
    domain = hosts[provider]["hostname"]
    provider = hosts[provider]["name"]
    if current_provider != provider:
        modify_provider_with_given_name_in_op_panel_using_gui(
            selenium,
            browser_id,
            current_provider,
            provider,
            domain,
            browser_id,
        )


@wt(
    parsers.parse(
        "user {user} sees that oneS3 node in provider cluster in {provider} is of"
        ' status "{status}"'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_provider_cluster_ones3_node_status_rest(
    hosts, provider, onepanel_credentials, status
):
    host = f"{hosts[provider]['pod-name']}.{hosts[provider]["hostname"]}"
    res = get_provider_service_nodes_statuses(
        hosts, provider, onepanel_credentials, OnedataService.ONES3
    )
    exp_res = {host: status}
    err_msg = f"expected {exp_res}, but got {res}"
    assert exp_res == res, err_msg


@wt(parsers.parse("user {user} adds oneS3 node to provider cluster in {provider}"))
def add_provider_cluster_ones3_node_rest(hosts, provider, onepanel_credentials):
    host = f"{hosts[provider]['pod-name']}.{hosts[provider]["hostname"]}"
    data = {"hosts": [host]}
    add_provider_service_node(
        hosts, provider, onepanel_credentials, data, OnedataService.ONES3
    )


@wt(
    parsers.re(
        "user (?P<user>.*?) (?P<option>starts|stops) oneS3 node in provider cluster in"
        " (?P<provider>.*?)"
    )
)
def stop_provider_cluster_ones3_node_rest(
    option, hosts, provider, onepanel_credentials
):
    host = f"{hosts[provider]['pod-name']}.{hosts[provider]["hostname"]}"
    start_stop_provider_service_node(
        hosts,
        host,
        provider,
        onepanel_credentials,
        OnedataService.ONES3,
        start=option == "starts",
    )
