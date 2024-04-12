"""Utils and fixtures to facilitate operations Share/Publish modal.
"""

__author__ = "Jakub Liput"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import NamedButton, Input
from tests.gui.utils.common.modals.modal import Modal

class Share(Modal):
    input_name = Input('.form-control.new-share-name')
    create = NamedButton('button', text='Create')

    def __str__(self):
        return 'Share / Publish modal'


