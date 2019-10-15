"""Utils and fixtures to facilitate operations on choose element modal.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import NamedButton, WebElement
from .modal import Modal


class ChooseElementModal(Modal):
    _toggle = WebElement('.dropdown-container '
                         '.ember-basic-dropdown-trigger[role="button"]')

    add = NamedButton('button', text='Add')
    cancel = NamedButton('button', text='Cancel')

    def expand_dropdown(self):
        self._toggle.click()

    def __str__(self):
        return 'Choose element modal'

