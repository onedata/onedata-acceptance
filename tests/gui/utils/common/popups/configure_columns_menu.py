"""Utils and fixtures to facilitate operations in configure
columns menu popup.
"""

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Label,
    NamedButton,
    WebElement,
    WebItem,
    WebItemsSequence,
)

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


class ColumnOption(PageObject):
    name = id = Label(".column-name-label .truncate")
    checkbox = WebElement(".filter-column-checkbox")
    modify_column_icon = Button(".modify-column .oneicon-browser-rename")
    remove_column_icon = Button(".remove-column .oneicon-close")

    def select(self):
        if "unselected" in self.checkbox.get_attribute("class"):
            self.checkbox.click()

    def unselect(self):
        if "checked" in self.checkbox.get_attribute("class"):
            self.checkbox.click()

    def hover_to_button_and_click(self, button_type: str, driver):
        btn = getattr(self, f"{button_type}_column_icon")
        ActionChains(driver).move_to_element(btn.web_elem).click(btn.web_elem).perform()


class ColumnEditor(PageObject):
    enter_an_xattr_key = WebElement(
        ".autocomplete-dropdown-field-trigger .ember-power-select-search-input"
    )

    def clear_actual_key(self):
        self.enter_an_xattr_key.send_keys(Keys.CONTROL, "a")
        self.enter_an_xattr_key.send_keys(Keys.BACKSPACE)

    create = NamedButton(".edit-column-btn", text="Create")
    apply_changes = NamedButton(".edit-column-btn", text="Apply")

    column_label = WebElement(".columnLabel-field input")


class ConfigureColumnsMenu(PageObject):
    columns = WebItemsSequence(".column-item", cls=ColumnOption)
    new_xattr_column_button = Button(".new-column-item")
    column_editor = WebItem(".column-editor", cls=ColumnEditor)
