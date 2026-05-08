"""Utils to facilitate operations on endpoints in "Docs" page of Onedata documentation"""

__author__ = "Mateusz Zając"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.web_elements import (
    ButtonWithTextPageObject,
    Label,
    WebItem,
    WebItemsSequence,
)
from tests.gui.utils.core.web_objects import PageObject


class DocsSidebar(PageObject):
    category_rows = WebItemsSequence("a", cls=ButtonWithTextPageObject)

    def get_active_rows_names(self):
        return [row.id for row in self.category_rows if row.is_active()]


class DocsPage(PageObject):
    current_header = Label(".docs-main-content h1")
    sidebar = WebItem(".sidebar-root-list", cls=DocsSidebar)

    def __getitem__(self, item):
        if hasattr(self, "elements_list"):
            return self.elements_list[item]
        raise ValueError("there is not elements_list member in class instance")
