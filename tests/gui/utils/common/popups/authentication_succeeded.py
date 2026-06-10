"""Utils to facilitate operations on authentication succeeded popup."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button


class AuthenticationSucceeded(PageObject):
    close = Button(".close")

    def __str__(self):
        return "Authentication succeeded popup"
