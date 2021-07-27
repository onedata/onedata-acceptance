"""Utils for dataset browser and it's components in Oneprovider GUI tests
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from functools import partial
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItemsSequence, WebItem
from .data_row import DataRow
from .archive_row import ArchiveRow
from ..breadcrumbs import Breadcrumbs


class _DatasetBrowser(PageObject):
    breadcrumbs = Breadcrumbs('.fb-breadcrumbs')
    data = WebItemsSequence('.data-row.fb-table-row', cls=DataRow)
    archives = WebItemsSequence('.data-row.fb-table-row', cls=ArchiveRow)

    def __str__(self):
        return f'dataset browser in {self.parent}'


DatasetBrowser = partial(WebItem, cls=_DatasetBrowser)
