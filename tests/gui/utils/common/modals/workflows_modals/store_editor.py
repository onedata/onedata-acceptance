"""Utils and fixtures to facilitate operations on Create new store for
workflow modal.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

from tests.gui.utils.core.web_elements import Button, Input, WebElement

from ...common import Toggle
from ..modal import Modal


class StoreEditor(Modal):
    store_name = Input(".name-field .form-control")
    create = ok = Button(".btn-submit")
    type_dropdown_menu = WebElement(".type-field .dropdown-field-trigger")
    data_type_dropdown_menu = WebElement(
        ".dataSpec-field .ember-basic-dropdown-trigger"
    )
    data_type_remove = Button(".dataSpec-field .remove-trigger")
    user_input = Toggle(".needsUserInput-field .form-control")

    def __str__(self):
        return "Store editor modal"
