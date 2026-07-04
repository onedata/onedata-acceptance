"""Utils to facilitate operations on alert info popups."""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button, Label


class AlertInfoPopup(PageObject):
    message = id = Label(".message-body")
    close = Button(".close")

    def __str__(self) -> str:
        return "alert info popup"
