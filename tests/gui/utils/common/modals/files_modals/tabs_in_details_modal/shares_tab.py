"""Utils and fixtures to facilitate operations on shares tab of file modal."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Input,
    Label,
    NamedButton,
    WebItemsSequence,
)


class SharesOptions(PageObject):
    name = id = Label(".item-name")
    share_details_link = Button(".share-local-url")
    copy_icon = Button(".oneicon-browser-copy")


class SharesTab(Modal):
    share_options = WebItemsSequence(".file-share-item", cls=SharesOptions)
    create_another_share = NamedButton("button", text="Create another share")

    def __str__(self):
        return "Shares tab"
