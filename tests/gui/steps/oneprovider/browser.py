"""Steps used for common in different browsers operations in Oneprovider GUI"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import re
import time
from datetime import datetime

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.oneprovider.common import wait_for_item_to_appear
from tests.gui.utils.generic import WhichBrowser, parse_seq, transform
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_BACKEND)
def click_and_press_enter_on_item_in_browser(
    selenium,
    browser_id,
    item_name,
    tmp_memory,
    op_container,
    which_browser="file browser",
):
    which_browser = transform(which_browser)
    browser = tmp_memory[browser_id][which_browser]
    driver = selenium[browser_id]

    # clicking on the background of browser to ensure correct
    # working of click_and enter
    browser.click_on_background()

    # checking if file is located in file browser
    start = time.time()
    while item_name not in browser.data:
        time.sleep(1)
        if time.time() > start + WAIT_BACKEND:
            raise RuntimeError("waited too long")

    click_and_enter_with_check(driver, op_container, browser, which_browser, item_name)


@wt(
    parsers.parse(
        "user of {browser_id} clicks and presses enter on item named"
        ' "{item_name}" in {which_browser}'
    )
)
def wt_click_and_press_enter_on_item_in_browser(
    selenium, browser_id, item_name, tmp_memory, op_container, which_browser
):
    click_and_press_enter_on_item_in_browser(
        selenium,
        browser_id,
        item_name,
        tmp_memory,
        op_container,
        which_browser=which_browser,
    )


@repeat_failed(timeout=WAIT_BACKEND)
def click_and_enter_with_check(driver, op_container, browser, which_browser, item_name):
    # this function does not check correctly if parent and children directory
    # have the same name
    browser.data[item_name].click_and_enter()
    if item_name.startswith("dir"):
        for _ in range(5):
            breadcrumbs = check_if_breadcrumbs_on_share_page(
                driver, op_container, which_browser
            )
            if breadcrumbs.split("/")[-1] == item_name:
                return
            time.sleep(1)
        raise RuntimeError("Click and enter has not entered the directory")


@repeat_failed(timeout=WAIT_BACKEND)
def check_if_breadcrumbs_on_share_page(
    driver, op_container, which_browser="file browser"
):
    try:
        breadcrumbs = op_container(driver).shares_page.breadcrumbs.pwd()
    except RuntimeError:
        breadcrumbs = getattr(
            op_container(driver), transform(which_browser)
        ).breadcrumbs.pwd()

    return breadcrumbs


@wt(
    parsers.parse(
        "user of {browser_id} sees that current working directory "
        'displayed in breadcrumbs on {which_browser} is "{path}"'
    )
)
def wt_is_displayed_breadcrumbs_in_data_tab_in_op_correct(
    selenium, browser_id, path, op_container, which_browser
):
    is_displayed_breadcrumbs_in_data_tab_in_op_correct(
        selenium, browser_id, path, op_container, which_browser=which_browser
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def is_displayed_breadcrumbs_in_data_tab_in_op_correct(
    selenium, browser_id, path, op_container, which_browser="file browser"
):
    driver = selenium[browser_id]
    breadcrumbs = getattr(
        op_container(driver), transform(which_browser)
    ).breadcrumbs.pwd()

    if which_browser == "archive file browser":
        breadcrumbs = re.split("/", breadcrumbs, 2)[-1]
        path = re.split("/", path, 2)[-1]

    assert path == breadcrumbs, f"expected breadcrumbs {path}; displayed: {breadcrumbs}"


@wt(
    parsers.parse(
        "user of {browser_id} clicks on menu on breadcrumbs in {which_browser}"
    )
)
def wt_click_on_breadcrumbs_menu(selenium, browser_id, op_container, which_browser):
    click_on_breadcrumbs_menu(
        selenium, browser_id, op_container, which_browser=which_browser
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_breadcrumbs_menu(
    selenium, browser_id, op_container, which_browser="file browser"
):
    driver = selenium[browser_id]
    breadcrumbs = getattr(op_container(driver), transform(which_browser)).breadcrumbs
    breadcrumbs.menu_button()


@repeat_failed(timeout=WAIT_FRONTEND)
def _get_items_list_from_browser(
    selenium, browser_id, tmp_memory, which_browser="file browser"
):

    browser = tmp_memory[browser_id][transform(which_browser)]
    data = {f.name for f in browser.data if f.name}
    driver = selenium[browser_id]

    if len(data) != len(browser.data):

        def condition(data_):
            return len(data_) != len(browser.data)

        data = _gather_data_from_browser(driver, browser, condition)
        browser.scroll_to_number_file(driver, 2, browser)

    return data


def _gather_data_from_browser(driver, browser, condition):
    data = {f.name: f for f in browser.data if f.name}
    while condition(data):
        browser.scroll_to_number_file(driver, len(data), browser)
        partial_data = {f.name: f for f in browser.data if f.name}
        data.update(partial_data)

    return data


@wt(
    parsers.parse(
        "user of {browser_id} sees item(s) named {item_list} in "
        "{which_browser:WhichBrowser}",
        extra_types={"WhichBrowser": WhichBrowser},
    )
)
@wt(
    parsers.parse(
        "user of {browser_id} sees that item named {item_list} has appeared in "
        "{which_browser:WhichBrowser}",
        extra_types={"WhichBrowser": WhichBrowser},
    )
)
@wt(
    parsers.parse(
        "user of {browser_id} sees that items named {item_list} have appeared"
        " in {which_browser:WhichBrowser}",
        extra_types={"WhichBrowser": WhichBrowser},
    )
)
def wt_assert_items_presence_in_browser(
    selenium, browser_id, item_list, tmp_memory, which_browser
):
    assert_items_presence_in_browser(
        selenium,
        browser_id,
        item_list,
        tmp_memory,
        which_browser=which_browser.value,
    )


@repeat_failed(timeout=WAIT_BACKEND)
def assert_items_presence_in_browser(
    selenium, browser_id, item_list, tmp_memory, which_browser="file browser"
):
    data = _get_items_list_from_browser(selenium, browser_id, tmp_memory, which_browser)
    if not isinstance(item_list, list):
        item_list = parse_seq(item_list)
    for item_name in item_list:
        assert item_name in data, f'not found "{item_name}" in browser'


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_only_expected_items_presence_in_browser(
    selenium, browser_id, item_list, tmp_memory, which_browser="file browser"
):
    data = _get_items_list_from_browser(selenium, browser_id, tmp_memory, which_browser)

    assert len(item_list) == len(data), (
        f"there is different number of items in {which_browser}, "
        f"actual items: {data}, expected items: {item_list}"
    )

    assert_items_presence_in_browser(
        selenium, browser_id, item_list, tmp_memory, which_browser
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def check_if_item_is_dir_in_browser(
    selenium, browser_id, item_name, tmp_memory, which_browser="file browser"
):
    driver = selenium[browser_id]
    browser = tmp_memory[browser_id][transform(which_browser)]
    data = [f.name for f in browser.data if f.name]

    while item_name not in data and len(data) != len(browser.data):
        browser.scroll_to_number_file(driver, len(data), browser)
        partial_data = [f.name for f in browser.data if f.name]
        data.extend(partial_data)

    try:
        item = browser.data[item_name]
    except RuntimeError:
        browser.scroll_to_number_file(driver, data.index(item_name), browser)
        item = browser.data[item_name]

    return not item.is_file()


@wt(
    parsers.parse(
        "user of {browser_id} sees that item named {item_list} "
        "has disappeared from {which_browser}"
    )
)
@wt(
    parsers.parse(
        "user of {browser_id} sees that items named {item_list} "
        "have disappeared from {which_browser}"
    )
)
@wt(
    parsers.parse(
        "user of {browser_id} does not see any item(s) named "
        "{item_list} in {which_browser}"
    )
)
def wt_assert_items_absence_in_browser(
    selenium, browser_id, item_list, tmp_memory, which_browser
):
    assert_items_absence_in_browser(
        selenium, browser_id, item_list, tmp_memory, which_browser=which_browser
    )


@repeat_failed(timeout=WAIT_BACKEND)
def assert_items_absence_in_browser(
    selenium, browser_id, item_list, tmp_memory, which_browser="file browser"
):
    data = _get_items_list_from_browser(selenium, browser_id, tmp_memory, which_browser)
    for item_name in parse_seq(item_list):
        assert (
            item_name not in data
        ), f'found "{item_name}" in browser, while it should not'


@wt(
    parsers.re(
        r"user of (?P<browser_id>.+?) sees that there "
        r"(is 1|are (?P<num>\d+)) items? in (?P<which_browser>.*)"
    )
)
def assert_num_of_files_are_displayed_in_browser_(
    browser_id, num, tmp_memory, which_browser
):
    assert_num_of_files_are_displayed_in_browser(
        browser_id, num, tmp_memory, which_browser=which_browser
    )


@repeat_failed(timeout=WAIT_BACKEND)
def assert_num_of_files_are_displayed_in_browser(
    browser_id, num, tmp_memory, which_browser="file_browser"
):
    browser = tmp_memory[browser_id][transform(which_browser)]
    err_msg = "displayed number of files {} does not match expected {}"
    files_num = browser.data.count()
    num = 1 if num is None else int(num)
    assert files_num == num, err_msg.format(files_num, num)


@wt(
    parsers.parse(
        "user of {browser_id} sees {status_type} "
        'status tag for "{item_name}" in {which_browser}'
    )
)
def wt_assert_status_tag_for_file_in_browser(
    browser_id, status_type, item_name, tmp_memory, which_browser
):
    assert_status_tag_for_file_in_browser(
        browser_id,
        status_type,
        item_name,
        tmp_memory,
        which_browser=which_browser,
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_status_tag_for_file_in_browser(
    browser_id, status_type, item_name, tmp_memory, which_browser="file browser"
):
    browser = tmp_memory[browser_id][transform(which_browser)]
    err_msg = f"{status_type} tag for {item_name} in {which_browser} not visible"
    assert browser.data[item_name].is_tag_visible(transform(status_type)), err_msg


@wt(
    parsers.parse(
        "user of {browser_id} sees {status_type} "
        'status tag with "{text}" text for "{item_name}" '
        "in {which_browser}"
    )
)
def wt_assert_status_tag_text_for_file_in_browser(
    browser_id, status_type, text, item_name, tmp_memory, which_browser
):
    assert_status_tag_text_for_file_in_browser(
        browser_id,
        status_type,
        text,
        item_name,
        tmp_memory,
        which_browser=which_browser,
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_status_tag_text_for_file_in_browser(
    browser_id,
    status_type,
    text,
    item_name,
    tmp_memory,
    which_browser="file browser",
):
    assert_status_tag_for_file_in_browser(
        browser_id, status_type, item_name, tmp_memory, which_browser
    )
    browser = tmp_memory[browser_id][transform(which_browser)]
    actual_text = browser.data[item_name].get_tag_text(transform(status_type))
    err_msg = (
        f"{status_type} tag for {item_name} in browser has text "
        f"{actual_text} not {text}"
    )
    assert actual_text == text, err_msg


@wt(
    parsers.parse(
        "user of {browser_id} does not see {status_type} "
        'status tag for "{item_name}" in {which_browser}'
    )
)
def wt_assert_not_status_tag_for_file_in_browser(
    browser_id, status_type, item_name, tmp_memory, which_browser
):
    assert_not_status_tag_for_file_in_browser(
        browser_id,
        status_type,
        item_name,
        tmp_memory,
        which_browser=which_browser,
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_not_status_tag_for_file_in_browser(
    browser_id, status_type, item_name, tmp_memory, which_browser="file browser"
):
    browser = tmp_memory[browser_id][transform(which_browser)]
    err_msg = (
        f"{status_type} tag for {item_name} in {which_browser} visible, "
        "while should not be"
    )
    assert not browser.data[item_name].is_tag_visible(status_type), err_msg


def _choose_menu(selenium, browser_id, which_browser, popups):
    if which_browser == "archive browser":
        return popups(selenium[browser_id]).archive_row_menu
    if which_browser == "dataset browser":
        return popups(selenium[browser_id]).dataset_row_menu
    if which_browser == "automation workflows page":
        return popups(selenium[browser_id]).workflow_menu
    return popups(selenium[browser_id]).data_row_menu


@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_data_row_menu_in_browser(
    selenium, browser_id, option, popups, which_browser="file browser"
):
    menu = _choose_menu(selenium, browser_id, which_browser, popups)
    menu.choose_option(option)


@wt(
    parsers.parse(
        'user of {browser_id} clicks "{option}" option '
        "in data row menu in {which_browser}"
    )
)
def wt_click_option_in_data_row_menu_in_browser(
    selenium, browser_id, option, popups, which_browser
):
    click_option_in_data_row_menu_in_browser(
        selenium, browser_id, option, popups, which_browser=which_browser
    )


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{option}" option is '
        "{option_state} in opened item menu in {which_browser}"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_option_state_in_data_row_menu(
    selenium, browser_id, option, popups, option_state, which_browser
):
    err_msg = (
        f"{option} option is not {option_state} in opened item menu in file browser"
    )

    menu = _choose_menu(selenium, browser_id, which_browser, popups)
    menu_option = menu.return_option(option)
    assert menu_option.get_state() == option_state, err_msg


@wt(
    parsers.parse(
        "user of {browser_id} clicks on {state} view mode on {which} browser page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_state_view_mode_tab(
    browser_id, oz_page, selenium, state, which, tmp_memory
):
    driver = selenium[browser_id]
    if which == "archive file":
        which_browser = which + " browser"
        browser = tmp_memory[browser_id][transform(which_browser)]
        browser.click_on_dip_aip_view_mode(driver, transform(state))
    else:
        driver.switch_to.default_content()
        header = f"{transform(which)}_header"
        getattr(getattr(oz_page(driver)["data"], header), transform(state))()
    # if we make call to fast after changing view mode
    # we do not see items in this mode, to avoid this wait some time
    time.sleep(0.5)


@wt(
    parsers.re(
        'user of (?P<browser_id>.*) clicks on menu for "(?P<item_name>.*)" '
        "(?P<type>dataset|directory|file) in (?P<which_browser>.*)"
    )
)
def wt_click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory, which_browser):
    click_menu_for_elem_in_browser(
        browser_id, item_name, tmp_memory, which_browser=which_browser
    )


@repeat_failed(timeout=WAIT_FRONTEND)
def click_menu_for_elem_in_browser(
    browser_id, item_name, tmp_memory, which_browser="file browser"
):
    browser = tmp_memory[browser_id][transform(which_browser)]
    browser.data[item_name].menu_button()


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) clicks on (?P<tag>.*tag.*|.*icon.*) "
        'for "(?P<item_name>.*)" (?P<type>.*) in (?P<which_browser>.*)'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_tag_for_elem_in_browser(
    browser_id, item_name, tmp_memory, tag, which_browser
):
    browser = tmp_memory[browser_id][transform(which_browser)]
    getattr(browser.data[item_name], transform(tag)).click()


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) sees that item named "
        '"(?P<item_name>.*)" is of (?P<number>.*) (?P<option>size) in '
        "(?P<which_browser>archive file browser|file browser)"
    )
)
@wt(
    parsers.re(
        "user of (?P<browser_id>.*) sees that item named "
        '"(?P<item_name>.*)" has (?P<number>.*) (?P<option>replication '
        "rate) in (?P<which_browser>archive file browser|file browser)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_value_in_column_for_item(
    browser_id, item_name, number, option, which_browser, selenium, op_container
):
    driver = selenium[browser_id]
    browser = getattr(op_container(driver), transform(which_browser))
    item_elem = getattr(browser.data[item_name], transform(option))
    err_msg = (
        f"displayed {option} {item_elem} for {item_name} does not "
        f"match expected {number}"
    )
    assert number == item_elem, err_msg


@wt(
    parsers.re(
        'user of (?P<browser_id>.*) saves content of "(?P<option>.*)" '
        'column for "(?P<item_name>.*)" in '
        "(?P<which_browser>archive file browser|file browser)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def save_value_in_column_for_item(
    browser_id,
    item_name,
    option,
    which_browser,
    selenium,
    op_container,
    tmp_memory,
):
    driver = selenium[browser_id]
    browser = getattr(op_container(driver), transform(which_browser))
    value = getattr(browser.data[item_name], transform(option))
    tmp_memory["columns-content"] = {item_name: value}


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) sees that date time in "
        '"(?P<option>.*)" column for "(?P<item_name>.*)" has become '
        "more current in (?P<which_browser>archive file browser|file browser)"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def compare_value_in_column_for_item(
    browser_id,
    item_name,
    option,
    which_browser,
    selenium,
    op_container,
    tmp_memory,
):
    driver = selenium[browser_id]
    browser = getattr(op_container(driver), transform(which_browser))
    new_value = getattr(browser.data[item_name], transform(option))
    old_value = tmp_memory["columns-content"][item_name]
    new_value = datetime.strptime(new_value, "%d %b %Y %H:%M:%S")
    old_value = datetime.strptime(old_value, "%d %b %Y %H:%M:%S")
    err_msg = f"visible date time: {new_value} is not more current than {old_value}"
    assert new_value > old_value, err_msg


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) enables only (?P<columns>.*) "
        "columns? in columns configuration popover in "
        "(?P<which_browser>file browser|archive browser|"
        "dataset browser) table"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def select_columns_to_be_visible_in_browser(
    selenium, browser_id, columns, which_browser, tmp_memory, popups
):
    option_select = "select"
    option_unselect = "unselect"
    browser = tmp_memory[browser_id][transform(which_browser)]
    browser.configure_columns.click()
    columns_menu = popups(selenium[browser_id]).configure_columns_menu.columns
    wait_for_item_to_appear(
        popups(selenium[browser_id]).configure_columns_menu.web_elem
    )
    columns = list(map(lambda s: s.lower(), parse_seq(columns)))
    for column in columns_menu:
        if column.name.lower() in columns:
            getattr(columns_menu[column.name], option_select)()
        else:
            getattr(columns_menu[column.name], option_unselect)()
    # hide columns menu popup
    browser.configure_columns.click()


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) sees only (?P<columns>.*) columns "
        "in (?P<which_browser>file browser|archive browser|"
        "dataset browser)"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_visible_columns_in_browser(browser_id, tmp_memory, columns, which_browser):
    columns = parse_seq(columns)
    browser = tmp_memory[browser_id][transform(which_browser)]
    browser_columns = browser.column_headers
    browser_columns = list(map(lambda x: x.name.lower(), browser_columns))
    err_msg = (
        "there is different number of columns visible: "
        f"{len(browser_columns)} than expected: {len(columns)}, in "
        f"{which_browser}"
    )
    assert len(columns) == len(browser_columns), err_msg
    for column in columns:
        if column.lower() not in browser_columns:
            raise AssertionError(f"column {column} is not visible in {which_browser}")


@wt(
    parsers.parse(
        'user of {browser_id} does not see button "{button}" in {which_browser}'
    )
)
def assert_button_not_visible_in_browser(browser_id, tmp_memory, button, which_browser):
    browser = tmp_memory[browser_id][transform(which_browser)]
    try:
        getattr(browser, transform(button) + "_button")
        raise AssertionError(f"button {button} is visible in {which_browser} browser")
    except RuntimeError:
        pass
