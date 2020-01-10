"""Steps used for handling of data tab elements (e.g. toolbar)
in various oneprovider GUI testing scenarios
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import pytest
from pytest_bdd import given, when, then, parsers

from tests.utils.acceptance_utils import wt
from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.utils.generic import (parse_seq, upload_file_path, transform)
from tests.utils.utils import repeat_failed


@when(parsers.parse('user of {browser_id} uses spaces select to change '
                    'data space to "{space_name}"'))
@then(parsers.parse('user of {browser_id} uses spaces select to change '
                    'data space to "{space_name}"'))
@repeat_failed(timeout=WAIT_BACKEND)
def change_space_view_in_data_tab_in_op(selenium, browser_id,
                                        space_name, op_page):
    driver = selenium[browser_id]
    selector = op_page(driver).data.sidebar.space_selector
    selector.expand()
    selector.spaces[space_name].click()


@wt(parsers.re('user of (?P<browser_id>.*?) sees "(?P<space_name>.*?)" '
               '(?P<option>is|is not) in spaces list on Oneprovider page'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_if_list_contains_space_in_data_tab_in_op(selenium, browser_id,
                                                    space_name, option,
                                                    op_page):
    driver = selenium[browser_id]
    space_selector = op_page(driver).data.sidebar.space_selector
    space_selector.expand()
    if option == 'is':
        assert space_name in space_selector.spaces, ('space named "{}" found '
                                                     'in spaces list, while it '
                                                     'should not be')\
            .format(space_name)
    else:
        assert space_name not in space_selector.spaces, ('space named "{}" not '
                                                         'found in spaces list, '
                                                         'while it should be')\
            .format(space_name)


@wt(parsers.re('user of (?P<browser_id>.*?) clicks '
               '"(?P<button>New directory)" button '
               'from file browser menu bar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_from_file_browser_menu_bar(selenium, browser_id,
                                            button, op_page):
    driver = selenium[browser_id]
    getattr(op_page(driver).file_browser, transform(button)).click()


@when(parsers.parse('user of {browser_id} sees that {btn_list} button '
                    'is enabled in toolbar in data tab in Oneprovider gui'))
@then(parsers.parse('user of {browser_id} sees that {btn_list} button '
                    'is enabled in toolbar in data tab in Oneprovider gui'))
@when(parsers.parse('user of {browser_id} sees that {btn_list} buttons '
                    'are enabled in toolbar in data tab in Oneprovider gui'))
@then(parsers.parse('user of {browser_id} sees that {btn_list} buttons '
                    'are enabled in toolbar in data tab in Oneprovider gui'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_btn_enabled_in_toolbar_in_data_tab_in_op(selenium, browser_id,
                                                    btn_list, op_page):
    driver = selenium[browser_id]
    toolbar = op_page(driver).data.toolbar
    for btn in parse_seq(btn_list):
        item = getattr(toolbar, transform(btn))
        assert item.is_enabled() is True, ('{} should be disabled but is not'
                                           ''.format(item))


@when(parsers.parse('user of {browser_id} sees that {btn_list} button is '
                    'disabled in toolbar in data tab in Oneprovider gui'))
@then(parsers.parse('user of {browser_id} sees that {btn_list} button is '
                    'disabled in toolbar in data tab in Oneprovider gui'))
@when(parsers.parse('user of {browser_id} sees that {btn_list} buttons are '
                    'disabled in toolbar in data tab in Oneprovider gui'))
@then(parsers.parse('user of {browser_id} sees that {btn_list} buttons are '
                    'disabled in toolbar in data tab in Oneprovider gui'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_btn_disabled_in_toolbar_in_data_tab_in_op(selenium, browser_id,
                                                     btn_list, op_page):
    driver = selenium[browser_id]
    toolbar = op_page(driver).data.toolbar
    for btn in parse_seq(btn_list):
        item = getattr(toolbar, transform(btn))
        assert item.is_enabled() is False, ('{} btn should be disabled but is '
                                            'not in toolbar in op data tab'
                                            ''.format(btn))


@wt(parsers.parse('user of {browser_id} sees that current working directory '
                  'displayed in breadcrumbs is {path}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def is_displayed_breadcrumbs_in_data_tab_in_op_correct(selenium, browser_id,
                                                       path, op_page):
    driver = selenium[browser_id]
    breadcrumbs = op_page(driver).file_browser.breadcrumbs.pwd()
    assert path == breadcrumbs, ('expected breadcrumbs {}; displayed: {}'
                                 .format(path, breadcrumbs))


@wt(parsers.parse('user of {browser_id} changes current working directory '
                  'to {path} using breadcrumbs'))
@repeat_failed(timeout=WAIT_BACKEND)
def change_cwd_using_breadcrumbs_in_data_tab_in_op(selenium, browser_id,
                                                   path, op_page):
    if path == 'home':
        op_page(selenium[browser_id]).file_browser.breadcrumbs.home()
    else:
        op_page(selenium[browser_id]).file_browser.breadcrumbs.chdir(path)


@when(parsers.parse('user of {browser_id} sees that current working directory '
                    'displayed in directory tree is {path}'))
@then(parsers.parse('user of {browser_id} sees that current working directory '
                    'displayed in directory tree is {path}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def is_displayed_dir_tree_in_data_tab_in_op_correct(selenium, browser_id,
                                                    path, op_page):
    driver = selenium[browser_id]
    cwd = op_page(driver).data.sidebar.cwd.pwd()
    assert path == cwd, 'expected path {}\n got: {}'.format(path, cwd)


@when(parsers.parse('user of {browser_id} changes current working directory '
                    'to {path} using directory tree'))
@then(parsers.parse('user of {browser_id} changes current working directory '
                    'to {path} using directory tree'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_cwd_using_dir_tree_in_data_tab_in_op(selenium, browser_id,
                                                path, op_page):
    driver = selenium[browser_id]
    cwd = op_page(driver).data.sidebar.root_dir
    cwd.click()
    for directory in (dir for dir in path.split('/') if dir != ''):
        if not cwd.is_expanded():
            cwd.expand()
        cwd = cwd[directory]
        cwd.click()


@when(parsers.parse('user of {browser_id} does not see {path} in directory tree'))
@then(parsers.parse('user of {browser_id} does not see {path} in directory tree'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_absence_of_path_in_dir_tree(selenium, browser_id, path, op_page):
    driver = selenium[browser_id]
    curr_dir = op_page(driver).data.sidebar.root_dir
    with pytest.raises(RuntimeError):
        for directory in (dir for dir in path.split('/') if dir != ''):
            curr_dir = curr_dir[directory]


@repeat_failed(timeout=WAIT_FRONTEND)
def _is_space_viewed_space_in_data_tab_in_op(driver, is_home, space_name,
                                             op_page):
    selector = op_page(driver).data.sidebar.space_selector
    displayed_name = selector.selected_space_name
    err_msg = 'current directory tree is displayed for "{}" instead of "{}"'
    assert displayed_name == space_name, err_msg.format(displayed_name,
                                                        space_name)
    if is_home:
        assert selector.is_selected_space_home() is True, \
            'space {} is not home space'.format(displayed_name)


@given(parsers.re('user of (?P<browser_id>.+?) seen that displayed directory '
                  'tree in sidebar panel belonged to (?P<is_home>(home )?)space '
                  'named "(?P<space_name>.+?)'))
def g_is_space_tree_root(selenium, browser_id, is_home, space_name, op_page):
    driver = selenium[browser_id]
    _is_space_viewed_space_in_data_tab_in_op(driver, True if is_home else False,
                                             space_name, op_page)


@when(parsers.re('user of (?P<browser_id>.+?) sees that displayed directory '
                 'tree in sidebar panel belongs to (?P<is_home>(home )?)space '
                 'named "(?P<space_name>.+?)"'))
@then(parsers.re('user of (?P<browser_id>.+?) sees that displayed directory '
                 'tree in sidebar panel belongs to (?P<is_home>(home )?)space '
                 'named "(?P<space_name>.+?)"'))
def wt_is_space_tree_root(selenium, browser_id, is_home, space_name, op_page):
    driver = selenium[browser_id]
    _is_space_viewed_space_in_data_tab_in_op(driver, True if is_home else False,
                                             space_name, op_page)


@when(parsers.parse('user of {browser_id} sees nonempty file browser '
                    'in data tab in Oneprovider page'))
@then(parsers.parse('user of {browser_id} sees nonempty file browser '
                    'in data tab in Oneprovider page'))
@repeat_failed(timeout=WAIT_BACKEND * 2)
def assert_nonempty_file_browser_in_data_tab_in_op(selenium, browser_id,
                                                   op_page, tmp_memory):
    driver = selenium[browser_id]
    file_browser = op_page(driver).data.file_browser
    assert not file_browser.is_empty(), ('file browser in data tab in op'
                                         'should not be empty but is')
    tmp_memory[browser_id]['file_browser'] = file_browser


@wt(parsers.parse('user of {browser_id} sees empty file browser '
                  'in data tab in Oneprovider page'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_empty_file_browser_in_data_tab_in_op(selenium, browser_id,
                                                op_page, tmp_memory):
    driver = selenium[browser_id]
    iframe = driver.find_element_by_tag_name('iframe')
    driver.switch_to.frame(iframe)
    file_browser = op_page(driver).file_browser
    assert file_browser.is_empty(), ('file browser in data tab in op'
                                     'should be empty but is not')
    tmp_memory[browser_id]['file_browser'] = file_browser


@wt(parsers.parse('user of {browser_id} sees file browser '
                  'in data tab in Oneprovider page'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_file_browser_in_data_tab_in_op(selenium, browser_id,
                                          op_page, tmp_memory):
    driver = selenium[browser_id]
    iframe = driver.find_element_by_tag_name('iframe')
    driver.switch_to.frame(iframe)
    file_browser = op_page(driver).file_browser
    tmp_memory[browser_id]['file_browser'] = file_browser


@when(parsers.parse('user of {browser_id} records displayed name length for '
                    '{path} in directory tree sidebar'))
@when(parsers.parse('user of {browser_id} records displayed name length for '
                    '{path} in directory tree sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_displayed_dir_name_len_in_dir_tree(selenium, browser_id, path,
                                             op_page, tmp_memory):
    driver = selenium[browser_id]
    cwd = op_page(driver).data.sidebar.root_dir
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
                                                  op_page, tmp_memory):
    driver = selenium[browser_id]
    cwd = op_page(driver).data.sidebar.root_dir
    cwd.click()
    for directory in (dir for dir in path.split('/') if dir != ''):
        cwd = cwd[directory]

    prev_len = tmp_memory[browser_id][path]
    curr_len = cwd.displayed_name_width
    assert prev_len != curr_len, \
        'name len of {} is the same as before {}'.format(path, curr_len)


@when(parsers.re(r'user of (?P<browser_id>.+?) expands data tab sidebar to the '
                 r'(?P<direction>right|left) of approximately (?P<offset>\d+)px'))
@then(parsers.re(r'user of (?P<browser_id>.+?) expands data tab sidebar to the '
                 r'(?P<direction>right|left) of approximately (?P<offset>\d+)px'))
@repeat_failed(timeout=WAIT_FRONTEND)
def resize_data_tab_sidebar(selenium, browser_id, direction, offset, op_page):
    driver = selenium[browser_id]
    sidebar = op_page(driver).data.sidebar
    offset = (-1 if direction == 'left' else 1) * int(offset)
    sidebar.width += offset


@when(parsers.parse('user of {browser_id} waits for file upload to finish'))
@then(parsers.parse('user of {browser_id} waits for file upload to finish'))
@repeat_failed(timeout=WAIT_BACKEND * 3)
def wait_for_file_upload_to_finish(selenium, browser_id, op_page):
    driver = selenium[browser_id]
    uploader = op_page(driver).data.file_uploader
    assert not uploader.is_visible(), \
        'file upload not finished within given time'


@wt(parsers.parse('user of {browser_id} uses upload button from file browser '
                  'menu bar to upload file "{file_name}" to current dir'))
def upload_file_to_cwd_in_file_browser(selenium, browser_id, file_name, op_page):
    driver = selenium[browser_id]
    op_page(driver).file_browser.upload_files(upload_file_path(file_name))


@when(parsers.parse('user of {browser_id} uses upload button in toolbar to '
                    'upload files from local directory "{dir_path}" to remote '
                    'current dir'))
@then(parsers.parse('user of {browser_id} uses upload button in toolbar to '
                    'upload files from local directory "{dir_path}" to remote '
                    'current dir'))
def upload_files_to_cwd_in_data_tab(selenium, browser_id, dir_path,
                                    tmpdir, op_page):
    driver = selenium[browser_id]
    directory = tmpdir.join(browser_id, *dir_path.split('/'))
    if directory.isdir():
        op_page(driver).data.toolbar.upload_files('\n'.join(str(item) for item
                                                            in
                                                            directory.listdir()
                                                            if item.isfile()))
    else:
        raise RuntimeError('directory {} does not exist'.format(str(directory)))


@when(parsers.parse('user of {browser_id} sees that chunk bar for provider '
                    '"{provider}" is of {size} size'))
@then(parsers.parse('user of {browser_id} sees that chunk bar for provider '
                    '"{provider}" is of {size} size'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_provider_chunk_in_data_distribution_size(selenium, browser_id,
                                                    size, provider, modals,
                                                    hosts):
    driver = selenium[browser_id]
    provider = hosts[provider]['name']
    prov_rec = modals(driver).data_distribution.providers[provider]
    distribution = prov_rec.distribution
    displayed_size = distribution.end
    assert displayed_size == size, 'displayed chunk size {} in data' \
                                   'distribution modal does not match expected ' \
                                   '{}'.format(displayed_size, size)


@when(parsers.parse('user of {browser_id} sees that chunk bar for provider '
                    '"{provider}" is entirely filled'))
@then(parsers.parse('user of {browser_id} sees that chunk bar for provider '
                    '"{provider}" is entirely filled'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_provider_chunk_in_data_distribution_filled(selenium, browser_id,
                                                      provider, modals, hosts):
    driver = selenium[browser_id]
    provider = hosts[provider]['name']
    prov_rec = modals(driver).data_distribution.providers[provider]
    distribution = prov_rec.distribution
    size, _ = distribution.size
    chunks = distribution.chunks
    assert len(chunks) == 1, 'distribution for {} is not ' \
                             'entirely filled'.format(provider)
    chunk = chunks[0]
    assert chunk[1] - chunk[0] == size, \
        'distribution for {} is not filled entirely, but only from ' \
        '{} to {}'.format(provider, chunk[0], chunk[1])


@when(parsers.parse('user of {browser_id} sees that chunk bar for provider '
                    '"{provider}" is entirely empty'))
@then(parsers.parse('user of {browser_id} sees that chunk bar for provider '
                    '"{provider}" is entirely empty'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_provider_chunk_in_data_distribution_empty(selenium, browser_id,
                                                     provider, modals, hosts):
    driver = selenium[browser_id]
    provider = hosts[provider]['name']
    prov_rec = modals(driver).data_distribution.providers[provider]
    distribution = prov_rec.distribution
    size, _ = distribution.size
    chunks = distribution.chunks
    assert not chunks, 'distribution for {} is not entirely empty. ' \
                       'Visible chunks: {}'.format(provider, chunks)


@when(parsers.parse('user of {browser_id} sees {chunks} chunk(s) for provider '
                    '"{provider}" in chunk bar'))
@then(parsers.parse('user of {browser_id} sees {chunks} chunk(s) for provider '
                    '"{provider}" in chunk bar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_provider_chunks_in_data_distribution(selenium, browser_id, chunks,
                                                provider, modals, hosts):
    driver = selenium[browser_id]
    provider = hosts[provider]['name']
    prov_rec = modals(driver).data_distribution.providers[provider]
    distribution = prov_rec.distribution
    size, _ = distribution.size
    displayed_chunks = distribution.chunks
    expected_chunks = parse_seq(chunks, pattern=r'\(.+?\)')
    assert len(displayed_chunks) == len(expected_chunks), \
        'displayed {} chunks instead of expected {}'.format(
            len(displayed_chunks),
            len(expected_chunks))
    for chunk1, chunk2 in zip(displayed_chunks, expected_chunks):
        assert all(round(x - z) == 0 for x, z in zip(chunk1,
                                                     parse_seq(chunk2,
                                                               pattern='\d+',
                                                               default=int))), \
            'displayed chunk {} instead of expected {}'.format(chunk1, chunk2)


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
            assert content == file_content, \
                ('expected {} as {} content, '
                 'instead got {}'.format(content, file_name, file_content))
    else:
        raise RuntimeError('file {} has not been downloaded'.format(file_name))
