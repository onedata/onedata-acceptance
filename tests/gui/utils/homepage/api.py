"""Utils to facilitate operations on the API page of Onedata homepage."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from dataclasses import dataclass
from enum import Enum
from typing import Self

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    ButtonWithTextPageObject,
    Label,
    WebItem,
    WebItemsSequence,
)
from tests.gui.utils.homepage.documentation_base import (
    BaseDocumentationPage,
    BaseDocumentationSidebar,
)


class ServiceType(Enum):
    ONEPROVIDER = "Oneprovider"
    ONEPANEL = "Onepanel"
    ONEZONE = "Onezone"


@dataclass(frozen=True)
class EndpointInfo:
    method: str
    name: str
    category: str
    service_type: ServiceType

    @property
    def chapter(self) -> str:
        return f"{self.service_type.value} REST API"

    @property
    def reference_title(self) -> str:
        return f"{self.service_type.value} API Reference"

    @classmethod
    def space(cls, method: str, name: str) -> Self:
        return cls(
            method=method,
            name=name,
            category="Space",
            service_type=ServiceType.ONEZONE,
        )

    @classmethod
    def file_details(cls, method: str, name: str, category: str) -> Self:
        return cls(
            method=method,
            name=name,
            category=category,
            service_type=ServiceType.ONEPROVIDER,
        )


class GuiRestCommand(PageObject):
    endpoint_title = Label(".api-command-title")
    endpoint_method = Label(".api-command-type")


class WebRestCommand(ButtonWithTextPageObject):
    endpoint_title = Label(".method-summary")
    endpoint_method = Label(".method-badge")


class ApiSidebar(BaseDocumentationSidebar):
    endpoint_rows = WebItemsSequence("a", cls=WebRestCommand)

    def get_active_endpoints(self) -> list[WebRestCommand]:
        return [endpoint for endpoint in self.endpoint_rows if endpoint.is_active()]


class APIPage(BaseDocumentationPage):
    sidebar = WebItem(".sidebar-root-list", cls=ApiSidebar)
