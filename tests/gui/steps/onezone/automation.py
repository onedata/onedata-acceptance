"""This module contains gherkin steps to run acceptance tests featuring
automation management in onezone web GUI """

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import wt, parsers
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.utils import repeat_failed
from tests.gui.steps.common.miscellaneous import press_enter_on_active_element


@wt(parsers.parse('user of {browser_id} clicks on Create automation inventory '
                  'button in automation sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_automation_button_in_sidebar(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['automation'].create_automation()


@wt(parsers.parse('user of {browser_id} writes "{text}" into inventory name '
                  'text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def input_name_into_input_box_on_main_automation_page(selenium, browser_id,
                                                      text, oz_page):
    oz_page(selenium[browser_id])['automation'].input_box.value = text


@wt(parsers.parse('user of {browser_id} clicks on confirmation button on '
                  'automation page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_name_input_on_main_automation_page(selenium, browser_id,
                                               oz_page):
    oz_page(selenium[browser_id])['automation'].input_box.confirm()


@wt(parsers.re('user of (?P<browser_id>.*) clicks on '
               '"(?P<option>Rename|Leave|Remove)" '
               'button in inventory "(?P<inventory>.*)" menu in the '
               'sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_in_inventory_menu(selenium, browser_id, option, inventory,
                                   oz_page, popups):
    driver = selenium[browser_id]
    page = oz_page(driver)['automation']
    page.elements_list[inventory]()
    page.elements_list[inventory].menu()
    popups(driver).menu_popup_with_text.menu[option]()


@wt(parsers.parse('user of {browser_id} writes '
                  '"{text}" into rename inventory text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def input_new_inventory_name_into_rename_inventory_input_box(selenium,
                                                             browser_id, text,
                                                             oz_page):
    page = oz_page(selenium[browser_id])['automation']
    page.elements_list[''].edit_box.value = text


@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_confirmation_button_to_rename_inventory(selenium, browser_id,
                                                     oz_page):
    oz_page(selenium[browser_id])['automation'].elements_list[
        ''].edit_box.confirm()


@wt(parsers.re('user of (?P<browser_id>.*) confirms inventory rename with '
               'confirmation button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_rename_the_inventory(selenium, browser_id, oz_page):
    click_on_confirmation_button_to_rename_inventory(selenium, browser_id,
                                                     oz_page)


@wt(parsers.re('users? of (?P<browser_ids>.*) (?P<option>does not see|sees) '
               'inventory "(?P<inventory>.*)" on inventory list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_inventory_exists(selenium, browser_ids, option, inventory, oz_page):
    for browser_id in parse_seq(browser_ids):
        elem_list = oz_page(selenium[browser_id])['automation'].elements_list

        if option == 'does not see':
            assert inventory not in elem_list, f'inventory: {inventory} found'
        else:
            assert inventory in elem_list, f'inventory: {inventory} not found'


@wt(parsers.re('user of (?P<browser_id>.*) opens inventory "(?P<inventory>.*)" '
               '(?P<subpage>workflows|lambdas|members|main) subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def go_to_inventory_subpage(selenium, browser_id, inventory, subpage, oz_page):
    page = oz_page(selenium[browser_id])['automation']
    page.elements_list[inventory]()
    if subpage != 'main':
        getattr(page.elements_list[inventory], subpage)()


@wt(parsers.parse('user of {browser_ids} sees "{text}" label in "{inventory}" '
                  'main page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_inventory_exists(selenium, browser_ids, oz_page, text):
    for browser_id in parse_seq(browser_ids):
        err_msg = oz_page(selenium[browser_id])['automation'].privileges_err_msg

        assert text in err_msg, f'Error message: {text} not found'
