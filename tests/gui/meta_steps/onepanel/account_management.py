"""This module contains meta steps for operations on account in Onepanel
using web GUI
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from tests.gui.steps.onepanel.account_management import *
from tests.gui.steps.common.login import *
from tests.gui.steps.common.notifies import *


def change_user_password_in_oz_panel_using_gui(selenium, user, onepage, users,
                                               new_password, popups):
    option_name = 'Manage account'
    button_name = 'Change password'
    notify_type = 'info'
    notify_text_regexp = '.*[Pp]assword.*changed.*successfully.*'

    wt_click_on_user_account_btn_panel(selenium, user, onepage)
    wt_click_option_in_user_account_popover(selenium, user, option_name,
                                            popups)
    wt_click_on_btn_in_account_management(selenium, user, button_name, onepage)
    wt_type_password_of_user_to_curr_passwd(selenium, user, user, users,
                                            onepage)
    wt_type_text_to_in_box_in_chpasswd_form(selenium, user, 'New',
                                            new_password, onepage)
    wt_type_text_to_in_box_in_chpasswd_form(selenium, user, 'Retype new',
                                            new_password, onepage)
    wt_click_confirm_btn_in_chpasswd_form(selenium, user, onepage)
    notify_visible_with_text(selenium, user, notify_type, notify_text_regexp)


def login_to_oz_panel_using_new_password_gui(selenium, user, password,
                                             login_page):
    notify_type = 'info'
    notify_text_regexp = '.*[Aa]uthentication.*succeeded.*'

    wt_enter_text_to_field_in_login_form(selenium, user, 'Username', user,
                                         login_page)
    wt_enter_text_to_field_in_login_form(selenium, user, 'Password', password,
                                         login_page)
    wt_press_sign_in_btn_on_login_page(selenium, user, login_page)

    notify_visible_with_text(selenium, user, notify_type, notify_text_regexp)


def log_out_from_oz_panel_gui(username, selenium, onepage, login_page,
                              popups):
    button_name = 'Logout'

    wt_click_on_user_account_btn_panel(selenium, username, onepage)
    wt_click_option_in_user_account_popover(selenium, username, button_name,
                                            popups)
    wt_assert_login_page(selenium, username, login_page)