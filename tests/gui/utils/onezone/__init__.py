"""Utils and fixtures to facilitate operations on Onezone web GUI."""

__author__ = "Bartosz Walkowicz Michal Stanisz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement
from selenium.webdriver.support.ui import WebDriverWait

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebElement, WebElementsSequence
from tests.utils.bdd_utils import Any
from tests.utils.entities_setup.spaces import WAIT_FRONTEND
from tests.utils.utils import cast

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
    _sidebar_menu = WebElement(".main-menu-column")
    _panels = WebElementsSequence(".main-menu-content li.main-menu-item")
    _profile = WebElement(".app-layout")

    uploads_web_elem = WebElement(".main-menu-column .main-menu-upload-item")

    provider_alert_message = Label(".content-info-content-container .text-center")

    profile_username = Label(".main-menu-column .user-account-button-username")

    panels_classes: dict[str, type[PageObject]] = {
        "data": DataPage,
        "shares": SharesPage,
        "providers": ProvidersPage,
        "groups": GroupsPage,
        "tokens": TokensPage,
        "discovery": DiscoveryPage,
        "automation": AutomationPage,
        "clusters": ClustersPage,
        "cluster": ClustersPage,
    }

    def __init__(self, driver: WebDriver) -> None:
        self.web_elem = driver

    def __str__(self) -> str:
        return "Onezone page"

    def _element_has_class(
        self,
        element: SeleniumWebElement,
        class_name: str,
    ) -> bool:
        element_class = element.get_attribute("class") or ""
        return class_name in element_class

    def _panel_has_class(self, item: str, class_name: str) -> bool:
        return self._element_has_class(self.get_panel_by_name(item), class_name)

    def is_panel_menu_expanded(self) -> bool:
        try:
            _ = self._sidebar_menu
        except RuntimeError:
            self.web_elem.switch_to.default_content()
        return self._element_has_class(self._sidebar_menu, "expanded")

    def is_panel_disabled(self, item: str) -> bool:
        return self._panel_has_class(item, "disabled")

    def is_panel_active(self, item: str) -> bool:
        return self._panel_has_class(item, "active")

    def is_panel_selected(self, item: str) -> bool:
        return self._panel_has_class(item, "selected")

    def get_panel_by_name(self, name: str) -> SeleniumWebElement:
        if not self.is_panel_menu_expanded():
            raise RuntimeError(
                f'cannot get "{name}" panel, because main panel is not expanded'
            )
        name = name.lower()
        for panel in self._panels:
            panel_name = panel.text.lower()
            if panel_name == name:
                return panel
            if name == "cluster" and panel_name == "clusters":
                return panel
            if name == "clusters" and panel_name == "cluster":
                return panel
        raise RuntimeError(f'no "{name}" on {self} found')

    def click_on_sidebar_menu_panel(self, name: str) -> None:
        panel = self.get_panel_by_name(name)
        panel.click()

    def _wait_for_panel_to_expand(self) -> None:
        WebDriverWait(self.web_elem, WAIT_FRONTEND).until(
            lambda _: self.is_panel_menu_expanded(),
            message="did not manage to expand main panel",
        )

    def expand_panel_if_needed(self) -> None:
        if self.is_panel_menu_expanded():
            return
        ActionChains(self.web_elem).move_to_element(self._sidebar_menu).perform()
        self._wait_for_panel_to_expand()

    def _panel_page(self, name: str) -> PageObject:
        page_cls = self.panels_classes[name]
        return page_cls(self.web_elem, self.web_elem, parent=self)

    def get_page(self, item: str) -> Any:
        # returns GenericPage subclasses
        item = item.lower()
        if item not in self.panels_classes:
            raise RuntimeError(f'no "{item}" on {self} found')
        self.expand_panel_if_needed()

        if not self.is_panel_selected(item):
            self.click_on_sidebar_menu_panel(item)

        return self._panel_page(item)

    @property
    def data(self) -> DataPage:
        return cast(DataPage, self._panel_page("data"))

    @property
    def shares(self) -> SharesPage:
        return cast(SharesPage, self._panel_page("shares"))

    @property
    def providers(self) -> ProvidersPage:
        return cast(ProvidersPage, self._panel_page("providers"))

    @property
    def groups(self) -> GroupsPage:
        return cast(GroupsPage, self._panel_page("groups"))

    @property
    def tokens(self) -> TokensPage:
        return cast(TokensPage, self._panel_page("tokens"))

    @property
    def discovery(self) -> DiscoveryPage:
        return cast(DiscoveryPage, self._panel_page("discovery"))

    @property
    def automation(self) -> AutomationPage:
        return cast(AutomationPage, self._panel_page("automation"))

    @property
    def clusters(self) -> ClustersPage:
        return cast(ClustersPage, self._panel_page("clusters"))

    @property
    def cluster(self) -> ClustersPage:
        return self.clusters

    @property
    def profile(self) -> ManageAccountPage:
        return ManageAccountPage(self.web_elem, self._profile, parent=self)

    @property
    def uploads(self) -> UploadsPage:
        return UploadsPage(self.web_elem, self.web_elem, parent=self)
