"""Utils and fixtures to facilitate operations on Cease oneprovider support
for space modal.
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

from tests.gui.utils.core.web_elements import Button, NamedButton

from ..modal import Modal


class CeaseSupportForSpaceModal(Modal):
    cease_support = NamedButton("button", text="Cease support")
    understand_risk_checkbox = Button(".one-checkbox-danger")
    cancel = NamedButton("button", text="Cancel")

    # TODO: delete after space support revoke fixes in 21.02 (VFS-6383)
    space_delete_link = Button(".info-condensed .clickable")

    def __str__(self):
        return "Cease support for space modal"
