"""Utils for dataset browser and it's components in Oneprovider GUI tests"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from functools import partial

from tests.gui.utils.core.web_elements import WebItem

from ..browser import Browser
from .data_row import DataRow


class _ArchiveRecallBrowser(Browser):
    row_cls = DataRow


ArchiveRecallBrowser = partial(WebItem, cls=_ArchiveRecallBrowser)
