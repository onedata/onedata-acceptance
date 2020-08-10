"""Utils and fixtures to facilitate operations on delete user account menu popup.
"""

__author__ = "Piotr Duleba"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItemsSequence, Label


class MenuItem(PageObject):
    name = id = Label('a.clickable .text')

    def __call__(self):
        self.click()


class UserDeleteAccountPopoverMenu(PageObject):
    menu = WebItemsSequence('.one-collapsible-toolbar-item', cls=MenuItem)

    def __str__(self):
        return 'Delete account menu popup'


