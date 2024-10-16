"""Utils to facilitate operations on clusters page in Onezone gui"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Label,
    NamedButton,
    WebElement,
    WebItem,
    WebItemsSequence,
)
from tests.gui.utils.onezone.generic_page import GenericPage


class TokenPage(PageObject):
    copy = Button(".copy-btn")


class GuiSettingsPage(PageObject):
    sign_in_notification = Button(".sign-in-notification-item")
    sign_in_notification_input = WebElement(".sign-in-notification-input")
    save_sign_in_notification = Button(".btn-save")

    privacy_policy = Button(".privacy-policy-item")
    privacy_policy_input = WebElement(".privacy-policy .pell-content")
    save_privacy_policy = Button(".privacy-policy .btn-save")

    terms_of_use = Button(".terms-of-use-item")
    terms_of_use_input = WebElement(".terms-of-use .pell-content")
    save_terms_of_use = Button(".terms-of-use .btn-save")

    cookie_consent_notification = Button(".cookie-consent-notification-item")
    cookie_consent_notification_input = WebElement(".cookie-consent-notification-input")
    save_cookie_consent_notification = Button(".cookie-consent-notification .btn-save")
    insert_privacy_policy_link = Button(".insert-privacy-policy-link")
    insert_terms_of_use_link = Button(".insert-terms-of-use-link")


class MenuItem(PageObject):
    name = id = Label(".item-name")
    status_icon = WebElement(".sidebar-item-icon")
    menu_button = Button(".btn-toolbar")

    # conflicted clusters have 4-letter cluster id digest added to label
    id_hash = Label(".conflict-label")

    def __call__(self):
        self.click()

    def is_not_working(self):
        return "error" in self.status_icon.get_attribute("class")

    def is_working(self):
        return not self.is_not_working()


class SubmenuItem(PageObject):
    name = id = Label(".one-label")

    def __call__(self):
        self.click()


class ClustersPage(GenericPage):
    add_new_provider_cluster = Button(".add-cluster-btn")

    token_page = WebItem(".main-content", cls=TokenPage)

    menu_button = Button(".with-menu .collapsible-toolbar-toggle")
    menu = WebItemsSequence(
        ".sidebar-clusters .two-level-sidebar .one-list-item.resource-item",
        cls=MenuItem,
    )
    submenu = WebItemsSequence(".second-level-items .item-header", cls=SubmenuItem)

    deregister_label = Button(".text-danger")
    deregister_provider = Button(".btn-danger.btn-deregister-provider")
    deregistration_checkbox = Button(".text-understand")
    confirm_deregistration = Button(".btn-danger.btn-deregister")

    edit_settings = NamedButton(".one-button.btn-default", text="Edit settings")
    confirm_modify_provider_details = NamedButton(
        "button", text="Modify provider details"
    )
    gui_settings_page = WebItem(".content-clusters-gui-settings", cls=GuiSettingsPage)
    page_name = Label(".header-row .one-label")
