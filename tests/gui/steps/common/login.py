"""This module contains gherkin steps to run acceptance tests featuring
login page in web GUI.
"""

__author__ = "Bartosz Walkowicz, Michal Stanisz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import time

from tests.conftest import SeleniumDrivers, Users
from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.common.url import assert_main_page_loaded
from tests.gui.types import GuiObject
from tests.gui.utils import LoginPage, OnePage
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_BACKEND * 2)
def _login_using_basic_auth(
    login_page: GuiObject, username: str, password: str
) -> None:
    login_page.username = username
    login_page.password = password
    login_page.sign_in()


@repeat_failed(timeout=WAIT_BACKEND * 2)
def _login_using_passphrase(login_page: GuiObject, password: str) -> None:
    login_page.passphrase = password
    login_page.sign_in()


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) clicks Sign in to emergency "
        "interface in Onepanel login page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_sign_in_to_emergency_interface(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    LoginPage(selenium[browser_id]).sign_in_to_emergency_interface()


def _login_to_service(
    selenium: SeleniumDrivers,
    browser_id_list: str,
    user_id_list: str,
    service_list: str,
    users: Users,
) -> None:
    for browser_id, username, service in zip(
        parse_seq(browser_id_list),
        parse_seq(user_id_list),
        parse_seq(service_list),
    ):
        driver = selenium[browser_id]

        if "emergency interface" in service:
            click_sign_in_to_emergency_interface(selenium, browser_id)
            time.sleep(1)
            _login_using_passphrase(LoginPage(driver), users[username].password)
        else:
            _login_using_basic_auth(
                LoginPage(driver), username, users[username].password
            )
        assert_main_page_loaded(selenium, browser_id)


@given(
    parsers.re(
        "users? of (?P<browser_id_list>.*) logged "
        "as (?P<user_id_list>.*) to (?P<service_list>.*) service"
    )
)
@wt(
    parsers.re(
        "users? of (?P<browser_id_list>.*) logs? "
        "as (?P<user_id_list>.*) to (?P<service_list>.*) service"
    )
)
def login_using_basic_auth(
    selenium: SeleniumDrivers,
    browser_id_list: str,
    user_id_list: str,
    users: Users,
    service_list: str,
) -> None:
    _login_to_service(selenium, browser_id_list, user_id_list, service_list, users)


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) types "(?P<text>.*?)" to '
        r"(?P<in_box>Username|Password|Passphrase) input "
        r"in (Onepanel|Onezone) login form"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_enter_text_to_field_in_login_form(
    selenium: SeleniumDrivers, browser_id: str, in_box: str, text: str
) -> None:
    setattr(LoginPage(selenium[browser_id]), transform(in_box), text)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) types password of "
        r'"(?P<username>.*?)" to Password input in Onezone login form'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_enter_password_of_user(
    selenium: SeleniumDrivers, browser_id: str, username: str, users: Users
) -> None:
    password = users[username].password
    setattr(LoginPage(selenium[browser_id]), "password", password)


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) presses Sign in button "
        "in (Onepanel|Onezone) login page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_press_sign_in_btn_on_login_page(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    LoginPage(selenium[browser_id]).sign_in()


@wt(parsers.re("user of (?P<browser_id>.*) successfully signed in (?P<service>.*)"))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_successful_login(
    selenium: SeleniumDrivers, browser_id: str, service: str
) -> None:
    logged_in_service = OnePage(selenium[browser_id]).service
    assert (
        service.lower() in logged_in_service.lower()
    ), f"logged in {logged_in_service} instead of {service}"


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) sees that he was logged out from (Onepanel|Onezone)"
    )
)
@wt(parsers.re("user of (?P<browser_id>.*) sees (Onepanel|Onezone) login page"))
@repeat_failed(timeout=WAIT_BACKEND * 2)
def wt_assert_login_page(selenium: SeleniumDrivers, browser_id: str) -> None:
    _ = LoginPage(selenium[browser_id]).header


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) sees error message "
        "about invalid credentials in (Onepanel|Onezone) "
        "login page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_err_msg_about_credentials(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    assert LoginPage(
        selenium[browser_id]
    ).err_msg, "no err msg about invalid credentials found"


@wt(
    parsers.parse(
        "user of {browser_id} sees sign in notification message: "
        '"{text}" in the login page'
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_sign_in_notification(
    text: str, selenium: SeleniumDrivers, browser_id: str
) -> None:
    err_msg = "sign in notification message is not as expected"
    assert (
        LoginPage(selenium[browser_id]).login_notification_message.text == text
    ), err_msg
