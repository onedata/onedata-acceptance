"""Utils and fixtures to facilitate operations on Upload workflow modal.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import (NamedButton, Button)


class UploadWorkflow(Modal):
    apply = NamedButton('button', text='Apply')
    cancel = NamedButton('button', text='Cancel')
    persist_as_new_workflow = Button('.option-create .one-way-radio-control')
    merge_into_existing_workflow = Button('.option-merge .one-way-radio-control')

    def __str__(self):
        return 'Upload workflow modal'
