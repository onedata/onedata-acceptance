"""Utils to facilitate operations on file download modal."""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) Onedata.org"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.web_elements import NamedButton

from ..modal import Modal


class FileDownloadModal(Modal):
    cancel = NamedButton("button", text="Cancel")
    download = NamedButton("button", text="Download")

    def __str__(self):
        return "Download element modal"
