"""Utils and fixtures to facilitate operations on modify storage modal.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import NamedButton, Button


class ModifyStorage(Modal):
    proceed = NamedButton('button', text='Proceed')
    cancel = NamedButton('button', text='Cancel')
    understand_checkbox = Button('.one-checkbox-understand')

    def __str__(self):
        return 'Modify storage modal'

