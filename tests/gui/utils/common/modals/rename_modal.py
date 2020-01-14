"""Utils and fixtures to facilitate operations on rename modal.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import NamedButton, Input
from .modal import Modal


class RenameModal(Modal):
    input_name = Input('.form-control.new-item-name')
    rename = NamedButton('button', text='Rename')
    cancel = NamedButton('button', text='Cancel')

    def __str__(self):
        return 'Rename modal'
