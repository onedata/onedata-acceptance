"""Utilities and fixtures for archive external symbolic link modal."""

__author__ = "Jakub Karczewski, Mateusz Zając"
__copyright__ = "Copyright (C) 2026 Onedata AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import Button


class ArchiveExternalSymlink(Modal):
    open = Button(".btn-open")
    cancel = Button(".btn-cancel")

    def __str__(self):
        return "Archive External Symbolic Link"
