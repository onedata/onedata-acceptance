"""Utils and fixtures to facilitate operations on menu popup."""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebItemsSequence


class MenuItem(PageObject):
    name = id = Label("a.clickable .one-label")

    def __call__(self):
        self.click()


class MenuPopupWithLabel(PageObject):
    menu = WebItemsSequence("ul li:not(.separator)", cls=MenuItem)

    def __str__(self):
        return "Menu popup with label"

    def choose_option(self, name):
        if name not in self.menu:
            self.scroll_to_bottom()
        self.menu[name].click()

    def scroll_to_bottom(self):
        option_len = len(self.menu)
        self.driver.execute_script(
            "arguments[0].scrollIntoView();", self.menu[option_len - 1].web_elem
        )
