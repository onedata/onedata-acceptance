"""Utils and fixtures to facilitate operations on Duplicate revision modal.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (NamedButton, WebElement)


class DuplicateRevision(PageObject):
    apply = NamedButton('button', text='Apply')
    cancel = NamedButton('button', text='Cancel')
    dropdown_menu = WebElement('.dropdown-field-trigger')

