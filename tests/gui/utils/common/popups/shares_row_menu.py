"""Utils and fixtures to facilitate operations on shares row menu popup."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebItemsSequence


class Options(PageObject):
    name = id = Label(".one-label")


class SharesRowMenu(PageObject):
    options = WebItemsSequence(".share-actions.dropdown-menu a.clickable", cls=Options)

    def __str__(self):
        return "Shares row menu"
