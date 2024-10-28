"""Utils and fixtures to facilitate operations on recall archive modal."""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import Button, Input


class RecallArchive(Modal):
    target_name_input = Input(".target-name-input")
    recall = Button(".submit-btn")

    def __str__(self):
        return "Recall archive"
