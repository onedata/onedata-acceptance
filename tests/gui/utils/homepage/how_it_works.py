"""Utils to facilitate operations on endpoints in "How it works" page of Onedata documentation"""

__author__ = "Mateusz Zając"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.types import GuiObject
from tests.gui.utils.core.web_objects import PageObject


class HowItWorksPage(PageObject):
    def __getitem__(self, item: GuiObject) -> GuiObject:
        if hasattr(self, "elements_list"):
            return self.elements_list[item]
        raise ValueError("there is not elements_list member in class instance")
