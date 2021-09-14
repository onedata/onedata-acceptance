"""Utils and fixtures to facilitate operation on archive row in archive file
browser in oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, Button, WebElement
from selenium.webdriver import ActionChains
from tests.gui.utils.generic import transform


class DataRow(PageObject):
    name = id = Label('.file-name-inner')
    size = Label('.fb-table-col-size .file-item-text')
    menu_button = Button('.file-row-actions-trigger')
    symlink_tag = WebElement('.fb-table-row-symlink .one-icon-tag-circle')
    hardlink_tag = WebElement('.file-status-hardlinks')

    def double_click(self):
        ActionChains(self.driver).double_click(self.web_elem).perform()

    def is_tag_visible(self, name):
        try:
            getattr(self, f'{transform(name)}_tag')
        except RuntimeError:
            return False
        else:
            return True

    def get_tag_text(self, name):
        return getattr(self, f'{transform(name)}_tag').text

