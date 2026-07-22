"""Utils and fixtures to facilitate operations on Onezone web GUI."""

__author__ = "Bartosz Walkowicz Michal Stanisz Jakub Karczewski Mateusz Zajac"
__copyright__ = "Copyright (C) 2017-2026 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import ClassVar, TypeVar

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement
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
    _current_page_by_session_id: ClassVar[dict[str, type[GenericPage]]] = {}

    _page_class_by_name: ClassVar[dict[PageName, type[SidebarPanelPage]]] = {
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

    _atlas = WebElement(".onezone-atlas")
    _sidebar_menu = WebElement(".main-menu-column")
    _panels = WebElementsSequence(".main-menu-content li.main-menu-item")
    _profile = WebElement(".app-layout")

    uploads_web_elem = WebElement(".main-menu-column .main-menu-upload-item")

    provider_alert_message = Label(".content-info-content-container .text-center")

    profile_username = Label(".main-menu-column .user-account-button-username")

    def __init__(self, driver: WebDriver) -> None:
        self.web_elem = driver
        self._current_page_by_session_id.setdefault(self._session_id, DataPage)

    @property
    def _session_id(self) -> str:
        session_id = self.web_elem.session_id
        if session_id is None:
            raise RuntimeError("WebDriver has no active session")
        return session_id

    @property
    def current_page_cls(self) -> type[GenericPage]:
        return self._current_page_by_session_id[self._session_id]

    def set_current_page(self, page_cls: type[GenericPage]) -> None:
        self._current_page_by_session_id[self._session_id] = page_cls

    def set_current_page_during_login_logout(
        self, *, is_login: bool, emergency_interface: bool
    ) -> None:
        # Emergency interface sessions always start with `ClustersPage` as the
        # current panel. The previously selected panel may persist after logout
        # and can also carry over between emergency and regular Onezone sessions,
        # so we explicitly reset it after a successful emergency login. Regular
        # Onezone logout logic similarly resets the current panel to `DataPage`,
        # which is the expected default unless the next login uses the emergency
        # interface.
        if is_login and not emergency_interface:
            return

        default_page = ClustersPage if emergency_interface else DataPage
        self.set_current_page(default_page)

    def get_current_page(self) -> type[GenericPage]:
        return self._current_page_by_session_id[self._session_id]

    def update_current_page(self) -> None:
        self.expand_panel_if_needed()
        for page_name, page_cls in self._page_class_by_name.items():
            if self.is_panel_active(page_name):
                self._current_page_by_session_id[self._session_id] = page_cls
                return
        raise RuntimeError("No page is selected")

    def __str__(self) -> str:
        return "Onezone page"

    @staticmethod
    def get_page_class(page_name: PageName) -> type[SidebarPanelPage]:
        return OZLoggedIn._page_class_by_name[page_name]

    def _panel_has_class(self, panel_name: PageName, class_name: str) -> bool:
        return element_has_class(self.get_panel_by_name(panel_name), class_name)

    def is_panel_menu_expanded(self) -> bool:
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
        for panel in self._panels:
            name = panel.text.lower()
            if name == panel_name:
                return panel
            if name == "cluster" and panel_name == "clusters":
                return panel
            if name == "clusters" and panel_name == "cluster":
                return panel
        raise RuntimeError(f'no "{panel_name}" on {self} found')

    @repeat_failed(timeout=WAIT_FRONTEND)
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

    def open_panel(self, page_cls: type[PageT]) -> None:
        if page_cls is self.current_page_cls:
            return

        self.expand_panel_if_needed()

        if page_cls is UploadsPage:
            self.uploads_web_elem.click()
        elif issubclass(page_cls, SidebarPanelPage):
            panel_name = page_cls.panel_name

            if not self.is_panel_selected(panel_name):
                self.click_on_sidebar_menu_panel(panel_name)

        self.set_current_page(page_cls)

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
