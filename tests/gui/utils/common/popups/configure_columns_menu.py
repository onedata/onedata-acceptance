"""Utils and fixtures to facilitate operations in configure
columns menu popup.
"""

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

    def select(self):
        if "unselected" in self.checkbox.get_attribute("class"):
            self.checkbox.click()

    def unselect(self):
        if "checked" in self.checkbox.get_attribute("class"):
            self.checkbox.click()

class JsonMode(PageObject):
    whole_document = Button(".clickable.option-all.one-way-radio-control")
    extract_key = Button(".clickable.option-key.one-way-radio-control")
    query = Button(".clickable.option-query.one-way-radio-control")
    # Can be replaced with named button

class NewXattrColumn(PageObject):
    enter_an_xattr_key = WebElement(
        ".autocomplete-dropdown-field-trigger .ember-power-select-search-input"
    )
    create = NamedButton(".edit-column-btn", text="Create")
    column_label = WebElement(".columnLabel-field input")

class NewJsonColumn(PageObject):
    choose_mode = WebItem(".jsonType-field .field-edit-mode")

class ConfigureColumnsMenu(PageObject):
    columns = WebItemsSequence(".column-item", cls=ColumnOption)
    new_xattr_column_button = Button(".new-column-item")
    new_xattr_column = WebItem(".column-editor", cls=NewXattrColumn)
    new_json_column = WebItem(".column-editor", cls = NewJsonColumn)
