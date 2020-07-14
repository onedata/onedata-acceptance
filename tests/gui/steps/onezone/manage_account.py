"""This module contains gherkin steps to run acceptance tests featuring
account management in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz, Piotr Duleba"
__copyright__ = "Copyright (C) 2017-2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from pytest_bdd import parsers, when, then
from tests.utils.acceptance_utils import wt
from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.utils import repeat_failed
from tests.gui.utils.common.popups import Popups as popups


@when(parsers.parse('user of {browser_id} expands account settings '
                    'dropdown in the sidebar'))
@then(parsers.parse('user of {browser_id} expands account settings '
                    'dropdown in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def expand_account_settings_in_oz(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['profile'].profile()


@when(parsers.re(r'user of (?P<browser_id>.+?) clicks on '
                 r'(?P<option>Logout|Manage account) item in expanded '
                 r'settings dropdown in the sidebar'))
@then(parsers.re(r'user of (?P<browser_id>.+?) clicks on '
                 r'(?P<option>Logout|Manage account) item in expanded '
                 r'settings dropdown in the sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_option_in_account_settings_in_oz(selenium, browser_id, option):
    driver = selenium[browser_id]
    popups(driver).user_account_menu.options[option].click()


@wt(parsers.parse('user of {browser_id} clicks on remove user toolbar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_remove_user_toolbar_in_oz(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['profile'].show_user_account_menu_toolbar\
        .click()


@wt(parsers.parse('user of {browser_id} clicks on remove user button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_remove_user_button_in_oz(selenium, browser_id, popups):
    popups(selenium[browser_id]).user_delete_account_popover_menu.click()


@wt(parsers.parse('user of {browser_id} checks understand consequences '
                  'checkbox'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_understand_consequences_checkbox_in_oz(selenium, browser_id, modals):
    modals(selenium[browser_id]).delete_user_account.understand_consequences\
        .click()


@wt(parsers.parse('user of {browser_id} clicks on delete account button'
                  ' in modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_delete_account_button_in_oz(selenium, browser_id, modals, users):
    modals(selenium[browser_id]).delete_user_account.delete_account.click()
    users.pop('user1', None)


@wt(parsers.parse('user of {browser_id} activates edit box by clicking on '
                  'the {credential} in Profile page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def activate_password_edit_box_in_oz(selenium, browser_id, oz_page, credential):
    getattr(oz_page(selenium[browser_id])['profile'], 'rename_'+credential)()


@wt(parsers.parse('user of {browser_id} types current password for "{username}"'
                  ' in account management page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_cur_passwd_of_user_into_box_in_oz(selenium, browser_id, username,
                                           oz_page, users):
    cur_passwd = users[username].password
    oz_page(selenium[browser_id])['profile'].current_password_box = cur_passwd


@wt(parsers.parse('user of {browser_id} {type_attempt} "{new_password}" '
                  'as new password for user in account management page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_new_passwd_into_box_in_oz(selenium, browser_id, type_attempt,
                                      oz_page, new_password):
     setattr(oz_page(selenium[browser_id])['profile'],
             type_attempt.rstrip('s') + "_new_password_box", new_password)


@wt(parsers.parse('user of {browser_id} clicks on change password confirm'
                  ' button'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_new_passwd_confirm_btn_in_oz(selenium, browser_id, oz_page):
    oz_page(selenium[browser_id])['profile'].change_password.click()


@wt(parsers.parse('user of {browser_id} types "{text}" to user name '
                  'edit box in Profile page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_text_into_user_name_edit_box_in_oz(selenium, browser_id,
                                            text, oz_page):
    oz_page(selenium[browser_id])['profile'].edit_user_name_box.value = text


@wt(parsers.re(r'user of (?P<browser_id>.+?) clicks on '
               r'(?P<btn>confirm|cancel) button displayed next to user '
               r'name edit box in Profile page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_btn_for_user_name_edit_box_in_oz(selenium, browser_id,
                                              btn, oz_page):
    getattr(oz_page(selenium[browser_id])['profile'].edit_user_name_box, btn)\
        .click()


@wt(parsers.parse('user of {browser_id} sees that the user name displayed '
                  'in Profile page is "{expected_user_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_correct_user_name_in_oz(selenium, browser_id, expected_user_name,
                                   oz_page):
    displayed_user_name = oz_page(selenium[browser_id])['profile'].user_name
    err_msg = ('expected "{}" as user name, but instead displayed is "{}" '
               'in USER NAME oz panel'.format(expected_user_name,
                                              displayed_user_name))
    assert displayed_user_name == expected_user_name, err_msg

