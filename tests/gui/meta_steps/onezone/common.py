"""This module contains meta steps for common operations in Onezone
using web GUI
"""

from itertools import zip_longest

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.browser_creation import \
    create_instances_of_webdriver
from tests.gui.steps.common.login import g_login_using_basic_auth
from tests.gui.steps.common.url import g_open_onedata_service_page
from tests.gui.steps.oneprovider.data_tab import (
    assert_browser_in_tab_in_op,
    click_choose_other_oneprovider_on_file_browser,
    choose_provider_in_selected_page)
from tests.gui.steps.onezone.providers import parse_seq
from tests.gui.steps.onezone.spaces import (
    click_element_on_lists_on_left_sidebar_menu,
    click_on_option_of_space_on_left_sidebar_menu)
from tests.utils.acceptance_utils import list_parser
from tests.utils.bdd_utils import wt, given, parsers
from tests.utils.utils import repeat_failed
from tests.gui.utils.core import scroll_to_css_selector


@given(parsers.re('opened (?P<browser_id_list>.*) with (?P<user_list>.*) '
                  'signed in to (?P<host_list>.*) service'))
@repeat_failed(timeout=WAIT_FRONTEND)
def login_using_gui(host_list, selenium, driver, tmpdir, tmp_memory, xvfb,
                    driver_kwargs, driver_type, firefox_logging, displays,
                    firefox_path, screen_width, screen_height, hosts,
                    users, login_page, browser_id_list, user_list,
                    xvfb_recorder, test_type):
    create_instances_of_webdriver(selenium, driver, user_list, tmpdir,
                                  tmp_memory, driver_kwargs, driver_type,
                                  firefox_logging, firefox_path,
                                  xvfb, xvfb_recorder,
                                  screen_width, screen_height, displays)
    g_open_onedata_service_page(selenium, user_list, host_list, hosts)

    for browser, user in zip(parse_seq(browser_id_list), parse_seq(user_list)):
        if test_type == 'gui':
            selenium[browser] = selenium[user]
            selenium.pop(user, None)
        tmp_memory[browser] = tmp_memory[user]
        displays[browser] = displays[user]

    # mixed tests use user_list instead of browser_id_list because
    # some mixed steps don't use browser
    login_ids = browser_id_list if test_type == 'gui' else user_list
    g_login_using_basic_auth(selenium, login_ids, user_list, login_page,
                             users, host_list)


@repeat_failed(timeout=WAIT_FRONTEND)
def visit_op(selenium, browser_id, oz_page, provider_name, popups):
    driver = selenium[browser_id]
    providers_panel = oz_page(driver)['providers']
    providers_panel[provider_name]()
    click_visit_provider(driver, popups)


@repeat_failed(timeout=WAIT_FRONTEND)
def click_visit_provider(driver, popups):
    popups(driver).provider_map_popover.visit_provider()


def g_wt_visit_op(selenium, oz_page, browser_id_list, providers_list, hosts,
                  popups):
    providers_list = list_parser(providers_list)
    for browser_id, provider in zip_longest(list_parser(browser_id_list),
                                            providers_list,
                                            fillvalue=providers_list[-1]):
        visit_op(selenium, browser_id, oz_page, hosts[provider]['name'],
                 popups)


@given(parsers.re('opened (?P<providers_list>.*) Oneprovider view in web GUI '
                  'by (users? of )?(?P<browser_id_list>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def g_visit_op(selenium, oz_page, browser_id_list, providers_list, hosts,
               popups):
    g_wt_visit_op(selenium, oz_page, browser_id_list, providers_list, hosts,
                  popups)


@wt(parsers.re('users? of (?P<browser_id_list>.*) opens? '
               '(?P<providers_list>.*) Oneprovider view in web GUI'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_visit_op(selenium, oz_page, browser_id_list, providers_list, hosts,
                modals):
    g_wt_visit_op(selenium, oz_page, browser_id_list, providers_list, hosts,
                  modals)


def visit_file_browser(selenium, oz_page, providers_list, spaces_list,
                       browser_id_list, op_container, tmp_memory, hosts):
    option = 'spaces'
    option_in_submenu = 'Files'

    for browser_id, provider, space in zip_longest(parse_seq(browser_id_list),
                                                   parse_seq(providers_list),
                                                   parse_seq(spaces_list)):
        click_element_on_lists_on_left_sidebar_menu(selenium, browser_id, option,
                                                    space, oz_page)
        click_on_option_of_space_on_left_sidebar_menu(selenium, browser_id,
                                                      space, option_in_submenu,
                                                      oz_page)
        click_choose_other_oneprovider_on_file_browser(selenium, browser_id,
                                                       oz_page)
        choose_provider_in_selected_page(selenium, browser_id, provider,
                                         hosts, oz_page)
        assert_browser_in_tab_in_op(selenium, browser_id,
                                    op_container, tmp_memory)


@given(parsers.re('opened (?P<providers_list>.*) Oneprovider file browser '
                  'for (?P<spaces_list>.*) space in web GUI '
                  'by (users? of )?(?P<browser_id_list>.*)'))
def g_visit_file_browser(selenium, oz_page, providers_list, spaces_list,
                         browser_id_list, op_container, tmp_memory, hosts):
    visit_file_browser(selenium, oz_page, providers_list, spaces_list,
                       browser_id_list, op_container, tmp_memory, hosts)


@wt(parsers.re('users? of (?P<browser_id_list>.*) opens? '
               '(?P<providers_list>.*) Oneprovider file browser '
               'for (?P<spaces_list>.*) space'))
def wt_visit_file_browser(selenium, oz_page, providers_list, spaces_list,
                          browser_id_list, op_container, tmp_memory, hosts):
    visit_file_browser(selenium, oz_page, providers_list, spaces_list,
                       browser_id_list, op_container, tmp_memory, hosts)


def search_for_members(driver, records, member_name, parent_name, fun):
    for record in records:
        record_id = record.clickable_name.get_attribute('id')
        scroll_to_css_selector(driver, f'#{record_id}')
        elements = driver.find_elements_by_css_selector(
            f'#{record_id} .membership-row-element.membership-block')
        relations = [elem.text for elem in elements]
        if member_name in relations and parent_name in relations:
            member_index = relations.index(member_name)
            parent_index = relations.index(parent_name)
            if member_index + 1 == parent_index:
                if fun(record, member_index):
                    return True
    return False


@wt(parsers.parse('user of {browser_id} logs out from Onezone page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def logout_from_onezone_page(selenium, browser_id, oz_page, popups):
    driver = selenium[browser_id]
    oz_page(driver)['profile'].profile()
    popups(driver).user_account_menu.options["Logout"].click()


@wt(parsers.parse('user of {browser_id} changes {username} username '
                  'to {new_username}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_username(selenium, browser_id, username, new_username, oz_page,
                    popups, users):
    driver = selenium[browser_id]
    profile = oz_page(driver)['profile']
    profile.profile()
    popups(driver).user_account_menu.options["Manage account"].click()
    profile.rename_username()
    profile.edit_user_name_box.value = new_username
    getattr(profile.edit_user_name_box, "confirm").click()
    users[username].username = new_username


@wt(parsers.parse('user of {browser_id} changes {username} password'
                  ' to {new_password}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_password(selenium, browser_id, new_password, username, oz_page,
                    users, popups):
    driver = selenium[browser_id]
    cur_passwd = users[username].password
    profile = oz_page(driver)['profile']
    profile.profile()
    popups(driver).user_account_menu.options["Manage account"].click()
    profile.rename_password()
    profile.current_password_box = cur_passwd
    profile.type_new_password_box = new_password
    profile.retype_new_password_box = new_password
    profile.change_password.click()
    users[username].password = new_password
