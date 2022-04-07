"""Utils and fixtures to facilitate operations on delete modal.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import NamedButton
from ..modal import Modal


class DeleteModal(Modal):
    no = NamedButton('button', text='No')
    yes = NamedButton('button', text='Yes')

    def __str__(self):
        return 'Delete modal'

