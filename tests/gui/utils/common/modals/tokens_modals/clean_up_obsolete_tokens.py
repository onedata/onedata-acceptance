"""Utils and fixtures to facilitate operations on clean up obsolete tokens
modal.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Label,
    NamedButton,
    WebItemsSequence,
)

from ..modal import Modal


class SingleTokenRecord(PageObject):
    id = name = Label(".item-content")
    checkbox = Button(".one-checkbox")


class TokenTypeRecord(PageObject):
    id = name = Label(".header-text")
    checkbox = Button(".one-checkbox")


class CleanUpObsoleteTokensModal(Modal):
    remove = NamedButton("button", text="Remove")
    cancel = NamedButton("button", text="Cancel")
    token_types = WebItemsSequence(".checkbox-list-header", cls=TokenTypeRecord)
    tokens = WebItemsSequence(".checkbox-list-item", cls=SingleTokenRecord)

    def __str__(self):
        return "Clean up obsolete tokens"
