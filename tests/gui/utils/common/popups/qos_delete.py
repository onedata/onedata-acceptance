"""Utils and fixtures to facilitate operations on delete quality of service
popup.
"""

__author__ = "Michal Dronka"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button


class DeleteQosPopup(PageObject):
    confirm = Button(".btn-danger")
    cancel = Button(".btn-info")

    def __str__(self):
        return "Quality of Service popup"
