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


@wt(parsers.parse('user of {browser_id} sees {status_type} '
                  'status tag with "{text}" text for "{item_name}" '
                  'in file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_status_tag_text_for_file_in_file_browser(browser_id, status_type,
                                                    text, item_name,
                                                    tmp_memory):
    assert_status_tag_for_file_in_file_browser(browser_id, status_type,
                                               item_name, tmp_memory)
    browser = tmp_memory[browser_id]['file_browser']
    actual_text = browser.data[item_name].get_tag_text(transform(status_type))
    err_msg = (f'{status_type} tag for {item_name} in file browser has text '
               f'{actual_text} not {text}')
    assert actual_text == text, err_msg


@wt(parsers.parse('user of {browser_id} clicks on {status_type} status tag '
                  'for "{item_name}" in file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_status_tag_for_file_in_file_browser(browser_id, status_type,
                                                 item_name, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    browser.data[item_name].click_on_status_tag(status_type)


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


@wt(parsers.re(r'user of (?P<browser_id>.*?) sees that item named '
               r'"(?P<item_name>.*?)" is ('
               r'?P<item_attr>file|directory|symbolic link|'
               r'directory symbolic link|malformed symbolic link) '
               r'in file browser'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_item_in_file_browser_is_of_type(browser_id, item_name, item_attr,
                                           tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    action = getattr(browser.data[item_name], f'is_{transform(item_attr)}')
    assert action(), f'"{item_name}" is not {item_attr}, while it should'


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


def check_file_owner_in_file_details_modal(selenium, browser_id, modals, owner):
    actual = modals(selenium[browser_id]).file_details.owner
    assert actual == owner, f'Expected {owner} as file owner but got {actual}'


@wt(parsers.parse('user of {browser_id} sees that "File details" modal is '
                  'opened on "Hard links" tab'))
def check_file_dets_modal_opened_on_hardlinks_tab(selenium, browser_id, modals):
    hardlink_tab = modals(selenium[browser_id]).file_details.hardlinks_tab
    assert hardlink_tab.is_active(), ('Hardlink tab is not active in file '
                                      'details modal')


def assert_num_of_hardlinks_in_file_dets_tab_name_modal(selenium, browser_id,
                                                        number, modals):
    name = modals(selenium[browser_id]).file_details.hardlinks_tab.tab_name
    actual_num = name.split()[-1].strip('(').strip(')')
    assert number == actual_num, (f'Expected {number}, got {actual_num} in ' 
                                  f'hardlinks tab name')


def assert_num_of_hardlinks_entry_in_file_dets_modal(selenium, browser_id,
                                                     number, modals):
    entries = modals(selenium[browser_id]).file_details.hardlinks_tab.files
    assert len(entries) == int(number), (f'Expected {number} hardlinks '
                                         f'entries, got {len(entries)}')


@wt(parsers.parse('user of {browser_id} sees that there are {number} '
                  'hardlinks in "File details" modal'))
def assert_num_of_hardlinks_in_file_dets_modal(selenium, browser_id, number,
                                               modals):
    assert_num_of_hardlinks_in_file_dets_tab_name_modal(selenium, browser_id,
                                                        number, modals)
    assert_num_of_hardlinks_entry_in_file_dets_modal(selenium, browser_id,
                                                     number, modals)


@wt(parsers.parse('user of {browser_id} sees that path of "{file}" hardlink '
                  'is "{path}" in "File details" modal'))
def assert_hardlink_path_in_file_dets_modal(selenium, browser_id, file,
                                            path, modals):
    entries = modals(selenium[browser_id]).file_details.hardlinks_tab.files
    actual_path = entries[file].path
    assert path == actual_path, (f'Hardlink {file} path should be {path}, '
                                 f'but is {actual_path}')


@wt(parsers.parse('user of {browser_id} sees paths {paths} '
                  'of hardlinks in "File details" modal'))
def assert_hardlinks_paths_in_file_dets_modal(selenium, browser_id, paths,
                                              modals):
    entries = modals(selenium[browser_id]).file_details.hardlinks_tab.files
    entries_paths = [entry.path for entry in entries]
    parsed_paths = parse_seq(paths)
    for path in parsed_paths:
        assert path in entries_paths, f'{path} not in {entries_paths}'


@wt(parsers.parse('user of {browser_id} sees that {link_property} is "{value}" '
                  'in "Symbolic link details" modal'))
def assert_property_in_symlink_dets_modal(selenium, browser_id, link_property,
                                          value, modals, clipboard, displays):
    modal = modals(selenium[browser_id]).symbolic_link_details
    actual_value = modal.get_property(link_property, clipboard, displays,
                                      browser_id)
    assert actual_value == value, (f'{link_property} has {actual_value} '
                                   f'not expected {value}')

