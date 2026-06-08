"""Utils for archive container and it's components in Oneprovider GUI tests"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from functools import partial
from typing import Any

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebItem


class _ArchiveContainer(PageObject):
    message = Label(".bottom-panel-text")

    def __str__(self) -> Any:
        return f"archive container in {self.parent}"


ArchiveContainer = partial(WebItem, cls=_ArchiveContainer)
