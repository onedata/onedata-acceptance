"""Utils and fixtures to facilitate operations on Unlink lambda modal.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import Button


class UnlinkLambda(Modal):
    unlink = Button('.submit-btn')
    cancel = Button('.cancel-btn')

    def __str__(self):
        return 'Unlink lambda modal'
