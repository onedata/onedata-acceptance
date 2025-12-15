"""Meta steps for xattr columns modification"""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2025 Onedata.org"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.steps.oneprovider.common import wait_for_item_to_appear
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.bdd_utils import parsers, wt


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) (?P<res>disables|enables) (?P<columns>.*) "
        r"columns? in columns configuration popover in "
        r"(?P<which_browser>file browser|archive browser|"
        r"dataset browser) table"
    )
)
def change_visibility_for_xattr_columns(
    selenium, browser_id, res, columns, which_browser, tmp_memory, popups
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
            if res == "enables":
                getattr(columns_menu[column.name], option_select)()
            else:
                getattr(columns_menu[column.name], option_unselect)()

    # hide columns menu popup
    browser.configure_columns.click()


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) removes xattr column named "(?P<name>.*)"'
        r" in columns configuration popover in (?P<which_browser>file"
        r" browser|archive browser|dataset browser) table"
    )
)
def remove_xattr_column(selenium, browser_id, name, which_browser, tmp_memory, popups):
    driver = selenium[browser_id]
    browser = tmp_memory[browser_id][transform(which_browser)]
    browser.configure_columns.click()

    wait_for_item_to_appear(
        popups(selenium[browser_id]).configure_columns_menu.web_elem
    )

    current_xattr_column = popups(driver).configure_columns_menu.columns[name]
    current_xattr_column.hover_to_button_and_click("remove", driver)

    # hide columns menu popup
    browser.configure_columns.click()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) modifies xattr column with"
        r' "(?P<name>.*)" key by changing (?P<elem>label|key)'
        r' to "(?P<new_elem_name>.*)" in (?P<which_browser>file'
        r" browser|archive browser|dataset browser) table"
    )
)
def modify_label_for_xattr_column_in_columns_menu_in_browser(
    selenium, browser_id, which_browser, tmp_memory, popups, name, elem, new_elem_name
):

    driver = selenium[browser_id]
    browser = tmp_memory[browser_id][transform(which_browser)]

    browser.configure_columns.click()
    wait_for_item_to_appear(
        popups(selenium[browser_id]).configure_columns_menu.web_elem
    )

    current_xattr_column = popups(driver).configure_columns_menu.columns[name]

    current_xattr_column.hover_to_button_and_click("modify", driver)
    modify_xattr_column = popups(driver).configure_columns_menu.column_editor

    if elem == "label":
        modify_xattr_column.column_label.clear()
        modify_xattr_column.column_label.send_keys(new_elem_name)
    else:
        enter_key = modify_xattr_column.enter_an_xattr_key
        modify_xattr_column.clear_actual_key()
        enter_key.send_keys(new_elem_name)

    modify_xattr_column.apply_changes.click()

    # hide columns menu popup
    browser.configure_columns.click()
