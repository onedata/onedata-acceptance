"""Utils to facilitate operations on sidebar in
data tab in oneprovider web GUI.
"""

from __future__ import annotations

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from collections.abc import Iterator

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement

from tests.gui.utils.core.base import ExpandableMixin, PageObject
from tests.gui.utils.core.web_elements import (
    Label,
    WebElement,
    WebElementsSequence,
    WebItem,
)
from tests.gui.utils.core.web_objects import PageObjectNotFoundError
from tests.gui.utils.oneprovider.data_tab.space_selector import SpaceSelector


class DataTabSidebar(PageObject):
    space_selector = WebItem(".data-spaces-select", cls=SpaceSelector)
    _root_dir = WebElementsSequence(
        ".data-files-tree ul:not(.dropdown-menu) li:not(.clickable)"
    )

    def __init__(
        self,
        driver: WebDriver,
        web_elem: SeleniumWebElement,
        parent: object | None = None,
        *,
        resize_handler: SeleniumWebElement,
    ) -> None:
        self._resize_handler = resize_handler
        super().__init__(driver, web_elem, parent)

    def __str__(self) -> str:
        return f"sidebar in {self.parent}"

    @property
    def width(self) -> int:
        return self._resize_handler.location["x"]

    @width.setter
    def width(self, value: int) -> None:
        offset = value - self.width
        action = ActionChains(self.driver)
        action.drag_and_drop_by_offset(self._resize_handler, offset, 0)
        action.perform()

    @property
    def root_dir(self) -> DirectoryTree:
        root, root_content = self._root_dir[:2]
        return DirectoryTree(self.driver, root, self, children=root_content)

    @property
    def cwd(self) -> DirectoryTree:
        return self._cwd(self.root_dir)

    def _cwd(self, curr_dir: DirectoryTree) -> DirectoryTree:
        if curr_dir.is_active():
            return curr_dir
        for directory in curr_dir:
            cwd = self._cwd(directory)
            if cwd:
                return cwd
        raise PageObjectNotFoundError("no working directory found")


class DirectoryTree(PageObject, ExpandableMixin):
    name = Label(".item-label")
    _toggle = WebElement(".item-icon .one-icon")
    _header = WebElement(".secondary-sidebar-item.dir-item")
    _click_area = WebElement(".secondary-sidebar-item.dir-item .item-click-area")
    _header_label = WebElement(
        ".secondary-sidebar-item.dir-item .truncate-secondary-sidebar-item"
    )

    def __init__(
        self,
        driver: WebDriver,
        web_elem: SeleniumWebElement,
        parent: object | None = None,
        *,
        children: SeleniumWebElement,
    ) -> None:
        self._children = children
        super().__init__(driver, web_elem, parent)

    def __str__(self) -> str:
        return f"DirectoryTree({self.pwd()}) in {self.parent}"

    def __iter__(self) -> Iterator[DirectoryTree]:
        css_selector = "ul.data-files-tree-list li:not(.clickable)"
        elements = self._children.find_elements(By.CSS_SELECTOR, css_selector)
        for dir_tree in elements:
            yield DirectoryTree(self.driver, dir_tree, self, children=dir_tree)

    def __getitem__(self, name: str) -> DirectoryTree:
        for directory in self:
            if directory.name == name:
                return directory
        raise PageObjectNotFoundError(f'no subdirectory named "{name}" found in {self}')

    def is_expanded(self) -> bool:
        return "open" in self._toggle.get_attribute("class")

    def is_active(self) -> bool:
        return "active" in self._header.get_attribute("class")

    def pwd(self) -> str:
        if not isinstance(self.parent, DirectoryTree):
            return "/"
        return f"{self.parent.pwd()}{self.name}/"

    @property
    def displayed_name_width(self) -> int:
        return self.driver.execute_script(
            "return $(arguments[0]).width();", self._header_label
        )
