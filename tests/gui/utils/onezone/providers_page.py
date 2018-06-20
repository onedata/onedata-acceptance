"""Utils and fixtures to facilitate operations on providers page in Onezone gui"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button, NamedButton, WebItemsSequence, Label, WebItem


class Provider(PageObject):
    name = Label('.one-label')
    supported_size = Label('.status-toolbar .oneicon-null') #!!!!!!
    supported_spaces_number = Label('.status-toolbal .oneicon-provider') #!!!!!!!


class Space(PageObject):
    space_name = Label('.space-label')
    support = Label('.space-size')


class ProviderPopover(PageObject):
    provider_name = Label('.provider-label')
    copy_hostname_button = Button('.provider-host-copy-btn .oneicon-clipboard-copy')
    spaces_list = WebItemsSequence('.spaces-list li.provider-place-drop-space', cls=Space)
    visit_provider_button = NamedButton('.btn-container .btn-go-to-files', text='Visit provider')


class ProvidersPage(PageObject):
    get_started_button = NamedButton('.btn-default', text='Get started')

    popover = WebItem('.webui-popover .provider-place-drop', cls=ProviderPopover)
    providers_list = WebItemsSequence('.sidebar-providers li.one-list-item.clickable', cls=Provider)

    def __getitem__(self, item):
        item = item.lower()
        for space in self.providers_list:
            if space.name == item:
                return space
        raise RuntimeError('No provider named "{}" found in Providers Page'.format(item))
