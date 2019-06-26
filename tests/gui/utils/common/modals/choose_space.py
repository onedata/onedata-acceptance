"""Utils and fixtures to facilitate operations on choose space modal.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import NamedButton
from tests.gui.utils.common.common import DropdownSelector
from .modal import Modal


class ChooseSpaceModal(Modal):
    dropdown = DropdownSelector('.ember-basic-dropdown')

    cancel = NamedButton('button', text='Cancel')
    add = NamedButton('button', text='Add')

    def __str__(self):
        return 'Choose space modal'

