from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItemsSequence
from tests.gui.utils.core.web_elements import Label
from tests.gui.utils.onezone.generic_page import GenericPage


class SharesSidebarRecord(PageObject):
    name = id = Label('.sidebar-item-title-upper .one-label')
    space_name = Label('.sidebar-item-title-lower .space-name')


class SharesPage(GenericPage):
    shares_list = WebItemsSequence('.sidebar-shares .one-list-item',
                                   cls=SharesSidebarRecord)