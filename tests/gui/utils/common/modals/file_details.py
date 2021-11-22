"""Utils and fixtures to facilitate operations on file details modal.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (Label, NamedButton, WebItem,
                                               WebItemsSequence, WebElement,
                                               Button)
from tests.gui.utils.generic import strip_path

class HardlinkEntry(PageObject):
    name = id = Label('.file-name')
    path = Label('.file-path .anchor-container')

    def get_path_string(self):
        return strip_path(self.path)


class HardlinkTab(PageObject):
    tab_name = Label('a[href="#hardlinks"]')
    tab = WebElement('a[href="#hardlinks"]')
    files = WebItemsSequence('.file-hardlink', cls=HardlinkEntry)

    def is_active(self):
        return 'active' in self.tab.get_attribute('class')


class FileDetailsModal(Modal):
    modal_name = Label('.modal-header h1')
    owner = Label('.file-info-row-owner .property-value')
    close = NamedButton('.btn-default', text='Close')
    hardlinks_tab = WebItem('.modal-body', cls=HardlinkTab)
    space_id = Button('.file-info-row-space-id .clipboard-btn')
    file_id = Button('.file-info-row-cdmi-object-id .clipboard-btn ')

    def __str__(self):
        return 'File details modal'
