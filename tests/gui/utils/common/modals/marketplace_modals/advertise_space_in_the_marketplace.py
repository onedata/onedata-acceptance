"""Utils and fixtures to facilitate operations on advertise space
in the Marketplace modal.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.web_elements import Button, Input

from ..modal import Modal


class AdvertiseSpaceInTheMarketplace(Modal):
    contact_email = Input(".contactEmail-field .form-control")
    checkbox = Button(".one-checkbox")
    proceed = Button(".proceed-btn")

    def __str__(self):
        return "Advertise space in the Marketplace modal"
