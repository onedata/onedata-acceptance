"""Utils and fixtures to facilitate operations on Emergency interface modal.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import NamedButton
from .modal import Modal


class EmergencyInterface(Modal):
    open_in_onezone = NamedButton('.modal-footer a', text='Open in Onezone')
    close = NamedButton('.modal-footer button', text='Close')

    def __str__(self):
        return 'Emergency interface'

