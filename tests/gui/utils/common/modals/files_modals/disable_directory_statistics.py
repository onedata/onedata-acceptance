"""Utils and fixtures to facilitate operations on disable directory statistics
modal."""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import Button


class DisableDirectoryStatistics(Modal):
    disable = Button(".question-yes")

    def __str__(self):
        return "Disable directory statistics modal"
