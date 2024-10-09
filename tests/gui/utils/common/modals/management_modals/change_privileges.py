"""Utils and fixtures to facilitate operations on change privileges with bulk
edit modal.
"""

__author__ = "Emilia Kwolek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.common.privilege_tree import PrivilegeTree
from tests.gui.utils.core.web_elements import Button, WebItem


class ChangePrivilegesModal(Modal):
    privilege_tree = WebItem(".table-privileges", cls=PrivilegeTree)
    cancel_button = Button(".cancel")
    save_button = Button(".proceed")

    def __str__(self):
        return "Change privileges in bulk menu"
