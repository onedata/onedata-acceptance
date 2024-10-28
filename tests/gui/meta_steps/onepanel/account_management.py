"""This module contains meta steps for operations on account in Onepanel
using web GUI
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.login import (
    notify_visible_with_text,
    wt_assert_login_page,
    wt_enter_text_to_field_in_login_form,
    wt_press_sign_in_btn_on_login_page,
)
from tests.gui.steps.onepanel.account_management import (
    wt_click_confirm_btn_in_chpasswd_form,
    wt_click_on_btn_in_account_management,
    wt_click_on_user_account_btn_panel,
    wt_click_option_in_user_account_popover,
    wt_type_password_of_user_to_curr_passwd,
    wt_type_text_to_in_box_in_chpasswd_form,
)
from tests.gui.steps.onepanel.common import wt_click_on_subitem_for_item
from tests.gui.steps.onepanel.emergency_passphrase import (
    click_button_on_emergency_passphrase_page,
    type_text_to_input_on_emergency_passphrase_page,
)
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


def change_user_password_in_oz_panel_using_gui(
    selenium, user, onepage, users, new_password, popups
):
    option_name = "Manage account"
    button_name = "Change password"
    notify_type = "info"
    notify_text_regexp = ".*[Pp]assword.*changed.*successfully.*"

    wt_click_on_user_account_btn_panel(selenium, user, onepage)
    wt_click_option_in_user_account_popover(selenium, user, option_name, popups)
    wt_click_on_btn_in_account_management(selenium, user, button_name, onepage)
    wt_type_password_of_user_to_curr_passwd(selenium, user, user, users, onepage)
    wt_type_text_to_in_box_in_chpasswd_form(
        selenium, user, "New", new_password, onepage
    )
    wt_type_text_to_in_box_in_chpasswd_form(
        selenium, user, "Retype new", new_password, onepage
    )
    wt_click_confirm_btn_in_chpasswd_form(selenium, user, onepage)
    notify_visible_with_text(selenium, user, notify_type, notify_text_regexp)


def login_to_oz_panel_using_new_password_gui(selenium, user, password, login_page):
    notify_type = "info"
    notify_text_regexp = ".*[Aa]uthentication.*succeeded.*"

    wt_enter_text_to_field_in_login_form(selenium, user, "Username", user, login_page)
    wt_enter_text_to_field_in_login_form(
        selenium, user, "Password", password, login_page
    )
    wt_press_sign_in_btn_on_login_page(selenium, user, login_page)

    notify_visible_with_text(selenium, user, notify_type, notify_text_regexp)


def log_out_from_oz_panel_gui(username, selenium, onepage, login_page, popups):
    button_name = "Logout"

    wt_click_on_user_account_btn_panel(selenium, username, onepage)
    wt_click_option_in_user_account_popover(selenium, username, button_name, popups)
    wt_assert_login_page(selenium, username, login_page)


@wt(
    parsers.parse(
        "user of {browser_id} changes passphrase from "
        '"{current_passphrase}" to "{new_passphrase}" '
        "on emergency passphrase page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def change_passphrase(
    selenium, browser_id, onepanel, current_passphrase, new_passphrase, hosts
):
    change_passphrase_button = "Change passphrase"
    confirm_button = "Change"
    current_passphrase_input = "Current passphrase"
    new_passphrase_input = "New passphrase"
    retype_new_passphrase_input = "Retype new passphrase"
    sidebar = "CLUSTERS"
    sub_item = "Emergency passphrase"
    record = "oneprovider-1"

    wt_click_on_subitem_for_item(
        selenium, browser_id, sidebar, sub_item, record, onepanel, hosts
    )
    click_button_on_emergency_passphrase_page(
        selenium, browser_id, onepanel, change_passphrase_button
    )
    type_text_to_input_on_emergency_passphrase_page(
        selenium,
        browser_id,
        onepanel,
        current_passphrase,
        current_passphrase_input,
    )
    type_text_to_input_on_emergency_passphrase_page(
        selenium, browser_id, onepanel, new_passphrase, new_passphrase_input
    )
    type_text_to_input_on_emergency_passphrase_page(
        selenium,
        browser_id,
        onepanel,
        new_passphrase,
        retype_new_passphrase_input,
    )
    click_button_on_emergency_passphrase_page(
        selenium, browser_id, onepanel, confirm_button
    )
