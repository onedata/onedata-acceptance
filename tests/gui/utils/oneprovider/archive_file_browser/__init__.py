"""Utils for archive file browser and it's components in Oneprovider GUI tests
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from functools import partial
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItemsSequence, WebItem
from .data_row import DataRow
from ..breadcrumbs import Breadcrumbs


class _ArchiveFileBrowser(PageObject):
    data = WebItemsSequence('.data-row.fb-table-row', cls=DataRow)
    breadcrumbs = Breadcrumbs('.fb-breadcrumbs')

    def __str__(self):
        return f'archive file browser in {self.parent}'


ArchiveFileBrowser = partial(WebItem, cls=_ArchiveFileBrowser)

