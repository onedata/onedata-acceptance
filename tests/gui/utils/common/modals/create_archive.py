"""Utils and fixtures to facilitate operations on create archive modal.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from .modal import Modal
from tests.gui.utils.core.web_elements import NamedButton, Input, Button


class CreateArchive(Modal):
    create = NamedButton('.btn-primary', text='Create')
    description = Input('.textarea-field .form-control')
    bagit = Button('.option-bagit .one-way-radio-control')

    def __str__(self):
        return 'Create archive'
