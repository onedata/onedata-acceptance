"""Utils and fixtures to facilitate operations on Select files, directories
 or symlinks modal.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (Button, WebItemsSequence, Label,
                                               WebElement)
from tests.gui.utils.oneprovider import FileBrowser


class Files(PageObject):
    name = Label('.file-name')
    clickable_field = WebElement('.file-base-name')


class SelectFiles(Modal):
    file_browser = FileBrowser('.items-select-browser-part'
                               '.upload-drop-zone-container')
    confirm_button = Button('.submit-selection-btn')
    files = WebItemsSequence('.fb-table-tbody .data-row', cls=Files)

    def __str__(self):
        return 'Select files, directories or symlinks modal'
