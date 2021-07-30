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
def double_click_on_item_in_browser(browser_id, item_name, tmp_memory,
                                    which_browser='file browser'):
    which_browser = transform(which_browser)
    browser = tmp_memory[browser_id][which_browser]
    start = time.time()
    while item_name not in browser.data:
        time.sleep(1)
        if start + time.time() > start + WAIT_BACKEND:
            raise RuntimeError('waited too long')
    browser.data[item_name].double_click()


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

