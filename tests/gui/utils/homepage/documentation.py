"""Utils to facilitate operations on "Docs" and "API" pages of Onedata homepage"""

__author__ = "Mateusz Zając"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from dataclasses import dataclass

from tests.gui.utils.core.web_elements import (
    ButtonWithTextPageObject,
    Label,
    WebItem,
    WebItemsSequence,
)
from tests.gui.utils.core.web_objects import PageObject


@dataclass
class EndpointInfo:
    method: str
    name: str
    category: str

    @property
    def label(self) -> str:
        return f"{self.method}\n{self.name}"


class DocsSidebar(PageObject):
    category_rows = WebItemsSequence("a", cls=ButtonWithTextPageObject)
    expanded_folders = WebItemsSequence(
        ".sidebar-folder.expanded", cls=ButtonWithTextPageObject
    )

    def get_active_rows_names(self):
        return [row.id for row in self.category_rows if row.is_active()]

    def get_expanded_folders_names(self):
        return [folder.id.split("\n")[0] for folder in self.expanded_folders]


class DocumentationPage(PageObject):
    current_header = Label(".docs-main-content h1")
    sidebar = WebItem(".sidebar-root-list", cls=DocsSidebar)

    def __getitem__(self, item):
        if hasattr(self, "elements_list"):
            return self.elements_list[item]
        raise ValueError("there is not elements_list member in class instance")


class APIPage(DocumentationPage):
    pass


class DocsPage(DocumentationPage):
    pass
