"""Utils and fixtures to facilitate operations on chart statistics popup."""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from typing import Any

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label


class ChartStatistics(PageObject):
    header = Label(".tooltip-header")

    def __str__(self) -> Any:
        return "Chart Statistics"
