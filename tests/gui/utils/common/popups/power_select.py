"""Utils and fixtures to facilitate operations on power-select options"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from collections.abc import Iterable

from selenium.webdriver.remote.webelement import WebElement

from tests.gui.utils.common.constants import CONFLICT_NAME_SEPARATOR
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebElementsSequence
from tests.gui.utils.core.web_objects import PageObjectNotFoundError


class PowerSelect(PageObject):
    items = WebElementsSequence(".ember-power-select-option")
    item_groups = WebElementsSequence(".ember-power-select-group")

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

    def choose_item_with_id(self, property_name: str) -> None:
        separator = CONFLICT_NAME_SEPARATOR
        for item in self.items:
            if item.text.split(separator)[0].strip() == property_name:
                item.click()
                return
        raise PageObjectNotFoundError(f"{property_name} not found in popup menu")

    def __str__(self) -> str:
        return "Power select options"
