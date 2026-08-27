"""This module contains gherkin steps to run acceptance tests featuring groups
management in onezone web GUI
"""

__author__ = "Michal Stanisz, Lukasz Niemiec"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.steps.common.common import (
    close_alert_popup_if_present,
    get_visible_items_list,
)
from tests.gui.steps.common.miscellaneous import press_enter_on_active_element
from tests.gui.utils import OZLoggedIn, Popups
from tests.gui.utils.common.constants import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.utils.common.modals import Modals
from tests.gui.utils.common.popups.generic import CreatedItemAlertPopup
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    ListElement,
    parse_elements_sequence,
    transform,
)
from tests.gui.utils.onezone.groups.groups_page import Group, GroupsPage
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) clicks on "Create group" button in groups sidebar'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_group_button_in_panel(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    oz_page = OZLoggedIn(selenium[browser_id])
    oz_page.open_panel(GroupsPage)
    oz_page.groups.create_group()


@wt(parsers.parse('user of {browser_id} writes "{text}" into group name text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def input_name_into_input_box_on_main_groups_page(
    selenium: SeleniumDrivers, browser_id: str, text: str
) -> None:
    OZLoggedIn(selenium[browser_id]).groups.input_box.value = text


@wt(parsers.parse("user of {browser_id} clicks on confirmation button"))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_name_input_on_main_groups_page(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    OZLoggedIn(selenium[browser_id]).groups.input_box.confirm()
    close_alert_popup_if_present(
        selenium[browser_id], popup=CreatedItemAlertPopup.GROUP
    )


def _find_groups(page: GroupsPage, group_name: str) -> list[Group]:
    return list(filter(lambda g: g.name == group_name, page.groups_list))


@repeat_failed(timeout=WAIT_FRONTEND)
def get_group_by_name_from_main_page(driver: WebDriver, group_name: str) -> Group:
    oz_page = OZLoggedIn(driver)
    oz_page.open_panel(GroupsPage)
    page = oz_page.groups
    return page.groups_list[group_name]


@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_in_group_menu_and_get_group(
    driver: WebDriver, group_name: str, option: str
) -> Group:
    group = get_group_by_name_from_main_page(driver, group_name)
    group.menu()
    Popups(driver).menu_popup_with_text.menu[option]()
    return group


@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_confirmation_button_to_rename_group(group: Group) -> None:
    group.edit_box.confirm()


@repeat_failed(timeout=WAIT_FRONTEND)
def input_new_group_name_into_rename_group_inpux_box(group: Group, text: str) -> None:
    group.edit_box.value = text
    assert group.edit_box.value == text, "Failed to write new group name to input box"


@wt(
    parsers.re(
        rf"users? of (?P<browser_ids>{ELEMENTS_SEQUENCE_PATTERN}) "
        r"(?P<option>does not see|sees) "
        r'group "(?P<group>.*)" on groups list'
    ),
    converters={
        "browser_ids": parse_elements_sequence,
    },
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_group_exists(
    selenium: SeleniumDrivers,
    browser_ids: list[str],
    option: str,
    group: str,
) -> None:
    for browser_id in browser_ids:
        oz_page = OZLoggedIn(selenium[browser_id])
        oz_page.open_panel(GroupsPage)
        groups_count = len(
            _find_groups(
                oz_page.groups,
                group,
            )
        )
        if option == "does not see":
            assert groups_count == 0, f'group "{group}" found'
        else:
            assert groups_count == 1, f'group "{group}" not found'


@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_of_group_menu_on_left_sidebar_menu(
    selenium: SeleniumDrivers, browser_id: str, group_name: str, option: str
) -> None:
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    page = OZLoggedIn(driver).groups
    page.groups_list[group_name]()
    getattr(page.groups_list[group_name], transform(option))()


@wt(parsers.parse("user of {browser_id} sees that create group button is inactive"))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_create_button_inactive(selenium: SeleniumDrivers, browser_id: str) -> None:
    page = OZLoggedIn(selenium[browser_id]).groups
    assert not page.input_box.confirm.is_enabled(), '"Create group" button is enabled'


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) opens group "(?P<group_name>.*)" '
        r"(?P<subpage>members|hierarchy|main) subpage"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def go_to_group_subpage(
    selenium: SeleniumDrivers, browser_id: str, group_name: str, subpage: str
) -> None:
    oz_page = OZLoggedIn(selenium[browser_id])
    oz_page.open_panel(GroupsPage)
    groups_page = oz_page.groups
    group: Group = groups_page.groups_list[group_name]

    if groups_page.get_visible_active_group_name() != group_name:
        group.click()

    if subpage != "main" and group.get_active_subpage() != subpage:
        getattr(group, subpage)()


@wt(parsers.parse('user of {browser_id} see that page with text "{text}" appeared'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_error_page_appeared(
    selenium: SeleniumDrivers, browser_id: str, text: str
) -> None:
    page = OZLoggedIn(selenium[browser_id]).groups
    assert page.main_page.error_label == text, f'page with text "{text}" not found'


@wt(parsers.re(r"user of (?P<browser_id>.*) confirms using (?P<option>.*)"))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_add_group(selenium: SeleniumDrivers, browser_id: str, option: str) -> None:
    if option == "enter":
        press_enter_on_active_element(selenium, browser_id)
        close_alert_popup_if_present(
            selenium[browser_id], popup=CreatedItemAlertPopup.GROUP
        )
    else:
        confirm_name_input_on_main_groups_page(selenium, browser_id)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) clicks on group "
        r'"(?P<group_name>.*)" menu button in hierarchy subpage'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_group_trigger(
    selenium: SeleniumDrivers, browser_id: str, group_name: str
) -> None:
    driver = selenium[browser_id]
    (
        OZLoggedIn(driver)
        .groups.main_page.hierarchy.groups[group_name]
        .click_group_menu_button(driver)
    )


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) clicks on group "
        r'"(?P<group_name>.*)" menu button to (?P<relation>.*) '
        r"relation in hierarchy subpage"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_group_relation_trigger(
    selenium: SeleniumDrivers,
    browser_id: str,
    group_name: str,
    relation: str,
) -> None:
    driver = selenium[browser_id]
    (
        OZLoggedIn(driver)
        .groups.main_page.hierarchy.groups[group_name]
        .click_relation_menu_button(driver, relation)
    )


@wt(parsers.parse('user of {browser_id} clicks on "{option}" in group hierarchy menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_in_group_hierarchy_menu(
    selenium: SeleniumDrivers, browser_id: str, option: str
) -> None:
    driver = selenium[browser_id]
    Popups(driver).group_hierarchy_menu.options[option].click()


@wt(parsers.parse('user of {browser_id} clicks on "{option}" in relation menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_in_relation_menu(
    selenium: SeleniumDrivers, browser_id: str, option: str
) -> None:
    driver = selenium[browser_id]
    Popups(driver).relation_menu.options[option].click()


@wt(
    parsers.parse(
        'user of {browser_id} writes "{group_name}" '
        "into group name text field in create group modal"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def write_name_group_in_create_new_child_group_modal(
    selenium: SeleniumDrivers, browser_id: str, group_name: str
) -> None:
    driver = selenium[browser_id]
    Modals(driver).create_group.input_name = group_name


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) (?P<option>does not see|sees) "
        r'"(?P<group_name>.*)" as a (?P<relation>child|parent) '
        r'of "(?P<active_group>.*)" in hierarchy subpage'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_list_of_children_contains_group(
    selenium: SeleniumDrivers,
    browser_id: str,
    group_name: str,
    relation: str,
    option: str,
) -> None:
    relation_name = "children" if relation == "child" else "parents"

    groups = getattr(
        OZLoggedIn(selenium[browser_id]).groups.main_page.hierarchy, relation_name
    )
    if option == "sees":
        assert group_name in groups
    else:
        assert group_name not in groups


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) clicks show parent groups in hierarchy subpage"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_show_parent_groups_in_hierarchy_page(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    (OZLoggedIn(selenium[browser_id]).groups.main_page.hierarchy.show_parent_groups())


@wt(parsers.parse('user of {browser_id} sees "{text}" error on groups page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_error_detail_text(
    selenium: SeleniumDrivers, browser_id: str, text: str
) -> None:
    page = OZLoggedIn(selenium[browser_id]).groups
    assert text in page.main_page.error_header, f'page with text "{text}" not found'


@wt(parsers.parse('user of {browser_id} sees "{group_name}" group members subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_user_sees_group_page(
    selenium: SeleniumDrivers, browser_id: str, group_name: str
) -> None:
    driver = selenium[browser_id]
    group_name_on_page = OZLoggedIn(driver).groups.selected_group_name
    error_message = f"expected group name {group_name}, found {group_name_on_page}"
    assert group_name_on_page == group_name, error_message


@wt(
    parsers.parse(
        'user of {browser_id} can see there is group "{group_name}" on the '
        "groups list in the sidebar"
    )
)
@repeat_failed(timeout=WAIT_BACKEND * 4)
def assert_group_in_groups_page(
    browser_id: str, selenium: SeleniumDrivers, group_name: str
) -> None:
    driver = selenium[browser_id]

    group_headers = get_visible_items_list(
        OZLoggedIn(driver).groups, ListElement.GROUPS_HEADERS, "name"
    )

    header = [header for header in group_headers if header.name == group_name]
    assert header, f"There is no group {group_name} in groups list."
