"""Utils to facilitate operations on sidebar in
data tab in oneprovider web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from tests.gui.utils.core.base import ExpandableMixin, PageObject
from tests.gui.utils.core.web_elements import (
    Label,
    WebElement,
    WebElementsSequence,
    WebItem,
)
from tests.gui.utils.oneprovider.data_tab.space_selector import SpaceSelector


class DataTabSidebar(PageObject):
    space_selector = WebItem(".data-spaces-select", cls=SpaceSelector)
    _root_dir = WebElementsSequence(
        ".data-files-tree ul:not(.dropdown-menu) li:not(.clickable)"
    )

    def __init__(self, *args, **kwargs):
        self._resize_handler = kwargs.pop("resize_handler")
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"sidebar in {self.parent}"

    @property
    def width(self):
        return self._resize_handler.location["x"]

    @width.setter
    def width(self, value):
        offset = value - self.width
        action = ActionChains(self.driver)
        action.drag_and_drop_by_offset(self._resize_handler, offset, 0)
        action.perform()

    @property
    def root_dir(self):
        root, root_content = self._root_dir[:2]
        return DirectoryTree(self.driver, root, self, children=root_content)

    @property
    def cwd(self):
        return self._cwd(self.root_dir)

    def _cwd(self, curr_dir):
        if curr_dir.is_active():
            return curr_dir
        for directory in curr_dir:
            cwd = self._cwd(directory)
            if cwd:
                return cwd
        raise RuntimeError("no working directory found")


class DirectoryTree(PageObject, ExpandableMixin):
    name = Label(".item-label")
    _toggle = WebElement(".item-icon .one-icon")
    _header = WebElement(".secondary-sidebar-item.dir-item")
    _click_area = WebElement(
        ".secondary-sidebar-item.dir-item .item-click-area"
    )
    _header_label = WebElement(
        ".secondary-sidebar-item.dir-item .truncate-secondary-sidebar-item"
    )

    def __init__(self, *args, **kwargs):
        self._children = kwargs.pop("children")
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"DirectoryTree({self.pwd()}) in {self.parent}"

    def __iter__(self):
        css_sel = "ul.data-files-tree-list li:not(.clickable)"
        return (
            DirectoryTree(self.driver, dir_tree, self, children=dir_tree)
            for dir_tree in self._children.find_elements(
                By.CSS_SELECTOR, css_sel
            )
        )

    def __getitem__(self, name):
        for directory in self:
            if directory.name == name:
                return directory
        raise RuntimeError(f'no subdirectory named "{name}" found in {self}')

    def is_expanded(self):
        return "open" in self._toggle.get_attribute("class")

    def is_active(self):
        return "active" in self._header.get_attribute("class")

    def pwd(self):
        if not isinstance(self.parent, DirectoryTree):
            return "/"
        return f"{self.parent.pwd()}{self.name}/"

    @property
    def displayed_name_width(self):
        return self.driver.execute_script(
            "return $(arguments[0]).width();", self._header_label
        )
