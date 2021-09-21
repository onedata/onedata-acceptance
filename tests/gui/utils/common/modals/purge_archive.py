"""Utils and fixtures to facilitate operations on purge archive modal.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from .modal import Modal
from tests.gui.utils.core.web_elements import Input, NamedButton


class PurgeArchive(Modal):
    confirmation_input = Input('.form-control')
    purge_archive = NamedButton('.btn-danger', text='Purge archive')

    def __str__(self):
        return 'Purge archive'










