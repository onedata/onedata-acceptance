"""Utils to facilitate operations on shares page in Onezone gui"""

__author__ = "Jakub Pilch"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from collections.abc import Collection

from tests.gui.constants import DEFAULT_SCREEN_SIZE, WAIT_FRONTEND, ScreenSize
from tests.gui.utils.core.base import NamedElement
from tests.gui.utils.core.web_elements import Label, WebItemsSequence
from tests.gui.utils.onezone.generic_page import SidebarPanelPage
from tests.gui.utils.onezone.virtualized_list_page import (
    ScrollAnchors,
    VirtualizedListPage,
)
from tests.utils.utils import repeat_failed

SHARES_SIDEBAR_SELECTOR_PREFIX = ".sidebar-shares .one-list-item.data-row:nth-of-type"
NEXT_SCROLL_SHIFT = 9
CONST_SCROLL_IDX = 24
SHARES_SCROLLBAR = ".perfect-scrollbar-element.ps--active-y:not(.col-sidebar)"


class SharesSidebarRecord(NamedElement):
    name = id = Label(".sidebar-item-title-upper .one-label", scroll=False)
    space_name = Label(".sidebar-item-title-lower .space-name", scroll=False)


class SharesPage(SidebarPanelPage, VirtualizedListPage[SharesSidebarRecord]):
    panel_name = "shares"
    item_cls = SharesSidebarRecord
    item_selector_prefix = SHARES_SIDEBAR_SELECTOR_PREFIX
    scroll_shift = NEXT_SCROLL_SHIFT
    next_window_offset = -10

    shares_list = WebItemsSequence(".sidebar-shares .one-list-item", cls=SharesSidebarRecord)

    def get_visible_items(self) -> list[SharesSidebarRecord]:
        return self.get_visible_shares_list()

    def get_all_rendered_items(self) -> Collection[SharesSidebarRecord]:
        return self.shares_list

    def scroll_to_list_top(self, timeout: float = WAIT_FRONTEND) -> None:
        self.scroll_to_top(timeout=timeout, selector=SHARES_SCROLLBAR)

    @repeat_failed(timeout=WAIT_FRONTEND)
    def get_visible_shares_list(self) -> list[SharesSidebarRecord]:
        return [share for share in self.shares_list if share.name != ""]

    def get_initial_and_next_scroll_anchors(self) -> ScrollAnchors:
        return ScrollAnchors(20 if DEFAULT_SCREEN_SIZE == ScreenSize.MEDIUM else 24, 24)
