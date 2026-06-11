"""This module contains gherkin steps to run acceptance tests featuring clusters
management in onezone web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time
from typing import Any

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import _enter_text
from tests.gui.utils import OZLoggedIn, Popups, PrivacyPolicy, TermsOfUse
from tests.gui.utils.common.constants import CONFLICT_NAME_SEPARATOR
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed
from tests.conftest import Hosts, SeleniumDrivers


@wt(parsers.parse("user of {browser_id} clicks on {button} button in clusters {where}"))
@repeat_failed(timeout=WAIT_BACKEND)
def click_button_in_cluster_page(selenium: SeleniumDrivers, browser_id: Any, button: Any) -> Any:
    driver = selenium[browser_id]
    getattr(
        OZLoggedIn(driver).get_page_and_click("clusters"), transform(button)
    ).click()


@wt(parsers.parse("user of {browser_id} copies registration token from clusters page"))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_registration_cluster_token(selenium: SeleniumDrivers, browser_id: Any) -> Any:
    driver = selenium[browser_id]
    OZLoggedIn(driver)["clusters"].token_page.copy()


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "Onedatify documentation" link in clusters page'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_docs_link_in_clusters_page(selenium: SeleniumDrivers, browser_id: Any) -> Any:
    driver = selenium[browser_id]
    OZLoggedIn(driver)["clusters"].token_page.onedatify_documentation.click()


@wt(parsers.parse('user of {browser_id} sees "{record}" in clusters menu'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_record_in_clusters_menu(
    selenium: SeleniumDrivers, browser_id: Any, record: Any, hosts: Hosts
) -> Any:
    records = _get_clusters(selenium, browser_id)
    record = hosts[record]["name"]
    assert record in records, f"{record} not in clusters"


def _get_clusters(selenium: SeleniumDrivers, browser_id: Any) -> Any:
    driver = selenium[browser_id]
    return OZLoggedIn(driver).get_page_and_click("clusters").menu


def _get_cluster_record(
    selenium: SeleniumDrivers, browser_id: Any, record_name: Any, hosts: Hosts
) -> Any:
    menu = _get_clusters(selenium, browser_id)
    record = hosts[record_name]["name"]
    return menu[record]


@wt(parsers.parse('user of {browser_id} does not see "{record}" in clusters menu'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_record_not_in_clusters_menu(
    selenium: SeleniumDrivers, browser_id: Any, record: Any, hosts: Hosts
) -> Any:
    record = hosts[record]["name"]
    records = _get_clusters(selenium, browser_id)
    assert record not in records, f"{record} in clusters"


@wt(parsers.parse('user of {browser_id} clicks on "{record}" in clusters menu'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_record_in_clusters_menu(
    selenium: SeleniumDrivers, browser_id: Any, record: Any, hosts: Hosts
) -> Any:
    _get_cluster_record(selenium, browser_id, record, hosts)()


@wt(parsers.parse('user of {browser_id} sees "{record}" subpage in Clusters page'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_subpage_in_cluster_page(
    selenium: SeleniumDrivers, browser_id: Any, record: Any, hosts: Hosts
) -> Any:
    driver = selenium[browser_id]
    page_name = OZLoggedIn(driver)["clusters"].page_name
    record_name = hosts[record]["name"]
    err_msg = f"user does not see {record} page in Clusters page"
    assert page_name == record_name, err_msg


@wt(parsers.parse('user of {browser_id} clicks {option} of "{record}" in the sidebar'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_option_of_record_in_the_sidebar(
    selenium: SeleniumDrivers, browser_id: Any, option: Any
) -> Any:
    driver = selenium[browser_id]
    OZLoggedIn(driver)["clusters"].submenu[option].click()


@wt(parsers.parse('user of {browser_id} clicks "{button}" button in GUI settings page'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_button_in_gui_settings_page(
    selenium: SeleniumDrivers, browser_id: Any, button: Any
) -> Any:
    driver = selenium[browser_id]
    getattr(OZLoggedIn(driver)["clusters"].gui_settings_page, transform(button))()


@wt(
    parsers.parse(
        'user of {browser_id} writes "{text}" in the "{box}" in GUI settings page'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def write_input_in_gui_settings_page(
    selenium: SeleniumDrivers, browser_id: Any, box: Any, text: Any
) -> Any:
    driver = selenium[browser_id]
    input_box = getattr(
        OZLoggedIn(driver)["clusters"].gui_settings_page, transform(box)
    )
    _enter_text(input_box, text)


@wt(parsers.parse("user of {browser_id} removes {notification} in GUI settings page"))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_notification_in_gui_settings_page(
    selenium: SeleniumDrivers, browser_id: Any, notification: Any
) -> Any:
    notification = notification + " input"
    text = " "
    write_input_in_gui_settings_page(selenium, browser_id, notification, text)


@wt(parsers.parse("user of {browser_id} checks the understand notice in clusters page"))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_the_understand_notice(selenium: SeleniumDrivers, browser_id: Any) -> Any:
    driver = selenium[browser_id]
    OZLoggedIn(driver)["clusters"].deregistration_checkbox()


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{provider}" cluster '
        "is not working in clusters menu"
    )
)
@repeat_failed(timeout=WAIT_BACKEND * 4)
def assert_cluster_not_working_in_oz_panel(
    selenium: SeleniumDrivers, browser_id: Any, provider: Any, hosts: Hosts
) -> Any:
    provider_record = _get_cluster_record(selenium, browser_id, provider, hosts)
    time.sleep(3)
    assert provider_record.is_not_working(), f"Provider {provider} is working"


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{provider}" cluster '
        "is working in clusters menu"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_cluster_working_in_oz_panel(
    selenium: SeleniumDrivers, browser_id: Any, provider: Any, hosts: Hosts
) -> Any:
    provider_record = _get_cluster_record(selenium, browser_id, provider, hosts)
    assert provider_record.is_working(), f"Provider {provider} is not working"


@repeat_failed(timeout=WAIT_FRONTEND)
def click_cluster_menu_button(
    selenium: SeleniumDrivers, browser_id: Any, provider: Any, hosts: Hosts
) -> Any:
    provider_record = _get_cluster_record(selenium, browser_id, provider, hosts)
    provider_record.menu_button()


@wt(
    parsers.parse(
        'user of {browser_id} sees only one "{provider}" record in clusters menu'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_one_record_in_clusters_menu(
    selenium: SeleniumDrivers, browser_id: Any, provider: Any, hosts: Hosts
) -> Any:
    _assert_num_cluster_records(selenium, browser_id, provider, 1, hosts)


def _assert_num_cluster_records(
    selenium: SeleniumDrivers, browser_id: Any, provider: Any, num: Any, hosts: Hosts
) -> Any:
    records = _get_clusters(selenium, browser_id)
    record = hosts[provider]["name"]
    selected = [row for row in records if row.name == record]

    assert (
        len(selected) == num
    ), f"Expected {num} {record} record but got {len(selected)}"


@repeat_failed(timeout=WAIT_FRONTEND)
def _get_old_or_new_cluster_record(
    selenium: SeleniumDrivers, browser_id: Any, provider: Any, age: Any, tmp_memory: Any, hosts: Hosts
) -> Any:
    records = _get_clusters(selenium, browser_id)
    return get_old_or_new_cluster_record_from_list(
        provider, records, age, tmp_memory, hosts
    )


def get_old_or_new_cluster_record_from_list(
    provider: Any, prov_list: Any, age: Any, tmp_memory: Any, hosts: Hosts
) -> Any:
    record_name = hosts[provider]["name"]
    old_id = tmp_memory[provider]["cluster id"]

    selected = [row for row in prov_list if row.name == record_name]
    separator = CONFLICT_NAME_SEPARATOR

    # conflicted clusters have 4-letter cluster id digest added to label
    if age == "old":
        new_list = [
            row for row in selected if row.id_hash.strip(separator) == old_id[:4]
        ]
    else:
        new_list = [
            row for row in selected if row.id_hash.strip(separator) != old_id[:4]
        ]

    if new_list:
        return new_list[0]
    raise AssertionError(f"No {provider} cluster record in clusters menu")


@wt(parsers.parse('user of browser sees that {age} "{provider}" cluster is working'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_new_cluster_working(
    selenium: SeleniumDrivers, browser_id: Any, provider: Any, hosts: Hosts, age: Any, tmp_memory: Any
) -> Any:
    record = _get_old_or_new_cluster_record(
        selenium, browser_id, provider, age, tmp_memory, hosts
    )
    assert record.is_working(), f"{provider} cluster not working"


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "{provider}" with {age} '
        "cluster id in clusters menu"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_new_or_old_cluster_record(
    selenium: SeleniumDrivers, browser_id: Any, provider: Any, age: Any, tmp_memory: Any, hosts: Hosts
) -> Any:
    record = _get_old_or_new_cluster_record(
        selenium, browser_id, provider, age, tmp_memory, hosts
    )
    record.click()


@wt(parsers.parse("user of {browser_id} clicks deregistration link in clusters page"))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_deregister_link_in_cluster_page(selenium: SeleniumDrivers, browser_id: Any) -> Any:
    driver = selenium[browser_id]
    OZLoggedIn(driver)["clusters"].deregister_label.click()


@wt(
    parsers.parse(
        "user of {browser_id} clicks on {kind_of_agreement} link in cookies popup"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_link_in_cookies_popup(
    selenium: SeleniumDrivers, browser_id: Any, kind_of_agreement: Any
) -> Any:
    driver = selenium[browser_id]
    kind_of_agreement = transform(kind_of_agreement) + "_link"
    getattr(Popups(driver).cookies, kind_of_agreement)()


@wt(parsers.parse('user of {browser_id} clicks "{button}" button in cookies popup'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_in_cookies_popup(selenium: SeleniumDrivers, browser_id: Any, button: Any) -> Any:
    driver = selenium[browser_id]
    getattr(Popups(driver).cookies, transform(button))()


@wt(parsers.parse('user of {browser_id} sees "{text}" on {kind_of_agreement} page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_message_on_agreement_page(
    selenium: SeleniumDrivers, browser_id: Any, text: Any, kind_of_agreement: Any
) -> Any:
    err_msg = f"Message on {kind_of_agreement} page is not as expected"
    if kind_of_agreement == "privacy policy":
        assert PrivacyPolicy(selenium[browser_id]).message.text == text, err_msg
    else:
        assert TermsOfUse(selenium[browser_id]).message.text == text, err_msg


@wt(
    parsers.re(
        'user of (?P<browser_id>.*?) clicks "(?P<button>.*?)" button '
        "on (?P<kind_of_agreement>privacy policy|terms of use) page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_on_agreement_page(
    selenium: SeleniumDrivers,
    browser_id: Any,
    button: Any,
    kind_of_agreement: Any,
) -> Any:
    if kind_of_agreement == "privacy policy":
        getattr(PrivacyPolicy(selenium[browser_id]), transform(button))()
    else:
        getattr(TermsOfUse(selenium[browser_id]), transform(button))()


@wt(parsers.parse("user of {browser_id} goes to {kind_of_agreement} page"))
@repeat_failed(timeout=WAIT_FRONTEND)
def go_to_agreement_page(selenium: SeleniumDrivers, browser_id: Any, kind_of_agreement: Any) -> Any:
    driver = selenium[browser_id]
    OZLoggedIn(driver)["profile"].profile()
    Popups(driver).user_account_menu.options[kind_of_agreement].click()
