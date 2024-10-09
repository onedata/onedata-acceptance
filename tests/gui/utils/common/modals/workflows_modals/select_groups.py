"""Utils and fixtures to facilitate operations on Select groups modal."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button, Label, WebItemsSequence

from ..modal import Modal


class Group(PageObject):
    name = id = Label(".item-name")


class SelectGroups(Modal):
    groups = WebItemsSequence(".resource-item", cls=Group)
    confirm_selection = Button(".btn-confirm")
    cancel = Button(".btn-cancel")

    def select(self, groups):
        for group in groups:
            self.groups[group].web_elem.click()
        self.confirm_selection.click()

    def __str__(self):
        return "Select groups modal"
