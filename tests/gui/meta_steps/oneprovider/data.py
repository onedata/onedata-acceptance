"""Meta steps for operations in data tab in Oneprovider"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

import time

from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from tests.gui.meta_steps.oneprovider.common import (
    navigate_to_tab_in_op_using_gui,
)
from tests.gui.meta_steps.oneprovider.files_tree import (
    check_file_structure_in_browser,
)
from tests.gui.steps.common.miscellaneous import (
    click_option_in_popup_labeled_menu,
)
from tests.gui.steps.common.url import refresh_site
from tests.gui.steps.modals.details_modal import (
    click_on_navigation_tab_in_modal,
)
from tests.gui.steps.modals.modal import (
    assert_error_modal_with_text_appeared,
    close_modal,
    write_name_into_text_field_in_modal,
    wt_wait_for_modal_to_appear,
)
from tests.gui.steps.oneprovider.browser import *
from tests.gui.steps.oneprovider.data_tab import *
from tests.gui.steps.oneprovider.file_browser import *
from tests.gui.steps.oneprovider.metadata import *
from tests.gui.steps.onezone.spaces import (
    _click_on_option_in_the_sidebar,
    _click_on_option_of_space_on_left_sidebar_menu,
    click_element_on_lists_on_left_sidebar_menu,
)
from tests.utils.entities_setup.spaces import init_storage


def _click_menu_for_elem_somewhere_in_file_browser(
    selenium, browser_id, path, space, tmp_memory, oz_page, op_container
):
    item_name, _ = get_item_name_and_containing_dir_path(path)

    try:
        go_to_path_without_last_elem(
            selenium, browser_id, tmp_memory, path, op_container
        )
        browser = tmp_memory[browser_id]["file_browser"]
        browser.click_on_background()
        click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory)
    except (KeyError, RuntimeError, StaleElementReferenceException):
        go_to_filebrowser(
            selenium, browser_id, oz_page, op_container, tmp_memory, space
        )
        # TODO VFS-12315 remove sleep in acc tests
        time.sleep(0.5)
        go_to_path_without_last_elem(
            selenium, browser_id, tmp_memory, path, op_container
        )
        click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory)


@wt(
    parsers.re(
        r"user of (?P<browser_id>\w+) (?P<res>.*) to rename "
        '"(?P<path>.*)" to "(?P<new_path>.*)" in "(?P<space>.*)"'
    )
)
def rename_item(
    selenium,
    browser_id,
    path,
    new_path,
    tmp_memory,
    res,
    space,
    modals,
    oz_page,
    op_container,
    popups,
):
    option = "Rename"
    modal_header = "Rename"
    modal_name = "Rename modal"
    confirmation_option = "button"
    text = "Renaming the file failed"
    new_name = new_path.split("/")[-1]

    open_modal_for_file_browser_item(
        selenium,
        browser_id,
        popups,
        modal_header,
        path,
        tmp_memory,
        option,
        space,
        oz_page,
        op_container,
    )
    write_name_into_text_field_in_modal(
        selenium, browser_id, new_name, modal_name, modals
    )
    confirm_rename_directory(selenium, browser_id, confirmation_option, modals)
    if res == "fails":
        assert_error_modal_with_text_appeared(selenium, browser_id, text)
    else:
        assert_items_presence_in_browser(
            selenium, browser_id, new_name, tmp_memory
        )


@wt(
    parsers.re(
        r"user of (?P<browser_id>\w+) (?P<res>.*) to remove "
        '"(?P<path>.*)" in "(?P<space>.*)"'
    )
)
def remove_item_in_op_gui(
    selenium,
    browser_id,
    path,
    tmp_memory,
    op_container,
    res,
    space,
    modals,
    oz_page,
    popups,
):
    option = "Delete"
    button = "Yes"
    modal = "Delete modal"
    modal_header = "Delete"
    text = "Deleting file(s) failed"

    open_modal_for_file_browser_item(
        selenium,
        browser_id,
        popups,
        modal_header,
        path,
        tmp_memory,
        option,
        space,
        oz_page,
        op_container,
    )
    click_modal_button(selenium, browser_id, button, modal, modals)

    if res == "fails":
        assert_error_modal_with_text_appeared(selenium, browser_id, text)
    else:
        assert_items_absence_in_browser(selenium, browser_id, path, tmp_memory)


def remove_dir_and_parents_in_op_gui(
    selenium,
    browser_id,
    path,
    tmp_memory,
    op_container,
    res,
    space,
    modals,
    oz_page,
    popups,
):
    item_name = _select_item(
        selenium, browser_id, tmp_memory, path, op_container
    )
    remove_item_in_op_gui(
        selenium,
        browser_id,
        item_name,
        tmp_memory,
        op_container,
        res,
        space,
        modals,
        oz_page,
        popups,
    )


@wt(
    parsers.re(
        r"using web gui, (?P<browser_id>\w+) (?P<res>.*) to see item "
        'named "(?P<subfiles>.*)" in "(?P<path>.*)" in space'
        '"(?P<space>.*)" in oneprovider-1'
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>\w+) (?P<res>.*) to see "
        '(?P<subfiles>.*) in "(?P<path>.*)" in "(?P<space>.*)"'
    )
)
def see_items_in_op_gui(
    selenium,
    browser_id,
    path,
    subfiles,
    tmp_memory,
    op_container,
    res,
    space,
    oz_page,
):
    selenium[browser_id].refresh()

    try:
        option_in_menu = "Data"
        _click_on_option_in_the_sidebar(
            selenium, browser_id, option_in_menu, oz_page, force=False
        )
        option = "Files"
        _click_on_option_of_space_on_left_sidebar_menu(
            selenium, browser_id, space, option, oz_page, force=False
        )
        assert_browser_in_tab_in_op(
            selenium, browser_id, op_container, tmp_memory
        )
    except NoSuchElementException:
        go_to_filebrowser(
            selenium, browser_id, oz_page, op_container, tmp_memory, space
        )

    if path:
        for item in path.split("/"):
            click_and_press_enter_on_item_in_browser(
                selenium, browser_id, item, tmp_memory, op_container
            )

    if res == "fails":
        assert_items_absence_in_browser(
            selenium, browser_id, subfiles, tmp_memory
        )
    else:
        assert_items_presence_in_browser(
            selenium, browser_id, subfiles, tmp_memory
        )


@wt(
    parsers.re(
        r"user of (?P<browser_id>\w+) (?P<res>.*) to create "
        r'(?P<item_type>directory) "(?P<name>[\w._-]+)" '
        '(in "(?P<path>.*)" )?in "(?P<space>.*)"'
    )
)
def create_item_in_op_gui(
    selenium,
    browser_id,
    path,
    item_type,
    name,
    tmp_memory,
    op_container,
    res,
    space,
    modals,
    oz_page,
):
    # change None to empty string if path not given
    path = path.lstrip("/") if path else ""
    button = f"New {item_type}"
    modal_header = f"Create new {item_type}:"
    modal_name = "Create dir"
    text = "Creating directory failed"
    option = "enter"

    def _open_menu_for_item_in_file_browser():
        if path:
            go_to_path(selenium, browser_id, tmp_memory, path, op_container)
        click_button_from_file_browser_menu_bar(browser_id, button, tmp_memory)

    try:
        _open_menu_for_item_in_file_browser()
    except (RuntimeError, KeyError) as e:
        go_to_filebrowser(
            selenium, browser_id, oz_page, op_container, tmp_memory, space
        )
        _open_menu_for_item_in_file_browser()

    wt_wait_for_modal_to_appear(selenium, browser_id, modal_header, tmp_memory)
    write_name_into_text_field_in_modal(
        selenium, browser_id, name, modal_name, modals
    )
    confirm_create_new_directory(selenium, browser_id, option, modals)
    if res == "fails":
        assert_error_modal_with_text_appeared(selenium, browser_id, text)
    else:
        assert_items_presence_in_browser(selenium, browser_id, name, tmp_memory)


@wt(
    parsers.parse(
        'user of {browser_id} creates dir "{dir_name}" in current dir'
    )
)
def create_dir_in_current_dir(
    selenium, browser_id, tmp_memory, modals, dir_name
):
    button = "New directory"
    modal_header = "Create new directory:"
    modal_name = "Create dir"
    option = "enter"

    click_button_from_file_browser_menu_bar(browser_id, button, tmp_memory)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_header, tmp_memory)
    write_name_into_text_field_in_modal(
        selenium, browser_id, dir_name, modal_name, modals
    )
    confirm_create_new_directory(selenium, browser_id, option, modals)
    # clicking on the background of browser in order to deselect
    # already created directory
    browser = tmp_memory[browser_id]["file_browser"]
    browser.click_on_background()


@wt(
    parsers.re(
        r"user of (?P<browser_id>\w+) sees that each file in "
        '"(?P<directory>.*)" directory has following '
        r"metadata:\n(?P<config>(.|\s)*)"
    )
)
def check_metadata_for_file_in_directory(
    selenium, browser_id, directory, config, tmp_memory, op_container, modals
):
    which_browser = "file_browser"
    metadata = yaml.load(config, yaml.Loader)

    click_and_press_enter_on_item_in_browser(
        selenium, browser_id, directory, tmp_memory, op_container, which_browser
    )
    assert_browser_in_tab_in_op(
        selenium, browser_id, op_container, tmp_memory, which_browser
    )
    browser = tmp_memory[browser_id][which_browser]
    for item in browser.data:
        item.click_on_status_tag("Metadata")
        time.sleep(1)
        modal = modals(selenium[browser_id]).details_modal
        entries = [entry.key for entry in modal.metadata.basic.entries]
        err_msg = (
            f"Number of expected metadata entries ({len(metadata)}) does"
            " not equal number of actual metadata entries "
            f"({len(entries)}) for {item.name} in {directory}"
        )
        assert len(entries) == len(metadata), err_msg
        for expected in metadata:
            err_msg2 = (
                f"{expected} metadata key is not in metadata for "
                f"{item.name} in {directory}"
            )
            assert expected in entries, err_msg2
        modal.x()


def go_to_and_assert_browser(
    selenium,
    browser_id,
    oz_page,
    space_name,
    option_in_space,
    op_container,
    tmp_memory,
    item_browser="file browser",
):
    option = "Data"
    element = "spaces"
    _click_on_option_in_the_sidebar(
        selenium, browser_id, option, oz_page, force=False
    )
    click_element_on_lists_on_left_sidebar_menu(
        selenium, browser_id, element, space_name, oz_page
    )
    _click_on_option_of_space_on_left_sidebar_menu(
        selenium, browser_id, space_name, option_in_space, oz_page, force=False
    )
    assert_browser_in_tab_in_op(
        selenium,
        browser_id,
        op_container,
        tmp_memory,
        item_browser=item_browser,
    )


def assert_space_content_in_op_gui(
    config,
    selenium,
    user,
    op_container,
    tmp_memory,
    tmpdir,
    space_name,
    oz_page,
    which_browser="file browser",
):
    try:
        assert_browser_in_tab_in_op(
            selenium, user, op_container, tmp_memory, item_browser=which_browser
        )
    except (KeyError, NoSuchElementException):
        option_in_space = (
            "Files" if which_browser == "file browser" else "Datasets, Archives"
        )
        go_to_and_assert_browser(
            selenium,
            user,
            oz_page,
            space_name,
            option_in_space,
            op_container,
            tmp_memory,
            item_browser=which_browser,
        )

    check_file_structure_in_browser(
        user,
        config,
        selenium,
        tmp_memory,
        op_container,
        tmpdir,
        which_browser=which_browser,
    )


def see_num_of_items_in_path_in_op_gui(
    selenium,
    user,
    tmp_memory,
    op_container,
    path,
    space,
    num,
    oz_page,
    provider,
    hosts,
    popups,
):
    tab_name = "data"

    try:
        assert_browser_in_tab_in_op(selenium, user, op_container, tmp_memory)
    except KeyError:
        navigate_to_tab_in_op_using_gui(
            selenium, user, oz_page, provider, tab_name, hosts, popups
        )
        _select_item(selenium, user, tmp_memory, path, op_container)
        refresh_site(selenium, user)
        assert_browser_in_tab_in_op(selenium, user, op_container, tmp_memory)
    assert_num_of_files_are_displayed_in_browser(user, num, tmp_memory)


def assert_file_content_in_op_gui(
    text,
    path,
    space,
    selenium,
    user,
    users,
    provider,
    hosts,
    oz_page,
    op_container,
    tmp_memory,
    tmpdir,
    modals,
):
    cwd = "space root"
    try:
        assert_browser_in_tab_in_op(selenium, user, op_container, tmp_memory)
        go_to_path_without_last_elem(
            selenium, user, tmp_memory, path, op_container
        )
    except (KeyError, NoSuchElementException):
        go_to_filebrowser(
            selenium, user, oz_page, op_container, tmp_memory, space
        )
        go_to_path_without_last_elem(
            selenium, user, tmp_memory, path, op_container
        )
    item_name = _select_item(selenium, user, tmp_memory, path, op_container)
    click_and_press_enter_on_item_in_browser(
        selenium, user, item_name, tmp_memory, op_container
    )
    has_downloaded_file_content(user, item_name, text, tmpdir)
    change_cwd_using_breadcrumbs_in_data_tab_in_op(
        selenium, user, cwd, op_container
    )


@given(
    parsers.re(
        r"directory structure created by (?P<user>\w+) "
        r'in "(?P<space>.*)" space on (?P<host>.*) as follows:\n'
        r"(?P<config>(.|\s)*)"
    )
)
def g_create_directory_structure(user, config, space, host, users, hosts):
    owner = users[user]
    items = yaml.load(config, yaml.Loader)
    provider_hostname = hosts[host]["hostname"]

    init_storage(owner, space, hosts, provider_hostname, users, items)


def create_directory_structure_in_op_gui(
    selenium,
    user,
    op_container,
    config,
    space,
    tmp_memory,
    modals,
    oz_page,
    popups,
):
    items = yaml.load(config, yaml.Loader)
    cwd = ""

    _create_content(
        selenium,
        user,
        items,
        cwd,
        space,
        tmp_memory,
        op_container,
        modals,
        oz_page,
        popups,
    )


def _create_item(
    selenium,
    browser_id,
    name,
    content,
    cwd,
    space,
    tmp_memory,
    op_container,
    modals,
    oz_page,
    popups,
):
    path = "space root"
    item_type = "directory" if name.startswith("dir") else "file"
    if item_type == "directory":
        create_item_in_op_gui(
            selenium,
            browser_id,
            cwd,
            item_type,
            name,
            tmp_memory,
            op_container,
            "succeeds",
            space,
            modals,
            oz_page,
        )
    else:
        upload_file_to_op_gui(
            cwd,
            selenium,
            browser_id,
            space,
            "succeeds",
            name,
            op_container,
            tmp_memory,
            oz_page,
            popups,
        )
    change_cwd_using_breadcrumbs_in_data_tab_in_op(
        selenium, browser_id, path, op_container
    )
    if not content:
        return
    cwd += "/" + name
    _create_content(
        selenium,
        browser_id,
        content,
        cwd,
        space,
        tmp_memory,
        op_container,
        modals,
        oz_page,
        popups,
    )


def _create_content(
    selenium,
    browser_id,
    content,
    cwd,
    space,
    tmp_memory,
    op_container,
    modals,
    oz_page,
    popups,
):
    for item in content:
        try:
            [(name, content)] = item.items()
        except AttributeError:
            name = item
            content = None
        _create_item(
            selenium,
            browser_id,
            name,
            content,
            cwd,
            space,
            tmp_memory,
            op_container,
            modals,
            oz_page,
            popups,
        )


@wt(
    parsers.re(
        'user of (?P<browser_id>.*) uploads "(?P<path>.*)" to the '
        'root directory of "(?P<space>.*)"'
    )
)
@wt(
    parsers.re(
        'user of (?P<browser_id>.*) uploads "(?P<path>.*)" to the '
        'root directory of "(?P<space>.*)" using (?P<provider>.*) GUI'
    )
)
def successfully_upload_file_to_op_gui(
    path, selenium, browser_id, space, op_container, tmp_memory, oz_page, popups
):
    go_to_filebrowser(
        selenium, browser_id, oz_page, op_container, tmp_memory, space
    )
    upload_file_to_cwd_in_file_browser(
        selenium, browser_id, path, op_container, popups
    )
    assert_items_presence_in_browser(selenium, browser_id, path, tmp_memory)


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) (?P<res>.*) to upload "
        '"(?P<filename>.*)" to "(?P<path>.*)" in "(?P<space>.*)"'
    )
)
def upload_file_to_op_gui(
    path,
    selenium,
    browser_id,
    space,
    res,
    filename,
    op_container,
    tmp_memory,
    oz_page,
    popups,
):
    try:
        assert_browser_in_tab_in_op(
            selenium, browser_id, op_container, tmp_memory
        )
        go_to_path(selenium, browser_id, tmp_memory, path, op_container)
    except (KeyError, NoSuchElementException):
        go_to_filebrowser(
            selenium, browser_id, oz_page, op_container, tmp_memory, space
        )
        go_to_path(selenium, browser_id, tmp_memory, path, op_container)
    if res == "succeeds":
        upload_file_to_cwd_in_file_browser(
            selenium, browser_id, filename, op_container, popups
        )
        assert_items_presence_in_browser(
            selenium, browser_id, filename, tmp_memory
        )
    else:
        upload_file_to_cwd_in_file_browser_no_waiting(
            selenium, browser_id, filename, op_container
        )
        check_error_in_upload_presenter(selenium, browser_id, popups)


@repeat_failed(timeout=WAIT_BACKEND)
def assert_mtime_not_earlier_than_op_gui(
    path, time, browser_id, tmp_memory, selenium, op_container
):
    assert_nonempty_file_browser_in_files_tab_in_op(
        selenium,
        browser_id,
        op_container,
        tmp_memory,
        item_browser="file browser",
    )
    item_name = _select_item(
        selenium, browser_id, tmp_memory, path, op_container
    )
    assert_item_in_file_browser_is_of_mdate(
        browser_id, item_name, time, tmp_memory
    )


def _select_item(selenium, browser_id, tmp_memory, path, op_container):
    item_name, path = get_item_name_and_containing_dir_path(path)
    go_to_path_without_last_elem(
        selenium, browser_id, tmp_memory, path, op_container
    )
    select_files_from_file_list_using_ctrl(browser_id, item_name, tmp_memory)
    return item_name


@wt(parsers.parse('user of {browser_id} goes to "{path}" in {which_browser}'))
def go_to_path_(
    selenium, browser_id, tmp_memory, path, op_container, which_browser
):
    go_to_path(
        selenium,
        browser_id,
        tmp_memory,
        path,
        op_container,
        which_browser=which_browser,
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def go_to_path(
    selenium,
    browser_id,
    tmp_memory,
    path,
    op_container,
    which_browser="file browser",
):
    if "/" in path:
        item_name, path_list = get_item_name_and_containing_dir_path(path)
        path_list.append(item_name)
    else:
        path_list = [path]
    for directory in path_list:
        # go back
        if directory == "..":
            breadcrumbs = getattr(
                op_container(selenium[browser_id]), transform(which_browser)
            ).breadcrumbs
            breadcrumbs = breadcrumbs._breadcrumbs
            breadcrumbs[len(breadcrumbs) - 2].click()
        elif directory != "":
            click_and_press_enter_on_item_in_browser(
                selenium,
                browser_id,
                directory,
                tmp_memory,
                op_container,
                which_browser,
            )


def go_to_path_without_last_elem(
    selenium,
    browser_id,
    tmp_memory,
    path,
    op_container,
    item_browser="file browser",
):
    if "/" in path:
        _, path_list = get_item_name_and_containing_dir_path(path)

        for directory in path_list:
            click_and_press_enter_on_item_in_browser(
                selenium,
                browser_id,
                directory,
                tmp_memory,
                op_container,
                item_browser,
            )


def get_item_name_and_containing_dir_path(path):
    path_list = path.strip('"').split("/")
    item_name = path_list.pop()
    return item_name, path_list


@wt(
    parsers.parse('user of {browser_id} opens file browser for "{space}" space')
)
def go_to_filebrowser(
    selenium, browser_id, oz_page, op_container, tmp_memory, space
):
    option_in_menu = "Data"
    option_in_space_submenu = "Files"

    _click_on_option_in_the_sidebar(
        selenium, browser_id, option_in_menu, oz_page, force=False
    )
    _click_on_option_of_space_on_left_sidebar_menu(
        selenium,
        browser_id,
        space,
        option_in_space_submenu,
        oz_page,
        force=False,
    )
    assert_browser_in_tab_in_op(selenium, browser_id, op_container, tmp_memory)


def open_modal_for_file_browser_item(
    selenium,
    browser_id,
    popups,
    modal_name,
    path,
    tmp_memory,
    option,
    space,
    oz_page,
    op_container,
):
    _click_menu_for_elem_somewhere_in_file_browser(
        selenium, browser_id, path, space, tmp_memory, oz_page, op_container
    )
    click_option_in_data_row_menu_in_browser(
        selenium, browser_id, option, popups
    )
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)


def check_file_owner(
    selenium, browser_id, owner, file_name, tmp_memory, modals, popups
):
    option = "Information"
    modal_name = "File details"

    click_menu_for_elem_in_browser(browser_id, file_name, tmp_memory)
    click_option_in_data_row_menu_in_browser(
        selenium, browser_id, option, popups
    )
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    check_file_owner_in_file_details_modal(selenium, browser_id, modals, owner)
    close_modal(selenium, browser_id, modal_name, modals)


@wt(
    parsers.parse(
        'user of {browser_id} creates hardlink of "{file_name}" '
        'file in space "{space}" in file browser'
    )
)
def create_hardlinks_of_file(
    selenium,
    browser_id,
    file_name,
    space,
    tmp_memory,
    oz_page,
    op_container,
    popups,
):
    option = "Create hard link"
    button = "Place hard link"

    _create_link_in_file_browser(
        selenium,
        browser_id,
        file_name,
        space,
        tmp_memory,
        oz_page,
        op_container,
        popups,
        option,
        button,
    )


@wt(
    parsers.parse(
        'user of {browser_id} creates symlink of "{file_name}" '
        'file in space "{space}" in file browser'
    )
)
def create_symlinks_of_file(
    selenium,
    browser_id,
    file_name,
    space,
    tmp_memory,
    oz_page,
    op_container,
    popups,
):
    option = "Create symbolic link"
    button = "place symbolic link"

    _create_link_in_file_browser(
        selenium,
        browser_id,
        file_name,
        space,
        tmp_memory,
        oz_page,
        op_container,
        popups,
        option,
        button,
    )


@wt(
    parsers.parse(
        'user of {browser_id} creates symbolic link of "{file_name}" '
        'placed in "{path}" directory on {which_browser} in "{space}"'
    )
)
def create_symlinks_of_file_with_path(
    selenium,
    browser_id,
    file_name,
    space,
    tmp_memory,
    oz_page,
    op_container,
    popups,
    path,
):
    option = "Create symbolic link"
    button = "Place symbolic link"

    _create_link_in_file_browser(
        selenium,
        browser_id,
        file_name,
        space,
        tmp_memory,
        oz_page,
        op_container,
        popups,
        option,
        button,
        path=path,
        go_to_file_browser=False,
    )


@wt(
    parsers.parse(
        'user of {browser_id} creates hard link of "{file_name}" '
        'placed in "{path}" directory on {which_browser} in "{space}"'
    )
)
def create_hardlinks_of_file_with_path(
    selenium,
    browser_id,
    file_name,
    space,
    tmp_memory,
    oz_page,
    op_container,
    popups,
    path,
):
    option = "Create hard link"
    button = "Place hard link"

    _create_link_in_file_browser(
        selenium,
        browser_id,
        file_name,
        space,
        tmp_memory,
        oz_page,
        op_container,
        popups,
        option,
        button,
        path=path,
        go_to_file_browser=False,
    )


def _create_link_in_file_browser(
    selenium,
    browser_id,
    file_name,
    space,
    tmp_memory,
    oz_page,
    op_container,
    popups,
    option,
    button,
    path=None,
    go_to_file_browser=True,
):
    if go_to_file_browser:
        go_to_filebrowser(
            selenium, browser_id, oz_page, op_container, tmp_memory, space
        )
    _click_menu_for_elem_somewhere_in_file_browser(
        selenium,
        browser_id,
        file_name,
        space,
        tmp_memory,
        oz_page,
        op_container,
    )
    # TODO VFS-12315 remove sleep in acc tests
    time.sleep(0.5)
    click_option_in_data_row_menu_in_browser(
        selenium, browser_id, option, popups
    )
    if path:
        go_to_path(selenium, browser_id, tmp_memory, path, op_container)
    click_file_browser_button(browser_id, button, tmp_memory)


@wt(
    parsers.re(
        r'using web GUI, (?P<user>\w+) copies "(?P<name>.*)" ID to'
        r' clipboard from "(?P<modal>.*)" modal in space '
        r'"(?P<space>\w+)" in (?P<host>.*)'
    )
)
def copy_object_id_to_tmp_memory(
    tmp_memory,
    selenium,
    user,
    name,
    space,
    oz_page,
    op_container,
    modals,
    modal,
    popups,
):
    option = "Information"
    button = "File ID"
    if modal == "Directory Details":
        modal = "File details"
    _click_menu_for_elem_somewhere_in_file_browser(
        selenium, user, name, space, tmp_memory, oz_page, op_container
    )
    click_option_in_data_row_menu_in_browser(selenium, user, option, popups)
    click_modal_button(selenium, user, button, modal, modals)
    close_modal(selenium, user, modal, modals)


# TODO: VFS-8740 Function just for the needs of scenario "User downloads
#  files from shared directory on single share view in full Onezone
#  interface" working properly
@wt(
    parsers.parse(
        'user of {browser_id} downloads item "{item_name}" by '
        "clicking and pressing enter and then sees that "
        'content of downloaded file is equal to: "{content}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_and_press_enter_with_content_check(
    browser_id,
    item_name,
    content,
    tmpdir,
    tmp_memory,
    which_browser="file browser",
):
    which_browser = transform(which_browser)
    browser = tmp_memory[browser_id][which_browser]
    browser.data[item_name].click_and_enter()

    has_downloaded_file_content(browser_id, item_name, content, tmpdir)


def get_file_id_from_details_modal(
    selenium,
    browser_id,
    oz_page,
    space_name,
    op_container,
    tmp_memory,
    file_name,
    popups,
    modals,
    clipboard,
    displays,
):
    option_in_space = "Files"
    option_in_menu = "Information"

    _click_on_option_of_space_on_left_sidebar_menu(
        selenium, browser_id, space_name, option_in_space, oz_page, force=False
    )
    assert_browser_in_tab_in_op(selenium, browser_id, op_container, tmp_memory)
    if "/" in file_name:
        go_to_path_without_last_elem(
            selenium, browser_id, tmp_memory, file_name, op_container
        )
        file_name = file_name.split("/")[-1]

    modal_name = "Directory details" if "dir" in file_name else "File details"
    click_menu_for_elem_in_browser(browser_id, file_name, tmp_memory)
    click_option_in_data_row_menu_in_browser(
        selenium, browser_id, option_in_menu, popups
    )
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    click_modal_button(selenium, browser_id, "file_id", modal_name, modals)
    return clipboard.paste(display=displays[browser_id])


@wt(
    parsers.parse(
        "user of {browser_id} opens size statistics per provider view"
        ' using breadcrumbs menu in "{space}"'
    )
)
def go_to_size_statistics_per_provider_by_breadcrumbs(
    selenium, modals, popups, op_container, browser_id, tmp_memory, space
):
    browser = "file browser"
    option = "Information"
    tab_name = "Size stats"
    modal = "Directory Details"
    path = space
    assert_browser_in_tab_in_op(
        selenium, browser_id, op_container, tmp_memory, item_browser=browser
    )
    is_displayed_breadcrumbs_in_data_tab_in_op_correct(
        selenium, browser_id, path, op_container, which_browser=browser
    )
    click_on_breadcrumbs_menu(selenium, browser_id, op_container, browser)
    click_option_in_popup_labeled_menu(selenium, browser_id, option, popups)
    click_on_navigation_tab_in_modal(
        selenium, browser_id, tab_name, modals, modal
    )
    expand_size_statistics_for_providers(selenium, browser_id, modals)


def delete_first_n_files(
    browser_id, num_files_to_delete, tmp_memory, selenium, popups, modals
):
    option_to_select = "Delete"
    modal = "Delete modal"
    modal_option = "Yes"
    select_first_n_files(browser_id, num_files_to_delete, tmp_memory)
    if num_files_to_delete > 1:
        choose_option_from_selection_menu(
            browser_id, selenium, option_to_select, popups, tmp_memory
        )
    else:
        click_menu_for_elem_in_browser(browser_id, 0, tmp_memory)
        click_option_in_data_row_menu_in_browser(
            selenium, browser_id, option_to_select, popups
        )
    click_modal_button(selenium, browser_id, modal_option, modal, modals)


@wt(
    parsers.parse(
        "user of {browser_id} deletes first {num_files_to_delete} "
        "files from current directory"
    )
)
def delete_first_n_files_with_fixed_step(
    browser_id, num_files_to_delete: int, tmp_memory, selenium, popups, modals
):
    deleted_files = 0
    fixed_step = 5
    while deleted_files + fixed_step <= num_files_to_delete:
        delete_first_n_files(
            browser_id, fixed_step, tmp_memory, selenium, popups, modals
        )
        deleted_files += fixed_step
    else:
        num_remaining_files_to_delete = num_files_to_delete - deleted_files
        if num_remaining_files_to_delete > 0:
            delete_first_n_files(
                browser_id,
                num_remaining_files_to_delete,
                tmp_memory,
                selenium,
                popups,
                modals,
            )
            deleted_files += num_remaining_files_to_delete
    err_msg = f"deleted {deleted_files} files instead of {num_files_to_delete}"
    assert deleted_files == num_files_to_delete, err_msg
