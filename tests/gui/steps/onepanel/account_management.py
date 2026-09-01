"""This module contains gherkin steps to run acceptance tests featuring
account management in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from time import sleep

from tests.gui.utils import OnePage, Popups
from tests.gui.utils.common.constants import WAIT_FRONTEND
from tests.gui.utils.generic import transform
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.user_utils import Users
from tests.utils.utils import repeat_failed


@wt(parsers.parse("user of {browser_id} clicks on logout button in main menu"))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_user_account_btn_panel(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    sleep(1)
    OnePage(selenium[browser_id]).logout.click()


@wt(
    parsers.parse("user of {browser_id} clicks on {btn} button in user account popover")
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_option_in_user_account_popover(
    selenium: SeleniumDrivers, browser_id: str, btn: str
) -> None:
    Popups(selenium[browser_id]).user_account_menu.options[btn].click()


@wt(
    parsers.parse(
        "user of {browser_id} types password for {user} "
        "in Current password in change password form "
        "in account management page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_password_of_user_to_curr_passwd(
    selenium: SeleniumDrivers, browser_id: str, user: str, users: Users
) -> None:
    form = OnePage(selenium[browser_id]).content.account_management.chpasswd_form
    form.current_password = users[user].password


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) types "(?P<text>.*?)" to '
        r"(?P<in_box>New|Retype new|Current) password in change "
        r"password form in account management page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_text_to_in_box_in_chpasswd_form(
    selenium: SeleniumDrivers, browser_id: str, in_box: str, text: str
) -> None:
    form = OnePage(selenium[browser_id]).content.account_management.chpasswd_form
    setattr(form, transform(in_box + " password"), text)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) clicks on Confirm password change "
        r"button in change password form in account management page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_confirm_btn_in_chpasswd_form(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    form = OnePage(selenium[browser_id]).content.account_management.chpasswd_form
    form.confirm_password_change()


@wt(
    parsers.parse(
        "user of {browser_id} clicks on {btn} button in account management page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_btn_in_account_management(
    selenium: SeleniumDrivers, browser_id: str, btn: str
) -> None:
    getattr(
        OnePage(selenium[browser_id]).content.account_management, transform(btn)
    ).click()
