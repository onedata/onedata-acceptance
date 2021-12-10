"""Utils for archive browser and it's components in Oneprovider GUI tests
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from functools import partial
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (WebItemsSequence, WebItem,
                                               Button, Label)
from .data_row import DataRow
from ..breadcrumbs import Breadcrumbs


class _ArchiveBrowser(PageObject):
    data = WebItemsSequence('.data-row.fb-table-row', cls=DataRow)
    breadcrumbs = Breadcrumbs('.fb-breadcrumbs')
    create_archive = Button('.hidden-xs .toolbar-buttons '
                            '.oneicon-browser-archive-add')
    empty_dir_msg = Label('.empty-dir-text')
    error_msg = Label('.error-dir-text')

    def __str__(self):
        return f'archive browser in {self.parent}'


ArchiveBrowser = partial(WebItem, cls=_ArchiveBrowser)

