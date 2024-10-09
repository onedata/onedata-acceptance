"""Utils and fixtures to facilitate operations on create dir modal."""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import Input, NamedButton


class CreateDir(Modal):
    input_name = Input(".form-control.new-item-name")
    create = NamedButton("button", text="Create")
    cancel = NamedButton("button", text="Cancel")

    def __str__(self):
        return "Create dir"
