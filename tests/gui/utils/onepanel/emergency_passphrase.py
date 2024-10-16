"""Utils to facilitate emergency passphrase operations in op panel GUI."""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import NamedButton, WebElement


class EmergencyPassphrase(PageObject):
    change_passphrase_button = NamedButton("button", text="Change passphrase")

    current_passphrase_input = WebElement(".field-verify-currentPassword")
    new_passphrase_input = WebElement(".field-change-newPassword")
    retype_new_passphrase_input = WebElement(".field-change-newPasswordRetype")

    change_button = NamedButton("button", text="Change")
    cancel_button = NamedButton("button", text="Cancel")
