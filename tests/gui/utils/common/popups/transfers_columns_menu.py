"""Utils and fixtures to facilitate operations in transfers table
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


class TransfersColumnsMenu(PageObject):
    user = WebItem('.filter-column-checkbox.userName-checkbox',
                   cls=ColumnOption)
    destination = WebItem('.filter-column-checkbox.destination-checkbox',
                          cls=ColumnOption)
    started_at = WebItem('.filter-column-checkbox.startedAt-checkbox',
                         cls=ColumnOption)
    processed = WebItem('.filter-column-checkbox.processed-checkbox',
                        cls=ColumnOption)
    replicated = WebItem('.filter-column-checkbox.replicated-checkbox',
                         cls=ColumnOption)
    evicted = WebItem('.filter-column-checkbox.evicted-checkbox',
                      cls=ColumnOption)
    type = WebItem('.filter-column-checkbox.type-checkbox',
                   cls=ColumnOption)
    status = WebItem('.filter-column-checkbox.status-checkbox',
                     cls=ColumnOption)
