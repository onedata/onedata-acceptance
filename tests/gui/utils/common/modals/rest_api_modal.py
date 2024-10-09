"""Utils and fixtures to facilitate operations on rest api modal."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

from tests.gui.utils.core.web_elements import Button

from .modal import Modal


class RESTApiModal(Modal):
    copy_command_button = Button(".copy-btn")

    def __str__(self):
        return "REST Api modal"
