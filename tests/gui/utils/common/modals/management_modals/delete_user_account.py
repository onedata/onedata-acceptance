"""Utils and fixtures to facilitate operations on delete user account modal."""

__author__ = "Piotr Duleba"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import Button, Input, NamedButton


class DeleteUserAccountModal(Modal):
    understand_consequences = Button(".one-checkbox-understand")
    delete_account = Button(".btn-danger.proceed")

    def __str__(self):
        return "Delete User Account"
