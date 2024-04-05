"""Utils and fixtures to facilitate operations on share modal.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import (NamedButton, Input,
                                               Button, Label, WebItemsSequence)
from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.base import PageObject


class SharesOptions(PageObject):
    name = id = Label('.item-name')
    browser_share_icon = Button('.share-name')
    copy_icon = Button('.oneicon-browser-copy')


class ShareDirectory(Modal):
    input_name = Input('.form-control.new-share-name')
    create = NamedButton('button', text='Create')

    share_options = WebItemsSequence('.file-share-item', cls=SharesOptions)
    create_another_share = NamedButton('button', text='Create another share')

    def __str__(self):
        return 'Share / Publish directory'



