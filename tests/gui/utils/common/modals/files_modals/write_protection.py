"""Utils and fixtures to facilitate operations on write protection modal."""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.utils.common.common import Button, Toggle

from ..modal import Modal


class WriteProtection(Modal):
    data_protection_toggle = Toggle(".direct-dataset-item .data-flag-toggle")
    metadata_protection_toggle = Toggle(".direct-dataset-item .metadata-flag-toggle")
    close = Button(".close-btn")

    def __str__(self):
        return "Write protection modal"
