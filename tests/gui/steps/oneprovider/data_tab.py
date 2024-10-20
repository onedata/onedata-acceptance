"""Steps used for handling of files tab elements (e.g. toolbar)
in various oneprovider GUI testing scenarios
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time

import pytest
from tests.gui.conftest import WAIT_BACKEND, WAIT_EXTENDED_UPLOAD, WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import switch_to_iframe
from tests.gui.steps.oneprovider.browser import click_and_press_enter_on_item_in_browser
from tests.gui.utils.generic import parse_seq, transform, upload_file_path
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.entities_setup import (
    DOWNLOAD_INACTIVITY_PERIOD_SEC,
    GUI_DOWNLOAD_CHUNK_SIZE,
    GUI_UPLOAD_CHUNK_SIZE,
    UPLOAD_INACTIVITY_PERIOD_SEC,
)
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_BACKEND)
def check_browser_to_load(selenium, browser_id, tmp_memory, op_container, browser):
    driver = selenium[browser_id]
    if transform(browser) == "shares_browser":
        items_browser = op_container(driver).shares_page.shares_browser
    else:
        items_browser = getattr(op_container(driver), transform(browser))
    tmp_memory[browser_id][transform(browser)] = items_browser


@wt(
    parsers.re(
        'user of (?P<browser_id>.*?) sees "(?P<space_name>.*?)" '
        "(?P<option>is|is not) in spaces list on Oneprovider page"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_if_list_contains_space_in_data_tab_in_op(
    selenium, browser_id, space_name, option, op_container
):
    driver = selenium[browser_id]
    space_selector = op_container(driver).data.sidebar.space_selector
    space_selector.expand()
    if option == "is":
        assert (
            space_name in space_selector.spaces
        ), f'space named "{space_name}" found in spaces list, while it should not be'
    else:
        assert (
            space_name not in space_selector.spaces
        ), f'space named "{space_name}" not found in spaces list, while it should be'


@wt(
    parsers.re(
        "user of (?P<browser_id>.*?) clicks the button "
        "from top menu bar with tooltip "
        '"(?P<tooltip>Create directory|Create file|Share element|'
        "Edit metadata|Rename element|Change element permissions|"
        "Copy element|Cut element|Remove element|"
        'Show data distribution)"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_tooltip_from_toolbar_in_data_tab_in_op(
    selenium, browser_id, tooltip, op_container
):
    driver = selenium[browser_id]
    getattr(op_container(driver).data.toolbar, transform(tooltip)).click()


@wt(
    parsers.re(
        "user of (?P<browser_id>.*?) clicks "
        '"(?P<button>New directory|Upload files|Refresh|Paste)" button '
        "from file browser menu bar"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_from_file_browser_menu_bar(browser_id, button, tmp_memory):
    button = transform(button) + "_button"
    file_browser = tmp_memory[browser_id]["file_browser"]
    getattr(file_browser, transform(button)).click()


@wt(
    parsers.parse(
        "user of {browser_id} changes current working directory "
        "to {path} using breadcrumbs in {which_browser}"
    )
)
def wt_change_cwd_using_breadcrumbs_in_data_tab_in_op(
    selenium, browser_id, path, op_container, which_browser
):
    change_cwd_using_breadcrumbs_in_data_tab_in_op(
        selenium, browser_id, path, op_container, which_browser=which_browser
    )


@wt(
    parsers.parse(
        "user of {browser_id} changes current working directory "
        "to {path} using breadcrumbs"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def change_cwd_using_breadcrumbs_in_data_tab_in_op(
    selenium, browser_id, path, op_container, which_browser="file browser"
):
    # this cannot be first step that uses which_browser,
    # browser must be loaded before in some previous step
    archive = which_browser == "archive file browser"
    breadcrumbs = _get_breadcrumbs(browser_id, selenium, op_container, which_browser)
    path = transform(path)
    if path == "space_root":
        breadcrumbs.space_root()
    else:
        breadcrumbs.chdir(path, archive)


@repeat_failed(timeout=WAIT_BACKEND)
def go_one_back_using_breadcrumbs_in_data_tab_in_op(
    selenium, browser_id, op_container, which_browser="file browser"
):
    # this cannot be first step that uses which_browser,
    # browser must be loaded before in some previous step
    breadcrumbs = _get_breadcrumbs(browser_id, selenium, op_container, which_browser)
    breadcrumbs.go_one_back()


def _get_breadcrumbs(browser_id, selenium, op_container, which_browser):
    try:
        breadcrumbs = getattr(
            op_container(selenium[browser_id]), transform(which_browser)
        ).breadcrumbs
    except RuntimeError:
        which_browser = "archive browser"
        breadcrumbs = getattr(
            op_container(selenium[browser_id]), transform(which_browser)
        ).breadcrumbs
    return breadcrumbs


@wt(
    parsers.parse(
        "user of {browser_id} sees that current working directory "
        "displayed in directory tree is {path}"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def is_displayed_dir_tree_in_data_tab_in_op_correct(
    selenium, browser_id, path, op_container
):
    driver = selenium[browser_id]
    cwd = op_container(driver).data.sidebar.cwd.pwd()
    assert path == cwd, f"expected path {path}\n got: {path}"


@wt(parsers.parse("user of {browser_id} does not see {path} in directory tree"))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_absence_of_path_in_dir_tree(selenium, browser_id, path, op_container):
    driver = selenium[browser_id]
    curr_dir = op_container(driver).data.sidebar.root_dir
    with pytest.raises(RuntimeError):
        for directory in (dir for dir in path.split("/") if dir != ""):
            curr_dir = curr_dir[directory]


@repeat_failed(timeout=WAIT_FRONTEND)
def _is_space_viewed_space_in_data_tab_in_op(driver, is_home, space_name, op_container):
    selector = op_container(driver).data.sidebar.space_selector
    displayed_name = selector.selected_space_name
    err_msg = 'current directory tree is displayed for "{}" instead of "{}"'
    assert displayed_name == space_name, err_msg.format(displayed_name, space_name)
    if is_home:
        assert (
            selector.is_selected_space_home() is True
        ), f"space {displayed_name} is not home space"


@given(
    parsers.re(
        "user of (?P<browser_id>.+?) seen that displayed directory "
        "tree in sidebar panel belonged to (?P<is_home>(home "
        ")?)space "
        'named "(?P<space_name>.+?)'
    )
)
def g_is_space_tree_root(selenium, browser_id, is_home, space_name, op_container):
    driver = selenium[browser_id]
    _is_space_viewed_space_in_data_tab_in_op(
        driver, bool(is_home), space_name, op_container
    )


@wt(
    parsers.re(
        "user of (?P<browser_id>.+?) sees that displayed directory "
        "tree in sidebar panel belongs to (?P<is_home>(home )?)space "
        'named "(?P<space_name>.+?)"'
    )
)
def wt_is_space_tree_root(selenium, browser_id, is_home, space_name, op_container):
    driver = selenium[browser_id]
    _is_space_viewed_space_in_data_tab_in_op(
        driver, bool(is_home), space_name, op_container
    )


@repeat_failed(timeout=WAIT_BACKEND * 2)
def assert_nonempty_file_browser_in_files_tab_in_op(
    selenium, browser_id, op_container, tmp_memory, item_browser="file browser"
):
    switch_to_iframe(selenium, browser_id)
    check_browser_to_load(selenium, browser_id, tmp_memory, op_container, item_browser)
    items_browser = tmp_memory[browser_id][transform(item_browser)]
    assert (
        not items_browser.is_empty()
    ), f"{item_browser} in files tab in opshould not be empty but is"


@repeat_failed(timeout=WAIT_BACKEND)
def assert_empty_browser_in_files_tab_in_op(
    selenium, browser_id, op_container, tmp_memory, item_browser="file browser"
):
    switch_to_iframe(selenium, browser_id)
    check_browser_to_load(selenium, browser_id, tmp_memory, op_container, item_browser)
    items_browser = tmp_memory[browser_id][transform(item_browser)]
    assert (
        items_browser.is_empty()
    ), f"{item_browser} in files tab in op should be empty but is not"
    tmp_memory[browser_id][transform(item_browser)] = items_browser


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_browser_in_tab_in_op(
    selenium, browser_id, op_container, tmp_memory, item_browser="file browser"
):
    switch_to_iframe(selenium, browser_id)
    check_browser_to_load(selenium, browser_id, tmp_memory, op_container, item_browser)


@wt(
    parsers.parse(
        "user of {browser_id} sees {item_browser} in {} tab in Oneprovider page"
    )
)
def wt_assert_browser_in_tab_in_op(
    selenium, browser_id, op_container, tmp_memory, item_browser
):
    if "empty" in item_browser.split(" "):
        assert_empty_browser_in_files_tab_in_op(
            selenium,
            browser_id,
            op_container,
            tmp_memory,
            item_browser=item_browser.replace("empty ", ""),
        )
    elif "nonempty" in item_browser.split(" "):
        assert_nonempty_file_browser_in_files_tab_in_op(
            selenium,
            browser_id,
            op_container,
            tmp_memory,
            item_browser=item_browser.replace("nonempty ", ""),
        )
    else:
        assert_browser_in_tab_in_op(
            selenium,
            browser_id,
            op_container,
            tmp_memory,
            item_browser=item_browser,
        )


@wt(
    parsers.parse(
        "user of {browser_id} records displayed name length for "
        "{path} in directory tree sidebar"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def check_displayed_dir_name_len_in_dir_tree(
    selenium, browser_id, path, op_container, tmp_memory
):
    driver = selenium[browser_id]
    cwd = op_container(driver).data.sidebar.root_dir
    cwd.click()
    for directory in (dir for dir in path.split("/") if dir != ""):
        cwd = cwd[directory]

    tmp_memory[browser_id][path] = cwd.displayed_name_width


@wt(
    parsers.parse(
        "user of {browser_id} sees that displayed name length for "
        "{path} in directory tree sidebar is larger than before"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_diff_in_len_of_dir_name_before_and_now(
    selenium, browser_id, path, op_container, tmp_memory
):
    driver = selenium[browser_id]
    cwd = op_container(driver).data.sidebar.root_dir
    cwd.click()
    for directory in (dir for dir in path.split("/") if dir != ""):
        cwd = cwd[directory]

    prev_len = tmp_memory[browser_id][path]
    curr_len = cwd.displayed_name_width
    assert prev_len != curr_len, f"name len of {path} is the same as before {curr_len}"


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) expands data tab sidebar to the "
        r"(?P<direction>right|left) of approximately "
        r"(?P<offset>\d+)px"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def resize_data_tab_sidebar(selenium, browser_id, direction, offset, op_container):
    driver = selenium[browser_id]
    sidebar = op_container(driver).data.sidebar
    offset = (-1 if direction == "left" else 1) * int(offset)
    sidebar.width += offset


@wt(parsers.re("user of (?P<browser_id>.*) waits for file uploads? to finish"))
@repeat_failed(timeout=WAIT_EXTENDED_UPLOAD)
def wait_for_file_upload_to_finish(selenium, browser_id, popups):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    time.sleep(1)
    assert not popups(
        driver
    ).is_upload_presenter(), "file upload not finished within given time"
    switch_to_iframe(selenium, browser_id)


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) waits extended time for file uploads? to finish"
    )
)
@repeat_failed(timeout=WAIT_EXTENDED_UPLOAD)
def wait_extended_time_for_file_upload_to_finish(selenium, browser_id, popups):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    assert not popups(
        driver
    ).is_upload_presenter(), "file upload not finished within given time"
    switch_to_iframe(selenium, browser_id)


@wt(
    parsers.parse(
        "user of {browser_id} uses upload button from file browser "
        'menu bar to upload {option} "{file_name}" to current dir '
        "without waiting for upload to finish"
    )
)
@repeat_failed(timeout=2 * WAIT_BACKEND)
def upload_file_to_cwd_in_file_browser_no_waiting(
    selenium, browser_id, file_name, op_container
):
    driver = selenium[browser_id]
    op_container(driver).file_browser.upload_files(upload_file_path(file_name))


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) uses upload button from file "
        "browser menu bar to upload (?P<option>.*) "
        '"automation/(?P<inner_dir>.*)/'
        '(?P<file_name>.*)" to current dir'
    )
)
@repeat_failed(timeout=2 * WAIT_BACKEND)
def upload_automation_file_to_cwd_in_file_browser(
    selenium, browser_id, file_name, op_container, inner_dir, popups
):
    file_name = "automation/" + inner_dir + "/" + file_name.replace('"', "")
    driver = selenium[browser_id]
    op_container(driver).file_browser.upload_files(upload_file_path(file_name))
    wait_for_file_upload_to_finish(selenium, browser_id, popups)


@wt(
    parsers.parse(
        "user of {browser_id} uses upload button from file browser "
        'menu bar to upload file "{file_name}" to current dir'
    )
)
@repeat_failed(timeout=2 * WAIT_BACKEND)
def upload_file_to_cwd_in_file_browser(
    selenium, browser_id, file_name, op_container, popups
):
    upload_file_to_cwd_in_file_browser_no_waiting(
        selenium, browser_id, file_name, op_container
    )
    wait_for_file_upload_to_finish(selenium, browser_id, popups)


@wt(
    parsers.parse(
        "user of {browser_id} uses upload button from file browser "
        'menu bar to upload files from local directory "{dir_path}" '
        "to remote current dir"
    )
)
@repeat_failed(timeout=2 * WAIT_BACKEND)
def upload_files_to_cwd_in_data_tab(
    selenium, browser_id, dir_path, tmpdir, op_container, popups
):
    upload_files_to_cwd_in_data_tab_no_waiting(
        selenium, browser_id, dir_path, tmpdir, op_container
    )
    wait_for_file_upload_to_finish(selenium, browser_id, popups)


@wt(
    parsers.parse(
        "user of {browser_id} uses upload button from file browser "
        'menu bar to upload files from local directory "{dir_path}" '
        "to remote current dir without waiting for upload to finish"
    )
)
@repeat_failed(timeout=2 * WAIT_BACKEND)
def upload_files_to_cwd_in_data_tab_no_waiting(
    selenium, browser_id, dir_path, tmpdir, op_container
):
    driver = selenium[browser_id]
    directory = tmpdir.join(browser_id, *dir_path.split("/"))
    if directory.isdir():
        op_container(driver).file_browser.upload_files(
            "\n".join(str(item) for item in directory.listdir() if item.isfile())
        )
    else:
        raise RuntimeError(f"directory {directory} does not exist")


@wt(
    parsers.parse(
        "user of {browser_id} uses upload button from file browser "
        'menu bar to upload files from local directory "{dir_path}" '
        "to remote current dir and waits extended time for upload to "
        "finish"
    )
)
@repeat_failed(timeout=WAIT_EXTENDED_UPLOAD)
def upload_files_to_cwd_in_data_tab_extended_wait(
    selenium, browser_id, dir_path, tmpdir, op_container, popups
):
    upload_files_to_cwd_in_data_tab_no_waiting(
        selenium, browser_id, dir_path, tmpdir, op_container
    )
    wait_extended_time_for_file_upload_to_finish(selenium, browser_id, popups)


@wt(
    parsers.parse(
        "user of {browser_id} uses upload button from file browser "
        'menu bar to upload local file "{file_path}" '
        "to remote current dir"
    )
)
@repeat_failed(timeout=WAIT_EXTENDED_UPLOAD)
def upload_file_to_cwd_in_data_tab(
    selenium, browser_id, file_path, tmpdir, op_container, popups
):
    upload_file_to_cwd_in_data_tab_no_waiting(
        selenium, browser_id, file_path, tmpdir, op_container
    )
    wait_for_file_upload_to_finish(selenium, browser_id, popups)


@wt(
    parsers.parse(
        "user of {browser_id} uses upload button from file browser "
        'menu bar to upload {number} local files "{file_path}" '
        "to remote current dir"
    )
)
@repeat_failed(timeout=2 * WAIT_BACKEND)
def upload_number_of_files_to_cwd_in_data_tab(
    selenium, browser_id, file_path, tmpdir, op_container, popups, number
):
    for _ in range(int(number)):
        upload_file_to_cwd_in_data_tab_no_waiting(
            selenium, browser_id, file_path, tmpdir, op_container
        )
    wait_for_file_upload_to_finish(selenium, browser_id, popups)


@wt(
    parsers.parse(
        "user of {browser_id} uses upload button from file browser "
        'menu bar to upload local file "{file_path}" '
        "to remote current dir without waiting for upload to finish"
    )
)
@repeat_failed(timeout=2 * WAIT_BACKEND)
def upload_file_to_cwd_in_data_tab_no_waiting(
    selenium, browser_id, file_path, tmpdir, op_container
):
    driver = selenium[browser_id]
    file = tmpdir.join(browser_id, *file_path.split("/"))
    if file.isfile():
        op_container(driver).file_browser.upload_files(upload_file_path(file))
    else:
        raise RuntimeError(f"file {file} does not exist")


def network_throttling_upload(driver):
    upload_kb = (GUI_UPLOAD_CHUNK_SIZE / UPLOAD_INACTIVITY_PERIOD_SEC) * 1024

    driver.set_network_conditions(
        latency=5,
        download_throughput=500 * 1024,
        upload_throughput=float(upload_kb) / 8 * 1024,
    )


@wt(
    parsers.parse(
        "user of {browser_id} uses upload button from file browser "
        'menu bar to upload local file "{file_path}" '
        "to remote current dir with slow connection"
    )
)
@repeat_failed(timeout=WAIT_EXTENDED_UPLOAD)
def upload_file_to_cwd_in_data_tab_with_network_throttling(
    selenium, browser_id, file_path, tmpdir, op_container, popups
):
    driver = selenium[browser_id]
    network_throttling_upload(driver)
    file = tmpdir.join(browser_id, file_path)
    if file.isfile():
        op_container(driver).file_browser.upload_files(upload_file_path(file))
    else:
        raise RuntimeError(f"file {str(file)} does not exist")

    wait_extended_time_for_file_upload_to_finish(selenium, browser_id, popups)


@wt(
    parsers.parse(
        "user of {browser_id} sees that chunk bar for provider "
        '"{provider}" is of {size} size'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_provider_chunk_in_data_distribution_size(
    selenium, browser_id, size, provider, modals, hosts
):
    driver = selenium[browser_id]
    provider = hosts[provider]["name"]
    prov_rec = modals(driver).details_modal.data_distribution.providers[provider]
    distribution = prov_rec.distribution
    displayed_size = distribution.end
    assert displayed_size == size, (
        f"displayed chunk size {displayed_size} in data distribution modal "
        f"does not match expected {size}"
    )


@wt(
    parsers.parse(
        "user of {browser_id} sees that chunk bar for provider "
        '"{provider}" is entirely filled'
    )
)
@repeat_failed(timeout=WAIT_BACKEND * 2)
def assert_provider_chunk_in_data_distribution_filled(
    selenium, browser_id, provider, modals, hosts
):
    driver = selenium[browser_id]
    provider = hosts[provider]["name"]
    data_distribution = modals(driver).details_modal.data_distribution
    distribution = data_distribution.providers[provider].distribution
    size = data_distribution.size()
    chunks = distribution.chunks(size)
    assert len(chunks) == 1, f"distribution for {provider} is not entirely filled"
    chunk = chunks[0]
    assert chunk[1] - chunk[0] == size, (
        f"distribution for {provider} is not "
        "filled entirely, but only "
        f"from {chunk[0]} to {chunk[1]}"
    )


@wt(
    parsers.parse(
        "user of {browser_id} sees that chunk bar for provider "
        '"{provider}" is entirely empty'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_provider_chunk_in_data_distribution_empty(
    selenium, browser_id, provider, modals, hosts
):
    driver = selenium[browser_id]
    provider = hosts[provider]["name"]
    data_distribution = modals(driver).details_modal.data_distribution
    distribution = data_distribution.providers[provider].distribution
    size = data_distribution.size()
    chunks = distribution.chunks(size)
    assert (
        not chunks
    ), f"distribution for {provider} is not entirely empty. Visible chunks: {chunks}"


@wt(
    parsers.parse(
        "user of {browser_id} sees {chunks} chunk(s) for provider "
        '"{provider}" in chunk bar'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_provider_chunks_in_data_distribution(
    selenium, browser_id, chunks, provider, modals, hosts
):
    driver = selenium[browser_id]
    provider = hosts[provider]["name"]
    data_distribution = modals(driver).details_modal.data_distribution
    distribution = data_distribution.providers[provider].distribution
    size = data_distribution.size()
    displayed_chunks = distribution.chunks(size)
    expected_chunks = parse_seq(chunks, pattern=r"\(.+?\)")
    assert len(displayed_chunks) == len(expected_chunks), (
        f"displayed {len(displayed_chunks)} chunks instead "
        f"of expected {len(expected_chunks)}"
    )
    for chunk1, chunk2 in zip(displayed_chunks, expected_chunks):
        assert all(
            round(x - z) == 0
            for x, z in zip(chunk1, parse_seq(chunk2, pattern=r"\d+", default=int))
        ), f"displayed chunk {chunk1} instead of expected {chunk2}"


@wt(
    parsers.parse(
        "user of {browser_id} sees that content of downloaded "
        'file "{file_name}" is equal to: "{content}"'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def has_downloaded_file_content(browser_id, file_name, content, tmpdir):
    downloaded_file = tmpdir.join(browser_id, "download", file_name)
    if downloaded_file.isfile():
        with downloaded_file.open() as f:
            file_content = "".join(f.readlines())
            file_content = file_content.strip()
            assert (
                content == file_content
            ), f"expected {content} as {file_name} content, instead got {file_content}"
    else:
        raise RuntimeError(f"file {file_name} has not been downloaded")


@wt(
    parsers.parse(
        "user of {browser_id} chooses {option} option "
        "from selection menu on file browser page"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def choose_option_from_selection_menu(browser_id, selenium, option, popups, tmp_memory):
    driver = selenium[browser_id]
    file_browser = tmp_memory[browser_id]["file_browser"]
    file_browser.selection_menu_button()
    popups(driver).menu_popup_with_label.menu[option].click()


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{option}" option from file '
        'menu for "{file_name}" on file list'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_option_for_file_from_selection_menu(
    browser_id, selenium, option, popups, tmp_memory, file_name
):
    driver = selenium[browser_id]
    file_browser = tmp_memory[browser_id]["file_browser"]
    file_browser.data[file_name].menu_button()
    menu = popups(driver).menu_popup
    menu.choose_option(option)


@wt(parsers.parse("user of {browser_id} sees that upload file failed"))
def check_error_in_upload_presenter(selenium, browser_id, popups):
    driver = selenium[browser_id]
    driver.switch_to.default_content()

    assert popups(driver).upload_presenter[0].is_failed(), "upload not failed"


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "{provider}" provider on {which} page'
    )
)
def choose_provider_in_selected_page(selenium, browser_id, provider, hosts, oz_page):
    driver = selenium[browser_id]
    provider = hosts[provider]["name"]
    driver.switch_to.default_content()

    oz_page(driver)["data"].providers[provider].click()


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "Choose other Oneprovider" on file browser page'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def click_choose_other_oneprovider_on_file_browser(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    oz_page(driver)["data"].choose_other_provider()


def check_current_provider_in_space(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    current_provider = oz_page(driver)["data"].current_provider
    return current_provider


def _assert_current_provider_in_space(selenium, browser_id, provider, oz_page):
    current_provider = check_current_provider_in_space(selenium, browser_id, oz_page)
    assert (
        provider == current_provider
    ), f"{provider} is not current provider on file browser page"


def _assert_provider_in_space(selenium, browser_id, provider, oz_page):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    providers = oz_page(selenium[browser_id])["data"].providers

    assert provider in providers, f"{provider} provider not found on file browser page"


@wt(
    parsers.parse(
        "user of {browser_id} sees that current provider is "
        '"{provider}" on file browser page'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_current_provider_in_space(selenium, browser_id, provider, oz_page):
    _assert_current_provider_in_space(selenium, browser_id, provider, oz_page)


@wt(
    parsers.parse(
        "user of {browser_id} sees current provider named "
        '"{provider}" on file browser page'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_current_provider_name_in_space(
    selenium, browser_id, provider, hosts, oz_page
):
    provider = hosts[provider]["name"]
    _assert_current_provider_in_space(selenium, browser_id, provider, oz_page)


@wt(
    parsers.parse(
        'user of {browser_id} sees provider named "{provider}" on file browser page'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_provider_in_space(selenium, browser_id, provider, hosts, oz_page):
    provider = hosts[provider]["name"]
    _assert_provider_in_space(selenium, browser_id, provider, oz_page)


@wt(
    parsers.parse(
        'user of {browser_id} clicks "{button}" button from file browser menu bar'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def click_file_browser_button(browser_id, button, tmp_memory):
    file_browser = tmp_memory[browser_id]["file_browser"]
    getattr(file_browser, f"{transform(button)}_button").click()


def network_throttling_download(driver):
    download_kb = (GUI_DOWNLOAD_CHUNK_SIZE / DOWNLOAD_INACTIVITY_PERIOD_SEC) * 1024

    driver.set_network_conditions(
        latency=5,
        download_throughput=float(download_kb) / 8 * 1024,
        upload_throughput=500 * 1024,
    )


@wt(
    parsers.parse(
        'user of {browser_id} downloads item named "{item_name}" '
        "with slow connection in {which_browser}"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def download_file_with_network_throttling(
    selenium, browser_id, item_name, tmp_memory, op_container
):
    driver = selenium[browser_id]
    network_throttling_download(driver)

    click_and_press_enter_on_item_in_browser(
        selenium, browser_id, item_name, tmp_memory, op_container
    )


@wt(
    parsers.parse(
        "user of {browser_id} sees that data distribution for "
        "{provider} is at {percentage}"
    )
)
@repeat_failed(interval=1, timeout=40, exceptions=AssertionError)
def check_data_distribution_percentage_for_provider(
    selenium, browser_id, provider, percentage, modals, hosts
):
    driver = selenium[browser_id]
    provider = hosts[provider]["name"]
    # TODO VFS-12315 remove sleep in acc tests
    time.sleep(1)
    data_distribution = modals(driver).details_modal.data_distribution
    percentage_label = data_distribution.providers[provider].percentage_label
    assert percentage_label == percentage, (
        f"Data distribution at {percentage_label} instead of {percentage}"
        f" for provider {provider}!"
    )


@wt(
    parsers.parse(
        'user of {browser_id} sees that size distribution for {provider} is "{size}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def check_data_distribution_size_for_provider(
    selenium, browser_id, provider, size, modals, hosts
):
    driver = selenium[browser_id]
    provider = hosts[provider]["name"]
    data_distribution = modals(driver).details_modal.data_distribution
    size_label = data_distribution.providers[provider].size_label
    assert (
        size_label == size
    ), f"Data distribution at {size_label} instead of {size} for provider {provider}!"


@wt(
    parsers.parse(
        'user of {browser_id} clicks "Show statistics per provider" button'
        " on Size stats modal"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def expand_size_statistics_for_providers(selenium, browser_id, modals):
    driver = selenium[browser_id]
    modals(driver).details_modal.size_statistics.expand_stats_button()


@wt(
    parsers.re(
        "user of (?P<browser_id>.*?) sees that "
        "(?P<elem_type>physical_size|logical_size) for "
        '(?P<provider>.*?) is "(?P<expected>.*?)"'
    )
)
@repeat_failed(interval=1, timeout=40, exceptions=AssertionError)
def check_size_stats_for_provider(
    selenium, hosts, modals, browser_id, elem_type, provider, expected
):
    driver = selenium[browser_id]
    provider_name = hosts[provider]["name"]
    size = getattr(
        modals(driver).details_modal.size_statistics.dir_stats_row_per_provider[
            provider_name
        ],
        transform(elem_type),
    )

    assert (
        size == expected
    ), f"{elem_type} is {size} instead of {expected} for provider {provider_name}!"


@wt(
    parsers.parse(
        'user of {browser_id} sees that error message for {provider} is "{message}"'
    )
)
@repeat_failed(WAIT_FRONTEND)
def check_error_cell_for_provider(
    selenium, hosts, modals, browser_id, provider, message
):
    driver = selenium[browser_id]
    provider_name = hosts[provider]["name"]
    error_cell = (
        modals(driver)
        .details_modal.size_statistics.dir_stats_row_per_provider[provider_name]
        .error_cell
    )
    assert (
        message == error_cell
    ), f"Error message should be '{message}' for provider {provider_name}!"


@wt(parsers.parse('user of {browser_id} sees that {provider} content is "{content}"'))
@repeat_failed(WAIT_FRONTEND)
def check_content_for_provider(selenium, hosts, modals, browser_id, provider, content):
    driver = selenium[browser_id]
    provider_name = hosts[provider]["name"]
    provider_content = (
        modals(driver)
        .details_modal.size_statistics.dir_stats_row_per_provider[provider_name]
        .content
    )
    assert (
        provider_content == content
    ), f"Provider {provider} content is {provider_content} instead of {content}!"


@repeat_failed(interval=1, timeout=40, exceptions=AssertionError)
def check_size_statistic_in_dir_details(
    selenium, modals, browser_id, elem_type, expected
):
    driver = selenium[browser_id]
    size = getattr(modals(driver).details_modal.size_statistics, transform(elem_type))

    assert size == expected, f"{elem_type} is {size} instead of {expected}!"
