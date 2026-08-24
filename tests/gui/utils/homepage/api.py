"""Utils to facilitate operations on the API page of Onedata homepage."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from dataclasses import dataclass

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    ButtonWithTextPageObject,
    Label,
    WebItem,
    WebItemsSequence,
)
from tests.gui.utils.homepage.documentation import (
    DocumentationPage,
    DocumentationSidebar,
)


@dataclass(frozen=True)
class EndpointInfo:
    method: str
    name: str
    category: str
    chapter: str

    @classmethod
    def space(cls, method: str, name: str) -> "EndpointInfo":
        return cls(method, name, "Space", "Onezone REST API")

    @classmethod
    def file_details(cls, method: str, name: str, category: str) -> "EndpointInfo":
        return cls(method, name, category, "Oneprovider REST API")


class GuiRestCommand(PageObject):
    endpoint_title = Label(".api-command-title")
    endpoint_method = Label(".api-command-type")


class WebRestCommand(ButtonWithTextPageObject):
    endpoint_title = Label(".method-summary")
    endpoint_method = Label(".method-badge")


class ApiSidebar(DocumentationSidebar):
    endpoint_rows = WebItemsSequence("a", cls=WebRestCommand)

    def get_active_endpoints(self) -> list[WebRestCommand]:
        return [endpoint for endpoint in self.endpoint_rows if endpoint.is_active()]


class APIPage(DocumentationPage):
    sidebar = WebItem(".sidebar-root-list", cls=ApiSidebar)
