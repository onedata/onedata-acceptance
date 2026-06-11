"""Utils for dataset browser and it's components in Oneprovider GUI tests"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from functools import partial

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebItem

from ..browser import Browser
from .data_row import DataRow


class DatasetColumnHeader(PageObject):
    name = id = Label(".column-name")


class _DatasetBrowser(Browser):
    row_cls = DataRow
    column_header_cls = DatasetColumnHeader

    def __str__(self) -> str:
        return f"dataset browser in {self.parent}"


DatasetBrowser = partial(WebItem, cls=_DatasetBrowser)
