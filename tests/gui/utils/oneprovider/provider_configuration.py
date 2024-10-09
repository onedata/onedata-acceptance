"""Utils and fixtures to facilitate operations on space configuration
per provider in Oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

from functools import partial

from tests.gui.utils.common.common import Toggle
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItem


class _ProviderConfiguration(PageObject):
    size_statistics = Toggle(".toggle-field-dir-stats-config")

    def __str__(self):
        return f"space configuration in {self.parent}"


ProviderConfiguration = partial(WebItem, cls=_ProviderConfiguration)
