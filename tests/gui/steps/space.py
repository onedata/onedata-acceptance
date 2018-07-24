"""
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import parsers
from tests.utils.acceptance_utils import wt

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.utils.generic import parse_seq, repeat_failed


@wt(parsers.parse('user of {browser_id} clicks create new space on spaces on left menu'))
def choose_space_on_menu(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].create_space_button.click()


@wt(parsers.parse('user of {browser_id} types "{space}" on input'))
def click_on_input(selenium, browser_id, space, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].input_box.value = space


@wt(parsers.parse('user of {browser_id} clicks on create new space button'))
def create_new_space(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['spaces'].input_box.confirm.click()


@wt(parsers.parse('user of {browser_id} sees new "{space}" appeared'))
def assert_new_created_space(selenium, browser_id, space, oz_page):
    driver = selenium[browser_id]
    assert space in oz_page(driver)['spaces'].elements_list
