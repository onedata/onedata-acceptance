"""Utils to facilitate operations on providers page in Onezone gui"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (Button, NamedButton,
                                               WebItemsSequence, Label,
                                               WebItem, WebElement)
from tests.gui.utils.onezone.generic_page import Element, GenericPage


class Provider(Element):
    support_size = Label('.status-toolbar .outer-text')
    supported_spaces_number = Label('.status-toolbar .oneicon-space')


class Space(PageObject):
    name = Label('.space-label')
    support = Label('.space-size')


class ProviderPopover(PageObject):
    provider_name = Label('.provider-label')
    copy_hostname = Button('.provider-host-copy-btn .oneicon-clipboard-copy')
    spaces_list = WebItemsSequence('.spaces-list li.provider-place-drop-space',
                                   cls=Space)
    visit_provider = NamedButton('.btn-container .btn-go-to-files',
                                 text='Visit provider')


class DataPage(GenericPage):
    popover = WebItem('.webui-popover .provider-place-drop',
                      cls=ProviderPopover)
    _popover = WebElement('.webui-popover .provider-place-drop')
    elements_list = WebItemsSequence('.sidebar-data '
                                     'li.one-list-item.clickable', cls=Provider)
    icon = Button('.circle')

    def is_working(self):
        return 'online' in self._popover.get_attribute('class')
