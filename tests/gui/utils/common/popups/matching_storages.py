"""Utils and fixtures to facilitate operations on matching storages popup."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Any

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebElementsSequence


class MatchingStoragesPopup(PageObject):
    storages = WebElementsSequence(".storages-matching-item-text")

    def __str__(self) -> Any:
        return "Matching storages popup"
