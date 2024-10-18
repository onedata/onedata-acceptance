"""Utils and fixtures to facilitate operations on choose metadata type popup."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebItemsSequence


class Options(PageObject):
    name = id = Label(".truncated-string")


class MetadataType(PageObject):
    options = WebItemsSequence(".option-container", cls=Options)
