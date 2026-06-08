"""Utils and fixtures to facilitate operations on detach dataset modal."""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from typing import Any

from tests.gui.utils.core.web_elements import Button

from ..modal import Modal


class DetachDataset(Modal):
    proceed = Button(".question-yes")

    def __str__(self) -> Any:
        return "Detach Dataset"
