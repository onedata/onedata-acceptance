"""Utils and fixtures to facilitate operations on file details modal.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import (Label, NamedButton, Button)


class FileDetailsModal(Modal):
    modal_name = Label('.modal-header h1')
    owner = Label('.file-info-row-owner .property-value')
    close = NamedButton('.btn-default', text='Close')
    space_id = Button('.file-info-row-space-id .clipboard-btn')
    file_id = Button('.file-info-row-cdmi-object-id .clipboard-btn ')

    def __str__(self):
        return 'File details modal'


