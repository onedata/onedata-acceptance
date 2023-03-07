"""Utils and fixtures to facilitate operations on Store details modal.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button, NamedButton, \
    WebItemsSequence, Label
from tests.gui.utils.onezone.generic_page import Element
from ..modal import Modal


class FilterTab(Element):
    name = id = Label('.column-name')


class StoreDetailsObjectRow(PageObject):
    name = id = Label('.column-object-property')


class StoreDetailsListRow(PageObject):
    name = id = Label('.column-name')


class StoreDetails(Modal):
    close = Button('.modal-header .close')
    copy_button = Button('.copy-link')

    tabs = WebItemsSequence('.nav-tabs .ember-view', cls=FilterTab)
    store_content_list = WebItemsSequence('.entries-table .data-row',
                                          cls=StoreDetailsListRow)
    store_content_object = WebItemsSequence('.entries-table .data-row',
                                            cls=StoreDetailsObjectRow)

    def __str__(self):
        return 'Store details modal'