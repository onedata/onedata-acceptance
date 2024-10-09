"""Utils and fixtures to facilitate operations on Create new lane for
workflow modal.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

from tests.gui.utils.core.web_elements import Button, Input

from ..modal import Modal


class CreateNewLane(Modal):
    lane_name = Input(".name-field .form-control")
    create = Button(".btn-submit")

    def __str__(self):
        return "Create new lane modal"
