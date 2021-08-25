"""Utils and fixtures to facilitate operations on reattach dataset modal.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from .modal import Modal
from tests.gui.utils.core.web_elements import Button


class ReattachDataset(Modal):
    proceed = Button('.question-yes')

    def __str__(self):
        return 'Reattach Dataset'

