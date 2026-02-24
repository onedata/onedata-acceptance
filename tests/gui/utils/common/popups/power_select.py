"""Utils and fixtures to facilitate operations on power-select options"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.common.constants import CONFLICT_NAME_SEPARATOR
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebElementsSequence


class PowerSelect(PageObject):
    items = WebElementsSequence(".ember-power-select-option")
    item_groups = WebElementsSequence(".ember-power-select-group")

    def _choose_items(self, property_name, items, str_prefix, require_full_match):
        def predicate(item):
            if require_full_match and item.text.lower() == property_name.lower():
                return True
            if not require_full_match and property_name.lower() in item.text.lower():
                return True
            return False

        for item in items:
            if predicate(item):
                item.click()
                return
        raise RuntimeError(f"{str_prefix}{property_name} not found in popup menu")

    def choose_item(self, property_name, require_full_match=True):
        self._choose_items(property_name, self.items, "", require_full_match)

    def choose_group(self, property_name, require_full_match=False):
        self._choose_items(
            property_name, self.item_groups, "item group: ", require_full_match
        )

    def choose_item_with_id(self, property_name):
        separator = CONFLICT_NAME_SEPARATOR
        for item in self.items:
            if item.text.split(separator)[0].strip() == property_name:
                item.click()
                return
        raise RuntimeError(f"{property_name} not found in popup menu")

    def __str__(self):
        return "Power select options"
