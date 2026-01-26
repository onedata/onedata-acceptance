"""This module contains gherkin steps to run acceptance tests featuring
deployment management in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import re
import time

from selenium.webdriver.common.by import By

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.utils import LoginPage, Modals, Onepanel, Popups
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.environment_utils import add_etc_hosts_entries
from tests.utils.utils import repeat_failed


@given(
    parsers.re(
        "users? of (?P<browser_id_list>.*) created admin accounts? "
        '"(?P<name>.*):(?P<passphrase>.*)"'
    )
)
def g_create_admin_in_panels(selenium, browser_id_list, passphrase):
    for browser_id in parse_seq(browser_id_list):
        g_create_admin_in_panel(selenium, browser_id, passphrase)


@repeat_failed(timeout=WAIT_FRONTEND)
def g_create_admin_in_panel(selenium, browser_id, passphrase):
    init_page = Onepanel(selenium[browser_id]).init_page
    init_page.create_new_cluster()
    init_page.passphrase = passphrase
    init_page.confirm_passphrase = passphrase
    init_page.submit_button()


@wt(
    parsers.parse(
        "user of {browser_id} enables {options} options for "
        "{host_regexp} host in step 1 of deployment process "
        "in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_check_host_options_in_deployment_step1(
    selenium, browser_id, options, host_regexp
):
    parsed_options = parse_seq(options)
    wt_check_host_options_list_in_deployment_step1(
        selenium, browser_id, parsed_options, host_regexp
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def wt_check_host_options_list_in_deployment_step1(
    selenium, browser_id, options, host_regexp
):
    options = [transform(option) for option in options]
    # without this, deployment failed randomly when launched locally
    time.sleep(5)
    for host in Onepanel(selenium[browser_id]).content.deployment.step1.hosts:
        if re.match(host_regexp, host.name):
            for option in options:
                getattr(host, option).check()
    time.sleep(1)


@wt(
    parsers.re(
        'user of (?P<browser_id>.+?) types "(?P<text>.+?)" to '
        "(?P<input_box>.+?) field in "
        "(?P<step>step 1|step 2|step 4|last step) "
        "of deployment process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_text_to_in_box_in_deployment_step(
    selenium, browser_id, text: str, input_box, step
):
    step = getattr(
        Onepanel(selenium[browser_id]).content.deployment, step.replace(" ", "")
    )
    setattr(step, transform(input_box), text)


@wt(
    parsers.re(
        "user of (?P<browser_id>.+?) types second host to "
        "(?P<input_box>.+?) field in "
        "(?P<step>step 1|step 2|step 4|last step) of deployment "
        "process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_second_host_to_in_box_in_deployment_step(
    selenium, browser_id, input_box, step
):
    step = getattr(
        Onepanel(selenium[browser_id]).content.deployment, step.replace(" ", "")
    )
    text = step.hostname_label
    text = text.replace("0", "1") if "0" in text else text.replace("1", "0")
    setattr(step, transform(input_box), text)


@wt(
    parsers.re(
        "user of (?P<browser_id>.+?) types "
        '(?P<name_property>name|hostname) of "(?P<alias>.+?)" '
        "(zone|provider) to (?P<input_box>.+?) field in "
        "(?P<step>step 1|step 2) of deployment "
        "process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_property_to_in_box_in_deployment_step(
    selenium, browser_id, alias, name_property, input_box, step, hosts
):
    text = hosts[alias][name_property]
    step = getattr(
        Onepanel(selenium[browser_id]).content.deployment, step.replace(" ", "")
    )
    setattr(step, transform(input_box), text)


@wt(
    parsers.re(
        "user of (?P<browser_id>.+?) clicks on (?P<btn>.+?) button "
        "in (?P<step>step 1|step 2|step 3|web cert step|"
        "step 5|last step) of deployment process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def wt_click_on_btn_in_deployment_step(selenium, browser_id, btn, step):
    driver = selenium[browser_id]
    step = getattr(Onepanel(driver).content.deployment, step.lower().replace(" ", ""))
    getattr(step, transform(btn)).click()
    if btn == "Add host":

        for _ in range(10):
            selector = driver.find_elements(
                By.CSS_SELECTOR, ".cluster-host-table .cluster-host-table-row"
            )
            if len(selector) < 2:
                time.sleep(1)
            else:
                break


@wt(
    parsers.parse(
        "user of {browser_id} tries to register provider using Register button in"
        " {step} of deployment process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def wt_try_to_register_prov_using_register_btn(selenium, browser_id, step):
    driver = selenium[browser_id]
    btn = "Register"
    step = getattr(Onepanel(driver).content.deployment, step.lower().replace(" ", ""))
    getattr(step, transform(btn)).click()

    # if error modal occurred close it and repeat function execution
    try:
        error_modal = Modals(driver).error
        error_modal.close.click()
        raise AssertionError("Did not menage to register provider")
    except RuntimeError:
        pass


@repeat_failed(timeout=WAIT_FRONTEND)
def wait_for_next_step_in_deployment(driver, next_step_num):
    assert (
        int(Onepanel(driver).content.deployment.num) == next_step_num
        or Modals(driver).error.is_displayed()
    )


@wt(parsers.parse("user of {browser_id} sees that cluster deployment has started"))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_begin_of_cluster_deployment(selenium, browser_id):
    _ = Modals(selenium[browser_id]).cluster_deployment


@wt(
    parsers.parse(
        "user of {browser_id} waits {timeout:d} seconds "
        "for cluster deployment to finish"
    )
)
def wt_await_finish_of_cluster_deployment(selenium, browser_id, timeout):
    driver = selenium[browser_id]
    limit = time.time() + timeout
    while time.time() < limit:
        try:
            Modals(driver).cluster_deployment
        except RuntimeError:
            break
        else:
            time.sleep(1)
            continue
    else:
        raise RuntimeError(f"cluster deployment exceeded time limit: {timeout}")


@wt(
    parsers.re(
        'user of (?P<browser_id>.*) clicks on "Perform check" '
        "button in deployment setup DNS step"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_perform_check_in_dns_setup_step(selenium, browser_id):
    Onepanel(selenium[browser_id]).content.deployment.setup_dns.perform_check()


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) clicks on Proceed "
        "button in deployment setup DNS step"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_proceed_in_dns_setup_step(selenium, browser_id):
    Onepanel(selenium[browser_id]).content.deployment.setup_dns.proceed()


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) clicks on Yes "
        "button in warning modal in deployment setup DNS step"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_yes_in_warning_modal_in_dns_setup_step(selenium, browser_id):
    Modals(selenium[browser_id]).dns_configuration_warning.yes()


@wt(
    parsers.re(
        'user of (?P<browser_id>.*) clicks on "Setup IP addresses" '
        "button in deployment setup IP step"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def wt_click_setup_ip_in_deployment_setup_ip(selenium, browser_id):
    (
        Onepanel(
            selenium[browser_id]
        ).content.deployment.setup_ip.setup_ip_addresses.click()
    )


@wt(
    parsers.re(
        'user of (?P<browser_id>.*) types "(?P<new_ip>'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" for "(?P<hostname>.*)" '
        "hostname in deployment setup IP step"
    )
)
def wt_type_ip_address_for_hostname_in_deployment_setup_ip(
    selenium, browser_id, hostname, new_ip
):
    all_nodes = Onepanel(selenium[browser_id]).content.deployment.setup_ip.nodes
    nodes = [node for node in all_nodes if node.hostname == hostname]
    for node in nodes:
        node.ip_address = new_ip


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) sees that IP address for "
        r'"(?P<hostname>.*)" hostname is "(?P<expected_ip>\d{1,3}\.\d'
        r'{1,3}\.\d{1,3}\.\d{1,3})" in deployment setup IP step'
    )
)
def wt_assert_ip_address_in_deployment_setup_ip(
    selenium, browser_id, hostname, expected_ip
):
    all_nodes = Onepanel(selenium[browser_id]).content.deployment.setup_ip.nodes
    nodes = [node for node in all_nodes if node.hostname == hostname]
    for node in nodes:
        assert (
            node.ip_address == expected_ip
        ), f"{hostname} ip is {node.ip_address} instead of {expected_ip}"


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) sees that IP address of "
        '"(?P<host>.*)" host is that of "(?P<ip_host>.*)" in'
        " deployment setup IP step"
    )
)
@repeat_failed(timeout=WAIT_BACKEND * 4, interval=1)
def wt_assert_ip_address_of_known_host_in_deployment_setup_ip(
    selenium, host, browser_id, hosts, ip_host
):
    hostname = hosts[host]["hostname"]
    expected_ip = hosts[ip_host]["ip"]
    all_nodes = Onepanel(selenium[browser_id]).content.deployment.setup_ip.nodes
    nodes = [node for node in all_nodes if node.hostname == hostname]
    for node in nodes:
        assert (
            node.ip_address == expected_ip
        ), f"{hostname} ip is {node.ip_address} instead of {expected_ip}"


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) activates lets encrypt toggle in "
        "web cert step of deployment process in Onepanel"
    )
)
def wt_activate_lets_encrypt_toggle_in_deployment_step4(selenium, browser_id):
    (
        Onepanel(
            selenium[browser_id]
        ).content.deployment.webcertstep.lets_encrypt_toggle.check()
    )


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) deactivates lets encrypt toggle "
        "in web cert step of deployment process in Onepanel"
    )
)
def wt_deactivate_lets_encrypt_toggle_in_deployment_step4(selenium, browser_id):
    (
        Onepanel(
            selenium[browser_id]
        ).content.deployment.webcertstep.lets_encrypt_toggle.uncheck()
    )


@wt(
    parsers.parse(
        "user of {browser_id} selects {storage_type} from storage "
        "selector in step 5 of deployment process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_select_storage_type_in_deployment_step5(selenium, browser_id, storage_type):
    storage_selector = Onepanel(
        selenium[browser_id]
    ).content.deployment.step5.form.storage_selector
    storage_selector.expand()
    storage_selector_list = Popups(selenium[browser_id]).dropdown
    storage_selector_list.options[storage_type].click()


@wt(
    parsers.re(
        'user of (?P<browser_id>.*?) enables "(?P<option>.*?)" '
        "in (?P<form>POSIX) form in step 5 of "
        "deployment process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_enable_storage_option_in_deployment_step5(selenium, browser_id, option, form):
    form = getattr(
        Onepanel(selenium[browser_id]).content.deployment.step5.form,
        transform(form),
    )
    getattr(form, transform(option)).check()


@wt(
    parsers.re(
        'user of (?P<browser_id>.*?) types "(?P<text>.*?)" to '
        "(?P<input_box>.*?) field in (?P<form>POSIX) form "
        "in step 5 of deployment process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_text_to_in_box_in_deployment_step5(
    selenium, browser_id, text, form, input_box
):
    form = getattr(
        Onepanel(selenium[browser_id]).content.deployment.step5.form,
        transform(form),
    )
    setattr(form, transform(input_box), text)


@wt(
    parsers.parse(
        "user of {browser_id} clicks on Add button in add storage "
        "form in step 5 of deployment process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_add_btn_in_storage_add_form(selenium, browser_id):
    Onepanel(selenium[browser_id]).content.deployment.step5.form.add()


@wt(
    parsers.parse(
        'user of {browser_id} expands "{storage}" record on '
        "storages list in step 5 of deployment process "
        "in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_expand_storage_item_in_deployment_step5(selenium, browser_id, storage):
    storages = Onepanel(selenium[browser_id]).content.deployment.step5.storages
    storages[storage].expand()


@wt(
    parsers.re(
        'user of (?P<browser_id>.*?) sees that "(?P<st>.*?)" '
        "(?P<attr>Storage type|Mount point) is (?P<val>.*?) "
        "in step 5 of deployment process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_storage_attr_in_deployment_step5(selenium, browser_id, st, attr, val):
    storages = Onepanel(selenium[browser_id]).content.deployment.step5.storages
    displayed_val = getattr(storages[st], transform(attr)).lower()
    assert (
        displayed_val == val.lower()
    ), f"expected {displayed_val} as storage attribute; got {val}"


@wt(
    parsers.re(
        "user of (?P<browser_id>.*?) types received registration token "
        "in step 2 of deployment process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_registration_token_in_step2(selenium, browser_id, tmp_memory):
    token = tmp_memory[browser_id]["mailbox"]["token"]
    Onepanel(selenium[browser_id]).content.deployment.step2.token = token


@wt(
    parsers.re(
        "user of (?P<browser_id>.*?) clicks proceed button in step 2 "
        "of deployment process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_proceed_button_in_step2(selenium, browser_id):
    Onepanel(selenium[browser_id]).content.deployment.step2.proceed()


@wt(
    parsers.re(
        "user of (?P<browser_id>.*?) clicks on link to go "
        "to Emergency Onepanel interface in last step "
        "of deployment process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_go_to_emergency_onepanel_interface(selenium, browser_id):
    Onepanel(selenium[browser_id]).content.deployment.laststep.link()


@wt(
    parsers.parse(
        'provider "{provider}" with onezone domain host entry is added to /etc/hosts'
    )
)
def add_prov_with_oz_subdomain_to_etc_host(hosts, provider):
    new_hostname = f"{hosts[provider]["name"]}.{hosts["onezone"]["hostname"]}"
    add_etc_hosts_entries(
        hosts[provider]["ip"],
        new_hostname,
    )
    hosts[provider]["hostname"] = new_hostname


@wt(
    parsers.parse(
        "user of {browser_id} waits till login page of emergency interface of Onepanel"
        " appears"
    )
)
@repeat_failed(timeout=WAIT_BACKEND * 2)
def wait_for_emergency_interface_onepanel(browser_id, selenium):
    assert LoginPage(selenium[browser_id]).open_in_onezone.is_displayed()
