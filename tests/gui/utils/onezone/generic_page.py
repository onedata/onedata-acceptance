"""Utils to facilitate operations on pages in Onezone gui"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from abc import ABCMeta
from collections.abc import Iterable

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.types import DynamicObject
from tests.gui.utils.core.base import PageObject, PageObjectMeta
from tests.gui.utils.core.web_elements import Label, NamedButton


class Element(PageObject):
    name = id = Label(".one-label")

    def __call__(self, *args: object, **kwargs: object) -> None:
        self.web_elem.click()


class GenericPageMeta(PageObjectMeta, ABCMeta):
    pass  # this class is needed to avoid metaclass conflict between PageObjectMeta and ABCMeta


class GenericPage(PageObject, metaclass=GenericPageMeta):
    name = id = Label(".row-heading .col-title")
    get_started = NamedButton(".btn-default", text="Get started")

    def __getitem__(self, item: int | str) -> object:
        for attr in ListElement:
            attr_list = f"{attr.value}_list"
            if hasattr(self, attr_list):
                return getattr(self, attr_list)[item]
        raise ValueError("there is not any elements list member in class instance")

    @staticmethod
    @repeat_failed(timeout=WAIT_FRONTEND)
    def get_visible_elements_list(
        elements_list: Iterable[Element], main_field: str = "name"
    ) -> list[Element]:
        return [element for element in elements_list if getattr(element, main_field)]
