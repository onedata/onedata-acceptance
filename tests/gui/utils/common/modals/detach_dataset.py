"""Utils and fixtures to facilitate operations on detach dataset modal.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from .modal import Modal
from tests.gui.utils.core.web_elements import Button


class DetachDataset(Modal):
    proceed = Button('.spin-button-label')

    def __str__(self):
        return 'Detach Dataset'
