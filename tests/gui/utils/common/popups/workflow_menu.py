"""Utils and fixtures to facilitate operations on workflow menu popup."""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebItemsSequence


class Options(PageObject):
    name = id = Label(".one-label")


class WorkflowMenu(PageObject):
    options = WebItemsSequence("a.clickable", cls=Options)
    disabled_options = WebItemsSequence(".disabled a.clickable", cls=Options)

    def choose_option(self, name):
        if name not in self.options:
            self.scroll_to_bottom()
        self.options[name].click()

    def scroll_to_bottom(self):
        option_len = len(self.options)
        self.driver.execute_script(
            "arguments[0].scrollIntoView();",
            self.options[option_len - 1].web_elem,
        )

    def __str__(self):
        return "Workflow menu"
