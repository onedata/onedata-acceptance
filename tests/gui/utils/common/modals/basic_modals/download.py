"""Utils to facilitate operations on download element modal."""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.web_elements import NamedButton, Button
from ..modal import Modal

class FileDownloadModal(Modal):
    cancel = Button(".cancel")
    download = Button(".btn-primary")

    def __str__(self):
        return "Download element modal"