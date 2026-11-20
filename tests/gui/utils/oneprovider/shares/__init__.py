"""Utils and fixtures to facilitate operation on shares in Oneprovider GUI"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from collections.abc import Collection

from tests.gui.constants import WAIT_FRONTEND
from tests.gui.utils.core.base import NamedElement
from tests.gui.utils.core.web_elements import (
    Button,
    Input,
    Label,
    WebElement,
    WebItemsSequence,
)
from tests.gui.utils.oneprovider.browser import Browser
from tests.gui.utils.onezone.virtualized_list_page import (
    DEFAULT_SCROLLBAR_SELECTOR,
    ScrollAnchors,
    VirtualizedListPage,
)
from tests.utils.utils import repeat_failed

from ..breadcrumbs import Breadcrumbs
from ..file_browser import FileBrowser

SHARES_SELECTOR_PREFIX = ".share-list-item.data-row:nth-of-type"


class SharesOptions(NamedElement):
    name = id = Label(".item-name", scroll=False)
    menu_button = Button(".menu-toggle-frame", scroll=False)
    icon = WebElement(".one-icon-tag-icon", scroll=False)

    def points_to_del_dir(self) -> bool:
        return "oneicon-x" in self.icon.get_attribute("class")


class SharesContentPage(Browser, VirtualizedListPage[SharesOptions]):
    item_selector_prefix = SHARES_SELECTOR_PREFIX
    item_cls = SharesOptions
    scroll_shift = 6
    initial_window_offset = 6
    next_window_offset = -6

    no_shares_msg = Label(".content-info-content-container")
    name = Label(".file-browser .fb-breadcrumbs-dir > .truncate")
    shares_list = WebItemsSequence(".one-collapsible-list .list-header-row", cls=SharesOptions)
    path = Breadcrumbs(".share-header-path")
    url = Input(".clipboard-input.form-control")
    copy_icon = Button(".copy-btn-icon")
    breadcrumbs = Breadcrumbs(".file-browser-head-container")
    menu_button = Button(".menu-toggle-frame")
    shares_file_browser = FileBrowser(".file-browser")

    description_tab = Button(".nav-link-description")
    create_description = Button(".btn-content-info")
    description_input = Input(".code-textarea")
    save_description = Button(".btn-primary")
    switch_editor_markdown = Button(".btn-switch-editor-mode")
    editor_mode = Label(".btn-switch-editor-mode .text")
    link_type_selector = Button(".share-link-type-selector-trigger")

    def get_visible_items(self) -> list[SharesOptions]:
        return self.get_visible_shares_list()

    def get_all_rendered_items(self) -> Collection[SharesOptions]:
        return self.shares_list

    def scroll_to_list_top(self) -> None:
        self.scroll_to_top()

    @repeat_failed(timeout=WAIT_FRONTEND)
    def get_visible_shares_list(self) -> list[SharesOptions]:
        return [share for share in self.shares_list if share.name != ""]

    def get_initial_and_next_scroll_anchors(self) -> ScrollAnchors:
        return ScrollAnchors(20, 20)

    def scroll_to_top(
        self, timeout: float = WAIT_FRONTEND, selector: str = DEFAULT_SCROLLBAR_SELECTOR
    ) -> None:
        # Overrides function scroll_to_top from class Browser
        VirtualizedListPage.scroll_to_top(self, timeout, selector)
