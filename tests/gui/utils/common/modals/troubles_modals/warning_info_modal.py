"""Utils and fixtures to facilitate operations on Warning modal."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 Onedata.org"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Any

from tests.gui.utils.core.web_elements import NamedButton

from ..modal import Modal


class WarningInfoModal(Modal):
    cancel = NamedButton(".btn-default", text="Cancel")
    discard = NamedButton(".btn-default", text="Discard")
    enable_lets_encrypt = NamedButton(".btn-primary", text="Enable Let's Encrypt")

    def __str__(self) -> Any:
        return "Warning modal"
