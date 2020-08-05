"""Steps used for handling of data tab elements (e.g. toolbar)
in various oneprovider GUI testing scenarios
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import pytest

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import switch_to_iframe
from tests.gui.utils.generic import (parse_seq, upload_file_path, transform)
from tests.utils.utils import repeat_failed
from tests.utils.bdd_utils import given, wt, parsers, when, then


@repeat_failed(timeout=WAIT_BACKEND)
def check_file_browser_to_load(selenium, browser_id, tmp_memory, op_container,
                               browser):
    driver = selenium[browser_id]
    if browser == 'file browser':
        items_browser = op_container(driver).file_browser
    else:
        items_browser = op_container(driver).shares_page.shares_browser
    tmp_memory[browser_id][transform(browser)] = items_browser


@wt(parsers.re('user of (?P<browser_id>.*?) sees "(?P<space_name>.*?)" '
               '(?P<option>is|is not) in spaces list on Oneprovider page'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_if_list_contains_space_in_data_tab_in_op(selenium, browser_id,
                                                    space_name, option,
                                                    op_container):
    driver = selenium[browser_id]
    space_selector = op_container(driver).data.sidebar.space_selector
    space_selector.expand()
    if option == 'is':
        assert space_name in space_selector.spaces, (
            f'space named "{space_name}" '
            f'found in spaces list, '
            f'while it should not be')
    else:
        assert space_name not in space_selector.spaces, (f'space named '
                                                         f'"{space_name}" not '
                                                         f'found in spaces '
                                                         f'list, '
                                                         f'while it should be')


@when(parsers.re(r'user of (?P<browser_id>.*?) clicks the button '
                 r'from top menu bar with tooltip '
                 r'"(?P<tooltip>Create directory|Create file|Share element|'
                 r'Edit metadata|Rename element|Change element permissions|'
                 r'Copy element|Cut element|Remove element|'
                 r'Show data distribution)"'))
@then(parsers.re(r'user of (?P<browser_id>.*?) clicks the button '
                 r'from top menu bar with tooltip '
                 r'"(?P<tooltip>Create directory|Create file|Share element|'
                 r'Edit metadata|Rename element|Change element permissions|'
                 r'Copy element|Cut element|Remove element|'
                 r'Show data distribution)"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_tooltip_from_toolbar_in_data_tab_in_op(selenium, browser_id, tooltip,
                                                 op_container):
    driver = selenium[browser_id]
    getattr(op_container(driver).data.toolbar, transform(tooltip)).click()


@wt(parsers.re('user of (?P<browser_id>.*?) clicks '
               '"(?P<button>New directory|Upload files|Paste)" button '
               'from file browser menu bar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_from_file_browser_menu_bar(selenium, browser_id, button,
                                            op_container):
    driver = selenium[browser_id]
    button = transform(button) + '_button'
    getattr(op_container(driver).file_browser, transform(button)).click()


@wt(parsers.parse('user of {browser_id} sees that {btn_list} option '
                  'is in selection menu on file browser page'))
@wt(parsers.parse('user of {browser_id} sees that {btn_list} options '
                  'are in selection menu on file browser page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_btn_is_in_file_browser_menu_bar(selenium, browser_id, btn_list,
                                           tmp_memory, popups):
    driver = selenium[browser_id]
    file_browser = tmp_memory[browser_id]['file_browser']
    file_browser.selection_menu_button()

    menu = popups(driver).menu_popup.menu
    for btn in parse_seq(btn_list):
        assert btn in menu, (
            '{} should be in selection menu but is not'.format(btn))


@wt(parsers.parse('user of {browser_id} sees that {btn_list} option '
                  'is not in selection menu on file browser page'))
@wt(parsers.parse('user of {browser_id} sees that {btn_list} options '
                  'are not in selection menu on file browser page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_btn_is_not_in_file_browser_menu_bar(selenium, browser_id, btn_list,
                                               tmp_memory, popups):
    driver = selenium[browser_id]
    file_browser = tmp_memory[browser_id]['file_browser']
    file_browser.selection_menu_button()

    menu = popups(driver).menu_popup.menu
    for btn in parse_seq(btn_list):
        assert btn not in menu, (
            '{} should not be in selection menu'.format(btn))


@wt(parsers.parse('user of {browser_id} sees that current working directory '
                  'displayed in breadcrumbs is {path}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def is_displayed_breadcrumbs_in_data_tab_in_op_correct(selenium, browser_id,
                                                       path, op_container):
    driver = selenium[browser_id]
    breadcrumbs = op_container(driver).file_browser.breadcrumbs.pwd()
    assert path == breadcrumbs, (f'expected breadcrumbs {path}; '
                                 f'displayed: {breadcrumbs}')


@wt(parsers.parse('user of {browser_id} changes current working directory '
                  'to {path} using breadcrumbs'))
@repeat_failed(timeout=WAIT_BACKEND)
def change_cwd_using_breadcrumbs_in_data_tab_in_op(selenium, browser_id, path,
                                                   op_container):
    if path == 'home':
        op_container(selenium[browser_id]).file_browser.breadcrumbs.home()
    else:
        op_container(selenium[browser_id]).file_browser.breadcrumbs.chdir(path)


@when(parsers.parse('user of {browser_id} sees that current working directory '
                    'displayed in directory tree is {path}'))
@then(parsers.parse('user of {browser_id} sees that current working directory '
                    'displayed in directory tree is {path}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def is_displayed_dir_tree_in_data_tab_in_op_correct(selenium, browser_id, path,
                                                    op_container):
    driver = selenium[browser_id]
    cwd = op_container(driver).data.sidebar.cwd.pwd()
    assert path == cwd, 'expected path {}\n got: {}'.format(path, cwd)


@when(parsers.parse('user of {browser_id} changes current working directory '
                    'to {path} using directory tree'))
@then(parsers.parse('user of {browser_id} changes current working directory '
                    'to {path} using directory tree'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_cwd_using_dir_tree_in_data_tab_in_op(selenium, browser_id, path,
                                                op_container):
    driver = selenium[browser_id]
    cwd = op_container(driver).data.sidebar.root_dir
    cwd.click()
    for directory in (dir for dir in path.split('/') if dir != ''):
        if not cwd.is_expanded():
            cwd.expand()
        cwd = cwd[directory]
        cwd.click()


@when(
    parsers.parse('user of {browser_id} does not see {path} in directory tree'))
@then(
    parsers.parse('user of {browser_id} does not see {path} in directory tree'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_absence_of_path_in_dir_tree(selenium, browser_id, path,
                                       op_container):
    driver = selenium[browser_id]
    curr_dir = op_container(driver).data.sidebar.root_dir
    with pytest.raises(RuntimeError):
        for directory in (dir for dir in path.split('/') if dir != ''):
            curr_dir = curr_dir[directory]


@repeat_failed(timeout=WAIT_FRONTEND)
def _is_space_viewed_space_in_data_tab_in_op(driver, is_home, space_name,
                                             op_container):
    selector = op_container(driver).data.sidebar.space_selector
    displayed_name = selector.selected_space_name
    err_msg = 'current directory tree is displayed for "{}" instead of "{}"'
    assert displayed_name == space_name, err_msg.format(displayed_name,
                                                        space_name)
    if is_home:
        assert selector.is_selected_space_home() is True, 'space {} is not ' \
                                                          'home space'.format(
            displayed_name)


@given(parsers.re('user of (?P<browser_id>.+?) seen that displayed directory '
                  'tree in sidebar panel belonged to (?P<is_home>(home '
                  ')?)space '
                  'named "(?P<space_name>.+?)'))
def g_is_space_tree_root(selenium, browser_id, is_home, space_name,
                         op_container):
    driver = selenium[browser_id]
    _is_space_viewed_space_in_data_tab_in_op(driver, True if is_home else False,
                                             space_name, op_container)


@when(parsers.re('user of (?P<browser_id>.+?) sees that displayed directory '
                 'tree in sidebar panel belongs to (?P<is_home>(home )?)space '
                 'named "(?P<space_name>.+?)"'))
@then(parsers.re('user of (?P<browser_id>.+?) sees that displayed directory '
                 'tree in sidebar panel belongs to (?P<is_home>(home )?)space '
                 'named "(?P<space_name>.+?)"'))
def wt_is_space_tree_root(selenium, browser_id, is_home, space_name,
                          op_container):
    driver = selenium[browser_id]
    _is_space_viewed_space_in_data_tab_in_op(driver, True if is_home else False,
                                             space_name, op_container)


@wt(parsers.parse('user of {browser_id} sees nonempty {item_browser} '
                  'in data tab in Oneprovider page'))
@repeat_failed(timeout=WAIT_BACKEND * 2)
def assert_nonempty_file_browser_in_data_tab_in_op(selenium, browser_id,
                                                   op_container, tmp_memory,
                                                   item_browser='file browser'):
    switch_to_iframe(selenium, browser_id)
    check_file_browser_to_load(selenium, browser_id, tmp_memory, op_container,
                               item_browser)
    items_browser = tmp_memory[browser_id][transform(item_browser)]
    assert not items_browser.is_empty(), (f'{item_browser} in data tab in op'
                                          'should not be empty but is')


@wt(parsers.parse('user of {browser_id} sees empty {item_browser} '
                  'in data tab in Oneprovider page'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_empty_file_browser_in_data_tab_in_op(selenium, browser_id,
                                                op_container, tmp_memory,
                                                item_browser='file browser'):
    switch_to_iframe(selenium, browser_id)
    check_file_browser_to_load(selenium, browser_id, tmp_memory, op_container,
                               item_browser)
    items_browser = tmp_memory[browser_id][transform(item_browser)]
    assert items_browser.is_empty(), (f'{item_browser} in data tab in op'
                                      'should be empty but is not')
    tmp_memory[browser_id][transform(item_browser)] = items_browser


@wt(parsers.parse('user of {browser_id} sees {item_browser} '
                  'in data tab in Oneprovider page'))
def assert_file_browser_in_data_tab_in_op(selenium, browser_id, op_container,
                                          tmp_memory,
                                          item_browser='file browser'):
    switch_to_iframe(selenium, browser_id)
    check_file_browser_to_load(selenium, browser_id, tmp_memory, op_container,
                               item_browser)


@when(parsers.parse('user of {browser_id} records displayed name length for '
                    '{path} in directory tree sidebar'))
@when(parsers.parse('user of {browser_id} records displayed name length for '
                    '{path} in directory tree sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_displayed_dir_name_len_in_dir_tree(selenium, browser_id, path,
                                             op_container, tmp_memory):
    driver = selenium[browser_id]
    cwd = op_container(driver).data.sidebar.root_dir
    cwd.click()
    for directory in (dir for dir in path.split('/') if dir != ''):
        cwd = cwd[directory]

    tmp_memory[browser_id][path] = cwd.displayed_name_width


@when(parsers.parse('user of {browser_id} sees that displayed name length for '
                    '{path} in directory tree sidebar is larger than before'))
@then(parsers.parse('user of {browser_id} sees that displayed name length for '
                    '{path} in directory tree sidebar is larger than before'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_diff_in_len_of_dir_name_before_and_now(selenium, browser_id, path,
                                                  op_container, tmp_memory):
    driver = selenium[browser_id]
    cwd = op_container(driver).data.sidebar.root_dir
    cwd.click()
    for directory in (dir for dir in path.split('/') if dir != ''):
        cwd = cwd[directory]

    prev_len = tmp_memory[browser_id][path]
    curr_len = cwd.displayed_name_width
    assert prev_len != curr_len, 'name len of {} is the same as before {' \
                                 '}'.format(path, curr_len)


@when(parsers.re(r'user of (?P<browser_id>.+?) expands data tab sidebar to the '
                 r'(?P<direction>right|left) of approximately ('
                 r'?P<offset>\d+)px'))
@then(parsers.re(r'user of (?P<browser_id>.+?) expands data tab sidebar to the '
                 r'(?P<direction>right|left) of approximately ('
                 r'?P<offset>\d+)px'))
@repeat_failed(timeout=WAIT_FRONTEND)
def resize_data_tab_sidebar(selenium, browser_id, direction, offset,
                            op_container):
    driver = selenium[browser_id]
    sidebar = op_container(driver).data.sidebar
    offset = (-1 if direction == 'left' else 1) * int(offset)
    sidebar.width += offset


@wt(parsers.parse('user of {browser_id} waits for file upload to finish'))
@repeat_failed(timeout=WAIT_BACKEND * 3)
def wait_for_file_upload_to_finish(selenium, browser_id, popups):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    assert not popups(driver).is_upload_presenter(), (
        'file upload not finished '
        'within given time')
    switch_to_iframe(selenium, browser_id)


@wt(parsers.parse('user of {browser_id} uses upload button from file browser '
                  'menu bar to upload file "{file_name}" to current dir'))
@repeat_failed(timeout=2 * WAIT_BACKEND)
def upload_file_to_cwd_in_file_browser(selenium, browser_id, file_name,
                                       op_container):
    driver = selenium[browser_id]
    op_container(driver).file_browser.upload_files(upload_file_path(file_name))


@wt(parsers.parse('user of {browser_id} uses upload button from file browser '
                  'menu bar to upload files from local directory "{dir_path}" '
                  'to remote current dir'))
def upload_files_to_cwd_in_data_tab(selenium, browser_id, dir_path, tmpdir,
                                    op_container):
    driver = selenium[browser_id]
    directory = tmpdir.join(browser_id, *dir_path.split('/'))
    if directory.isdir():
        op_container(driver).file_browser.upload_files('\n'.join(
            str(item) for item in directory.listdir() if item.isfile()))
    else:
        raise RuntimeError('directory {} does not exist'.format(str(directory)))


@when(parsers.parse('user of {browser_id} sees that chunk bar for provider '
                    '"{provider}" is of {size} size'))
@then(parsers.parse('user of {browser_id} sees that chunk bar for provider '
                    '"{provider}" is of {size} size'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_provider_chunk_in_data_distribution_size(selenium, browser_id, size,
                                                    provider, modals, hosts):
    driver = selenium[browser_id]
    provider = hosts[provider]['name']
    prov_rec = modals(driver).data_distribution.providers[provider]
    distribution = prov_rec.distribution
    displayed_size = distribution.end
    assert displayed_size == size, 'displayed chunk size {} in data' \
                                   'distribution modal does not match ' \
                                   'expected ' \
                                   '{}'.format(displayed_size, size)


@wt(parsers.parse('user of {browser_id} sees that chunk bar for provider '
                  '"{provider}" is entirely filled'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_provider_chunk_in_data_distribution_filled(selenium, browser_id,
                                                      provider, modals, hosts):
    driver = selenium[browser_id]
    provider = hosts[provider]['name']
    data_distribution = modals(driver).data_distribution
    distribution = data_distribution.providers[provider].distribution
    size = data_distribution.size()
    chunks = distribution.chunks(size)
    assert len(chunks) == 1, (f'distribution for {provider} is not '
                              f'entirely filled')
    chunk = chunks[0]
    assert chunk[1] - chunk[0] == size, (f'distribution for {provider} is not '
                                         f'filled entirely, but only '
                                         f'from {chunk[0]} to {chunk[1]}')


@when(parsers.parse('user of {browser_id} sees that chunk bar for provider '
                    '"{provider}" is entirely empty'))
@then(parsers.parse('user of {browser_id} sees that chunk bar for provider '
                    '"{provider}" is entirely empty'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_provider_chunk_in_data_distribution_empty(selenium, browser_id,
                                                     provider, modals, hosts):
    driver = selenium[browser_id]
    provider = hosts[provider]['name']
    data_distribution = modals(driver).data_distribution
    distribution = data_distribution.providers[provider].distribution
    size = data_distribution.size()
    chunks = distribution.chunks(size)
    assert not chunks, 'distribution for {} is not entirely empty. ' \
                       'Visible chunks: {}'.format(provider, chunks)


@wt(parsers.parse('user of {browser_id} sees that chunk bar for provider '
                  '"{provider}" is never synchronized'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_provider_chunk_in_data_distribution_never_synchronized(selenium,
                                                                  browser_id,
                                                                  provider,
                                                                  modals, hosts):
    driver = selenium[browser_id]
    provider = hosts[provider]['name']
    data_distribution = modals(driver).data_distribution
    data_distribution.providers[provider].never_synchronized_text


@wt(parsers.parse('user of {browser_id} sees {chunks} chunk(s) for provider '
                  '"{provider}" in chunk bar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_provider_chunks_in_data_distribution(selenium, browser_id, chunks,
                                                provider, modals, hosts):
    driver = selenium[browser_id]
    provider = hosts[provider]['name']
    data_distribution = modals(driver).data_distribution
    distribution = data_distribution.providers[provider].distribution
    size = data_distribution.size()
    displayed_chunks = distribution.chunks(size)
    expected_chunks = parse_seq(chunks, pattern=r'\(.+?\)')
    assert len(displayed_chunks) == len(
        expected_chunks), 'displayed {} chunks instead of expected {}'.format(
        len(displayed_chunks), len(expected_chunks))
    for chunk1, chunk2 in zip(displayed_chunks, expected_chunks):
        assert all(round(x - z) == 0 for x, z in zip(chunk1, parse_seq(chunk2,
                                                                       pattern='\d+',
                                                                       default=int))), 'displayed chunk {} instead of expected {}'.format(
            chunk1, chunk2)


@when(parsers.parse('user of {browser_id} sees that content of downloaded '
                    'file "{file_name}" is equal to: "{content}"'))
@then(parsers.parse('user of {browser_id} sees that content of downloaded '
                    'file "{file_name}" is equal to: "{content}"'))
@repeat_failed(timeout=WAIT_BACKEND)
def has_downloaded_file_content(browser_id, file_name, content, tmpdir):
    downloaded_file = tmpdir.join(browser_id, 'download', file_name)
    if downloaded_file.isfile():
        with downloaded_file.open() as f:
            file_content = ''.join(f.readlines())
            file_content = file_content.strip()
            assert content == file_content, ('expected {} as {} content, '
                                             'instead got {}'.format(content,
                                                                     file_name,
                                                                     file_content))
    else:
        raise RuntimeError('file {} has not been downloaded'.format(file_name))


@wt(parsers.parse('user of {browser_id} chooses {option} option '
                  'from selection menu on file browser page'))
@repeat_failed(timeout=WAIT_BACKEND)
def choose_option_from_selection_menu(browser_id, selenium, option, popups,
                                      tmp_memory):
    driver = selenium[browser_id]
    file_browser = tmp_memory[browser_id]['file_browser']
    file_browser.selection_menu_button()
    popups(driver).menu_popup.menu[option].click()


@wt(parsers.parse('user of {browser_id} sees that upload file failed'))
def check_error_in_upload_presenter(selenium, browser_id, popups):
    driver = selenium[browser_id]
    driver.switch_to.default_content()

    assert popups(driver).upload_presenter[0].is_failed(), 'upload not failed'


@wt(parsers.parse('user of {browser_id} clicks on "{provider}" provider '
                  'on file browser page'))
def choose_provider_in_file_browser(selenium, browser_id, provider, hosts,
                                    oz_page):
    driver = selenium[browser_id]
    provider = hosts[provider]['name']
    driver.switch_to.default_content()

    oz_page(driver)['data'].providers[provider].click()
    iframe = driver.find_element_by_tag_name('iframe')
    driver.switch_to.frame(iframe)


@wt(parsers.parse('user of {browser_id} clicks on Choose other Oneprovider '
                  'on file browser page'))
def click_choose_other_oneprovider_on_file_browser(selenium, browser_id,
                                                   oz_page):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    oz_page(driver)['data'].choose_other_provider()


def check_current_provider_in_space(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    current_provider = oz_page(driver)['data'].current_provider
    return current_provider


def _assert_current_provider_in_space(selenium, browser_id, provider,
                                      oz_page):
    current_provider = check_current_provider_in_space(selenium, browser_id,
                                                       oz_page)
    assert provider == current_provider, (f'{provider} is not current provider '
                                          f'on file browser page')


def _assert_provider_in_space(selenium, browser_id, provider, oz_page):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    providers = oz_page(selenium[browser_id])['data'].providers

    assert provider in providers, (f'{provider} provider not found '
                                   f'on file browser page')


@wt(parsers.parse('user of {browser_id} sees that current provider is '
                  '"{provider}" on file browser page'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_current_provider_in_space(selenium, browser_id, provider, hosts,
                                     oz_page):
    _assert_current_provider_in_space(selenium, browser_id, provider, oz_page)


@wt(parsers.parse('user of {browser_id} sees current provider named '
                  '"{provider}" on file browser page'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_current_provider_name_in_space(selenium, browser_id, provider, hosts,
                                          oz_page):
    provider = hosts[provider]['name']
    _assert_current_provider_in_space(selenium, browser_id, provider, oz_page)


@wt(parsers.parse('user of {browser_id} sees provider named '
                  '"{provider}" on file browser page'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_provider_in_space(selenium, browser_id, provider, hosts, oz_page):
    provider = hosts[provider]['name']
    _assert_provider_in_space(selenium, browser_id, provider, oz_page)


@wt(parsers.parse('user of {browser_id} clicks file browser refresh button'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_refresh_file_browser_button(browser_id, tmp_memory):
    file_browser = tmp_memory[browser_id]['file_browser']
    file_browser.refresh_button()
