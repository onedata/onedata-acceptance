"""Utils and fixtures to facilitate operations on Provider popover popup.
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (Label, Button,
                                               WebItemsSequence, NamedButton,
                                               Input, WebElementsSequence)


class Space(PageObject):
    name = id = Label('.space-label')
    support = Label('.space-size')


class Values(PageObject):
    copy_to_clipboard = Button('.copy-btn-icon')


class ProviderDetails(PageObject):
    values = WebItemsSequence('td:nth-child(2)', cls=Values)
    labels = WebElementsSequence('td:first-child')


class ProviderPopover(PageObject):
    provider_name = id = Label('.provider-label')
    provider_hostname = Input('.provider-host-text')
    copy_hostname = Button('.provider-host-copy-btn .one-icon')
    spaces_list = WebItemsSequence('.spaces-list li.provider-place-drop-space',
                                   cls=Space)
    toggle_home_provider = NamedButton('.btn-container .btn-toggle-default',
                                       text='Toggle home provider')
    visit_provider = NamedButton('.btn-container .btn-go-to-files',
                                 text='Visit provider')
