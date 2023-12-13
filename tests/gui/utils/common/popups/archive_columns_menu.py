"""Utils and fixtures to facilitate operations in archive browser
columns menu popup.
"""

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItem

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


class ColumnOption(PageObject):
    def select(self):
        if 'unselected' in self.web_elem.get_attribute('class'):
            self.web_elem.click()

    def unselect(self):
        if 'checked' in self.web_elem.get_attribute('class'):
            self.web_elem.click()


class ArchiveColumnsMenu(PageObject):
    state = WebItem('.filter-column-checkbox.state-checkbox', cls=ColumnOption)
    base_archive = WebItem('.filter-column-checkbox.incremental-checkbox',
                           cls=ColumnOption)
    creator = WebItem('.filter-column-checkbox.creator-checkbox',
                      cls=ColumnOption)
