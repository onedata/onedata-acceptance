"""This module contains gherkin steps to run acceptance tests featuring
login page in web GUI.
"""

__author__ = "Bartosz Walkowicz, Michal Stanisz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import time

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.common.url import (
    HOSTS_SEQUENCE_PATTERN,
    assert_main_page_loaded,
    parse_hosts_sequence,
)
from tests.gui.steps.oneprovider.common import wait_for_item_to_disappear
from tests.gui.utils import LoginPage, OnePage
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    parse_elements_sequence,
    transform,
    wait_for_visible_element_using_getter,
)
from tests.type_definitions import SeleniumDrivers
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.user_utils import Users
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_BACKEND * 2)
def _login_using_basic_auth(
    login_page: LoginPage, username: str, password: str
) -> None:
    login_page.username = username
    login_page.password = password
    login_page.sign_in()


@repeat_failed(timeout=WAIT_BACKEND * 2)
def _login_using_passphrase(login_page: LoginPage, password: str) -> None:
    login_page.passphrase = password
    login_page.sign_in()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) clicks Sign in to emergency "
        r"interface in Onepanel login page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_sign_in_to_emergency_interface(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    LoginPage(selenium[browser_id]).sign_in_to_emergency_interface()


def _login_to_service(
    selenium: SeleniumDrivers,
    browser_id_list: list[str],
    user_id_list: list[str],
    service_list: list[str],
    users: Users,
) -> None:
    for browser_id, username, service in zip(
        browser_id_list,
        user_id_list,
        service_list,
    ):
        driver = selenium[browser_id]
        password = users[username].password

        if "emergency interface" in service:
            click_sign_in_to_emergency_interface(selenium, browser_id)
            time.sleep(1)
            _login_using_passphrase(LoginPage(driver), password)
        else:
            _login_using_basic_auth(LoginPage(driver), username, password)
        assert_main_page_loaded(selenium, browser_id)


@given(
    parsers.re(
        rf"users? of (?P<browser_id_list>{ELEMENTS_SEQUENCE_PATTERN}) logged "
        rf"as (?P<user_id_list>{ELEMENTS_SEQUENCE_PATTERN}) to"
        rf" (?P<service_list>{HOSTS_SEQUENCE_PATTERN}) service"
    ),
    converters={
        "browser_id_list": parse_elements_sequence,
        "service_list": parse_hosts_sequence,
        "user_id_list": parse_elements_sequence,
    },
)
@wt(
    parsers.re(
        rf"users? of (?P<browser_id_list>{ELEMENTS_SEQUENCE_PATTERN}) logs? "
        rf"as (?P<user_id_list>{ELEMENTS_SEQUENCE_PATTERN}) to"
        rf" (?P<service_list>{HOSTS_SEQUENCE_PATTERN}) service"
    ),
    converters={
        "browser_id_list": parse_elements_sequence,
        "service_list": parse_hosts_sequence,
        "user_id_list": parse_elements_sequence,
    },
)
def login_using_basic_auth(
    selenium: SeleniumDrivers,
    browser_id_list: list[str],
    user_id_list: list[str],
    users: Users,
    service_list: list[str],
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


@repeat_failed(timeout=WAIT_FRONTEND)
def press_sign_in_btn_on_login_page(selenium: SeleniumDrivers, browser_id: str) -> None:
    LoginPage(selenium[browser_id]).sign_in()


@wt(parsers.re(r"user of (?P<browser_id>.*) is logged in (?P<service>.*) service"))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_logged_in_service(
    selenium: SeleniumDrivers, browser_id: str, service: str
) -> None:
    logged_in_service = OnePage(selenium[browser_id]).service
    assert (
        service.lower() in logged_in_service.lower()
    ), f"logged in {logged_in_service} instead of {service}"


@wt(parsers.re(r"user of (?P<browser_id>.*) successfully signs in to (?P<service>.*)"))
def wt_assert_successful_login(
    selenium: SeleniumDrivers, browser_id: str, service: str
) -> None:
    driver = selenium[browser_id]
    sign_in_getter = lambda driver: LoginPage(driver).sign_in
    sign_in = wait_for_visible_element_using_getter(driver, sign_in_getter)
    sign_in.click()
    wait_for_item_to_disappear(sign_in.web_elem, driver)
    assert_main_page_loaded(selenium, browser_id)
    assert_logged_in_service(selenium, browser_id, service)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) fails to sign in (Onepanel|Onezone) due to invalid"
        r" credentials"
    )
)
def wt_assert_failed_login_credentials(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    sign_in_getter = lambda driver: LoginPage(driver).sign_in
    wait_for_visible_element_using_getter(driver, sign_in_getter).click()
    _assert_error_message_about_credentials(selenium, browser_id)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) sees that he was logged out "
        r"from (Onepanel|Onezone)"
    )
)
@wt(parsers.re(r"user of (?P<browser_id>.*) sees (Onepanel|Onezone) login page"))
@repeat_failed(timeout=WAIT_BACKEND * 2)
def wt_assert_login_page(selenium: SeleniumDrivers, browser_id: str) -> None:
    _ = LoginPage(selenium[browser_id]).header


@repeat_failed(timeout=WAIT_FRONTEND)
def _assert_error_message_about_credentials(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    assert LoginPage(
        selenium[browser_id]
    ).error_message, "no err msg about invalid credentials found"


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
    error_message = "sign in notification message is not as expected"
    assert (
        LoginPage(selenium[browser_id]).login_notification_message.text == text
    ), error_message
