"""Utils and fixtures to facilitate operations on external symbolic link modal."""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import Button, Label


class ExternalSymbolicLink(Modal):
    path = Label(".path")
    open = Button(".btn-open")
    cancel = Button(".btn-cancel")
    download = Button(".btn-open")

    def __str__(self):
        return "External symbolic link modal"
