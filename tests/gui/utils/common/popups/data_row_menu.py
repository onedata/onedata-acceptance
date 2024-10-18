"""Utils and fixtures to facilitate operations on data row menu popup."""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebItemsSequence


class Options(PageObject):
    name = id = Label(".one-label")

    def get_state(self):
        return (
            "disabled"
            if "disabled" in self.web_elem.get_attribute("class")
            else "enabled"
        )


class DataRowMenu(PageObject):
    options = WebItemsSequence(
        ".file-actions.dropdown-menu li:not(.separator)", cls=Options
    )

    def choose_option(self, name):
        if name not in self.options:
            self.scroll_to_bottom()
        self.options[name].click()

    def return_option(self, name):
        if name not in self.options:
            self.scroll_to_bottom()
        return self.options[name]

    def scroll_to_bottom(self):
        option_len = len(self.options)
        self.driver.execute_script(
            "arguments[0].scrollIntoView();",
            self.options[option_len - 1].web_elem,
        )

    def __str__(self):
        return "Data row menu"
