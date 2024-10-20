"""Utils and fixtures to facilitate operations on remove
group/user/storage/harvester modal.
"""

__author__ = "Lukasz Niemiec"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.web_elements import Button, NamedButton

from ..modal import Modal


class RemoveModal(Modal):
    cancel = NamedButton("button", text="Cancel")
    remove = NamedButton("button", text="Remove")
    understand_notice = Button(".one-checkbox-understand")

    def __str__(self):
        return "Remove group/user/storage/harvester/space modal"
