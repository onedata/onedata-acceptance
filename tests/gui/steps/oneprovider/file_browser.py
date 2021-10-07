"""This module contains gherkin steps to run acceptance tests featuring
file browser in oneprovider web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from time import time
from datetime import datetime

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import press_enter_on_active_element
from tests.gui.steps.modal import click_modal_button
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.utils import repeat_failed
from tests.utils.bdd_utils import wt, parsers


@wt(parsers.parse('user of {browser_id} sees "{msg}" '
                  'instead of file browser'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_msg_instead_of_browser(browser_id, msg, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    displayed_msg = browser.browser_msg_header
    assert displayed_msg == msg, ('displayed {} does not match expected '
                                  '{}'.format(displayed_msg, msg))


@wt(parsers.parse('user of {browser_id} does not see {status_type} '
                  'status tag for "{item_name}" in file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_not_status_tag_for_file_in_file_browser(browser_id, status_type,
                                                   item_name, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    err_msg = (f'{status_type} tag for {item_name} in file browser visible, '
               f'while should not be')
    assert not browser.data[item_name].is_tag_visible(status_type), err_msg


@wt(parsers.parse('user of {browser_id} sees {status_type} '
                  'status tag for "{item_name}" in file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_status_tag_for_file_in_file_browser(browser_id, status_type,
                                               item_name, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    err_msg = f'{status_type} tag for {item_name} in file browser not visible'
    assert browser.data[item_name].is_tag_visible(transform(status_type)), err_msg


@wt(parsers.parse('user of {browser_id} clicks on {status_type} status tag '
                  'for "{item_name}" in file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_status_tag_for_file_in_file_browser(browser_id, status_type,
                                                 item_name, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    browser.data[item_name].click_on_status_tag(status_type)


def _get_items_list_from_file_browser(browser_id, tmp_memory):
    file_browser = tmp_memory[browser_id]['file_browser']
    data = {f.name for f in file_browser.data}
    return data


@wt(parsers.parse('user of {browser_id} sees that item named {item_list} '
                  'has disappeared from files browser'))
@wt(parsers.parse('user of {browser_id} sees that items named {item_list} '
                  'have disappeared from files browser'))
@wt(parsers.parse('user of {browser_id} does not see any item(s) named '
                  '{item_list} in file browser'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_items_absence_in_file_browser(browser_id, item_list, tmp_memory):
    data = _get_items_list_from_file_browser(browser_id, tmp_memory)
    for item_name in parse_seq(item_list):
        assert item_name not in data, (f'found "{item_name}" in file browser, '
                                       f'while it should not')


@wt(parsers.parse('user of {browser_id} sees item(s) '
                  'named {item_list} in file browser'))
@wt(parsers.parse('user of {browser_id} sees that item named '
                  '{item_list} has appeared in file browser'))
@wt(parsers.parse('user of {browser_id} sees that items named '
                  '{item_list} have appeared in file browser'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_items_presence_in_file_browser(browser_id, item_list, tmp_memory):
    file_browser = tmp_memory[browser_id]['file_browser']
    data = _get_items_list_from_file_browser(browser_id, tmp_memory)
    for item_name in parse_seq(item_list):
        assert (item_name in data and
                file_browser.data[item_name].size), (f'not found "{item_name}" '
                                                     f'in file browser')


@wt(parsers.parse('user of {browser_id} sees only items named {item_list}'
                  ' in file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_only_given_items_in_file_browser(browser_id, item_list, tmp_memory):
    file_browser = tmp_memory[browser_id]['file_browser']
    files = {f.name for f in file_browser.data}
    items = parse_seq(item_list)
    assert len(files) == len(items), 'numbers of items are not equal'
    for item_name in items:
        assert item_name in files, f'not found "{item_name}" in file browser'


@wt(parsers.re('user of (?P<browser_id>.+?) sees items? named '
               '(?P<item_list>.+?) in file browser in given order'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_presence_in_file_browser_with_order(browser_id, item_list,
                                               tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    items = iter(parse_seq(item_list))
    curr_item = next(items)
    for item in browser.data:
        if item.name == curr_item:
            try:
                curr_item = next(items)
            except StopIteration:
                return

    raise RuntimeError('item(s) not in browser or not in specified order '
                       '{order} starting from {item}'.format(order=item_list,
                                                             item=curr_item))


@wt(parsers.parse('user of {browser_id} sees that modification date of item '
                  'named "{item_name}" is not earlier than {err_time:d} '
                  'seconds ago in file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_item_in_file_browser_is_of_mdate(browser_id, item_name,
                                            err_time: float, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    date_fmt = '%d %b %Y %H:%M'
    # %b - abbreviated month name
    item_date = datetime.strptime(browser.data[item_name].modification_date,
                                  date_fmt)
    expected_date = datetime.fromtimestamp(time())
    err_msg = 'displayed mod time {} for {} does not match expected {}'
    assert abs(expected_date - item_date).seconds < err_time, err_msg.format(
        item_date, item_name, expected_date)


@wt(parsers.parse('user of {browser_id} sees that item named "{item_name}" '
                  'is of {size} size in file browser'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_item_in_file_browser_is_of_size(browser_id, item_name, size,
                                           tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    item_size = browser.data[item_name].size
    err_msg = 'displayed size {} for {} does not match expected {}'
    assert size == item_size, err_msg.format(item_size, item_name, size)


@wt(parsers.parse('user of {browser_id} scrolls to the bottom '
                  'of file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def scroll_to_bottom_of_file_browser(browser_id, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    browser.scroll_to_bottom()


@wt(parsers.re(r'user of (?P<browser_id>.+?) sees that there '
               r'(is 1|are (?P<num>\d+)) items? in file browser'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_num_of_files_are_displayed_in_file_browser(browser_id, num,
                                                      tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    err_msg = 'displayed number of files {} does not match expected {}'
    files_num = browser.data.count()
    num = 1 if num is None else int(num)
    assert files_num == num, err_msg.format(files_num, num)


@wt(parsers.re(r'user of (?P<browser_id>.*?) sees that item named '
               r'"(?P<item_name>.*?)" is (?P<item_attr>file|directory) '
               r'in file browser'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_item_in_file_browser_is_of_type(browser_id, item_name, item_attr,
                                           tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    action = getattr(browser.data[item_name], 'is_{}'.format(item_attr))
    assert action(), '"{}" is not {}, while it should'.format(item_name,
                                                              item_attr)


@wt(parsers.parse('user of {browser_id} double clicks on item '
                  'named "{item_name}" in file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def double_click_on_item_in_file_browser(selenium, browser_id, item_name,
                                         tmp_memory, op_container):
    browser = tmp_memory[browser_id]['file_browser']
    driver = selenium[browser_id]

    # checking if file is located in file browser
    start = time.time()
    while item_name not in browser.data:
        time.sleep(1)
        if time.time() > start + WAIT_BACKEND:
            raise RuntimeError('waited too long')
    browser.data[item_name].double_click()

    # if item is directory compare length of directories in breadcrumbs to
    # check if double-click has entered it
    if item_name.startswith('dir'):
        # check if breadcrumbs are not in file browser in shares
        breadcrumbs = check_if_breadcrumbs_on_share_page(driver, op_container)
        message = f'Double click has not entered the directory'

        # check if home directory where length of breadcrumbs doesn't matter
        # if it was home and now it isn't it means double-click worked
        if "/" not in breadcrumbs:
            browser.data[item_name].double_click()
            breadcrumbs = check_if_breadcrumbs_on_share_page(driver,
                                                             op_container)
            if "/" not in breadcrumbs:
                assert False, message
        else:
            length_of_past_dir = len(breadcrumbs)
            browser.data[item_name].double_click()
            breadcrumbs = check_if_breadcrumbs_on_share_page(driver,
                                                             op_container)
            length_of_current_dir = len(breadcrumbs)

            assert length_of_past_dir < length_of_current_dir, message
    else:
        browser.data[item_name].double_click()


def check_if_breadcrumbs_on_share_page(driver, op_container):
    try:
        breadcrumbs = op_container(driver).shares_page.breadcrumbs.pwd()
    except:
        breadcrumbs = getattr(op_container(driver),
                              ['file_browser']).breadcrumbs.pwd()

    return breadcrumbs


@wt(parsers.parse('user of {browser_id} clicks once on item '
                  'named "{item_name}" in file browser'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_item_in_file_browser(browser_id, item_name, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    browser.data[item_name].clickable_field.click()


@wt(parsers.re('user of (?P<browser_id>.+?) selects (?P<item_list>.+?) '
               'items? from file browser with pressed shift'))
def select_files_from_file_list_using_shift(browser_id, item_list, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    with browser.select_files() as selector:
        selector.shift_down()
        _select_files(browser, selector, item_list)
    with browser.select_files() as selector:
        selector.shift_up()


@wt(parsers.re('user of (?P<browser_id>.+?) selects (?P<item_list>.+?) '
               'items? from file browser with pressed ctrl'))
@repeat_failed(timeout=WAIT_FRONTEND)
def select_files_from_file_list_using_ctrl(browser_id, item_list, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    with browser.select_files() as selector:
        selector.ctrl_or_cmd_down()
        _select_files(browser, selector, item_list)
    with browser.select_files() as selector:
        selector.ctrl_or_cmd_up()


@wt(parsers.parse('user of {browser_id} deselects {item_list} '
                  'item(s) from file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def deselect_items_from_file_browser(browser_id, item_list, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    with browser.select_files() as selector:
        selector.ctrl_or_cmd_down()
        _deselect_files(browser, selector, item_list)
        selector.ctrl_or_cmd_up()


@repeat_failed(timeout=WAIT_BACKEND)
def _select_files(browser, selector, item_list):
    for item_name in parse_seq(item_list):
        item = browser.data[item_name]
        if not item.is_selected():
            selector.select(item)


def _deselect_files(browser, selector, item_list):
    for item_name in parse_seq(item_list):
        item = browser.files[item_name]
        if item.is_selected():
            selector.select(item)


@wt(parsers.parse('user of {browser_id} deselects all '
                  'selected items from file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def deselect_all_items_from_file_browser(browser_id, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    item = browser.files[0]
    item.click()
    if item.is_selected():
        item.click()


@wt(parsers.parse('user of {browser_id} sees that {item_list} '
                  'item is selected in file browser'))
@wt(parsers.parse('user of {browser_id} sees that {item_list} '
                  'items are selected in file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_items_are_selected_in_file_browser(browser_id, item_list,
                                              tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    err_msg = 'item "{name}" is not selected while it should be'
    for item_name in parse_seq(item_list):
        item = browser.data[item_name]
        assert item.is_selected(), err_msg.format(name=item_name)


@wt(parsers.parse('user of {browser_id} sees that {item_list} '
                  'item is not selected in file browser'))
@wt(parsers.parse('user of {browser_id} sees that {item_list} '
                  'items are not selected in file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_items_are_not_selected_in_file_browser(browser_id, item_list,
                                                  tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    err_msg = 'item "{name}" is selected while it should not be'
    for item_name in parse_seq(item_list):
        item = browser.data[item_name]
        assert not item.is_selected(), err_msg.format(name=item_name)


@wt(parsers.parse('user of {browser_id} sees that none '
                  'item is selected in file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_none_item_is_selected_in_file_browser(browser_id, item_list,
                                                 tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    err_msg = 'item "{name}" is selected while it should not be'
    for item_name in parse_seq(item_list):
        item = browser.files[item_name]
        assert not item.is_selected(), err_msg.format(name=item_name)


@wt(parsers.parse('user of {browser_id} sees empty directory message '
                  'in file browser'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_empty_dir_msg_in_file_browser(browser_id, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    expected_msg = 'empty directory'
    displayed_msg = browser.empty_dir_msg.lower()

    assert expected_msg == displayed_msg, (f'Displayed empty dir msg '
                                           f'"{displayed_msg}" does not match '
                                           f'expected one "{expected_msg}"')


@wt(parsers.re('user of (?P<browser_id>.*) confirms create new directory '
               'using (?P<option>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_create_new_directory(selenium, browser_id, option, modals):
    if option == 'enter':
        press_enter_on_active_element(selenium, browser_id)
    else:
        button = 'Create'
        modal = 'Create dir'
        click_modal_button(selenium, browser_id, button, modal, modals)


@wt(parsers.re('user of (?P<browser_id>.*) confirms rename directory '
               'using (?P<option>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_rename_directory(selenium, browser_id, option, modals):
    if option == 'enter':
        press_enter_on_active_element(selenium, browser_id)
    else:
        button = 'Rename'
        modal = 'Rename modal'
        click_modal_button(selenium, browser_id, button, modal, modals)


@wt(parsers.parse('user of {browser_id} clicks on menu '
                  'for "{item_name}" directory in file browser'))
@wt(parsers.parse('user of {browser_id} clicks on menu '
                  'for "{item_name}" file in file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_menu_for_elem_in_file_browser(browser_id, item_name, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    browser.data[item_name].menu_button()


@wt(parsers.parse('user of {browser_id} clicks "{option}" option '
                  'in data row menu in file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_data_row_menu_in_file_browser(selenium, browser_id, option,
                                                  modals):
    modals(selenium[browser_id]).data_row_menu.options[option].click()


@wt(parsers.parse('user of {browser_id} scrolls to the bottom of file browser '
                  'and sees there are {count} files'))
def count_files_while_scrolling(browser_id, count: int, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    detected_files = []
    tmp_files = browser.names_of_visible_elems()
    new_files = [f for f in tmp_files if f]
    while new_files:
        detected_files.extend(new_files)
        browser.scroll_to_bottom()
        tmp_files = browser.names_of_visible_elems()
        new_files = [f for f in tmp_files if f and f not in detected_files]
    else:
        err_msg = (f'There are {len(detected_files)} files in file browser '
                   f'when should be {count}')
        assert len(detected_files) == count, err_msg
