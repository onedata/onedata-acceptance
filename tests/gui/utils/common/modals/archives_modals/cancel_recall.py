"""Utils and fixtures to facilitate operations on cancel archive modal.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import Input, Button


class CancelRecall(Modal):
    yes = Button('.btn-danger')
    no = Button('.cancel')

    def __str__(self):
        return 'Cancel archive'
