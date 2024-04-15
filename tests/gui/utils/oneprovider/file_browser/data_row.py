"""Utils and fixtures to facilitate operation on file row in file browser
in oneprovider web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebElement, Button
from tests.gui.utils.generic import click_on_web_elem, transform
from tests.gui.utils.oneprovider.browser_row import BrowserRow


class DataRow(PageObject, BrowserRow):
    name = id = Label('.file-name-inner', parent_name='given data row')
    size = Label('.fb-table-col-size .file-item-text')
    modification_date = Label('.fb-table-col-modification .file-item-text')
    replication_rate = Label('.fb-table-col-replication .replication-rate-text')
    qos_status = WebElement('.status-icon .qos-status-icon')

    _icon = WebElement('.file-icon')
    _icon_tag = WebElement('.one-icon-tag')
    menu_button = Button('.fb-table-col-actions-menu .menu-toggle')

    _status_tag = WebElement('.file-status-tag')
    shared_tag = WebElement('.file-status-shared')
    metadata_tag = WebElement('.file-status-metadata')
    qos_tag = WebElement('.file-status-qos')
    dataset_tag = WebElement('.file-status-dataset')
    inherited_tag = WebElement('.item-inheritance-icon')
    data_protected_tag = WebElement('.file-data-protected-icon')
    metadata_protected_tag = WebElement('.file-metadata-protected-icon')
    no_access_tag = WebElement('.file-status-forbidden')
    hardlink_tag = WebElement('.file-status-hardlinks')
    recalled_tag = WebElement('.file-status-recalled')
    recalling_tag = WebElement('.file-status-recalling')
    clickable_field = WebElement('.file-name')
    tag_label = Label('.file-status-tag')
    size_statistics_icon = WebElement('.dir-size-container .one-icon')

    def __str__(self):
        return '{item} in {parent}'.format(item=self.name,
                                           parent=str(self.parent))

    def is_selected(self):
        return 'file-selected' in self.web_elem.get_attribute('class')

    def is_directory(self):
        return 'browser-directory' in self._icon.get_attribute('class')

    def is_symbolic_link(self):
        return ('browser-file' in self._icon.get_attribute('class') and
                'oneicon-shortcut' in self._icon_tag.get_attribute('class'))

    def is_directory_symbolic_link(self):
        return ('browser-directory' in self._icon.get_attribute('class') and
                'oneicon-shortcut' in self._icon_tag.get_attribute('class'))

    def is_malformed_symbolic_link(self):
        return ('browser-file' in self._icon.get_attribute('class') and
                'oneicon-x' in self._icon_tag.get_attribute('class'))

    def is_malformed_directory_symbolic_link(self):
        return ('browser-directory' in self._icon.get_attribute('class') and
                'oneicon-x' in self._icon_tag.get_attribute('class'))

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

    def click_on_status_tag(self, name):
        tag = getattr(self, '{tag}_tag'.format(tag=name.lower()))
        click_on_web_elem(self.driver, tag,
                          f'cannot click on "{name}" in {self}')

    def click_and_enter(self):
        time.sleep(0.1)
        if self.is_any_tag_visible():
            ActionChains(self.driver).click(self.clickable_field).perform()
        else:
            ActionChains(self.driver).click(self.web_elem).perform()
        self.wait_for_selected()
        ActionChains(self.driver).key_down(Keys.ENTER).perform()
