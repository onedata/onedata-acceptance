"""Utils and fixtures to facilitate operations on add one of groups modal.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import NamedButton, WebElement
from tests.gui.utils.common.common import DropdownSelector


class AddOneOfGroupsModal(Modal):
    _toggle = WebElement('.dropdown-container '
                         '.ember-basic-dropdown-trigger[role="button"]')

    cancel = NamedButton('button', text='Cancel')
    add = NamedButton('button', text='Add')
    group_selector = DropdownSelector('.ember-basic-dropdown')

    def expand_dropdown(self):
        self._toggle.click()

    def __str__(self):
        return 'Add one of group modal'

