"""Utils and fixtures to facilitate operations on leave harvester modal.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import NamedButton
from .modal import Modal


class LeaveHarvesterModal(Modal):
    cancel = NamedButton('button', text='Cancel')
    leave = NamedButton('button', text='Leave')

    def __str__(self):
        return 'Leave harvester modal'

