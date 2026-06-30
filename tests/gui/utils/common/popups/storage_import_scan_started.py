"""Utils to facilitate operations on Storage import scan started popup."""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button, WebElementWithText


class StorageImportScanStarted(PageObject):
    close = Button(".close")
    message = WebElementWithText(
        ".message-body", text="Storage import scan has started"
    )

    def __str__(self) -> str:
        return "Storage import scan started popup"
