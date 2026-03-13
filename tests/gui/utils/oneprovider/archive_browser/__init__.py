"""Utils for archive browser and it's components in Oneprovider GUI tests"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from functools import partial

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Label,
    WebElement,
    WebItem,
    WebItemsSequence,
)

from ..browser import Browser
from .data_row import DataRow


class ArchiveColumnHeader(PageObject):
    name = id = Label(".column-name")


class _ArchiveBrowser(Browser):
    row_cls = DataRow
    column_headers = WebItemsSequence(
        ".archive-table-head-row .fb-table-secondary-col", cls=ArchiveColumnHeader
    )

    create_archive = Button(".hidden-xs .toolbar-buttons .oneicon-browser-archive-add")
    create_archive_elem = WebElement(
        ".hidden-xs .toolbar-buttons .oneicon-browser-archive-add"
    )
    create_a_new_archive = Button(".empty-archives-create-action")

    def __str__(self):
        return f"archive browser in {self.parent}"


ArchiveBrowser = partial(WebItem, cls=_ArchiveBrowser)
