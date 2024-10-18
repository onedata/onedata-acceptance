"""Utils and fixtures to facilitate operations on advertise space modal."""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.web_elements import Button, WebElement

from ..modal import Modal


class AdvertiseSpace(Modal):
    configure = Button(".proceed-btn")
    spaces_dropdown_menu = WebElement(".spaces-dropdown-trigger")

    def __str__(self):
        return "Advertise space modal"
