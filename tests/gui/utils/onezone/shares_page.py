"""Utils to facilitate operations on shares page in Onezone gui"""

__author__ = "Jakub Pilch"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Label,
    WebElementsSequence,
    WebItemsSequence,
)
from tests.gui.utils.onezone.generic_page import GenericPage


class SharesSidebarRecord(PageObject):
    name = id = Label(".sidebar-item-title-upper .one-label")
    space_name = Label(".sidebar-item-title-lower .space-name")


class SharesPage(GenericPage):
    shares_sidebar_list = WebItemsSequence(
        ".sidebar-shares .one-list-item", cls=SharesSidebarRecord
    )
    shares_sidebar_list_web_elems = WebElementsSequence(
        ".sidebar-shares .one-list-item .share-name"
    )

    def get_visible_shares_list(self) -> list[object]:
        return [el for el in self.shares_sidebar_list_web_elems if el.text != ""]
