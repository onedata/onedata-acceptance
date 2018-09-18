"""This module contains gherkin steps to run acceptance tests featuring
deployment management in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import re
import time

from pytest_bdd import when, then, parsers

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.generic import repeat_failed, parse_seq, transform
from tests.gui.utils.generic import click_on_web_elem
from tests.utils.acceptance_utils import wt


@when(parsers.parse('user of {browser_id} enables {options} options for '
                    '{host_regexp} host in step 1 of deployment process '
                    'in Onepanel'))
@then(parsers.parse('user of {browser_id} enables {options} options for '
                    '{host_regexp} host in step 1 of deployment process '
                    'in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_check_host_options_in_deployment_step1(selenium, browser_id, options,
                                              host_regexp, onepanel):
    options = [transform(option) for option in parse_seq(options)]
    # without this, deployment failed randomly when launched locally
    time.sleep(1)
    for host in onepanel(selenium[browser_id]).content.deployment.step1.hosts:
        if re.match(host_regexp, host.name):
            for option in options:
                getattr(host, option).check()
    time.sleep(1)


@when(parsers.re('user of (?P<browser_id>.+?) types "(?P<text>.+?)" to '
                 '(?P<input_box>.+?) field in '
                 '(?P<step>step 1|step 2|step 4|last step) of deployment '
                 'process in Onepanel'))
@then(parsers.re('user of (?P<browser_id>.+?) types "(?P<text>.+?)" to '
                 '(?P<input_box>.+?) field in '
                 '(?P<step>step 1|step 2|step 4|last step) of deployment '
                 'process in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_text_to_in_box_in_deployment_step(selenium, browser_id, text,
                                              input_box, step, onepanel):
    step = getattr(onepanel(selenium[browser_id]).content.deployment,
                   step.replace(' ', ''))
    setattr(step, transform(input_box), text)


@when(parsers.re('user of (?P<browser_id>.+?) types '
                 '(?P<property>name|hostname) of "(?P<alias>.+?)" '
                 '(zone|provider) to (?P<input_box>.+?) field in '
                 '(?P<step>step 1|step 2) of deployment '
                 'process in Onepanel'))
@then(parsers.re('user of (?P<browser_id>.+?) types (?P<property>name|hostname) '
                 'of "(?P<alias>.+?)" '
                 '(zone|provider) to (?P<input_box>.+?) field in '
                 '(?P<step>step 1|step 2) of deployment '
                 'process in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_property_to_in_box_in_deployment_step(selenium, browser_id, alias,
                                                  property, input_box,
                                                  step, onepanel, hosts):
    text = hosts[alias][property]
    step = getattr(onepanel(selenium[browser_id]).content.deployment,
                   step.replace(' ', ''))
    setattr(step, transform(input_box), text)


@when(parsers.re('user of (?P<browser_id>.+?) clicks on (?P<btn>.+?) button '
                 'in (?P<step>step 1|step 2|step 3|web cert step|step 5|last step) of '
                 'deployment process in Onepanel'))
@then(parsers.re('user of (?P<browser_id>.+?) clicks on (?P<btn>.+?) button '
                 'in (?P<step>step 1|step 2|step 3|web cert step|step 5|last step) of '
                 'deployment process in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_btn_in_deployment_step(selenium, browser_id, btn,
                                       step, onepanel):
    step = getattr(onepanel(selenium[browser_id]).content.deployment,
                   step.replace(' ', ''))
    getattr(step, transform(btn)).click()


@when(parsers.parse('user of {browser_id} sees that cluster '
                    'deployment has started'))
@then(parsers.parse('user of {browser_id} sees that cluster '
                    'deployment has started'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_begin_of_cluster_deployment(selenium, browser_id, modals):
    _ = modals(selenium[browser_id]).cluster_deployment


@when(parsers.parse('user of {browser_id} waits {timeout:d} seconds '
                    'for cluster deployment to finish'))
@then(parsers.parse('user of {browser_id} waits {timeout:d} seconds '
                    'for cluster deployment to finish'))
def wt_await_finish_of_cluster_deployment(selenium, browser_id,
                                          timeout, modals):
    driver = selenium[browser_id]
    limit = time.time() + timeout
    while time.time() < limit:
        try:
            modals(driver).cluster_deployment
        except RuntimeError:
            break
        else:
            time.sleep(1)
            continue
    else:
        raise RuntimeError('cluster deployment exceeded '
                           'time limit: {}'.format(timeout))


@wt(parsers.re('user of (?P<browser_id>.*) clicks on "Perform check" '
               'button in deployment setup DNS step'))
def wt_click_perform_check_in_dns_setup_step(selenium, browser_id, onepanel):
    onepanel(selenium[browser_id]).content.deployment.setup_dns.perform_check()


@wt(parsers.re('user of (?P<browser_id>.*) clicks on Proceed '
               'button in deployment setup DNS step'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_proceed_in_dns_setup_step(selenium, browser_id, onepanel):
    onepanel(selenium[browser_id]).content.deployment.setup_dns.proceed()


@wt(parsers.re('user of (?P<browser_id>.*) clicks on Yes '
               'button in warning modal in deployment setup DNS step'))
def wt_click_yes_in_warning_modal_in_dns_setup_step(selenium, browser_id, modals):
    modals(selenium[browser_id]).dns_configuration_warning.yes()


@when(parsers.re('user of (?P<browser_id>.*) clicks on "Setup IP addresses" '
                 'button in deployment setup IP step'))
@then(parsers.re('user of (?P<browser_id>.*) clicks on "Setup IP addresses" '
                 'button in deployment setup IP step'))
def wt_click_setup_ip_in_deployment_setup_ip(selenium, browser_id, onepanel):
    (onepanel(selenium[browser_id])
            .content
            .deployment
            .setup_ip
            .setup_ip_addresses
            .click())


@when(parsers.re('user of (?P<browser_id>.*) types "(?P<new_ip>'
                 '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" for "(?P<hostname>.*)" '
                 'hostname in deployment setup IP step'))
@then(parsers.re('user of (?P<browser_id>.*) types "(?P<new_ip>'
                 '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" for "(?P<hostname>.*)" '
                 'hostname in deployment setup IP step'))
def wt_type_ip_address_for_hostname_in_deployment_setup_ip(selenium, browser_id,
                                                           onepanel, hostname,
                                                           new_ip):
    all_nodes = onepanel(selenium[browser_id]).content.deployment.setup_ip.nodes
    nodes = [node for node in all_nodes if node.hostname == hostname]
    for node in nodes:
        node.ip_address = new_ip


@when(parsers.re('user of (?P<browser_id>.*) sees that IP address for '
                 '"(?P<hostname>.*)" hostname is "(?P<expected_ip>\d{1,3}\.\d'
                 '{1,3}\.\d{1,3}\.\d{1,3})" in deployment setup IP step'))
@then(parsers.re('user of (?P<browser_id>.*) sees that IP address for '
                 '"(?P<hostname>.*)" hostname is "(?P<expected_ip>\d{1,3}\.\d'
                 '{1,3}\.\d{1,3}\.\d{1,3})" in deployment setup IP step'))
def wt_assert_ip_address_in_deployment_setup_ip(selenium, browser_id, onepanel,
                                                hostname, expected_ip):
    all_nodes = onepanel(selenium[browser_id]).content.deployment.setup_ip.nodes
    nodes = [node for node in all_nodes if node.hostname == hostname]
    for node in nodes:
        assert node.ip_address==expected_ip, "{} ip is {} instead of {}".format(
                                        hostname, node.ip_address, expected_ip)


@when(parsers.re('user of (?P<browser_id>.*) sees that IP address of '
                 '"(?P<host>.*)" host is that of "(?P<ip_host>.*)" in'
                 ' deployment setup IP step'))
@then(parsers.re('user of (?P<browser_id>.*) sees that IP address of '
                 '"(?P<host>.*)" host is that of "(?P<ip_host>.*)" in'
                 ' deployment setup IP step'))
def wt_assert_ip_address_of_known_host_in_deployment_setup_ip(selenium, host,
                                                              browser_id, hosts,
                                                              onepanel, ip_host):
    hostname = hosts[host]['hostname']
    expected_ip = hosts[ip_host]['ip']
    all_nodes = onepanel(selenium[browser_id]).content.deployment.setup_ip.nodes
    nodes = [node for node in all_nodes if node.hostname == hostname]
    for node in nodes:
        assert node.ip_address == expected_ip, ("{} ip is {} instead of {}".
                                format( hostname, node.ip_address, expected_ip))


@when(parsers.re('user of (?P<browser_id>.*) activates lets encrypt toggle in '
                 'web cert step of deployment process in Onepanel'))
@then(parsers.re('user of (?P<browser_id>.*) activates lets encrypt toggle in '
                 'web cert step of deployment process in Onepanel'))
def wt_activate_lets_encrypt_toggle_in_deployment_step4(selenium, browser_id,
                                                        onepanel):
    (onepanel(selenium[browser_id])
        .content
        .deployment
        .webcertstep
        .lets_encrypt_toggle
        .check())


@when(parsers.re('user of (?P<browser_id>.*) deactivates lets encrypt toggle '
                 'in web cert step of deployment process in Onepanel'))
@then(parsers.re('user of (?P<browser_id>.*) deactivates lets encrypt toggle '
                 'in web cert step of deployment process in Onepanel'))
def wt_deactivate_lets_encrypt_toggle_in_deployment_step4(selenium, browser_id,
                                                          onepanel):
    (onepanel(selenium[browser_id])
        .content
        .deployment
        .webcertstep
        .lets_encrypt_toggle
        .uncheck())


@when(parsers.parse('user of {browser_id} selects {storage_type} from storage '
                    'selector in step 5 of deployment process in Onepanel'))
@then(parsers.parse('user of {browser_id} selects {storage_type} from storage '
                    'selector in step 5 of deployment process in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_select_storage_type_in_deployment_step5(selenium, browser_id,
                                               storage_type, onepanel):
    storage_selector = (onepanel(selenium[browser_id]).content.deployment
                        .step5.form.storage_selector)
    storage_selector.expand()
    storage_selector.options[storage_type].click()


@when(parsers.re('user of (?P<browser_id>.*?) enables "(?P<option>.*?)" '
                 'in (?P<form>POSIX) form in step 5 of deployment process '
                 'in Onepanel'))
@then(parsers.re('user of (?P<browser_id>.*?) enables "(?P<option>.*?)" '
                 ' in (?P<form>POSIX) form in step 5 of deployment process '
                 'in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_enable_storage_option_in_deployment_step5(selenium, browser_id, option,
                                                 form, onepanel):
    form = getattr(onepanel(selenium[browser_id]).content.deployment
                   .step5.form, transform(form))
    getattr(form, transform(option)).check()


@when(parsers.re('user of (?P<browser_id>.*?) types "(?P<text>.*?)" to '
                 '(?P<input_box>.*?) field in (?P<form>POSIX) form '
                 'in step 5 of deployment process in Onepanel'))
@then(parsers.re('user of (?P<browser_id>.*?) types "(?P<text>.*?)" to '
                 '(?P<input_box>.*?) field in (?P<form>POSIX) form '
                 'in step 5 of deployment process in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_text_to_in_box_in_deployment_step5(selenium, browser_id, text,
                                               form, onepanel, input_box):
    form = getattr(onepanel(selenium[browser_id]).content.deployment.step5.form,
                   transform(form))
    setattr(form, transform(input_box), text)


@when(parsers.parse('user of {browser_id} clicks on Add button in add storage '
                    'form in step 5 of deployment process in Onepanel'))
@then(parsers.parse('user of {browser_id} clicks on Add button in add storage '
                    'form in step 5 of deployment process in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_add_btn_in_storage_add_form(selenium, browser_id, onepanel):
    onepanel(selenium[browser_id]).content.deployment.step5.form.add()


@when(parsers.parse('user of {browser_id} expands "{storage}" record on '
                    'storages list in step 5 of deployment process '
                    'in Onepanel'))
@then(parsers.parse('user of {browser_id} expands "{storage}" record on '
                    'storages list in step 5 of deployment process '
                    'in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_expand_storage_item_in_deployment_step5(selenium, browser_id,
                                               storage, onepanel):
    storages = onepanel(selenium[browser_id]).content.deployment.step5.storages
    storages[storage].expand()


@when(parsers.re('user of (?P<browser_id>.*?) sees that "(?P<st>.*?)" '
                 '(?P<attr>Storage type|Mount point) is (?P<val>.*?) '
                 'in step 5 of deployment process in Onepanel'))
@then(parsers.re('user of (?P<browser_id>.*?) sees that "(?P<st>.*?)" '
                 '(?P<attr>Storage type|Mount point) is (?P<val>.*?) '
                 'in step 5 of deployment process in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_storage_attr_in_deployment_step5(selenium, browser_id, st,
                                               attr, val, onepanel):
    storages = onepanel(selenium[browser_id]).content.deployment.step5.storages
    displayed_val = getattr(storages[st], transform(attr)).lower()
    assert displayed_val == val.lower(), \
        'expected {} as storage attribute; got {}'.format(displayed_val, val)
