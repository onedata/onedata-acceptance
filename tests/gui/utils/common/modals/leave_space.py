"""Utils and fixtures to facilitate operations on leave space modal.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import NamedButton
from .modal import Modal


class LeaveSpaceModal(Modal):
    no = NamedButton('button', text='No, stay here')
    yes = NamedButton('button', text='Yes, leave')

    def __str__(self):
        return 'Leave space modal'
