"""Utils and fixtures to facilitate operations on
common operations between various services.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from functools import partial

from tests.gui.utils.core.web_elements import (WebItemsSequence, Label,
                                               WebElement, Button, WebItem)
from tests.gui.utils.core.web_objects import ButtonWithTextPageObject
from tests.gui.utils.core.base import PageObject, ExpandableMixin

from .account_management import AccountManagementContentPage


class BaseContent(PageObject):
    _main_content = '.main-content'
    account_management = WebItem(_main_content,
                                 cls=AccountManagementContentPage)

    def __str__(self):
        return 'content in {}'.format(self.parent)


class OnePage(object):
    service = Label('.brand-info')
    account = WebElement('.user-account-button-main')
    content = WebItem('.col-content', cls=BaseContent)
    opened_tab = Label('#main-menu-container ul.main-menu '
                       'li.main-menu-item.active')
    main_menu = WebItemsSequence('#main-menu-container ul.main-menu '
                                 'li.main-menu-item',
                                 cls=ButtonWithTextPageObject)

    def __init__(self, driver):
        self.driver = self.web_elem = driver

    def __str__(self):
        return self.service


class _Toggle(PageObject):
    _lock = WebElement('.one-way-toggle-readonly-icon')

    def __str__(self):
        return 'toggle switch in {}'.format(self.parent)

    def is_checked(self):
        return 'checked' in self.web_elem.get_attribute('class')

    def check(self):
        if not self.is_checked():
            self.click()

    def uncheck(self):
        if self.is_checked():
            self.click()

    def is_enabled(self):
        try:
            self._lock
        except RuntimeError:
            return True
        else:
            return False


class _DropdownSelector(PageObject, ExpandableMixin):
    selected = Label('.ember-power-select-selected-item')
    options = WebItemsSequence('ul li', cls=ButtonWithTextPageObject)
    _toggle = WebElement('.ember-basic-dropdown-trigger[role="button"]')


Toggle = partial(WebItem, cls=_Toggle)
DropdownSelector = partial(WebItem, cls=_DropdownSelector)
