"""Utils and fixtures to facilitate operations on cancel archive modal.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import Input, Button


class CancelArchive(Modal):
    yes = Button('.question-yes')
    no = Button('.question-no')

    def __str__(self):
        return 'Cancel archive'
