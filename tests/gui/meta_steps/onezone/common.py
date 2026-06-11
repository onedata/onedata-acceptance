"""This module contains meta steps for common operations in Onezone
using web GUI
"""

import time
from itertools import zip_longest
from typing import Any

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.browser_creation import create_instances_of_webdriver
from tests.gui.steps.common.login import login_using_basic_auth
from tests.gui.steps.common.url import g_open_onedata_service_page
from tests.gui.steps.oneprovider.data_tab import (
    assert_browser_in_tab_in_op,
    choose_provider_in_selected_page,
    click_choose_other_oneprovider_on_file_browser,
)
from tests.gui.steps.onezone.providers import parse_seq
from tests.gui.steps.onezone.spaces import (
    click_element_on_lists_on_left_sidebar_menu,
    click_on_option_of_space_on_left_sidebar_menu,
)
from tests.gui.utils import OZLoggedIn, Popups
from tests.gui.utils.core import scroll_to_css_selector
from tests.utils.acceptance_utils import list_parser
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.utils import repeat_failed
from tests.conftest import Capabilities, Hosts, SeleniumDrivers, Users


@given(
    parsers.re(
        "opened (?P<browser_id_list>.*) with (?P<user_list>.*) "
        "signed in to (?P<host_list>.*) service"
    )
)
def login_using_gui(
    host_list: Any,
    selenium: SeleniumDrivers,
    driver: Any,
    tmpdir: Any,
    tmp_memory: Any,
    xvfb: Any,
    driver_type: Any,
    displays: Any,
    screen_width: Any,
    screen_height: Any,
    hosts: Hosts,
    users: Users,
    browser_id_list: Any,
    user_list: Any,
    test_type: Any,
    capabilities: Capabilities,
) -> Any:
    create_instances_of_webdriver(
        selenium,
        driver,
        user_list,
        tmpdir,
        tmp_memory,
        driver_type,
        xvfb,
        screen_width,
        screen_height,
        displays,
        capabilities,
    )
    g_open_onedata_service_page(selenium, user_list, host_list, hosts)
    browsers_to_users = selenium["request"].getfixturevalue("browsers_to_users")

    for browser, user in zip(parse_seq(browser_id_list), parse_seq(user_list)):
        browsers_to_users[browser] = user
        if test_type == "gui":
            selenium[browser] = selenium[user]
            selenium.pop(user, None)
        # some mixed tests steps also use browser instances
        elif test_type == "mixed":
            selenium[browser] = selenium[user]
        tmp_memory[browser] = tmp_memory[user]
        displays[browser] = displays[user]

    # mixed tests use user_list instead of browser_id_list because
    # some mixed steps don't use browser
    login_ids = browser_id_list if test_type == "gui" else user_list
    login_using_basic_auth(selenium, login_ids, user_list, users, host_list)


@repeat_failed(timeout=WAIT_FRONTEND)
def visit_op(selenium: SeleniumDrivers, browser_id: Any, provider_name: Any) -> Any:
    driver = selenium[browser_id]
    providers_panel = OZLoggedIn(driver).get_page_and_click("providers")
    time.sleep(0.5)
    providers_panel[provider_name]()
    click_visit_provider(driver)


@repeat_failed(timeout=WAIT_FRONTEND)
def click_visit_provider(driver: Any) -> Any:
    Popups(driver).provider_map_popover.visit_provider()


def g_wt_visit_op(
    selenium: SeleniumDrivers, browser_id_list: Any, providers_list: Any, hosts: Hosts
) -> Any:
    providers_list = list_parser(providers_list)
    for browser_id, provider in zip_longest(
        list_parser(browser_id_list),
        providers_list,
        fillvalue=providers_list[-1],
    ):
        visit_op(selenium, browser_id, hosts[provider]["name"])


@given(
    parsers.re(
        "opened (?P<providers_list>.*) Oneprovider view in web GUI "
        "by (users? of )?(?P<browser_id_list>.*)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def g_visit_op(
    selenium: SeleniumDrivers, browser_id_list: Any, providers_list: Any, hosts: Hosts
) -> Any:
    g_wt_visit_op(selenium, browser_id_list, providers_list, hosts)


@wt(
    parsers.re(
        "users? of (?P<browser_id_list>.*) opens? "
        "(?P<providers_list>.*) Oneprovider view in web GUI"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_visit_op(
    selenium: SeleniumDrivers, browser_id_list: Any, providers_list: Any, hosts: Hosts
) -> Any:
    g_wt_visit_op(selenium, browser_id_list, providers_list, hosts)


def visit_file_browser(
    selenium: SeleniumDrivers,
    providers_list: Any,
    spaces_list: Any,
    browser_id_list: Any,
    tmp_memory: Any,
    hosts: Hosts,
) -> Any:
    option = "spaces"
    option_in_submenu = "Files"

    for browser_id, provider, space in zip_longest(
        parse_seq(browser_id_list),
        parse_seq(providers_list),
        parse_seq(spaces_list),
    ):
        click_element_on_lists_on_left_sidebar_menu(selenium, browser_id, option, space)
        click_on_option_of_space_on_left_sidebar_menu(
            selenium, browser_id, space, option_in_submenu
        )
        click_choose_other_oneprovider_on_file_browser(selenium, browser_id)
        choose_provider_in_selected_page(selenium, browser_id, provider, hosts)
        assert_browser_in_tab_in_op(selenium, browser_id, tmp_memory, "file browser")


@given(
    parsers.re(
        "opened (?P<providers_list>.*) Oneprovider file browser "
        "for (?P<spaces_list>.*) space in web GUI "
        "by (users? of )?(?P<browser_id_list>.*)"
    )
)
def g_visit_file_browser(
    selenium: SeleniumDrivers,
    providers_list: Any,
    spaces_list: Any,
    browser_id_list: Any,
    tmp_memory: Any,
    hosts: Hosts,
) -> Any:
    visit_file_browser(
        selenium,
        providers_list,
        spaces_list,
        browser_id_list,
        tmp_memory,
        hosts,
    )


@wt(
    parsers.re(
        "users? of (?P<browser_id_list>.*) opens? "
        "(?P<providers_list>.*) Oneprovider file browser "
        "for (?P<spaces_list>.*) space"
    )
)
def wt_visit_file_browser(
    selenium: SeleniumDrivers,
    providers_list: Any,
    spaces_list: Any,
    browser_id_list: Any,
    tmp_memory: Any,
    hosts: Hosts,
) -> Any:
    visit_file_browser(
        selenium,
        providers_list,
        spaces_list,
        browser_id_list,
        tmp_memory,
        hosts,
    )


def search_for_members(
    driver: Any, records: Any, member_name: Any, parent_name: Any, fun: Any
) -> Any:
    for record in records:
        record_id = record.clickable_name.get_attribute("id")
        scroll_to_css_selector(driver, f"#{record_id}")
        elements = driver.find_elements(
            By.CSS_SELECTOR,
            f"#{record_id} .membership-row-element.membership-block",
        )
        relations = [elem.text.split()[0] for elem in elements if elem.text]
        if member_name in relations and parent_name in relations:
            member_index = relations.index(member_name)
            parent_index = relations.index(parent_name)
            if member_index + 1 == parent_index:
                if fun(record, member_index):
                    return True
    return False


@wt(parsers.parse("user of {browser_id} logs out from Onezone page"))
@repeat_failed(timeout=WAIT_FRONTEND)
def logout_from_onezone_page(selenium: SeleniumDrivers, browser_id: Any) -> Any:
    driver = selenium[browser_id]
    OZLoggedIn(driver)["profile"].profile()
    Popups(driver).user_account_menu.options["Logout"].click()


@wt(parsers.parse("user of {browser_id} logs out from Onezone Emergency panel"))
@repeat_failed(timeout=WAIT_FRONTEND)
def logout_from_onezone_emergency_panel(selenium: SeleniumDrivers, browser_id: Any) -> Any:
    driver = selenium[browser_id]
    button = OZLoggedIn(driver)["profile"].logout.web_elem
    ActionChains(driver).move_to_element(button).click(button).perform()


@wt(parsers.parse("user of {browser_id} changes {username} username to {new_username}"))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_username(
    selenium: SeleniumDrivers, browser_id: Any, username: Any, new_username: Any, users: Users
) -> Any:
    driver = selenium[browser_id]
    profile = OZLoggedIn(driver)["profile"]
    profile.profile()
    Popups(driver).user_account_menu.options["Manage account"].click()
    profile.rename_username()
    profile.edit_user_name_box.value = new_username
    getattr(profile.edit_user_name_box, "confirm").click()
    users[username].username = new_username


@wt(parsers.parse("user of {browser_id} changes {username} password to {new_password}"))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_password(
    selenium: SeleniumDrivers, browser_id: Any, new_password: Any, username: Any, users: Users
) -> Any:
    driver = selenium[browser_id]
    cur_passwd = users[username].password
    profile = OZLoggedIn(driver)["profile"]
    profile.profile()
    Popups(driver).user_account_menu.options["Manage account"].click()
    profile.rename_password()
    profile.current_password_box = cur_passwd
    profile.type_new_password_box = new_password
    profile.retype_new_password_box = new_password
    profile.change_password.click()
    users[username].password = new_password
