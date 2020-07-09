"""This module contains gherkin steps to run acceptance tests featuring
user full name management in onezone web GUI.
"""

__author__ = "Piotr Duleba"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import parsers

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.utils.utils import repeat_failed
from tests.utils.acceptance_utils import wt

@wt(parsers.parse('user of {browser_id} types current password for "{username}" in account management page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_cur_passwd_of_user_into_box_in_oz(selenium, browser_id,username, oz_page,users):
    cur_passwd = users[username].password
    oz_page(selenium[browser_id])['profile'].current_password_box = cur_passwd


@wt(parsers.parse('user of {browser_id} types "{new_password}" as new password for user in account management page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_new_passwd_into_box_in_oz(selenium, browser_id, oz_page,new_password):
    oz_page(selenium[browser_id])['profile'].new_password_box = new_password


@wt(parsers.parse('user of {browser_id} retypes "{new_password}" as new password for user in account management page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def retype_new_passwd_into_box_in_oz(selenium, browser_id, oz_page,new_password):
    oz_page(selenium[browser_id])['profile'].new_password_retype_box = new_password


@wt(parsers.parse('user of {browser_id} clicks on change password confirm button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_new_passwd_confirm_btn_in_oz(selenium, browser_id, oz_page,):
    oz_page(selenium[browser_id])['profile'].change_password.click()


@wt(parsers.parse('user of {browser_id} activates edit box by clicking on '
                  'the password in Profile page'))
@repeat_failed(timeout=WAIT_BACKEND)
def activate_password_edit_box_in_oz(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['profile'].rename_password()
