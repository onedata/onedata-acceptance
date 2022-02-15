"""Utils and fixtures to facilitate operations on Create new store for
workflow modal.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import WebItem, Button
from .modal import Modal
from ...onezone.common import InputBox


class CreateNewStore(Modal):
    name = WebItem('.name-field .text-like-field', cls=InputBox)
    submit_button = Button('.btn-submit')

    def __str__(self):
        return 'Create new store modal'
