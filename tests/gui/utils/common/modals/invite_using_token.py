"""Utils and fixtures to facilitate operations on invite using token modal.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import NamedButton, Input
from .modal import Modal


class InviteUsingTokenModal(Modal):
    token = Input('textarea')
    copy = NamedButton('button', text='Copy')
    close = NamedButton('button', text='Close')

    def __str__(self):
        return 'Invite using token modal'
