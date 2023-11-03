"""Utils and fixtures to facilitate operations error modal.
"""

__author__ = "Lukasz Niemiec"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import NamedButton, Label
from ..modal import Modal


class ErrorModal(Modal):
    close = NamedButton('button', text='Close')
    content = Label('.modal-body')
    title = Label('h1 .one-label')
    content_message = Label('.message-body')

    def __str__(self):
        return 'Error modal'
