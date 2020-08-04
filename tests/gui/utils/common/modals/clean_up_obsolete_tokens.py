"""Utils and fixtures to facilitate operations on clean up obsolete tokens
modal.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import NamedButton, Input
from .modal import Modal


class CleanUpObsoleteTokensModal(Modal):
    remove = NamedButton('button', text='Remove')
    cancel = NamedButton('button', text='Cancel')

    def __str__(self):
        return 'Clean up obsolete tokens'
