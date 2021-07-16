"""Utils and fixtures to facilitate operations on remove selected dataset modal.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from .modal import Modal
from tests.gui.utils.core.web_elements import NamedButton


class RemoveSelectedDataset(Modal):
    remove_button = NamedButton('.btn-danger', text='Remove')

    def __str__(self):
        return 'RemoveSelectedDataset'

