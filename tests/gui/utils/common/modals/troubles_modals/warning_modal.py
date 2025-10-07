"""Utils and fixtures to facilitate operations on Warning modal."""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.web_elements import Button, NamedButton

from ..modal import Modal


class WarningModal(Modal):
    proceed = Button(".question-yes")
    cancel = NamedButton(".btn-default", text="Cancel")
    discard = NamedButton(".btn-default", text="Discard")
    enable_lets_encrypt = NamedButton(".btn-primary", text="Enable Let's Encrypt")

    def __str__(self):
        return "Warning modal"
