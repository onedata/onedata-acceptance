"""Shared base objects for documentation pages of Onedata homepage."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    ButtonWithTextPageObject,
    Label,
    WebItem,
    WebItemsSequence,
)


class ExpandedFolder(PageObject):
    toggle = WebItem(".folder-toggle", cls=ButtonWithTextPageObject)


class BaseDocumentationSidebar(PageObject):
    expanded_folders = WebItemsSequence(".sidebar-folder.expanded", cls=ExpandedFolder)

    def get_expanded_folders_names(self) -> list[str]:
        return [folder.toggle.text for folder in self.expanded_folders]


class Chapters(PageObject):
    tabs = WebItemsSequence(".chapter-tab", cls=ButtonWithTextPageObject)

    def get_active_chapter_tabs_names(self) -> list[str]:
        return [tab.text for tab in self.tabs if tab.is_active()]


class BaseDocumentationPage(PageObject):
    current_header = Label(".docs-main-content h1")
    sidebar = WebItem(".sidebar-root-list", cls=BaseDocumentationSidebar)
    chapters = WebItem(".docs-tabs-row", cls=Chapters)

    def __getitem__(self, item: str) -> PageObject:
        if hasattr(self, "elements_list"):
            return self.elements_list[item]
        raise AttributeError("there is not elements_list member in class instance")
