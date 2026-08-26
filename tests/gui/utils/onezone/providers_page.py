"""Utils to facilitate operations on providers page in Onezone gui"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)

from tests.gui.utils.core.base import NamedElement
from tests.gui.utils.core.web_elements import (
    Button,
    Label,
    WebElement,
    WebItemsSequence,
)
from tests.gui.utils.onezone.generic_page import SidebarPanelPage
from tests.utils.utils import element_has_class


class Provider(NamedElement):
    name = id = Label(".one-label")
    support_size = Label(".status-toolbar .outer-text")
    supported_spaces_number = Label(".status-toolbar .oneicon-space .inner-text")
    home_icon = WebElement(".status-toolbar-icon:first-of-type span")


class Icon(NamedElement):
    name = id = icon = Button(".circle")


class ProvidersPage(SidebarPanelPage):
    panel_name = "providers"

    _popover = WebElement(".webui-popover .provider-place-drop")
    providers_list = WebItemsSequence(
        ".sidebar-providers li.one-list-item.clickable", cls=Provider
    )
    icons = WebItemsSequence(".provider-place", cls=Icon)
    map_point = Button('.one-map-container .jvectormap-container path[data-code="RO"]')

    def is_working(self) -> bool:
        try:
            popover = self._popover
            return bool(popover and element_has_class(popover, "online"))
        except (NoSuchElementException, StaleElementReferenceException):
            return False
