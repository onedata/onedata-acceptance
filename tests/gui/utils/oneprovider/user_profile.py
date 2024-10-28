"""Utils and fixtures to facilitate operations on user profile
in Oneprovider GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.utils.core.base import ExpandableMixin, PageObject
from tests.gui.utils.core.web_elements import NamedButton, WebElement


class UserProfile(PageObject, ExpandableMixin):
    _btn_css_sel = "ul.dropdown-menu-list li:not(.dropdown-menu-separator)"
    log_out = NamedButton(_btn_css_sel, text="log out")
    manage_account = NamedButton(_btn_css_sel, text="manage account")
    _toggle = WebElement("a.dropdown-toggle")
