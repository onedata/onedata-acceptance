"""Utils and fixtures to facilitate operations on Store details modal.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button, Input, WebElement, \
    NamedButton, WebItemsSequence
from ..modal import Modal


class StoreDetailsRow(PageObject):
    expander = Button('.entry-expander')
    details_content = Input('code-textarea')
    copy = Button('.clipboard-btn')

    def expand(self):
        self.expander.click()

    def get_content(self):
        self.expander.click()
        content = self.details_content.text
        return content

    def __str__(self):
        return 'Store details row {} in {}'.format(self.name, self.parent)


class StoreDetails(Modal):
    close = NamedButton('.btn-default', text='Close')

    details_list= WebItemsSequence('.store-content-table tr.data-row',
                                         cls=StoreDetailsRow)

    def __str__(self):
        return 'Store details modal'
