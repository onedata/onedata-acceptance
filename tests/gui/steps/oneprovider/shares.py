"""This module contains gherkin steps to run acceptance tests featuring
shares in oneprovider web GUI.
"""

__author__ = "Bartosz Walkowicz, Natalia Organek"
__copyright__ = "Copyright (C) 2017-2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time
from tests.utils.bdd_utils import wt, parsers

from selenium.common.exceptions import NoSuchElementException
from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} changes current working directory '
                  'to {path} using breadcrumbs on share\'s public interface'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_public_share_cwd_using_breadcrumbs(selenium, browser_id, path,
                                              public_share):
    public_share(selenium[browser_id]).breadcrumbs.chdir(path)


@wt(parsers.parse('user of {browser_id} changes current working '
                  'directory to current share using breadcrumbs on share\'s '
                  'public interface'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_public_share_to_home_cwd_using_breadcrumbs(selenium, browser_id,
                                                      public_share):
    public_share(selenium[browser_id]).breadcrumbs.home.click()


@wt(parsers.parse('user of {browser_id} sees that item named "{item_name}" '
                  'has appeared in file browser on shares page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_item_in_file_browser_in_shares_page(selenium, browser_id, item_name,
                                               op_container):
    file_browser = op_container(selenium[browser_id]).shares_page.file_browser
    data = {f.name for f in file_browser.data}
    assert item_name in data, f'Item  {item_name} not in file browser'


@wt(parsers.parse('user of {browser_id} clicks "{option}" option '
                  'in shares actions row menu in file browser'))
@wt(parsers.parse('user of {browser_id} clicks "{option}" option '
                  'in shares actions row menu in shares browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_data_row_menu_in_share_file_browser(selenium, browser_id,
                                                        option, modals):
    modals(selenium[browser_id]).shares_row_menu.options[option].click()


@wt(parsers.parse('user of {browser_id} clicks "{share_name}" '
                  'share in shares browser on Shares Page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_share_in_shares_browser(selenium, browser_id, share_name,
                                  op_container):
    browser = op_container(selenium[browser_id]).shares_page.shares_browser
    browser[share_name].click()


@wt(parsers.parse('user of {browser_id} sees that absolute share path '
                  'visible in share\'s info header is as follows: {path}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def is_share_abs_path_correct(selenium, browser_id, path, op_container):
    displayed_path = op_container(selenium[browser_id]).shares_page.path.pwd()
    assert displayed_path == path, (f'displayed share absolute path '
                                    f'is {displayed_path} '
                                    f'instead of expected {path}')


@wt(parsers.parse('user of {browser_id} sees that current working directory '
                  'path visible in share\'s file browser is as follows: {cwd}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def is_cwd_correct(selenium, browser_id, cwd, op_container):
    displayed_cwd = op_container(
        selenium[browser_id]).shares_page.breadcrumbs.pwd()
    assert displayed_cwd == cwd, (f'displayed share cwd in file browser'
                                  f' is {displayed_cwd} '
                                  f'instead of expected {cwd}')


@wt(parsers.parse('user of {browser_id} clicks on {path} '
                  'using breadcrumbs from share\'s info header'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_dir_in_abs_path(selenium, browser_id, path, op_page):
    op_page(selenium[browser_id]).shares_page.path.chdir(path)


def _change_iframe_for_public_share_page(selenium, browser_id, public_share):
    driver = selenium[browser_id]
    timeout = WAIT_BACKEND
    limit = time.time() + timeout
    while time.time() < limit:
        try:
            iframe = driver.find_element_by_tag_name('iframe')
            driver.switch_to.frame(iframe)
            time.sleep(1)
            displayed_name = public_share(driver).name
        except NoSuchElementException:
            time.sleep(1)
            continue
        else:
            return displayed_name
    else:
        raise NoSuchElementException


@wt(parsers.parse('user of {browser_id} sees that '
                  'public share is named "{share_name}"'))
@repeat_failed(timeout=WAIT_BACKEND, interval=0.5)
def is_public_share_named(selenium, browser_id, share_name, public_share):
    driver = selenium[browser_id]
    displayed_name = _change_iframe_for_public_share_page(selenium, browser_id,
                                                          public_share)
    assert displayed_name == share_name, (f'displayed public share name '
                                          f'is "{displayed_name}" instead of '
                                          f'expected "{share_name}"')


@wt(parsers.parse('user of {browser_id} sees that current working directory '
                  'path visible in share\'s public interface file browser '
                  'is as follows: {cwd}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def is_public_share_cwd_correct(selenium, browser_id, cwd, public_share):
    displayed_cwd = public_share(selenium[browser_id]).breadcrumbs.pwd()
    assert displayed_cwd == cwd, (f'displayed share cwd in file browser'
                                  f' is {displayed_cwd} '
                                  f'instead of expected {cwd}')


@wt(parsers.parse('user of {browser_id} sees file browser '
                  'on share\'s public interface'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_file_browser_in_public_share(selenium, browser_id, public_share,
                                        tmp_memory):
    file_browser = public_share(selenium[browser_id]).file_browser
    tmp_memory[browser_id]['file_browser'] = file_browser


@wt(parsers.parse('user of {browser_id} clicks on '
                  'copy icon on shares view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_copy_icon_on_shares_view(selenium, browser_id, op_container):
    op_container(selenium[browser_id]).shares_page.copy_icon()


@wt(parsers.parse('user of {browser_id} clicks on '
                  'copy icon on share\'s public interface'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_copy_icon_on_public_shares_view(selenium, browser_id, public_share):
    public_share(selenium[browser_id]).copy_icon()


@wt(parsers.parse('user of {browser_id} sees "{error_msg}" error'))
@repeat_failed(timeout=WAIT_FRONTEND)
def no_public_share_view(selenium, browser_id, error_msg, public_share):
    error_msg = error_msg.lower()
    driver = selenium[browser_id]
    assert error_msg in public_share(driver).error_msg.lower(), (
        f'displayed error msg does not contain {error_msg}')


@wt(parsers.parse('user of {browser_id} sees that selected share '
                  'is named "{share_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def is_selected_share_named(selenium, browser_id, share_name, op_container):
    displayed_name = op_container(selenium[browser_id]).shares_page.name
    assert displayed_name == share_name, (
        f'displayed share name is "{displayed_name}" instead of '
        f'expected "{share_name}"')


@wt(parsers.parse('user of {browser_id} clicks on menu on share view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_menu_button_on_shares_page(selenium, browser_id, op_container):
    op_container(selenium[browser_id]).shares_page.menu_button.click()


@wt(parsers.parse('user of {browser_id} clicks "{option}" option '
                  'in shares actions row menu'))
@wt(parsers.parse('user of {browser_id} clicks "{option}" option '
                  'in shares actions row menu in shares browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_share_row_menu(selenium, browser_id, option, modals):
    modals(selenium[browser_id]).shares_row_menu.options[option].click()


@wt(parsers.parse('user of {browser_id} sees there are no shares '
                  'on shares view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def no_shares_message(selenium, browser_id, op_container):
    msg = op_container(selenium[browser_id]).shares_page.no_shares_msg
    assert "no shares" in msg.lower(), ('There are shares on the view but '
                                        'shouldn\'t be any')


@wt(parsers.parse('user of browser sees that there is no "{share_name}" '
                  'share on shares view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_not_share_in_shares_browser_in_shares_page(selenium, browser_id,
                                                      op_container, share_name):
    shares_browser = op_container(
        selenium[browser_id]).shares_page.shares_browser
    data = {f.name for f in shares_browser}
    assert share_name not in data, f'Share {share_name} in shares browser'


@wt(parsers.parse('user of browser sees that there is "{share_name}" '
                  'share on shares view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_share_in_shares_browser_in_shares_page(selenium, browser_id,
                                                  op_container, share_name):
    shares_browser = op_container(
        selenium[browser_id]).shares_page.shares_browser
    data = {f.name for f in shares_browser}
    assert share_name in data, f'Share {share_name} not in shares browser'


@wt(parsers.parse('user of {browser_id} clicks on menu '
                  'for "{item_name}" share in shares browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_menu_for_elem_in_shares_browser(selenium, browser_id, item_name,
                                          op_container):
    browser = op_container(selenium[browser_id]).shares_page.shares_browser
    browser[item_name].menu_button.click()


@wt(parsers.parse('user of {browser_id} clicks "{share_name}" '
                  'share in shares browser on shares view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_share_in_shares_browser(selenium, browser_id, share_name,
                                  op_container):
    browser = op_container(selenium[browser_id]).shares_page.shares_browser
    browser[share_name].click()


@wt(parsers.parse(
    'user of {browser_id} sees file browser on single share view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_shares_browser_to_file_browser(selenium, browser_id, op_container,
                                          tmp_memory):
    browser = op_container(selenium[browser_id]).file_browser
    tmp_memory[browser_id]['file_browser'] = browser


@wt(parsers.parse('user of {browser_id} changes current working directory '
                  'to {path} using breadcrumbs from share\'s file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_cwd_using_breadcrumbs(selenium, browser_id, path, op_container):
    op_container(selenium[browser_id]).shares_page.breadcrumbs.chdir(path)


@wt(parsers.parse('user of {browser_id} changes current working'
                  ' directory to current share using breadcrumbs'
                  ' in shares view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_cwd_to_home_using_breadcrumbs(selenium, browser_id, op_container,
                                         tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    with browser.select_files() as selector:
        selector.shift_up()
        selector.ctrl_or_cmd_up()
    op_container(selenium[browser_id]).shares_page.breadcrumbs.home()
