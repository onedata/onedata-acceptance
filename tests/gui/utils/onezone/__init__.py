"""Utils and fixtures to facilitate operations on Onezone web GUI."""

__author__ = "Bartosz Walkowicz Michal Stanisz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

import time
from time import sleep

from selenium.webdriver.common.action_chains import ActionChains
from tests.gui.utils.core.web_elements import (
    Label,
    WebElement,
    WebElementsSequence,
)

from .automation_page import AutomationPage
from .clusters_page import ClustersPage
from .common import OZPanel
from .data_page import DataPage
from .discovery_page import DiscoveryPage
from .groups.groups_page import GroupsPage
from .manage_account_page import ManageAccountPage
from .providers_page import ProvidersPage
from .shares_page import SharesPage
from .tokens_page import TokensPage
from .uploads_page import UploadsPage

panels_dict = {
    "data": 0,
    "shares": 1,
    "providers": 2,
    "groups": 3,
    "tokens": 4,
    "discovery": 5,
    "automation": 6,
    "clusters": 7,
}


class OZLoggedIn:
    _atlas = WebElement(".onezone-atlas")
    _panels = WebElementsSequence(".main-menu-content li.main-menu-item")
    _profile = WebElement(".app-layout")

    uploads = WebElement(".main-menu-column .main-menu-upload-item")

    provider_alert_message = Label(
        ".content-info-content-container .text-center"
    )

    profile_username = Label(".main-menu-column .user-account-button-username")

    panels = {
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

    def is_panel_clicked(self, item):
        for idx, panel in enumerate(self._panels):
            if idx != panels_dict[item] and (
                "selected" in panel.get_attribute("class")
            ):
                return False
        panel = self._panels[panels_dict[item]]
        return any(
            el in panel.get_attribute("class") for el in ["active", "selected"]
        )

    def get_panels(self):
        return self._panels

    def get_profile(self):
        return self._profile


def get_page(oz_page, item, click=True):
    item = item.lower()
    cls = oz_page.panels.get(item, None)
    if cls:
        item = item.replace("_", " ").lower()
        panel = oz_page.get_panels()[panels_dict[item]]
        if click:
            panel.click()
            # wait till panel will open
            wait_for_panel_to_expand(oz_page)
        return cls(oz_page.web_elem, oz_page.web_elem, parent=oz_page)
    if item == "profile":
        return ManageAccountPage(
            oz_page.web_elem, oz_page.get_profile(), oz_page
        )
    if item == "uploads":
        return UploadsPage(oz_page.web_elem, oz_page.web_elem, oz_page)
    raise RuntimeError(f'no "{item}" on {oz_page} found')


def wait_for_panel_to_expand(oz_page):
    for _ in range(20):
        if oz_page.get_panels()[0].text == "DATA":
            return
        time.sleep(0.1)
    raise RuntimeError("did not manage to expand main panel")
