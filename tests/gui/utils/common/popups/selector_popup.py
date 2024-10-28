"""Utils and fixtures to facilitate operations on selector popup."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebItemsSequence


class SelectorItem(PageObject):
    name = id = Label(".tag-label")

    def __call__(self):
        self.click()


class SelectorPopup(PageObject):
    selectors = WebItemsSequence(".selector-item", cls=SelectorItem)

    def __str__(self):
        return "Selector popup"
