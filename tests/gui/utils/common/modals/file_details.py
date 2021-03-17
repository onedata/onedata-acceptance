"""Utils and fixtures to facilitate operations on file details modal.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import Label, NamedButton


class FileDetailsModal(Modal):
    modal_name = Label('.modal-header h1')
    owner = Label('.file-info-row-owner .property-value')
    close = NamedButton('.btn-default', text='Close')

    def __str__(self):
        return 'File details modal'
