"""Utils and fixtures to facilitate operations on Onezone web GUI."""

__author__ = "Bartosz Walkowicz Michal Stanisz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time

from selenium.webdriver import ActionChains

from tests.gui.utils.core.web_elements import Label, WebElement, WebElementsSequence

from .automation_page import AutomationPage
from .clusters_page import ClustersPage
from .data_page import DataPage
from .discovery_page import DiscoveryPage
from .groups.groups_page import GroupsPage
from .manage_account_page import ManageAccountPage
from .providers_page import ProvidersPage
from .shares_page import SharesPage
from .tokens_page import TokensPage
from .uploads_page import UploadsPage


class OZLoggedIn:
    _atlas = WebElement(".onezone-atlas")
    _sidebar_menu = WebElement(".main-menu-content")
    _panels = WebElementsSequence(".main-menu-content li.main-menu-item")
    _profile = WebElement(".app-layout")

    uploads = WebElement(".main-menu-column .main-menu-upload-item")

    provider_alert_message = Label(".content-info-content-container .text-center")

    profile_username = Label(".main-menu-column .user-account-button-username")

    panels_classes = {
        "data": DataPage,
        "shares": SharesPage,
        "providers": ProvidersPage,
        "groups": GroupsPage,
        "tokens": TokensPage,
        "discovery": DiscoveryPage,
        "automation": AutomationPage,
        "clusters": ClustersPage,
    }

    def __init__(self, driver):
        self.web_elem = driver

    def __str__(self):
        return "Onezone page"

    def __getitem__(self, item):
        return get_page(self, item, False)

    def get_page_and_click(self, item):
        return get_page(self, item)

    def is_panel_expanded(self):
        return self._panels[0].text == "DATA"

    def get_panel_by_name(self, name):
        if not self.is_panel_expanded():
            ActionChains(self.web_elem).move_to_element(self._sidebar_menu).perform()
        return [p for p in self._panels if p.text.lower() == name.lower()][0]

    def is_panel_clicked(self, item):
        panel = self.get_panel_by_name(item)
        return any(el in panel.get_attribute("class") for el in ["active", "selected"])

    def is_panel_disabled(self, item):
        panel = self.get_panel_by_name(item)
        return "disabled" in panel.get_attribute("class")

    def click_on_sidebar_menu_panel(self, name):
        panel = self.get_panel_by_name(name)
        panel.click()

    def get_profile(self):
        return self._profile


def get_page(oz_page, item, click=True):
    item = item.lower()
    cls = oz_page.panels_classes.get(item, None)
    if cls:
        if click:
            oz_page.click_on_sidebar_menu_panel(item)
            wait_for_panel_to_expand(oz_page)
        return cls(oz_page.web_elem, oz_page.web_elem, parent=oz_page)
    if item == "profile":
        return ManageAccountPage(oz_page.web_elem, oz_page.get_profile(), oz_page)
    if item == "uploads":
        return UploadsPage(oz_page.web_elem, oz_page.web_elem, oz_page)
    raise RuntimeError(f'no "{item}" on {oz_page} found')


def wait_for_panel_to_expand(oz_page):
    for _ in range(20):
        if oz_page.is_panel_expanded():
            return
        time.sleep(0.1)
    raise RuntimeError("did not manage to expand main panel")
