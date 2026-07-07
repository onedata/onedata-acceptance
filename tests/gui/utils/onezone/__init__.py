"""Utils and fixtures to facilitate operations on Onezone web GUI."""

__author__ = "Bartosz Walkowicz Michal Stanisz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Literal

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement
from selenium.webdriver.support.ui import WebDriverWait

from tests.gui.utils.core.web_elements import Label, WebElement, WebElementsSequence
from tests.gui.utils.onezone.generic_page import GenericPage
from tests.utils.entities_setup.spaces import WAIT_FRONTEND
from tests.utils.utils import element_has_class

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

PageName = Literal[
    "data",
    "shares",
    "providers",
    "groups",
    "tokens",
    "discovery",
    "automation",
    "clusters",
    "cluster",
]


class OZLoggedIn:
    _atlas = WebElement(".onezone-atlas")
    _sidebar_menu = WebElement(".main-menu-column")
    _panels = WebElementsSequence(".main-menu-content li.main-menu-item")
    _profile = WebElement(".app-layout")

    uploads_web_elem = WebElement(".main-menu-column .main-menu-upload-item")

    provider_alert_message = Label(".content-info-content-container .text-center")

    profile_username = Label(".main-menu-column .user-account-button-username")

    panels_classes: dict[PageName, type[GenericPage]] = {
        "data": DataPage,
        "shares": SharesPage,
        "providers": ProvidersPage,
        "groups": GroupsPage,
        "tokens": TokensPage,
        "discovery": DiscoveryPage,
        "automation": AutomationPage,
        "clusters": ClustersPage,
        "cluster": (
            ClustersPage
        ),  # sometimes the panel is called "cluster" instead of "clusters" in the gui
    }

    def __init__(self, driver: WebDriver) -> None:
        self.web_elem = driver

    def __str__(self) -> str:
        return "Onezone page"

    def _panel_has_class(self, item: PageName, class_name: str) -> bool:
        return element_has_class(self.get_panel_by_name(item), class_name)

    def is_panel_menu_expanded(self) -> bool:
        try:
            _ = self._sidebar_menu
        except RuntimeError:
            self.web_elem.switch_to.default_content()
        return element_has_class(self._sidebar_menu, "expanded")

    def is_panel_disabled(self, panel_name: PageName) -> bool:
        return self._panel_has_class(panel_name, "disabled")

    def is_panel_active(self, panel_name: PageName) -> bool:
        return self._panel_has_class(panel_name, "active")

    def is_panel_selected(self, panel_name: PageName) -> bool:
        return self._panel_has_class(panel_name, "selected")

    def get_panel_by_name(self, panel_name: PageName) -> SeleniumWebElement:
        if not self.is_panel_menu_expanded():
            raise RuntimeError(
                f'cannot get "{panel_name}" panel, because main panel is not expanded'
            )
        expected_panel = panel_name
        for panel in self._panels:
            name = panel.text.lower()
            if name == expected_panel:
                return panel
            if name == "cluster" and expected_panel == "clusters":
                return panel
            if name == "clusters" and expected_panel == "cluster":
                return panel
        raise RuntimeError(f'no "{expected_panel}" on {self} found')

    def click_on_sidebar_menu_panel(self, panel_name: PageName) -> None:
        panel = self.get_panel_by_name(panel_name)
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

    def open_panel(self, panel_name: PageName) -> None:
        self.expand_panel_if_needed()
        if not self.is_panel_selected(panel_name):
            self.click_on_sidebar_menu_panel(panel_name)

    @property
    def data(self) -> DataPage:
        return DataPage(self.web_elem, self.web_elem, parent=self)

    @property
    def shares(self) -> SharesPage:
        return SharesPage(self.web_elem, self.web_elem, parent=self)

    @property
    def providers(self) -> ProvidersPage:
        return ProvidersPage(self.web_elem, self.web_elem, parent=self)

    @property
    def groups(self) -> GroupsPage:
        return GroupsPage(self.web_elem, self.web_elem, parent=self)

    @property
    def tokens(self) -> TokensPage:
        return TokensPage(self.web_elem, self.web_elem, parent=self)

    @property
    def discovery(self) -> DiscoveryPage:
        return DiscoveryPage(self.web_elem, self.web_elem, parent=self)

    @property
    def automation(self) -> AutomationPage:
        return AutomationPage(self.web_elem, self.web_elem, parent=self)

    @property
    def clusters(self) -> ClustersPage:
        return ClustersPage(self.web_elem, self.web_elem, parent=self)

    @property
    def cluster(self) -> ClustersPage:
        return self.clusters

    @property
    def profile(self) -> ManageAccountPage:
        return ManageAccountPage(self.web_elem, self._profile, parent=self)

    @property
    def uploads(self) -> UploadsPage:
        return UploadsPage(self.web_elem, self.uploads_web_elem, parent=self)
