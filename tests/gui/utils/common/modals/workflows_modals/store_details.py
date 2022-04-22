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
    expander = Button('.oneicon-arrow-down')


class StoreDetails(Modal):
    close = NamedButton('.btn-default', text='Close')
    copy_button = Button('.copy-btn-icon')

    details_list = WebItemsSequence('.store-content-table tr.data-row',
                                    cls=StoreDetailsRow)

    def __str__(self):
        return 'Store details modal'
