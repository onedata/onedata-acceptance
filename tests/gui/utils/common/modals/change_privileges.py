"""Utils and fixtures to facilitate operations on group membership
relation menu modal.
"""

__author__ = "Emilia Kwolek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.common.privilege_tree import PrivilegeTree
from tests.gui.utils.core.web_elements import WebItem, Button


class ChangePrivilegesModal(Modal):
    privilege_tree = WebItem('.one-tree', cls=PrivilegeTree)
    cancel_button = Button('.cancel')
    save_button = Button('.ready')

    def __str__(self):
        return 'Change privileges in bulk menu'
