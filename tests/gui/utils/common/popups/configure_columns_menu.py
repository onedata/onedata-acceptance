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


class AddOrModifyXattrColumn(PageObject):
    enter_an_xattr_key = WebElement(
        ".autocomplete-dropdown-field-trigger .ember-power-select-search-input"
    )

    def clear_actual_key(self):
        self.enter_an_xattr_key.send_keys(Keys.CONTROL, "a")
        self.enter_an_xattr_key.send_keys(Keys.BACKSPACE)

    create = NamedButton(".edit-column-btn", text="Create")
    apply_changes = NamedButton(".edit-column-btn", text="Apply")

    column_label = WebElement(".columnLabel-field input")


class JsonMode(PageObject):
    whole_document = Button(".clickable.option-all .one-way-radio-control")
    extract_key = Button(".clickable.option-key .one-way-radio-control")
    query = Button(".clickable.option-query .one-way-radio-control")
    # Can be replaced with named button


class NewJsonColumn(PageObject):
    enter_json_key = WebElement(".autocomplete-dropdown-field-trigger")
    column_label = WebElement(".columnLabel-field input")

    choose_mode = WebItem(".jsonType-field.field-edit-mode", cls=JsonMode)
    create = NamedButton(".edit-column-btn", text="Create")
    apply_changes = NamedButton(".edit-column-btn", text="Apply")

    def clear_actual_key(self, driver):
        self.enter_json_key.send_keys(Keys.CONTROL, "a")
        self.enter_json_key.send_keys(Keys.BACKSPACE)


class ConfigureColumnsMenu(PageObject):
    columns = WebItemsSequence(".column-item", cls=ColumnOption)
    new_column_button = Button(".new-column-item")

    choose_xattr = Button(".clickable.option-xattr")
    choose_json = Button(".clickable.option-json")

    new_xattr_column = WebItem(".column-editor", cls=AddOrModifyXattrColumn)
    new_json_column = WebItem(".column-editor", cls=NewJsonColumn)
