"""Utils and fixtures to facilitate operations on member menu popup.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItemsSequence, Label


class MenuItem(PageObject):
    name = id = Label('a.clickable .text')

    def __call__(self):
        self.click()


class PopoverMenu(PageObject):
    menu = WebItemsSequence('.webui-popover-content '
                            '.one-collapsible-toolbar-popover .dropdown-menu '
                            '.one-collapsible-toolbar-item', cls=MenuItem)

    def __str__(self):
        return 'Menu popup'

