"""Utils to facilitate operations on tokens page in Onezone gui"""

__author__ = "Michal Stanisz, Natalia Organek"
__copyright__ = "Copyright (C) 2018-2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.utils.common.common import Toggle
from tests.gui.utils.common.privilege_tree_in_tokens import PrivilegeTree
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Input,
    Label,
    NamedButton,
    WebElement,
    WebElementsSequence,
    WebItem,
    WebItemsSequence,
)
from tests.gui.utils.onezone.common import InputBox
from tests.gui.utils.onezone.generic_page import SidebarPanelPage
from tests.gui.utils.onezone.token_caveats import CaveatField


class TokenRow(PageObject):
    id = name = Label(".item-name")
    menu_button = Button(".token-menu-trigger")
    icon = WebElement(".one-icon")

    def is_type_of(self, exp_type: str) -> bool:
        return exp_type in self.icon.get_attribute("class")

    def is_revoked(self) -> bool:
        return "inactive" in self.web_elem.get_attribute("class")

    def __str__(self) -> str:
        return "Tokens row"


class TokenFilter(PageObject):
    all = Button(".btn-all")
    access = Button(".btn-access")
    identity = Button(".btn-identity")
    invite = Button(".btn-invite")


class TokenInviteTargetOptions(PageObject):
    name = id = Label(".text")


class TokenInviteTargetNameOptions(PageObject):
    name = id = Label(".truncated-string")


class TokenInviteFilter(PageObject):
    dropdown_menus = WebElementsSequence(".ember-basic-dropdown-trigger")


class TokensSidebar(PageObject):
    create_new_token = Button(".one-sidebar-toolbar-button .oneicon-add-filled")
    tokens = WebItemsSequence(".token-item", cls=TokenRow)
    consume_token = Button(".oneicon-consume-token")
    clean_up_obsolete_tokens = Button(".clean-obsolete-tokens-trigger")
    filter = WebItem(".filter-control", cls=TokenFilter)
    invite_filter = WebItem(".filter-control.target-filter", cls=TokenInviteFilter)

    name_input = Input(".name-editor .form-control")
    confirm = Button(".save-icon")
    discard = Button(".cancel-icon")

    def click_create_new_token(self, driver: WebDriver) -> None:
        driver.execute_script(
            "arguments[0].click();",
            self.web_elem.find_element(By.CSS_SELECTOR, ".create-token-link-trigger"),
        )

    def __str__(self) -> str:
        return "Tokens sidebar"


class UsageLimitBar(PageObject):
    infinity_option = WebElement(".option-infinity .one-way-radio-control")
    number_option = WebElement(".option-number")
    number_input = Input(".text-like-field .form-control")


class CreateNewTokenPage(PageObject):
    create_custom_token = Button(".template-custom")
    header = Label(".resource-name")

    create_token = NamedButton(".submit-token", text="Create token")
    access_option = WebElement(".option-access .one-way-radio-control")
    identity_option = WebElement(".option-identity .one-way-radio-control")
    invite_option = WebElement(".option-invite .one-way-radio-control")

    access_input = WebElement(".field--access")
    identity_input = WebElement(".field--identity")
    invite_input = WebElement(".field--invite")

    token_name_input = WebItem(".name-field .field-component", cls=InputBox)

    invite_type = WebElement(".inviteType-field .dropdown-field-trigger")
    invite_target = WebElement(".target-field .dropdown-field-trigger")
    usage_limit = WebItem(".usageLimit-collapse", cls=UsageLimitBar)

    show_inactive_caveats = Button(".caveats-expand")
    expiration_caveat = WebItem(".expireCaveat-field", cls=CaveatField)
    region_caveat = WebItem(".regionCaveat-field", cls=CaveatField)
    country_caveat = WebItem(".countryCaveat-field", cls=CaveatField)
    asn_caveat = WebItem(".asnCaveat-field", cls=CaveatField)
    ip_caveat = WebItem(".ipCaveat-field", cls=CaveatField)
    consumer_caveat = WebItem(".consumerCaveat-field", cls=CaveatField)
    service_caveat = WebItem(".serviceCaveat-field", cls=CaveatField)
    interface_caveat = WebItem(".interfaceCaveat-field", cls=CaveatField)
    readonly_caveat = WebItem(".readonlyCaveat-field", cls=CaveatField)
    path_caveat = WebItem(".pathCaveat-field", cls=CaveatField)
    object_id_caveat = WebItem(".objectIdCaveat-field", cls=CaveatField)

    footer = WebElement(".footer-buttons")
    show_details = WebElement(".token-alert .clickable")
    documentation_link = WebElement(".documentation-link")
    tokens_documentation_link = WebElement(".documentation-link")
    data_access_caveats_documentation_link = WebElement(
        ".data-access-caveat-warning-details .documentation-link"
    )

    def __str__(self) -> str:
        return "Create new token page"

    def expand_invite_type_dropdown(self) -> None:
        self.invite_type.click()

    def expand_invite_target_dropdown(self) -> None:
        self.invite_target.click()

    def expand_caveats(self) -> None:
        if "show" in self.show_inactive_caveats.web_elem.text.lower():
            self.show_inactive_caveats()

    def caveats_expanded(self) -> bool:
        return "hide" in self.show_inactive_caveats.web_elem.text.lower()

    def hide_caveats(self) -> None:
        if "hide" in self.show_inactive_caveats.web_elem.text.lower():
            self.show_inactive_caveats()

    def scroll_to_bottom(self) -> None:
        self.driver.execute_script(
            "arguments[0].scrollTo(arguments[1]);", self.web_elem, self.footer
        )

    def get_caveat(self, name: str) -> CaveatField:
        self.scroll_to_bottom()
        return getattr(self, f"{name}_caveat")


class TokensPage(SidebarPanelPage):
    panel_name = "tokens"

    sidebar = WebItem(".sidebar-tokens", cls=TokensSidebar)
    create_token_page = WebItem(".col-content", cls=CreateNewTokenPage)

    copy_token = Button(".copy-btn")
    token = Label(".clipboard-input.form-control ")
    menu = Button(".with-menu .collapsible-toolbar-toggle")
    revoke_toggle = Toggle(".one-way-toggle")
    save_button = NamedButton(".submit-token", text="Save")

    privilege_tree = WebItem(".invitePrivilegesDetails-field", cls=PrivilegeTree)

    token_name = Label(".name-field .text-like-field")
    token_type = Label(".type-field .radio-field")
    invite_type = Label(".inviteType-field .field-component")
    invite_target = Label(".target-field .field-component")
    usage_count = Label(".usageCount-field .static-text-field")

    input_name = Input(".token-consumer .token-container input")
    _toggle = WebElement('.token-consumer .ember-basic-dropdown-trigger[role="button"]')
    confirm_button = NamedButton("button", text="Confirm")

    onezone_rest_access_template = WebElement(".template-onezoneRest")
    alert = Label(".alert")

    def expand_dropdown(self) -> None:
        self._toggle.click()

    def is_token_revoked(self) -> bool:
        return self.revoke_toggle.is_checked()

    def __str__(self) -> str:
        return "Tokens page"
