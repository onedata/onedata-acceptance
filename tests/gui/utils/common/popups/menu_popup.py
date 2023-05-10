"""Utils and fixtures to facilitate operations on menu popup.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebItemsSequence


class MenuItem(PageObject):
    name = id = Label('a.clickable .one-label')

    def __call__(self):
        self.click()


class MenuPopupWithLabel(PageObject):
    menu = WebItemsSequence('ul li:not(.separator)', cls=MenuItem)

    def __str__(self):
        return 'Menu popup with label'

