"""Utils and fixtures to facilitate operations on various web objects in web GUI."""

from tests.gui.utils.generic import nth

from .base import PageObject

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


class ButtonPageObject(PageObject):
    name = "button"
    item_not_found_msg = "{text} btn not found in {parent}"

    def __str__(self):
        return f"{self.name} btn in {self.parent}"

    def __call__(self):
        self.click()

    def is_enabled(self):
        return (
            self.web_elem.is_enabled()
            and "disabled" not in self.web_elem.get_attribute("class")
        )

    def is_active(self):
        return "active" in self.web_elem.get_attribute("class")


class ButtonWithTextPageObject(ButtonPageObject):
    def __str__(self):
        return f'{self.name} btn with "{self.text}" text in {self.parent}'

    @property
    def text(self):
        return self.web_elem.text

    id = text


class PageObjectsSequence:

    def __init__(self, driver, items, cls, parent=None):
        self.driver = driver
        self.items = items
        self.cls = cls
        self.parent = parent

    def _getitem_by_id(self, sel):
        for item in self:
            if item.id == sel:
                return item
        return None

    def _getitem_by_idx(self, idx):
        return nth(self.items, idx) if idx < len(self) else None

    def __iter__(self):
        return (self.cls(self.driver, item, self.parent) for item in self.items)

    def __reversed__(self):
        return (
            self.cls(self.driver, item, self.parent)
            for item in reversed(self.items)
        )

    def __getitem__(self, sel):
        if isinstance(sel, int):
            item = self._getitem_by_idx(sel)
            if item:
                return self.cls(self.driver, item, self.parent)
            raise RuntimeError(
                "Index out of bound. Requested item at "
                f"{sel} while limit is {len(self)} in "
                f"{self.parent}"
            )
        if isinstance(sel, str):
            item = self._getitem_by_id(sel)
            if item:
                return item
            raise RuntimeError(f'no "{sel}" found in {self.parent}')
        return None

    def __contains__(self, item):
        if isinstance(item, self.cls):
            item = item.id
        return self._getitem_by_id(item) is not None

    def __len__(self):
        return len(self.items)

    def count(self):
        return len(self)

    def index(self, item_for_idx):
        if isinstance(item_for_idx, self.cls):
            item_searched = item_for_idx.id
        else:
            item_searched = item_for_idx

        for i, item in enumerate(self):
            if item.id == item_searched:
                return i
        return None
