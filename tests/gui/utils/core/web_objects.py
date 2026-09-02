"""Utils and fixtures to facilitate operations on various web objects in web GUI."""

from collections.abc import Iterator, Sequence
from typing import Optional, TypeVar

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement

from tests.utils.utils import element_has_class

from .base import PageObject

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


class PageObjectNotFoundError(RuntimeError):
    """Raised when an item cannot be found in a page-object sequence."""


PageObjectT = TypeVar("PageObjectT", bound=PageObject)


class ButtonPageObject(PageObject):
    object_name = "button"
    item_not_found_msg = "{text} btn not found in {parent}"

    def __str__(self) -> str:
        return f"{self.object_name} btn in {self.parent}"

    def __call__(self) -> None:
        self.click()

    def is_enabled(self) -> bool:
        return self.web_elem.is_enabled() and element_has_class(
            self.web_elem, "disabled"
        )

    def is_active(self) -> bool:
        return element_has_class(self.web_elem, "active")


class ButtonWithTextPageObject(ButtonPageObject):
    def __str__(self) -> str:
        return f'{self.object_name} btn with "{self.text}" text in {self.parent}'

    @property
    def text(self) -> str:
        return self.web_elem.text

    id = text


class PageObjectsSequence[PageObjectT: PageObject]:
    def __init__(
        self,
        driver: WebDriver,
        items: Sequence[SeleniumWebElement],
        cls: type[PageObjectT],
        parent: Optional[object] = None,
    ) -> None:
        self.driver = driver
        self.items = items
        self.cls = cls
        self.parent = parent

    def _getitem_by_id(self, sel: object) -> PageObjectT | None:
        for item in self:
            if item.id == sel:
                return item
        return None

    def _getitem_by_idx(self, idx: int) -> SeleniumWebElement | None:
        try:
            return self.items[idx]
        except IndexError:
            return None

    def __iter__(self) -> Iterator[PageObjectT]:
        for item in self.items:
            yield self.cls(self.driver, item, self.parent)

    def __reversed__(self) -> Iterator[PageObjectT]:
        return (
            self.cls(self.driver, item, self.parent) for item in reversed(self.items)
        )

    def __getitem__(self, sel: int | str) -> PageObjectT:
        if isinstance(sel, int):
            item = self._getitem_by_idx(sel)
            if item:
                return self.cls(self.driver, item, self.parent)
            raise PageObjectNotFoundError(
                "Index out of bound. Requested item at "
                f"{sel} while limit is {len(self)} in "
                f"{self.parent}"
            )
        if isinstance(sel, str):
            item = self._getitem_by_id(sel)
            if item:
                return item
            raise PageObjectNotFoundError(f'no "{sel}" found in {self.parent}')
        raise TypeError(f"unsupported selector type: {type(sel).__name__}")

    def __contains__(self, item: object) -> bool:
        if isinstance(item, self.cls):
            item = item.id
        return self._getitem_by_id(item) is not None

    def __len__(self) -> int:
        return len(self.items)

    def count(self) -> int:
        return len(self)

    def index(self, item_for_idx: object) -> int:
        item_searched = (
            item_for_idx.id if isinstance(item_for_idx, self.cls) else item_for_idx
        )

        for i, item in enumerate(self):
            if item.id == item_searched:
                return i

        raise ValueError(f"{item_for_idx!r} is not in PageObjectsSequence")
