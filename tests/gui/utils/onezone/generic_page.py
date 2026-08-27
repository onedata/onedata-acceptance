"""Utils to facilitate operations on pages in Onezone gui"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from abc import ABCMeta
from collections.abc import Iterable
from inspect import getattr_static
from typing import Any, ClassVar

from tests.gui.utils.common.constants import WAIT_FRONTEND
from tests.gui.utils.core.base import PageObject, PageObjectMeta
from tests.gui.utils.core.web_elements import Label, NamedButton
from tests.gui.utils.generic import ListElement, PageName
from tests.utils.utils import repeat_failed


class Element(PageObject):
    name = id = Label(".one-label")

    def __call__(self, *args: object, **kwargs: object) -> None:
        self.web_elem.click()


class GenericPageMeta(PageObjectMeta, ABCMeta):
    pass  # this class is needed to avoid metaclass conflict between PageObjectMeta and ABCMeta


# TODO: VFS-13694 simplify generic page
class GenericPage(PageObject, metaclass=GenericPageMeta):
    name = id = Label(".row-heading .col-title")
    get_started = NamedButton(".btn-default", text="Get started")

    @staticmethod
    def _list_attr_name(list_element: ListElement) -> str:
        return f"{list_element.value.replace(' ', '_')}_list"

    def _get_items_list(self, list_element: ListElement) -> Any:
        attr_list = self._list_attr_name(list_element)
        list_descriptor = getattr_static(self, attr_list)
        if isinstance(list_descriptor, property):
            raise AttributeError(attr_list)
        if hasattr(list_descriptor, "__get__"):
            return list_descriptor.__get__(  # pylint: disable=unnecessary-dunder-call
                self, type(self)
            )
        return list_descriptor

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
        for attribute in ListElement:
            try:
                return self._get_items_list(attribute)[item]
            except AttributeError:
                pass
        raise ValueError("there is not any elements list member in class instance")

    @staticmethod
    @repeat_failed(timeout=WAIT_FRONTEND)
    def get_visible_elements_list(
        elements_list: Iterable[Element], main_field: str = "name"
    ) -> list[Element]:
        return [element for element in elements_list if getattr(element, main_field)]


class SidebarPanelPage(GenericPage):
    panel_name: ClassVar[PageName]
