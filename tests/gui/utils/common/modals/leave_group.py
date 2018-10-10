"""Utils and fixtures to facilitate operations on leave group modal.
"""

__author__ = "Lukasz Niemiec"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import NamedButton
from .modal import Modal


class LeaveGroupModal(Modal):
    cancel = NamedButton('button', text='Cancel')
    leave = NamedButton('button', text='Leave')

    def __str__(self):
        return 'Leave group modal'
