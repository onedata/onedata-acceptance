"""Utils and fixtures to facilitate operations on Onezone web GUI."""

__author__ = "Bartosz Walkowicz Michal Stanisz Jakub Karczewski Mateusz Zajac"
__copyright__ = "Copyright (C) 2017-2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import ClassVar, TypeVar

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from tests.gui.utils.core.web_elements import Label, WebElement, WebElementsSequence
from tests.gui.utils.generic import PageName
from tests.gui.utils.onezone.generic_page import GenericPage, SidebarPanelPage
from tests.utils.entities_setup.spaces import WAIT_FRONTEND
from tests.utils.utils import element_has_class, repeat_failed

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

PageT = TypeVar("PageT", bound=GenericPage)


class OZLoggedIn:
    _panel_id_by_page_class: ClassVar[dict[type[SidebarPanelPage], int]] = {
        DataPage: 0,
        SharesPage: 1,
        ProvidersPage: 2,
        GroupsPage: 3,
        TokensPage: 4,
        DiscoveryPage: 5,
        AutomationPage: 6,
        ClustersPage: 7,
    }

    _atlas = WebElement(".onezone-atlas")
    _sidebar_menu = WebElement(".main-menu-column")
    _panels = WebElementsSequence(".main-menu-content li.main-menu-item")
    _profile = WebElement(".app-layout")

    uploads_web_elem = WebElement(".main-menu-column .main-menu-upload-item")

    provider_alert_message = Label(".content-info-content-container .text-center")

    profile_username = Label(".main-menu-column .user-account-button-username")

    def __init__(self, driver: WebDriver) -> None:
        self.web_elem = driver

    def __str__(self) -> str:
        return "Onezone page"

    @classmethod
    def get_page_class(cls, page_name: PageName) -> type[SidebarPanelPage]:
        expected_name = "clusters" if page_name == "cluster" else page_name
        for page_cls in cls._panel_id_by_page_class:
            if page_cls.panel_name == expected_name:
                return page_cls
        raise KeyError(page_name)

    @classmethod
    def _get_panel_id(cls, panel_name: PageName) -> int:
        return cls._panel_id_by_page_class[cls.get_page_class(panel_name)]

    def _panel_has_class(self, panel_name: PageName, class_name: str) -> bool:
        panel_id = self._get_panel_id(panel_name)
        return element_has_class(self._panels[panel_id], class_name)

    def is_panel_menu_expanded(self) -> bool:
        return element_has_class(self._sidebar_menu, "expanded")

    def is_panel_disabled(self, panel_name: PageName) -> bool:
        return self._panel_has_class(panel_name, "disabled")

    def is_panel_active(self, panel_name: PageName) -> bool:
        return self._panel_has_class(panel_name, "active")

    def is_panel_selected(self, panel_name: PageName) -> bool:
        return self._panel_has_class(panel_name, "selected")

    @repeat_failed(timeout=WAIT_FRONTEND)
    def click_on_sidebar_menu_panel(self, panel_name: PageName) -> None:
        panel_id = self._get_panel_id(panel_name)
        self._panels[panel_id].click()

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

    def open_panel(self, page_cls: type[PageT]) -> None:
        if issubclass(page_cls, SidebarPanelPage):
            panel_name = page_cls.panel_name
            if self.is_panel_active(panel_name):
                return

        self.expand_panel_if_needed()

        if page_cls is UploadsPage:
            self.uploads_web_elem.click()
        elif issubclass(page_cls, SidebarPanelPage):
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
        return UploadsPage(self.web_elem, self.web_elem, parent=self)
