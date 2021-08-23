"""Utils and fixtures to facilitate operations on directory details modal.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import Label, NamedButton, Button
from tests.gui.utils.generic import transform


class DirectoryDetails(Modal):
    modal_name = Label('.modal-header h1')
    owner = Label('.file-info-row-owner .property-value')
    close = NamedButton('.btn-default', text='Close')
    space_id = Button('.file-info-row-space-id .clipboard-btn')
    file_id = Button('.file-info-row-cdmi-object-id .clipboard-btn ')

    def __str__(self):
        return 'Directory details modal'

    # def get_property(self, property_name, clipboard, displays, browser_id):
    #     getattr(self, transform(property_name)).click()
    #     return clipboard.paste(display=displays[browser_id])

