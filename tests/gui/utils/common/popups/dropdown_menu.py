"""Utils and fixtures to facilitate operations on dropdown menu popup.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebItemsSequence


class Item(PageObject):
    name = id = Label('.text')

    def __call__(self):
        self.click()


class DropdownMenu(PageObject):
    items = WebItemsSequence('.ember-power-select-option', cls=Item)

    def __str__(self):
        return 'Dropdown menu popup'
