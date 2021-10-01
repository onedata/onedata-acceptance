"""Utils and fixtures to facilitate operation on archive row in archive
browser in oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebElement, Button
from selenium.webdriver import ActionChains
from tests.gui.utils.generic import transform


class DataRow(PageObject):
    name = id = Label('.file-name-inner')
    state = Label('.fb-table-col-state .file-item-text')
    bagit_tag = WebElement('.archive-bagit-tag')
    dip_tag = WebElement('.archive-dip-tag')
    base_archive = Label('.base-archive-name')
    menu_button = Button('.file-row-actions-trigger')

    def double_click(self):
        ActionChains(self.driver).double_click(self.web_elem).perform()

    def is_tag_visible(self, name):
        try:
            getattr(self, f'{transform(name)}_tag')
        except RuntimeError:
            return False
        else:
            return True
