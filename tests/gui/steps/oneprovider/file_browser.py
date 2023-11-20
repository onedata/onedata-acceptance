"""This module contains gherkin steps to run acceptance tests featuring
file browser in oneprovider web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time
from datetime import datetime
import tarfile
import yaml
from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import press_enter_on_active_element
from tests.gui.steps.common.url import refresh_site
from tests.gui.steps.modals.modal import click_modal_button
from tests.gui.steps.modals.details_modal import click_on_context_menu_item
from tests.gui.steps.oneprovider.data_tab import assert_browser_in_tab_in_op,\
    choose_option_from_selection_menu
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.utils import repeat_failed
from tests.utils.bdd_utils import wt, parsers


@wt(parsers.parse('user of {browser_id} sees "{msg}" '
                  'instead of file browser'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_msg_instead_of_browser(browser_id, msg, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    displayed_msg = browser.browser_msg_header
    start = time.time()
    while displayed_msg != msg:
        time.sleep(1)
        displayed_msg = browser.browser_msg_header
        if time.time() > start + WAIT_BACKEND:
            assert displayed_msg == msg, (f'displayed {displayed_msg} does'
                                          f' not match expected {msg}')


@wt(parsers.parse('user of {browser_id} clicks on {status_type} status tag '
                  'for "{item_name}" in file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_status_tag_for_file_in_file_browser(browser_id, status_type,
                                                 item_name, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    browser.data[item_name].click_on_status_tag(transform(status_type))


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
    expected_date = datetime.fromtimestamp(time.time())
    err_msg = 'displayed mod time {} for {} does not match expected {}'
    assert abs(expected_date - item_date).seconds < err_time, err_msg.format(
        item_date, item_name, expected_date)


@wt(parsers.parse('user of {browser_id} sees that displayed size in data row '
                  'of "{item_name}" is "{size}"'))
@wt(parsers.parse('user of {browser_id} sees that item named "{item_name}" '
                  'is of {size} size in file browser'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_item_in_file_browser_is_of_size(browser_id, item_name, size,
                                           tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    item_size = browser.data[item_name].size
    err_msg = 'displayed size {} for {} does not match expected {}'
    assert size == item_size, err_msg.format(item_size, item_name, size)


@wt(parsers.parse('user of {browser_id} waits for displayed size in data row '
                  'of "{item_name}" to be "{size}"'))
@repeat_failed(timeout=WAIT_BACKEND)
def wait_for_size_to_be_displayed_in_data_row(selenium, browser_id,
                                              op_container, tmp_memory,
                                              item_name, size):
    # refresh site after enabling size statistics to see displayed size
    # in data row
    refresh_site(selenium, browser_id)
    assert_browser_in_tab_in_op(selenium, browser_id, op_container,
                                tmp_memory)
    browser = tmp_memory[browser_id]['file_browser']
    displayed_size = browser.data[item_name].size
    assert displayed_size == size, (
        f'Displayed {item_name} size is {displayed_size}, but expected is '
        f'{size}')


@wt(parsers.parse('user of {browser_id} scrolls to the bottom of file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def scroll_to_bottom_of_file_browser(browser_id, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    visible_files = browser.names_of_visible_elems()
    detected_files = []
    new_files = [f for f in visible_files if f]
    while new_files:
        detected_files.extend(new_files)
        browser.scroll_visible_fragment()
        visible_files = browser.names_of_visible_elems()
        new_files = [f for f in visible_files if f and f not in detected_files]


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


@wt(parsers.parse('user of {browser_id} selects first "{num_files_to_select}"'
                  ' files from file browser with pressed ctrl'))
@repeat_failed(timeout=WAIT_FRONTEND, exceptions=(Exception, AssertionError, ))
def select_first_n_files(browser_id, num_files_to_select: int, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    with browser.select_files() as selector:
        selector.ctrl_or_cmd_down()
        selected_files = []
        visible_files = browser.names_of_visible_elems()
        new_files = [f for f in visible_files if f]
        err_msg = (f'there are {len(new_files)} files in file browser'
                   f' should be at least {num_files_to_select}')
        assert len(new_files) >= num_files_to_select, err_msg
        new_files = new_files[:num_files_to_select]
        for new_file in new_files:
            item = browser.data[new_file]
            if not item.is_selected():
                selector.select(item)
                selected_files.append(new_file)
        err_msg = (f'There are {len(selected_files)} selected files in'
                   f' file browser when should be {num_files_to_select}')
        assert len(selected_files) == num_files_to_select, err_msg


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


@wt(parsers.parse('user of {browser_id} scrolls to the bottom of file browser '
                  'and sees there are {count} files'))
def count_files_while_scrolling(browser_id, count: int, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    detected_files = []
    visible_files = browser.names_of_visible_elems()
    new_files = [f for f in visible_files if f]
    while new_files:
        detected_files.extend(new_files)
        browser.scroll_visible_fragment()
        visible_files = browser.names_of_visible_elems()
        new_files = [f for f in visible_files if f and f not in detected_files]
    else:
        err_msg = (f'There are {len(detected_files)} files in file browser '
                   f'when should be {count}')
        assert len(detected_files) == count, err_msg


def check_file_owner_in_file_details_modal(selenium, browser_id, modals, owner):
    actual = modals(selenium[browser_id]).details_modal.owner
    assert actual == owner, f'Expected {owner} as file owner but got {actual}'


def assert_num_of_hardlinks_in_file_dets_tab_name_modal(selenium, browser_id,
                                                        number, modals):
    name = modals(selenium[browser_id]).details_modal.hardlinks.tab.text
    actual_num = name.split()[-1].strip('(').strip(')')
    assert number == actual_num, (f'Expected {number}, got {actual_num} in ' 
                                  f'hardlinks tab name')


def assert_num_of_hardlinks_entry_in_file_dets_modal(selenium, browser_id,
                                                     number, modals):
    entries = modals(selenium[browser_id]).details_modal.hardlinks.files
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
    entries = modals(selenium[browser_id]).details_modal.hardlinks.files
    actual_path = entries[file].get_path_string()
    assert path == actual_path, (f'Hardlink {file} path should be {path}, '
                                 f'but is {actual_path}')


@wt(parsers.parse('user of {browser_id} sees paths {paths} '
                  'of hardlinks in "File details" modal'))
def assert_hardlinks_paths_in_file_dets_modal(selenium, browser_id, paths,
                                              modals):
    entries = modals(selenium[browser_id]).details_modal.hardlinks.files
    entries_paths = [entry.get_path_string() for entry in entries]
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


@wt(parsers.parse('user of {browser_id} sees that contents of downloaded '
                  '{name} TAR file (with ID from clipboard) in download '
                  'directory have following structure:\n{contents}'))
@wt(parsers.parse('user of {browser_id} sees that contents of downloaded '
                  '"{name}" TAR file in download directory have following'
                  ' structure:\n{contents}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_contents_downloaded_tar_file(selenium, browser_id, contents, tmpdir,
                                        clipboard, displays, name):
    configured_dir_contents = {}
    if name == 'archive':
        name = (f'archive_'
                     f'{clipboard.paste(display=displays[browser_id])}.tar')
        contents = contents.replace('archive', name.split('.')[0])

    def _get_directory_contents(directory_tree, path=''):

        if not directory_tree:
            return

        for item in directory_tree:
            try:
                [(name, content)] = item.items()
            except AttributeError:
                name = item
                content = None

            if path == '':
                item_path = name
            else:
                item_path = path + '/' + name

            configured_dir_contents[item_path] = str(content)
            if name.startswith('dir') or name.startswith('archive'):
                configured_dir_contents[item_path] = None
                _get_directory_contents(content, item_path)

    download_path = tmpdir.join(browser_id, 'download')
    extract_path = download_path.join('extract')
    downloaded_tar_filename = download_path.join(name).strpath

    assert tarfile.is_tarfile(downloaded_tar_filename), (
                f'{downloaded_tar_filename} is not valid TAR file archive')

    tar = tarfile.open(downloaded_tar_filename)
    files_list = tar.getnames()
    tar.extractall(extract_path.strpath)

    dir_tree = yaml.load(contents)
    _get_directory_contents(dir_tree)

    for f in files_list:
        assert f in configured_dir_contents, (f'{f} is missing in downloaded '
                                              f'tar file')
        archive_file = tar.getmember(f)
        if archive_file.isfile():
            with open(extract_path.join(f).strpath, 'r') as o:
                file_contents = o.read()
                assert str(file_contents) == str(configured_dir_contents[f]), (
                    f'{f} content is different than expected '
                    f'{file_contents}!={configured_dir_contents[f]}')


@wt(parsers.re('user of (?P<browser_id>.*?) sees that items? named'
               ' (?P<item_list>.*?) (?P<option>is|are|is not|are not) '
               'currently visible in (?P<which>.*?) browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_item_displayed_on_page(browser_id, item_list, tmp_memory, option,
                                  which):
    browser = tmp_memory[browser_id][f'{which}_browser']
    visible_files = browser.names_of_visible_elems()
    items = parse_seq(item_list)
    data = [f for f in visible_files if f]
    for name in items:
        if 'not' in option:
            assert name not in data, f'{name} is displayed on page'
        else:
            assert name in data, (f'{name} is not displayed on page, '
                                  f'displayed files: {data}')


@wt(parsers.parse('user of {browser_id} writes "{prefix}" to jump input in'
                  ' file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def write_to_jump_input(browser_id, tmp_memory, prefix):
    browser = tmp_memory[browser_id]['file_browser']
    browser.jump_input = prefix


@wt(parsers.parse('user of {browser_id} sees alert that file cannot be '
                  '{option} because of insufficient privileges'))
def assert_message_at_alert_modal(browser_id, option, modals, selenium):
    driver = selenium[browser_id]
    modal = modals(driver).error
    messages_dict = {
        "downloaded": ("Starting file download failed!\nYou are not authorized "
                       "to perform this operation (insufficient privileges?)."),
        "deleted": "Deleting file(s) failed!\nOperation not permitted"
    }
    visible_message = None
    if option == "downloaded":
        visible_message = modal.content_message
    elif option == "deleted":
        visible_message = modal.content
    err_msg = (f"visible message is {visible_message}, which does not match to "
               f"expected message {messages_dict[option]}")
    assert visible_message == messages_dict[option], err_msg


@wt(parsers.parse('user of {browser_id} scrolls to the top in file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def scroll_to_top_in_file_browser(browser_id, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    browser.scroll_to_top()
