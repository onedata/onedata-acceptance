"""Steps used for common in different browsers operations in Oneprovider GUI"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed
from tests.gui.utils.generic import transform, parse_seq
import time


@wt(parsers.parse('user of {browser_id} double clicks on item named'
                  ' "{item_name}" in {which_browser}'))
@repeat_failed(timeout=WAIT_BACKEND)
def double_click_on_item_in_browser(selenium, browser_id, item_name, tmp_memory,
                                    op_container,
                                    which_browser='file browser'):
    which_browser = transform(which_browser)
    browser = tmp_memory[browser_id][which_browser]
    driver = selenium[browser_id]

    # checking if file is located in file browser
    start = time.time()
    while item_name not in browser.data:
        time.sleep(1)
        if time.time() > start + WAIT_BACKEND:
            raise RuntimeError('waited too long')

    double_click_with_check(driver, op_container, browser, which_browser,
                            item_name)


@repeat_failed(timeout=WAIT_BACKEND)
def double_click_with_check(driver, op_container, browser, which_browser,
                            item_name):
    # this function does not check correctly if parent and children directory
    # have the same name
    browser.data[item_name].double_click()
    if item_name.startswith('dir'):
        for _ in range(5):
            breadcrumbs = check_if_breadcrumbs_on_share_page(driver,
                                                             op_container,
                                                             which_browser)
            if breadcrumbs.split('/')[-1] == item_name:
                return
            else:
                time.sleep(1)
        raise RuntimeError(f'Double click has not entered the directory')


@repeat_failed(timeout=WAIT_BACKEND)
def check_if_breadcrumbs_on_share_page(driver, op_container,
                                       which_browser='file browser'):
    try:
        breadcrumbs = op_container(driver).shares_page.breadcrumbs.pwd()
    except RuntimeError:
        breadcrumbs = getattr(op_container(driver),
                              transform(which_browser)).breadcrumbs.pwd()

    return breadcrumbs


@wt(parsers.parse('user of {browser_id} sees that current working directory '
                  'displayed in breadcrumbs on {which_browser} is {path}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def is_displayed_breadcrumbs_in_data_tab_in_op_correct(selenium, browser_id,
                                                       path, op_container,
                                                       which_browser=
                                                       'file browser'):
    driver = selenium[browser_id]
    breadcrumbs = getattr(op_container(driver),
                          transform(which_browser)).breadcrumbs.pwd()

    assert path == breadcrumbs, (f'expected breadcrumbs {path}; '
                                 f'displayed: {breadcrumbs}')


def _get_items_list_from_browser(browser_id, tmp_memory,
                                 which_browser='file browser'):
    file_browser = tmp_memory[browser_id][transform(which_browser)]
    data = {f.name for f in file_browser.data}
    return data


@wt(parsers.parse('user of {browser_id} sees item(s) '
                  'named {item_list} in {which_browser}'))
@wt(parsers.parse('user of {browser_id} sees that item named '
                  '{item_list} has appeared in {which_browser}'))
@wt(parsers.parse('user of {browser_id} sees that items named '
                  '{item_list} have appeared in {which_browser}'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_items_presence_in_browser(browser_id, item_list, tmp_memory,
                                     which_browser='file browser'):
    browser = tmp_memory[browser_id][transform(which_browser)]
    data = _get_items_list_from_browser(browser_id, tmp_memory, which_browser)
    for item_name in parse_seq(item_list):
        if which_browser == 'dataset browser':
            assert item_name in data, (f'not found "{item_name}" '
                                       f'in browser')
        else:
            assert (item_name in data and browser.data[item_name]
                    .size), f'not found "{item_name}" in browser'


@wt(parsers.parse('user of {browser_id} sees that item named {item_list} '
                  'has disappeared from {which_browser}'))
@wt(parsers.parse('user of {browser_id} sees that items named {item_list} '
                  'have disappeared from {which_browser}'))
@wt(parsers.parse('user of {browser_id} does not see any item(s) named '
                  '{item_list} in {which_browser}'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_items_absence_in_browser(browser_id, item_list, tmp_memory,
                                    which_browser='file browser'):
    data = _get_items_list_from_browser(browser_id, tmp_memory, which_browser)
    for item_name in parse_seq(item_list):
        assert item_name not in data, (f'found "{item_name}" in browser, '
                                       f'while it should not')


@wt(parsers.re(r'user of (?P<browser_id>.+?) sees that there '
               r'(is 1|are (?P<num>\d+)) items? in (?P<which_browser>.*)'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_num_of_files_are_displayed_in_browser(browser_id, num, tmp_memory,
                                                 which_browser='file_browser'):
    browser = tmp_memory[browser_id][transform(which_browser)]
    err_msg = 'displayed number of files {} does not match expected {}'
    files_num = browser.data.count()
    num = 1 if num is None else int(num)
    assert files_num == num, err_msg.format(files_num, num)


@wt(parsers.parse('user of {browser_id} sees {status_type} '
                  'status tag for "{item_name}" in {which_browser}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_status_tag_for_file_in_browser(browser_id, status_type, item_name,
                                          tmp_memory,
                                          which_browser='file browser'):
    browser = tmp_memory[browser_id][transform(which_browser)]
    err_msg = (f'{status_type} tag for {item_name} in {which_browser} not '
               f'visible')
    assert browser.data[item_name].is_tag_visible(
        transform(status_type)), err_msg


@wt(parsers.parse('user of {browser_id} sees {status_type} '
                  'status tag with "{text}" text for "{item_name}" '
                  'in {which_browser}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_status_tag_text_for_file_in_browser(browser_id, status_type, text,
                                               item_name, tmp_memory,
                                               which_browser='file browser'):
    assert_status_tag_for_file_in_browser(browser_id, status_type,
                                          item_name, tmp_memory, which_browser)
    browser = tmp_memory[browser_id][transform(which_browser)]
    actual_text = browser.data[item_name].get_tag_text(transform(status_type))
    err_msg = (f'{status_type} tag for {item_name} in browser has text '
               f'{actual_text} not {text}')
    assert actual_text == text, err_msg


@wt(parsers.parse('user of {browser_id} does not see {status_type} '
                  'status tag for "{item_name}" in {which_browser}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_not_status_tag_for_file_in_browser(browser_id, status_type,
                                              item_name, tmp_memory,
                                              which_browser='file browser'):
    browser = tmp_memory[browser_id][transform(which_browser)]
    err_msg = (f'{status_type} tag for {item_name} in {which_browser} visible, '
               f'while should not be')
    assert not browser.data[item_name].is_tag_visible(status_type), err_msg


@wt(parsers.parse('user of {browser_id} clicks "{option}" option '
                  'in data row menu in {which_browser}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_data_row_menu_in_browser(selenium, browser_id, option,
                                             modals,
                                             which_browser='file browser'):

    archive = 'archive browser' == which_browser
    if archive:
        modals(selenium[browser_id]).archive_row_menu.choose_option(option)
    else:
        modals(selenium[browser_id]).data_row_menu.choose_option(option)


@wt(parsers.parse('user of {browser_id} cannot click "{option}" option '
                  'in data row menu in {} browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_not_click_option_in_data_row_menu(selenium, browser_id, option,
                                             modals):
    err_msg = f'user can click on option {option}'
    assert not (modals(selenium[browser_id]).data_row_menu
                .choose_option(option)), err_msg


@wt(parsers.parse('user of {browser_id} clicks on {state} view mode '
                  'on {which} browser page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_state_view_mode_tab(browser_id, oz_page, selenium, state, which):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    header = f'{transform(which)}_header'
    getattr(getattr(oz_page(driver)['data'], header), transform(state))()
    # if we make call to fast after changing view mode
    # we do not see items in this mode, to avoid this wait some time
    time.sleep(0.2)


@wt(parsers.parse('user of {browser_id} clicks on menu '
                  'for "{item_name}" {type} in {which_browser}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory,
                                   which_browser='file browser'):
    browser = tmp_memory[browser_id][transform(which_browser)]
    browser.data[item_name].menu_button()
