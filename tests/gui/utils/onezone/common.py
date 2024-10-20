"""Utils and fixtures to facilitate operations on panels (base for specific panels)
in Onezone web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.utils.core.base import ExpandableMixin, PageObject
from tests.gui.utils.core.web_elements import Button, Input, Label, WebElement


class OZPanel(PageObject, ExpandableMixin):
    name = Label("a.main-accordion-toggle", parent_name="oz panel")
    _toggle = WebElement("a.main-accordion-toggle")

    def __str__(self):
        return f"{self.name} panel in {self.parent}"


class EditBox(PageObject):
    value = Input("input")
    confirm = Button(".save-icon")
    cancel = Button(".cancel-icon")


class InputBox(PageObject):
    value = Input("input")
    confirm = Button("button")
