"""Utils and fixtures to facilitate operations on
common operations between various services.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from functools import partial

from tests.gui.utils.core.base import ExpandableMixin, PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Input,
    Label,
    NamedButton,
    WebElement,
    WebItem,
    WebItemsSequence,
)
from tests.gui.utils.core.web_objects import ButtonWithTextPageObject

from .account_management import AccountManagementContentPage


class BaseContent(PageObject):
    _main_content = ".main-content"
    account_management = WebItem(_main_content, cls=AccountManagementContentPage)

    def __str__(self):
        return f"content in {self.parent}"


class EmergencyInterfaceWarningBar(PageObject):
    info = Button(".oneicon-sign-info-rounded")


class OnePage:
    loading_error = Label(".application-error-message")
    service = Label(".brand-info")
    logout = WebElement(".user-account-button-main")
    content = WebItem(".col-content", cls=BaseContent)
    opened_tab = Label("#main-menu-container ul.main-menu li.main-menu-item.active")
    main_menu = WebItemsSequence(
        "#main-menu-container ul.main-menu li.main-menu-item",
        cls=ButtonWithTextPageObject,
    )
    warning_bar = WebItem(".one-warning-bar", cls=EmergencyInterfaceWarningBar)

    def __init__(self, driver):
        self.driver = self.web_elem = driver

    def __str__(self):
        return self.service


class PublicOnePage:
    loading_error = Label(".application-error-message")

    def __init__(self, driver):
        self.driver = self.web_elem = driver

    def __str__(self):
        return "public onedata page"


class _Toggle(PageObject):
    _lock = WebElement(".one-way-toggle-readonly-icon")

    def __str__(self):
        return f"toggle switch in {self.parent}"

    def is_checked(self):
        return "checked" in self.web_elem.get_attribute("class")

    def is_partial_checked(self):
        return "maybe" in self.web_elem.get_attribute("class")

    def is_unchecked(self):
        return not self.is_checked() and not self.is_partial_checked()

    def check(self):
        if not self.is_checked():
            self.click()

    def uncheck(self):
        if self.is_checked():
            self.click()
        elif self.is_partial_checked():
            self.click()
            self.click()

    def is_enabled(self):
        try:
            self._lock
        except RuntimeError:
            return True
        return False


class _DropdownSelector(PageObject, ExpandableMixin):
    selected = Label(".ember-power-select-trigger")
    options = WebItemsSequence("ul li", cls=ButtonWithTextPageObject)
    _toggle = WebElement('.ember-basic-dropdown-trigger[role="button"]')


class _MigrateDropdownSelector(PageObject, ExpandableMixin):
    selected = Label(".ember-power-select-trigger")
    providers_list = WebItemsSequence(
        "ul li .oneprovider-name", cls=ButtonWithTextPageObject
    )
    _toggle = WebElement('.ember-basic-dropdown-trigger[role="button"]')


Toggle = partial(WebItem, cls=_Toggle)
DropdownSelector = partial(WebItem, cls=_DropdownSelector)
MigrateDropdownSelector = partial(WebItem, cls=_MigrateDropdownSelector)


class LoginPage:
    header = Label(".row-login-header")
    sign_in_to_emergency_interface = Button(".text-link")
    username = Input('input[placeholder="Username"]')
    password = Input('input[placeholder="Password"]')
    passphrase = Input('input[placeholder="Passphrase"]')
    sign_in = NamedButton("button", text="Sign in")
    err_msg = Label(".login-error-message")
    open_in_onezone = Button(".btn-login-onezone")
    login_notification_message = WebElement(".login-notification")

    def __init__(self, driver):
        self.web_elem = self.driver = driver

    def __str__(self):
        return "Onezone Login page"
