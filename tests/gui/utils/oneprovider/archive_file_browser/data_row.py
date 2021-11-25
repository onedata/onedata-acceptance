"""Utils and fixtures to facilitate operation on archive row in archive file
browser in oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import time

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, Button, WebElement
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from tests.gui.utils.generic import transform


class DataRow(PageObject):
    name = id = Label('.file-name-inner')
    size = Label('.fb-table-col-size .file-item-text')
    menu_button = Button('.file-row-actions-trigger')
    symlink_tag = WebElement('.fb-table-row-symlink .one-icon-tag-circle')
    hardlink_tag = WebElement('.file-status-hardlinks')
    clickable_field = WebElement('.file-name')
    _status_tag = WebElement('.file-status-tag')

    def double_click(self):
        if self.is_any_tag_visible():
            ActionChains(self.driver).click(self.clickable_field).perform()
            self.active_waiting()
            ActionChains(self.driver).key_down(Keys.ENTER).perform()
        else:
            ActionChains(self.driver).click(self.web_elem).perform()
            self.active_waiting()
            ActionChains(self.driver).key_down(Keys.ENTER).perform()

    def is_tag_visible(self, name):
        try:
            getattr(self, f'{transform(name)}_tag')
        except RuntimeError:
            return False
        else:
            return True

    def get_tag_text(self, name):
        return getattr(self, f'{transform(name)}_tag').text

    def is_any_tag_visible(self):
        try:
            self._status_tag.get_attribute('class')
        except RuntimeError:
            return False
        else:
            return True

    def is_selected(self):
        return 'file-selected' in self.web_elem.get_attribute('class')

    def active_waiting(self):
        for i in range(30):
            time.sleep(0.1)
            if self.is_selected():
                break
