"""This module contains meta steps for common operations in Onezone
using web GUI
"""

import time
from collections.abc import Callable
from itertools import zip_longest
from typing import cast

from _pytest._py.path import LocalPath
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.browser_creation import create_instances_of_webdriver
from tests.gui.steps.common.login import (
    login_using_basic_auth,
    wt_enter_password_of_user,
    wt_enter_text_to_field_in_login_form,
    wt_press_sign_in_btn_on_login_page,
)
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
from tests.gui.type_definitions import TmpMemory
from tests.gui.utils import OZLoggedIn, Popups
from tests.gui.utils.core import scroll_to_css_selector
from tests.gui.utils.core.web_objects import PageObjectsSequence
from tests.gui.utils.onezone.members_subpage import MembershipRow
from tests.type_definitions import Hosts, JsonObject, SeleniumDrivers
from tests.utils.acceptance_utils import list_parser
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.user_utils import Users
from tests.utils.utils import repeat_failed


@given(
    parsers.re(
        "opened (?P<browser_id_list>.*) with (?P<user_list>.*) "
        "signed in to (?P<host_list>.*) service"
    )
)
def login_using_gui(
    host_list: str,
    selenium: SeleniumDrivers,
    driver: WebDriver,
    tmpdir: LocalPath,
    tmp_memory: TmpMemory,
    xvfb: list[str],
    driver_type: str,
    displays: dict[str, str],
    screen_width: int,
    screen_height: int,
    hosts: Hosts,
    users: Users,
    browser_id_list: str,
    user_list: str,
    test_type: str,
    capabilities: JsonObject,
) -> None:
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
def visit_op(selenium: SeleniumDrivers, browser_id: str, provider_name: str) -> None:
    driver = selenium[browser_id]
    providers_panel = OZLoggedIn(driver).get_page_and_click("providers")
    time.sleep(0.5)
    providers_panel[provider_name]()
    click_visit_provider(driver)


@repeat_failed(timeout=WAIT_FRONTEND)
def click_visit_provider(driver: WebDriver) -> None:
    Popups(driver).provider_map_popover.visit_provider()


def g_wt_visit_op(
    selenium: SeleniumDrivers, browser_id_list: str, providers_list: str, hosts: Hosts
) -> None:
    parsed_providers = list_parser(providers_list)
    for browser_id, provider in zip_longest(
        list_parser(browser_id_list),
        parsed_providers,
        fillvalue=parsed_providers[-1],
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
    selenium: SeleniumDrivers, browser_id_list: str, providers_list: str, hosts: Hosts
) -> None:
    g_wt_visit_op(selenium, browser_id_list, providers_list, hosts)


@wt(
    parsers.re(
        "users? of (?P<browser_id_list>.*) opens? "
        "(?P<providers_list>.*) Oneprovider view in web GUI"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_visit_op(
    selenium: SeleniumDrivers, browser_id_list: str, providers_list: str, hosts: Hosts
) -> None:
    g_wt_visit_op(selenium, browser_id_list, providers_list, hosts)


def visit_file_browser(
    selenium: SeleniumDrivers,
    providers_list: str,
    spaces_list: str,
    browser_id_list: str,
    tmp_memory: TmpMemory,
    hosts: Hosts,
) -> None:
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
    providers_list: str,
    spaces_list: str,
    browser_id_list: str,
    tmp_memory: TmpMemory,
    hosts: Hosts,
) -> None:
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
    providers_list: str,
    spaces_list: str,
    browser_id_list: str,
    tmp_memory: TmpMemory,
    hosts: Hosts,
) -> None:
    visit_file_browser(
        selenium,
        providers_list,
        spaces_list,
        browser_id_list,
        tmp_memory,
        hosts,
    )


def search_for_members(
    driver: WebDriver,
    records: PageObjectsSequence,
    member_name: str,
    parent_name: str,
    fun: Callable[[MembershipRow, int], bool],
) -> bool:
    for record in records:
        record = cast(MembershipRow, record)
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
def logout_from_onezone_page(selenium: SeleniumDrivers, browser_id: str) -> None:
    driver = selenium[browser_id]
    OZLoggedIn(driver)["profile"].profile()
    Popups(driver).user_account_menu.options["Logout"].click()


@wt(parsers.parse("user of {browser_id} logs out from Onezone Emergency panel"))
@repeat_failed(timeout=WAIT_FRONTEND)
def logout_from_onezone_emergency_panel(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    button = OZLoggedIn(driver)["profile"].logout.web_elem
    ActionChains(driver).move_to_element(button).click(button).perform()


@wt(parsers.parse("user of {browser_id} changes {username} username to {new_username}"))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_username(
    selenium: SeleniumDrivers,
    browser_id: str,
    username: str,
    new_username: str,
    users: Users,
) -> None:
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
    selenium: SeleniumDrivers,
    browser_id: str,
    new_password: str,
    username: str,
    users: Users,
) -> None:
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


@wt(
    parsers.parse(
        'user of {browser_id} logins as "{username}" without closing authentication'
        " info alert"
    )
)
def wt_sign_in_to_onezone_without_closing_auth_info_alert(
    selenium: SeleniumDrivers,
    browser_id: str,
    username: str,
    users: Users,
) -> None:
    wt_enter_text_to_field_in_login_form(selenium, browser_id, "Username", username)
    wt_enter_password_of_user(selenium, browser_id, username, users)
    wt_press_sign_in_btn_on_login_page(selenium, browser_id)
