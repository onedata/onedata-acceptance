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

    uploads_button = WebElement(".main-menu-column .main-menu-upload-item")

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

    def open_page_and_click(self, item):
        return self.get_page(item, True)
    
    def find_panels_with_name(self, name):
        return [p for p in self._panels if p.text.lower() == name.lower()]
            
    def get_panel_by_name(self, name):
        panel_found = self.find_panels_with_name(name) 
        if panel_found:
            return panel_found[0]

        alternate_name = {
            "cluster": "clusters",
            "clusters": "cluster",
        }.get(name)

        if alternate_name:
            return self.find_panels_with_name(alternate_name)[0]
        return self.find_panels_with_name(name)[0]

    def is_panel_clicked(self, item):
        panel = self.get_panel_by_name(item)
        return any(el in panel.get_attribute("class") for el in ["active", "selected"])

    def is_panel_disabled(self, item):
        panel = self.get_panel_by_name(item)
        return "disabled" in panel.get_attribute("class")

    def click_on_sidebar_menu_panel(self, name):
        panel = self.get_panel_by_name(name)
        panel.click()
    
    def is_panel_expanded(self):
        return self._panels[0].text == "DATA"

    def expand_panel(self):
        if self.is_panel_expanded():
            return
        ActionChains(self.web_elem).move_to_element(self._sidebar_menu).perform()
        for _ in range(20):
            if self.is_panel_expanded():
                return
            time.sleep(0.1)
        raise RuntimeError("did not manage to expand main panel")

    def get_page(self, item, click=False):
        item = item.lower()
        cls = self.panels_classes.get(item, None)
        if cls:
            if click:
                self.expand_panel()
                self.click_on_sidebar_menu_panel(item)
            return cls(self.web_elem, self.web_elem, parent=self)
        if item == "profile":
            self.expand_panel()
            return ManageAccountPage(self.web_elem, self._profile, self)
        if item == "uploads":
            self.expand_panel()
            return UploadsPage(self.web_elem, self.web_elem, self)
        raise RuntimeError(f'no "{item}" on {self} found')

    @property
    def data(self):
        return self.get_page("data")

    @property
    def shares(self):
        return self.get_page("shares")

    @property
    def providers(self):
        return self.get_page("providers")

    @property
    def groups(self):
        return self.get_page("groups")

    @property
    def tokens(self):
        return self.get_page("tokens")

    @property
    def discovery(self):
        return self.get_page("discovery")

    @property
    def automation(self):
        return self.get_page("automation")

    @property
    def clusters(self):
        return self.get_page("clusters")

    @property
    def profile(self):
        return self.get_page("profile")

    @property
    def uploads(self):
        return self.get_page("uploads")
