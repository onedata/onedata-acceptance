"""Utils to facilitate operations on providers page in Onezone gui"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import (Button, WebItemsSequence, Label,
                                               WebElement)
from tests.gui.utils.onezone.generic_page import Element, GenericPage


class Provider(Element):
    support_size = Label('.status-toolbar .outer-text')
    supported_spaces_number = Label('.status-toolbar .oneicon-space')
    home_icon = WebElement('.status-toolbar-icon:first-of-type span')

    def is_home_icon(self):
        return 'oneicon-home' in self.home_icon.get_attribute("class")


class Icon(Element):
    name = id = icon = Button('.circle')


class ProvidersPage(GenericPage):
    _popover = WebElement('.webui-popover .provider-place-drop')
    elements_list = WebItemsSequence('.sidebar-data '
                                     'li.one-list-item.clickable', cls=Provider)
    icons = WebItemsSequence('.provider-place', cls=Icon)
    map_point = Button('.one-map-container .jvectormap-container '
                       'path[data-code="RO"]')

    def is_working(self):
        return 'online' in self._popover.get_attribute('class')
