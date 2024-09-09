"""Utils and fixtures to facilitate operations in configure
columns menu popup.
"""

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (Label, WebItemsSequence,
                                               WebElement)

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


class ColumnOption(PageObject):
    name = id = Label('.column-name-label .truncate')
    checkbox = WebElement('.filter-column-checkbox')

    def select(self):
        if 'unselected' in self.checkbox.get_attribute('class'):
            self.checkbox.click()

    def unselect(self):
        if 'checked' in self.checkbox.get_attribute('class'):
            self.checkbox.click()


class ConfigureColumnsMenu(PageObject):
    columns = WebItemsSequence('.column-item', cls=ColumnOption)
