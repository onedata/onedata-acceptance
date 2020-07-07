"""Utils and fixtures to facilitate operation on file row in file browser
in oneprovider web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from selenium.webdriver import ActionChains

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebElement, Button
from tests.gui.utils.generic import click_on_web_elem


class DataRow(PageObject):
    name = id = Label('.file-name-inner', parent_name='given data row')
    size = Label('.fb-table-col-size .file-item-text')
    modification_date = Label('.fb-table-col-modification .file-item-text')

    _icon = WebElement('.file-icon')
    menu_button = Button('.fb-table-col-actions-menu .menu-toggle')

    _status_tag = WebElement('.file-status-tag')
    shared_tag = WebElement('.file-status-shared')
    metadata_tag = WebElement('.file-status-metadata')
    qos_tag = WebElement('.file-status-qos')
    clickable_field = WebElement('.file-name')

    def __str__(self):
        return '{item} in {parent}'.format(item=self.name,
                                           parent=str(self.parent))

    def is_selected(self):
        return 'file-selected' in self.web_elem.get_attribute('class')

    def is_file(self):
        return 'browser-file' in self._icon.get_attribute('class')

    def is_directory(self):
        return 'browser-directory' in self._icon.get_attribute('class')

    def is_tag_visible(self, name):
        try:
            getattr(self, '{tag}_tag'.format(tag=name))
        except RuntimeError:
            return False
        else:
            return True

    def is_any_tag_visible(self):
        try:
            self._status_tag.get_attribute('class')
        except RuntimeError:
            return False
        else:
            return True

    def click_on_status_tag(self, name):
        tag = getattr(self, '{tag}_tag'.format(tag=name))
        click_on_web_elem(self.driver, tag,
                          f'cannot click on "{name}" in {self}')

    def double_click(self):
        if self.is_any_tag_visible():
            ActionChains(self.driver).double_click(self.clickable_field).perform()
        else:
            ActionChains(self.driver).double_click(self.web_elem).perform()
