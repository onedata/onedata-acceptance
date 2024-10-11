"""Utils and fixtures to facilitate operations on power-select options"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

from tests.gui.utils.common.constants import CONFLICT_NAME_SEPARATOR
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebElementsSequence


class PowerSelect(PageObject):
    items = WebElementsSequence(".ember-power-select-option")

    def choose_item(self, property_name):
        for item in self.items:
            if item.text.lower() == property_name.lower():
                item.click()
                return
        raise RuntimeError(f"{property_name} not found in popup menu")

    def choose_item_with_id(self, property_name):
        separator = CONFLICT_NAME_SEPARATOR
        for item in self.items:
            if item.text.split(separator)[0].strip() == property_name:
                item.click()
                return
        raise RuntimeError(f"{property_name} not found in popup menu")

    def __str__(self):
        return "Power select options"
