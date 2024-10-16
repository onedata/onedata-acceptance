"""This module contains gherkin steps to run acceptance tests featuring
harvester management in onezone web GUI.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time

from tests import ELASTICSEARCH_PORT
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import _enter_text
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        "user of {browser_id} clicks on {button_name} button in discovery sidebar"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_on_discovery_on_left_sidebar_menu(
    selenium, browser_id, button_name, oz_page
):
    driver = selenium[browser_id]
    button = transform(button_name) + "_button"
    getattr(oz_page(driver)["discovery"], button).click()


@wt(parsers.parse("user of {browser_id} clicks on Create button in discovery page"))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_button_in_discovery_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)["discovery"].create_button()


@wt(
    parsers.re(
        'user of (?P<browser_id>.*) sees that "(?P<name>.*)" has'
        " (?P<option>.*) the (?P<list_type>harvesters|automation) "
        "list in the sidebar"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def check_element_exists_on_sidebar_list(
    selenium, browser_id, oz_page, name, option, list_type
):
    driver = selenium[browser_id]
    list_type = "discovery" if list_type == "harvesters" else list_type
    if option.startswith("appeared"):
        assert (
            name in oz_page(driver)[list_type].elements_list
        ), f'"{name}" not found on {list_type} list'
    else:
        assert (
            name not in oz_page(driver)[list_type].elements_list
        ), f'"{name}" found on {list_type} list'


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) clicks on "
        '"(?P<option>Rename|Leave|Remove)" '
        'button in harvester "(?P<name>.*)" menu '
        "in the sidebar"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_in_harvester_menu(selenium, browser_id, option, name, oz_page):
    page = oz_page(selenium[browser_id])["discovery"]
    page.elements_list[name]()
    page.elements_list[name].menu_button()
    page.menu[option]()


@wt(
    parsers.parse('user of {browser_id} types "{text}" to rename harvester input field')
)
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_to_rename_input_field_in_discovery_page(
    selenium, browser_id, oz_page, text
):
    driver = selenium[browser_id]
    input_field = oz_page(driver)["discovery"].rename_input
    _enter_text(input_field, text)


@wt(parsers.parse("user of {browser_id} confirms harvester rename using button"))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_harvester_rename_using_button(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)["discovery"].rename_button()


@wt(
    parsers.re(
        "user of (?P<browser_id>.*?) clicks (?P<option>.*?) "
        'of "(?P<harvester_name>.*?)" harvester in the sidebar'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_of_harvester_on_left_sidebar_menu(
    selenium, browser_id, harvester_name, option, oz_page
):
    driver = selenium[browser_id]
    getattr(
        oz_page(driver)["discovery"].elements_list[harvester_name],
        transform(option),
    ).click()


def click_option_in_discovery_page_menu(selenium, browser_id, oz_page, button_name):
    driver = selenium[browser_id]
    page = oz_page(driver)["discovery"]
    page.menu_button()
    page.menu[button_name].click()


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) sees "
        "(?P<alert_text>Insufficient privileges) alert "
        "on (?P<where>Spaces|Indices) subpage"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def see_insufficient_permissions_alert_on_discovery_page(
    selenium, browser_id, oz_page, alert_text
):
    driver = selenium[browser_id]
    forbidden_alert = oz_page(driver)["discovery"].forbidden_alert.text

    assert alert_text in forbidden_alert, f'alert with text "{alert_text}" not found'


@wt(
    parsers.parse(
        'user of {browser_id} types "{text}" to {input_name} input '
        "field in discovery page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_to_input_field_in_discovery_page(
    selenium, browser_id, oz_page, text, input_name
):
    driver = selenium[browser_id]
    input_field = getattr(oz_page(driver)["discovery"], input_name)
    _enter_text(input_field, text)


@wt(
    parsers.parse(
        "user of {browser_id} types the endpoint of deployed "
        "elasticsearch client to {input_name} input field "
        "in discovery page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def type_endpoint_to_input_field_in_discovery_page(
    selenium, browser_id, oz_page, input_name, hosts
):
    driver = selenium[browser_id]
    input_field = getattr(oz_page(driver)["discovery"], input_name)
    text = f"{hosts['elasticsearch']['ip']}:{ELASTICSEARCH_PORT}"
    _enter_text(input_field, text)


@wt(
    parsers.parse(
        "user of {browser_id} clicks {button_name} button in harvester spaces page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_in_harvester_spaces_page(selenium, browser_id, oz_page, button_name):
    driver = selenium[browser_id]
    button_name = transform(button_name) + "_button"
    getattr(oz_page(driver)["discovery"], button_name).click()


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{element_name}" from dropdown '
        "in add {element} modal"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_element_from_dropdown_in_add_element_modal(
    selenium,
    browser_id,
    element_name,
    modals,
    element,  # pylint: disable=unused-argument
    popups,
):
    driver = selenium[browser_id]
    modal_name = "add_one_of_elements"
    for _ in range(10):
        try:
            add_one_of_elements_modal = getattr(modals(driver), modal_name)
            add_one_of_elements_modal.expand_dropdown()
            popups(driver).dropdown.options[element_name].click()
        except RuntimeError:
            time.sleep(0.5)
            continue
        break


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{space_name}" has appeared '
        "on the spaces list in discovery page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_space_has_appeared_in_discovery_page(
    selenium, browser_id, space_name, oz_page
):
    driver = selenium[browser_id]
    assert (
        space_name in oz_page(driver)["discovery"].spaces_list
    ), f'space "{space_name}" not found'


def click_remove_space_option_in_menu_in_discover_spaces_page(
    selenium, browser_id, space_name, oz_page
):
    driver = selenium[browser_id]
    page = oz_page(driver)["discovery"]
    page.spaces_list[space_name].click_menu()
    page.menu["Remove this space"].click()
