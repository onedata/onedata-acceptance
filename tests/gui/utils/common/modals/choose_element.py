"""Utils and fixtures to facilitate operations on choose element modal.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import NamedButton
from tests.gui.utils.common.common import DropdownSelector
from .modal import Modal


class ChooseElementModal(Modal):
    dropdown = DropdownSelector('.ember-basic-dropdown')

    add = NamedButton('button', text='Add')
    cancel = NamedButton('button', text='Cancel')

    def __str__(self):
        return 'Choose element modal'
