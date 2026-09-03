"""Utils and fixtures to facilitate operations on power-select options"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from collections.abc import Iterable

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebElementsSequence
from tests.gui.utils.core.web_objects import (
    PageObjectNotFoundError,
    PageObjectsSequence,
)


class PowerSelect(PageObject):
    _items = WebElementsSequence(".ember-power-select-option")
    item_groups = WebElementsSequence(".ember-power-select-group")

    def __init__(
        self,
        driver: WebDriver,
        web_elem: WebElement,
        parent: object | None = None,
        item_cls: type[PageObject] | None = None,
        object_name: str = "",
    ) -> None:
        super().__init__(driver, web_elem, parent, object_name=object_name)
        self.item_cls = item_cls

    @property
    def items(self) -> list[WebElement] | PageObjectsSequence:
        if self.item_cls is None:
            return self._items
        return self.items_as(self.item_cls)

    def items_as(self, item_cls: type[PageObject]) -> PageObjectsSequence:
        return PageObjectsSequence(self.driver, self._items, item_cls, self)

    def _choose_items(
        self,
        property_name: str,
        items: Iterable[WebElement],
        str_prefix: str,
        require_full_match: bool,
    ) -> None:
        normalized_property_name = property_name.casefold()
        match_func = (
            (lambda item: normalized_property_name == item.text.casefold())
            if require_full_match
            else (lambda item: normalized_property_name in item.text.casefold())
        )

        for item in items:
            if match_func(item):
                item.click()
                return

        raise PageObjectNotFoundError(
            f"{str_prefix}{normalized_property_name} not found in popup menu"
        )

    def choose_item(self, property_name: str, require_full_match: bool = True) -> None:
        self._choose_items(property_name, self.items, "", require_full_match)

    def choose_group(
        self, property_name: str, require_full_match: bool = False
    ) -> None:
        self._choose_items(
            property_name, self.item_groups, "item group: ", require_full_match
        )

    def __str__(self) -> str:
        return "Power select options"
