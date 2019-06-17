"""This module contains gherkin steps to run acceptance tests featuring
user alias management in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz, Agnieszka Warchol"
__copyright__ = "Copyright (C) 2017-2019 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import parsers

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.utils.utils import repeat_failed
from tests.utils.acceptance_utils import wt


@wt(parsers.re(r'user of (?P<browser_id>.+?) clicks on '
               r'(?P<btn>confirm|cancel) button displayed next to user '
               r'full name edit box in Profile page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_btn_for_user_full_name_edit_box_in_oz(selenium, browser_id,
                                                   btn, oz_page):
    getattr(oz_page(selenium[browser_id])['profile'].edit_box, btn).click()


@wt(parsers.parse('user of {browser_id} types "{text}" to user full name '
                  'edit box in Profile page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_into_user_full_name_edit_box_in_oz(selenium, browser_id,
                                                 text, oz_page):
    oz_page(selenium[browser_id])['profile'].edit_box.value = text


@wt(parsers.parse('user of {browser_id} activates edit box by clicking on '
                  'the user full name in Profile page'))
@repeat_failed(timeout=WAIT_BACKEND)
def activate_user_full_name_edit_box_in_oz(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['profile'].rename_full_name()


@wt(parsers.parse('user of {browser_id} sees that the user full name displayed '
                  'in Profile page is "{expected_full_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_correct_usr_full_name_in_oz(selenium, browser_id,
                                       expected_full_name, oz_page):
    displayed_full_name = oz_page(selenium[browser_id])['profile'].full_name
    assert displayed_full_name == expected_full_name, \
        ('expected "{}" as user full name, but instead displayed is "{}" '
         'in USER FULL NAME oz panel'.format(expected_full_name,
                                             displayed_full_name))

