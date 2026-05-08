"""Utils to facilitate operations on "API" page of Onedata documentation"""

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

    @property
    def label(self) -> str:
        return f"{self.method}\n{self.name}"


class APISidebar(PageObject):
    category_rows = WebItemsSequence("a", cls=ButtonWithTextPageObject)

    def get_active_rows_names(self):
        return [row.id for row in self.category_rows if row.is_active()]


class APIPage(PageObject):
    current_endpoint = Label(".api-endpoint-title")
    sidebar = WebItem(".sidebar-root-list", cls=APISidebar)

    def __getitem__(self, item):
        if hasattr(self, "elements_list"):
            return self.elements_list[item]
        raise ValueError("there is not elements_list member in class instance")
