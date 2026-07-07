"""Utils to facilitate operations on pages in Onezone gui"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from abc import ABCMeta
from collections.abc import Iterable
from typing import Any, Literal

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.core.base import PageObject, PageObjectMeta, SidebarPanelPage
from tests.gui.utils.core.web_elements import Label, NamedButton
from tests.gui.utils.generic import ListElement
from tests.utils.utils import repeat_failed

PageName = Literal[
    "data",
    "shares",
    "providers",
    "groups",
    "tokens",
    "discovery",
    "automation",
    "clusters",
    "cluster",
]


class Element(PageObject):
    name = id = Label(".one-label")

    def __call__(self, *args: object, **kwargs: object) -> None:
        self.web_elem.click()


class GenericPageMeta(PageObjectMeta, ABCMeta):
    pass  # this class is needed to avoid metaclass conflict between PageObjectMeta and ABCMeta


class GenericPage(SidebarPanelPage, metaclass=GenericPageMeta):
    name = id = Label(".row-heading .col-title")
    get_started = NamedButton(".btn-default", text="Get started")

    @staticmethod
    def _list_attr_name(list_element: ListElement) -> str:
        return f"{list_element.value.replace(' ', '_')}_list"

    def _get_items_list(self, list_element: ListElement) -> Any:
        attr_list = self._list_attr_name(list_element)
        for cls in type(self).__mro__:
            if cls is GenericPage:
                break
            if attr_list in cls.__dict__:
                return getattr(self, attr_list)
        raise AttributeError(
            f'there is not "{attr_list}" elements list member in class instance'
        )

    @property
    def shares_list(self) -> Any:
        return self._get_items_list(ListElement.SHARES)

    @property
    def shares_sidebar_list(self) -> Any:
        return self._get_items_list(ListElement.SHARES_SIDEBAR)

    @property
    def groups_list(self) -> Any:
        return self._get_items_list(ListElement.GROUPS)

    @property
    def groups_headers_list(self) -> Any:
        return self._get_items_list(ListElement.GROUPS_HEADERS)

    @property
    def spaces_list(self) -> Any:
        return self._get_items_list(ListElement.SPACES)

    @property
    def spaces_headers_list(self) -> Any:
        return self._get_items_list(ListElement.SPACES_HEADERS)

    @property
    def files_list(self) -> Any:
        return self._get_items_list(ListElement.FILES)

    @property
    def uploads_list(self) -> Any:
        return self._get_items_list(ListElement.UPLOADS)

    @property
    def providers_list(self) -> Any:
        return self._get_items_list(ListElement.PROVIDERS)

    @property
    def harvesters_list(self) -> Any:
        return self._get_items_list(ListElement.HARVESTERS)

    @property
    def tokens_list(self) -> Any:
        return self._get_items_list(ListElement.TOKENS)

    @property
    def automations_list(self) -> Any:
        return self._get_items_list(ListElement.AUTOMATIONS)

    @property
    def lambdas_list(self) -> Any:
        return self._get_items_list(ListElement.LAMBDAS)

    @property
    def workflows_list(self) -> Any:
        return self._get_items_list(ListElement.WORKFLOWS)

    def __getitem__(self, item: int | str) -> Any:
        for attr in ListElement:
            try:
                return self._get_items_list(attr)[item]
            except AttributeError:
                pass
        raise ValueError("there is not any elements list member in class instance")

    @staticmethod
    @repeat_failed(timeout=WAIT_FRONTEND)
    def get_visible_elements_list(
        elements_list: Iterable[Element], main_field: str = "name"
    ) -> list[Element]:
        return [element for element in elements_list if getattr(element, main_field)]
