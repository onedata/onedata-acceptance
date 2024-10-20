"""Utils to facilitate operations on Onepanel of zone web GUI."""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.utils.common.common import BaseContent, OnePage
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button, Label, WebElement, WebItem
from tests.gui.utils.onezone.members_subpage import MembersPage

from .clusters import ClustersSidebar, WelcomePage
from .deployment import Deployment
from .emergency_passphrase import EmergencyPassphrase
from .init_page import PanelInitPage
from .members import MembersContentPage
from .nodes import NodesContentPage
from .overview import ClusterOverviewPage
from .provider import ProviderContentPage
from .spaces import SpacesContentPage
from .storages import StorageContentPage


class Sidebar(PageObject):
    title = Label(".col-title")
    clusters = WebItem(".one-sidebar", cls=ClustersSidebar)

    def __str__(self):
        return f"{self.title} sidebar in {self.parent}"


class Content(BaseContent):
    _main_content = ".main-content"
    overview = WebItem(_main_content, cls=ClusterOverviewPage)
    welcome = WebItem(_main_content, cls=WelcomePage)
    deployment = WebItem(_main_content, cls=Deployment)
    nodes = WebItem(_main_content, cls=NodesContentPage)
    provider = WebItem(_main_content, cls=ProviderContentPage)
    storages = WebItem(_main_content, cls=StorageContentPage)
    spaces = WebItem(_main_content, cls=SpacesContentPage)
    members = WebItem(_main_content, cls=MembersPage)
    members_emergency_interface = WebItem(_main_content, cls=MembersContentPage)
    emergency_passphrase = WebItem(_main_content, cls=EmergencyPassphrase)


class Onepanel(OnePage):
    init_page = WebItem(".container", cls=PanelInitPage)
    content = WebItem(".col-content", cls=Content)
    _main_sidebar = WebElement("#col-sidebar")
    _sub_sidebar = WebElement("#sidenav-sidebar")
    discard_button = Button(".modal-content .btn-toolbar button")

    @property
    def sidebar(self):
        sidebar = self._sub_sidebar
        if "ps-active-x" not in sidebar.get_attribute("class"):
            sidebar = self._main_sidebar
        return Sidebar(self.driver, sidebar, self)
