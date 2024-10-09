"""Utils and fixtures to facilitate operations on data distribution popup."""

__author__ = "Emilia Kwolek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebItemsSequence


class DataDistributionItem(PageObject):
    name = id = Label(".one-label")

    def __call__(self):
        self.click()


class DataDistributionPopup(PageObject):
    menu = WebItemsSequence("ul li", cls=DataDistributionItem)

    def __str__(self):
        return "Data distribution popup"
