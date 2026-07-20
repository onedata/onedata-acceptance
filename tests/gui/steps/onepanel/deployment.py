"""This module contains gherkin steps to run acceptance tests featuring
deployment management in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import re
import time
from typing import Optional, cast

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.expected_conditions import (
    invisibility_of_element_located,
    visibility_of_element_located,
)
from selenium.webdriver.support.ui import WebDriverWait

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.common.common import (
    try_click_without_throwing_error,
    wait_till_error_modal_stop_appearing,
)
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils import LoginPage, Modals, Onepanel, Popups
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    parse_elements_sequence,
    transform,
)
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.environment_utils import add_etc_hosts_entries
from tests.utils.utils import repeat_failed


@given(
    parsers.re(
        rf"users? of (?P<browser_id_list>{ELEMENTS_SEQUENCE_PATTERN}) created admin"
        r" accounts? "
        r'"(?P<name>.*):(?P<passphrase>.*)"'
    ),
    converters={
        "browser_id_list": parse_elements_sequence,
    },
)
def g_create_admin_in_panels(
    selenium: SeleniumDrivers, browser_id_list: list[str], passphrase: str
) -> None:
    for browser_id in browser_id_list:
        g_create_admin_in_panel(selenium, browser_id, passphrase)


@repeat_failed(timeout=WAIT_FRONTEND)
def g_create_admin_in_panel(
    selenium: SeleniumDrivers, browser_id: str, passphrase: str
) -> None:
    init_page = Onepanel(selenium[browser_id]).init_page
    init_page.create_new_cluster()
    init_page.passphrase = passphrase
    init_page.confirm_passphrase = passphrase
    init_page.submit_button()


@wt(
    parsers.parse(
        "user of {browser_id} enables {options} options for "
        "{host_pattern} host in step 1 of deployment process "
        "in Onepanel"
    ),
    converters={
        "options": parse_elements_sequence,
    },
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_check_host_options_in_deployment_step1(
    selenium: SeleniumDrivers,
    browser_id: str,
    options: list[str],
    host_pattern: str,
) -> None:
    wt_check_host_options_list_in_deployment_step1(
        selenium, browser_id, options, host_pattern
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def wt_check_host_options_list_in_deployment_step1(
    selenium: SeleniumDrivers,
    browser_id: str,
    options: list[str],
    host_pattern: str,
) -> None:
    options = [transform(option) for option in options]
    # without this, deployment failed randomly when launched locally
    time.sleep(5)
    for host in Onepanel(selenium[browser_id]).content.deployment.step1.hosts:
        if re.match(host_pattern, host.name):
            for option in options:
                getattr(host, option).check()
    time.sleep(1)


@wt(
    parsers.re(
        r'user of (?P<browser_id>.+?) types "(?P<text>.+?)" to '
        r"(?P<input_box>.+?) field in "
        r"(?P<step>step 1|step 2|step 4|last step) "
        r"of deployment process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_text_to_in_box_in_deployment_step(
    selenium: SeleniumDrivers,
    browser_id: str,
    text: str,
    input_box: str,
    step: str,
) -> None:
    step = getattr(
        Onepanel(selenium[browser_id]).content.deployment, step.replace(" ", "")
    )
    setattr(step, transform(input_box), text)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) types second host to "
        r"(?P<input_box>.+?) field in "
        r"(?P<step>step 1|step 2|step 4|last step) of deployment "
        r"process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_second_host_to_in_box_in_deployment_step(
    selenium: SeleniumDrivers, browser_id: str, input_box: str, step: str
) -> None:
    deployment_step = getattr(
        Onepanel(selenium[browser_id]).content.deployment, step.replace(" ", "")
    )
    text = deployment_step.hostname_label
    text = text.replace("0", "1") if "0" in text else text.replace("1", "0")
    setattr(deployment_step, transform(input_box), text)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) types "
        r'(?P<name_property>name|hostname) of "(?P<alias>.+?)" '
        r"(zone|provider) to (?P<input_box>.+?) field in "
        r"(?P<step>step 1|step 2) of deployment "
        r"process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_property_to_in_box_in_deployment_step(
    selenium: SeleniumDrivers,
    browser_id: str,
    alias: str,
    name_property: str,
    input_box: str,
    step: str,
    hosts: Hosts,
) -> None:
    text = cast(dict[str, str], hosts[alias])[name_property]
    step = getattr(
        Onepanel(selenium[browser_id]).content.deployment, step.replace(" ", "")
    )
    setattr(step, transform(input_box), text)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) clicks on (?P<btn>.+?) button "
        r"in (?P<step>step 1|step 2|step 3|web cert step|"
        r"step 5|last step) of deployment process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def wt_click_on_btn_in_deployment_step(
    selenium: SeleniumDrivers, browser_id: str, btn: str, step: str
) -> None:
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
        " step 2 of deployment process in Onepanel"
    )
)
def register_prov_using_register_btn(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    step = Onepanel(driver).content.deployment.step2

    max_time = 120
    start_time = time.time()
    while time.time() - start_time < max_time:
        try_click_without_throwing_error(
            lambda: step.register.click(),  # pylint: disable=unnecessary-lambda
            timeout=1,
        )
        if _check_error_modal_appeared_or_registration_finished(driver):
            return
        time.sleep(0.1)
    raise AssertionError("Registering provider failed after 120s")


def _check_error_modal_appeared_or_registration_finished(
    driver: WebDriver,
) -> Optional[bool]:
    error_modal_css_sel = ".alert-global.modal.in .modal-dialog"
    sidebar_css_sel = ".one-sidebar.sidebar-clusters"

    if _is_element_visible_on_page(driver, error_modal_css_sel):  # error modal appeared
        wait_till_error_modal_stop_appearing(driver)
        return False

    if _is_element_visible_on_page(
        driver, sidebar_css_sel
    ):  # sidebar is visible, it means we closed deployment page
        return True

    return None  # neither error modal appeared nor the deployment page closed


def _is_element_visible_on_page(driver: WebDriver, css_selector: str) -> bool:
    try:
        return visibility_of_element_located((By.CSS_SELECTOR, css_selector))(driver)
    except NoSuchElementException:
        return False


def wait_for_provider_registration(
    driver: WebDriver, register_btn_css_sel: str
) -> None:
    WebDriverWait(driver, 120).until(
        invisibility_of_element_located((By.CSS_SELECTOR, register_btn_css_sel)),
        "Provider registration is still in progress after 120s",
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def wait_for_next_step_in_deployment(driver: WebDriver, next_step_num: int) -> None:
    assert (
        int(Onepanel(driver).content.deployment.num) == next_step_num
        or Modals(driver).error.is_displayed()
    )


@wt(parsers.parse("user of {browser_id} sees that cluster deployment has started"))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_begin_of_cluster_deployment(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    _ = Modals(selenium[browser_id]).cluster_deployment


@wt(
    parsers.parse(
        "user of {browser_id} waits {timeout:d} seconds "
        "for cluster deployment to finish"
    )
)
def wt_await_finish_of_cluster_deployment(
    selenium: SeleniumDrivers, browser_id: str, timeout: int
) -> None:
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
        r'user of (?P<browser_id>.*) clicks on "Perform check" '
        r"button in deployment setup DNS step"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_perform_check_in_dns_setup_step(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    Onepanel(selenium[browser_id]).content.deployment.setup_dns.perform_check()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) clicks on Proceed "
        r"button in deployment setup DNS step"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_proceed_in_dns_setup_step(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    Onepanel(selenium[browser_id]).content.deployment.setup_dns.proceed()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) clicks on Yes "
        r"button in warning modal in deployment setup DNS step"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_yes_in_warning_modal_in_dns_setup_step(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    Modals(selenium[browser_id]).dns_configuration_warning.yes()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) clicks on "Setup IP addresses" '
        r"button in deployment setup IP step"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def wt_click_setup_ip_in_deployment_setup_ip(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    (
        Onepanel(
            selenium[browser_id]
        ).content.deployment.setup_ip.setup_ip_addresses.click()
    )


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) types "(?P<new_ip>'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})" for "(?P<hostname>.*)" '
        r"hostname in deployment setup IP step"
    )
)
def wt_type_ip_address_for_hostname_in_deployment_setup_ip(
    selenium: SeleniumDrivers, browser_id: str, hostname: str, new_ip: str
) -> None:
    all_nodes = Onepanel(selenium[browser_id]).content.deployment.setup_ip.nodes
    nodes = [node for node in all_nodes if node.hostname == hostname]
    for node in nodes:
        node.ip_address = new_ip


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees that IP address for "
        r'"(?P<hostname>.*)" hostname is "(?P<expected_ip>\d{1,3}\.\d'
        r'{1,3}\.\d{1,3}\.\d{1,3})" in deployment setup IP step'
    )
)
def wt_assert_ip_address_in_deployment_setup_ip(
    selenium: SeleniumDrivers,
    browser_id: str,
    hostname: str,
    expected_ip: str,
) -> None:
    all_nodes = Onepanel(selenium[browser_id]).content.deployment.setup_ip.nodes
    nodes = [node for node in all_nodes if node.hostname == hostname]
    for node in nodes:
        assert (
            node.ip_address == expected_ip
        ), f"{hostname} ip is {node.ip_address} instead of {expected_ip}"


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees that IP address of "
        r'"(?P<host>.*)" host is that of "(?P<ip_host>.*)" in'
        r" deployment setup IP step"
    )
)
@repeat_failed(timeout=WAIT_BACKEND * 4, interval=1)
def wt_assert_ip_address_of_known_host_in_deployment_setup_ip(
    selenium: SeleniumDrivers,
    host: str,
    browser_id: str,
    hosts: Hosts,
    ip_host: str,
) -> None:
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
        r"user of (?P<browser_id>.*) activates lets encrypt toggle in "
        r"web cert step of deployment process in Onepanel"
    )
)
def wt_activate_lets_encrypt_toggle_in_deployment_step4(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    (
        Onepanel(
            selenium[browser_id]
        ).content.deployment.webcertstep.lets_encrypt_toggle.check()
    )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) deactivates lets encrypt toggle "
        r"in web cert step of deployment process in Onepanel"
    )
)
def wt_deactivate_lets_encrypt_toggle_in_deployment_step4(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
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
def wt_select_storage_type_in_deployment_step5(
    selenium: SeleniumDrivers, browser_id: str, storage_type: str
) -> None:
    storage_selector = Onepanel(
        selenium[browser_id]
    ).content.deployment.step5.form.storage_selector
    storage_selector.expand()
    storage_selector_list = Popups(selenium[browser_id]).dropdown
    storage_selector_list.options[storage_type].click()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) enables "(?P<option>.*?)" '
        r"in (?P<form>POSIX) form in step 5 of "
        r"deployment process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_enable_storage_option_in_deployment_step5(
    selenium: SeleniumDrivers, browser_id: str, option: str, form: str
) -> None:
    form = getattr(
        Onepanel(selenium[browser_id]).content.deployment.step5.form,
        transform(form),
    )
    getattr(form, transform(option)).check()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) types "(?P<text>.*?)" to '
        r"(?P<input_box>.*?) field in (?P<form>POSIX) form "
        r"in step 5 of deployment process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_text_to_in_box_in_deployment_step5(
    selenium: SeleniumDrivers,
    browser_id: str,
    text: str,
    form: str,
    input_box: str,
) -> None:
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
def wt_click_on_add_btn_in_storage_add_form(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    Onepanel(selenium[browser_id]).content.deployment.step5.form.add()


@wt(
    parsers.parse(
        'user of {browser_id} expands "{storage}" record on '
        "storages list in step 5 of deployment process "
        "in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_expand_storage_item_in_deployment_step5(
    selenium: SeleniumDrivers, browser_id: str, storage: str
) -> None:
    storages = Onepanel(selenium[browser_id]).content.deployment.step5.storages
    storages[storage].expand()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) sees that "(?P<st>.*?)" '
        r"(?P<attribute>Storage type|Mount point) is (?P<val>.*?) "
        r"in step 5 of deployment process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_storage_attr_in_deployment_step5(
    selenium: SeleniumDrivers, browser_id: str, st: str, attribute: str, val: str
) -> None:
    storages = Onepanel(selenium[browser_id]).content.deployment.step5.storages
    displayed_val = getattr(storages[st], transform(attribute)).lower()
    assert (
        displayed_val == val.lower()
    ), f"expected {displayed_val} as storage attribute; got {val}"


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) types received registration token "
        r"in step 2 of deployment process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_registration_token_in_step2(
    selenium: SeleniumDrivers, browser_id: str, tmp_memory: TmpMemory
) -> None:
    token = tmp_memory[browser_id]["mailbox"]["token"]
    Onepanel(selenium[browser_id]).content.deployment.step2.token = token


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) clicks proceed button in step 2 "
        r"of deployment process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_proceed_button_in_step2(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    Onepanel(selenium[browser_id]).content.deployment.step2.proceed()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) clicks on link to go "
        r"to Emergency Onepanel interface in last step "
        r"of deployment process in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_go_to_emergency_onepanel_interface(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    Onepanel(selenium[browser_id]).content.deployment.laststep.link()


@wt(
    parsers.parse(
        'provider "{provider}" with onezone domain host entry is added to /etc/hosts'
    )
)
def add_prov_with_oz_subdomain_to_etc_host(hosts: Hosts, provider: str) -> None:
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
def wait_for_emergency_interface_onepanel(
    browser_id: str, selenium: SeleniumDrivers
) -> None:
    assert LoginPage(selenium[browser_id]).open_in_onezone.is_displayed()
