"""This module contains meta steps for common operations in Onezone
using web GUI
"""

from pytest_bdd import given, parsers

from tests.gui.steps.onezone.logged_in_common import g_expand_oz_panel
from tests.gui.steps.common.browser_creation import \
    create_instances_of_webdriver
from tests.gui.steps.onezone.login_page import g_login_to_zone_using_basic_auth
from tests.gui.steps.onezone.providers import \
    (parse_seq, g_click_on_provider_in_go_to_your_files_oz_panel,
     g_click_on_btn_in_provider_popup)
from tests.gui.steps.oneprovider.common import g_wait_for_op_session_to_start
from tests.gui.steps.common.url import g_open_onedata_service_page
from tests.gui.steps.onepanel.login import g_login_to_panel_using_basic_auth


@given(parsers.re('opened (?P<browser_id_list>.*) with (?P<user_list>.*) logged'
                  ' to (?P<host_list>.*) service'))
def login_to_oz_using_gui(host_list, selenium, driver, tmpdir, tmp_memory, xvfb,
                          driver_kwargs, driver_type, firefox_logging, displays,
                          firefox_path, screen_width, screen_height, hosts,
                          users, oz_login_page, browser_id_list, user_list,
                          panel_login_page, xvfb_recorder):
    create_instances_of_webdriver(selenium, driver, user_list, tmpdir,
                                  tmp_memory, driver_kwargs, driver_type,
                                  firefox_logging, firefox_path,
                                  xvfb, xvfb_recorder,
                                  screen_width, screen_height, displays)
    g_open_onedata_service_page(selenium, user_list, host_list, hosts)

    for user, host_name in zip(parse_seq(user_list),
                               parse_seq(host_list)):
        if 'panel' in host_name.lower().split():
            g_login_to_panel_using_basic_auth(selenium, user, user,
                                              panel_login_page, users)
        else:
            g_login_to_zone_using_basic_auth(selenium, user, user,
                                             oz_login_page, users)

    for browser, user in zip(parse_seq(browser_id_list), parse_seq(user_list)):
        selenium[browser] = selenium[user]
        tmp_memory[browser] = tmp_memory[user]
        displays[browser] = displays[user]


@given(parsers.re('opened (?P<provider_list>.*) Oneprovider view in web GUI by '
                  '(users? of )?(?P<browser_id_list>.*)'))
def go_to_provider(browser_id_list, provider_list, selenium, oz_page, hosts):
    g_expand_oz_panel(selenium, browser_id_list, 'GO TO YOUR FILES', oz_page)
    g_click_on_provider_in_go_to_your_files_oz_panel(selenium, browser_id_list,
                                                     provider_list, oz_page,
                                                     hosts)
    g_click_on_btn_in_provider_popup(selenium, browser_id_list,
                                     'go to your files', provider_list, oz_page,
                                     hosts)
    g_wait_for_op_session_to_start(selenium, browser_id_list)
