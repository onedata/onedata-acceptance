"""Utils and fixtures to facilitate operations on write protection modal.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from ..modal import Modal
from tests.gui.utils.common.common import Toggle, Button


class WriteProtection(Modal):
    data_protection_toggle = Toggle('.direct-dataset-item .data-flag-toggle'
                                    ' .one-way-toggle-track')
    metadata_protection_toggle = Toggle('.direct-dataset-item '
                                        '.metadata-flag-toggle '
                                        '.one-way-toggle-track')
    close = Button('.close-btn')

    def __str__(self):
        return 'Write protection modal'

