"""Utils and fixtures to facilitate operations on leave element modal.
"""

__author__ = "Lukasz Niemiec, Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018-2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import NamedButton, WebElement
from ..modal import Modal


class LeaveElementModal(Modal):
    leave = NamedButton('button', text='Leave')
    cancel = NamedButton('button', text='Cancel')

    info = WebElement('p:first-of-type')

    def __str__(self):
        return 'Leave element modal'

