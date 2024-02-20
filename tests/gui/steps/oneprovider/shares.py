"""This module contains gherkin steps to run acceptance tests featuring
shares in oneprovider web GUI.
"""

__author__ = "Bartosz Walkowicz, Natalia Organek"
__copyright__ = "Copyright (C) 2017-2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.utils.bdd_utils import wt, parsers

from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.utils import repeat_failed
from tests.gui.steps.common.miscellaneous import switch_to_iframe


@wt(parsers.parse('user of {browser_id} sees that item named "{item_name}" '
                  'has appeared in file browser on single share view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_item_in_file_browser_in_shares_page(selenium, browser_id, item_name,
                                               op_container):
    file_browser = op_container(selenium[browser_id]).shares_page.file_browser
    data = {f.name for f in file_browser.data}
    assert item_name in data, f'Item  {item_name} not in file browser'


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
def click_on_dir_in_abs_path(selenium, browser_id, path, op_container):
    op_container(selenium[browser_id]).shares_page.path.chdir(path)


@wt(parsers.parse('user of {browser_id} clicks on '
                  'copy icon on shares view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_copy_icon_on_shares_view(selenium, browser_id, op_container):
    op_container(selenium[browser_id]).shares_page.copy_icon()


@wt(parsers.parse('user of {browser_id} copies URL'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_current_url(selenium, browser_id, clipboard, displays):
    driver = selenium[browser_id]
    clipboard.copy(driver.current_url, display=displays[browser_id])


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
                  'in shares actions row menu in {} browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_share_row_menu(selenium, browser_id, option, popups):
    popups(selenium[browser_id]).shares_row_menu.options[option].click()


@wt(parsers.parse('user of {browser_id} sees there are no shares '
                  'on shares view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def no_shares_message(selenium, browser_id, op_container):
    driver = selenium[browser_id]
    try:
        msg = op_container(driver).shares_page.no_shares_msg
    except RuntimeError:
        driver.refresh()
        switch_to_iframe(selenium, browser_id)
        msg = op_container(driver).shares_page.no_shares_msg
    assert "no shares" in msg.lower(), ('There are shares on the view but '
                                        'shouldn\'t be any')


@wt(parsers.parse('user of {browser_id} sees that there is no "{share_name}" '
                  'share on shares view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_not_share_in_shares_browser_in_shares_page(selenium, browser_id,
                                                      op_container, share_name):
    shares_browser = op_container(
        selenium[browser_id]).shares_page.shares_browser
    assert share_name not in shares_browser, (f'Share {share_name} in '
                                              f'shares browser')


@wt(parsers.parse('user of {browser_id} sees that there is "{share_name}" '
                  'share on shares view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_share_in_shares_browser_in_shares_page(selenium, browser_id,
                                                  op_container, share_name):
    shares_browser = op_container(
        selenium[browser_id]).shares_page.shares_browser
    assert share_name in shares_browser, (f'Share {share_name} not in '
                                          f'shares browser')


@wt(parsers.parse('user of {browser_id} sees that there is "{share_name}" '
                  'share that points to deleted directory '
                  'on shares view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_share_point_to_del_dir_on_list(selenium, browser_id, op_container,
                                          share_name):
    shares_browser = op_container(
        selenium[browser_id]).shares_page.shares_browser
    assert share_name in shares_browser, (f'Share {share_name} not '
                                          f'in shares browser')
    share = shares_browser[share_name]
    assert share.points_to_del_dir(), (f'Share {share_name} does not point to '
                                       f'deleted directory')


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
def change_cwd_to_home_using_breadcrumbs(selenium, browser_id, op_container):
    op_container(selenium[browser_id]).shares_page.breadcrumbs.space_root()


@wt(parsers.parse('user of {browser_id} sees that share\'s '
                  'URL is the same as URL from clipboard'))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_urls_are_equal(selenium, browser_id, op_container, clipboard,
                         displays):
    share_url = op_container(selenium[browser_id]).shares_page.url
    modal_url = clipboard.paste(display=displays[browser_id])
    err_msg = f'modal URL is {modal_url} and share URL is {share_url}'
    assert share_url == modal_url, err_msg


@wt(parsers.parse('user of {browser_id} copies public REST endpoint '
                  'on shares view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_share_link(selenium, browser_id, op_container):
    op_container(selenium[browser_id]).shares_page.copy_icon()


@wt(parsers.parse('user of {browser_id} clicks share link type selector '
                  'on shares view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_share_link_type_selector(selenium, browser_id, op_container):
    op_container(selenium[browser_id]).shares_page.link_type_selector()


@wt(parsers.parse('user of {browser_id} chooses "{url_type}" share link type '
                  'on shares view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_share_link_type(selenium, browser_id, url_type, popups):
    driver = selenium[browser_id]
    popups(driver).power_select.choose_item(url_type)


@wt(parsers.parse('user of {browser_id} opens description tab on share view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def open_description_tab(selenium, browser_id, op_container):
    op_container(selenium[browser_id]).shares_page.description_tab()


@wt(parsers.parse('user of {browser_id} clicks on add description button '
                  'on share description tab'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_add_description_button(selenium, browser_id, op_container):
    op_container(selenium[browser_id]).shares_page.create_description()


@wt(parsers.parse('user of {browser_id} appends "{description}" '
                  'to description on share description tab'))
@repeat_failed(timeout=WAIT_FRONTEND)
def append_description(selenium, browser_id, description, op_container):
    driver = selenium[browser_id]

    # check if editor is in preview or edit mode
    if op_container(driver).shares_page.editor_mode == 'Edit Markdown':
        op_container(driver).shares_page.switch_editor_markdown()
    op_container(driver).shares_page.description_input += description


@wt(parsers.parse('user of {browser_id} clicks on save changes button '
                  'in description share'))
@repeat_failed(timeout=WAIT_FRONTEND)
def save_description_changes(selenium, browser_id, op_container):
    driver = selenium[browser_id]
    op_container(driver).shares_page.save_description()
