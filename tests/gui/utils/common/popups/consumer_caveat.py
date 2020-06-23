"""Utils and fixtures to facilitate operations on consumer caveat popup.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Label, WebItemsSequence, Button, WebElement, Input)


class TypeItem(PageObject):
    name = id = Label('.text')

    def __call__(self):
        self.web_elem.click()

    def __str__(self):
        return f'Consumer type item with text {self.name}'


class Consumer(PageObject):
    name = id = Label('.tag-label')

    def __call__(self):
        self.click()

    def __str__(self):
        return 'Consumer item'


class ConsumerCaveat(PageObject):
    list_option = Button('.btn-list')
    id_option = Button('.btn-by-id')
    consumer_type = WebElement('.ember-power-select-trigger')
    consumer_types = WebItemsSequence(
        '.ember-power-select-option', cls=TypeItem)
    consumers = WebItemsSequence('.selector-item', cls=Consumer)
    input = Input('.record-id')
    add_button = Button('.add-id')

    def expand_consumer_types(self):
        self.consumer_type.click()

    def __str__(self):
        return 'Consumer caveat popup'

