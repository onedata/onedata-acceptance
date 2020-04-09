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

    share_icon = WebElement('.file-status-icon.file-status-shared')

    # TODO: change test because of a new gui (metadata)
    # _metadata_tool = WebElement('.file-tool-metadata')

    def __str__(self):
        return '{item} in {parent}'.format(item=self.name,
                                           parent=str(self.parent))

    def is_selected(self):
        return 'file-selected' in self.web_elem.get_attribute('class')

    def is_file(self):
        return 'browser-file' in self._icon.get_attribute('class')

    def is_directory(self):
        return 'browser-directory' in self._icon.get_attribute('class')

    def is_icon_visible(self, name):
        icon = getattr(self, '{icon}_icon'.format(icon=name))
        return 'file-status-icon' in icon.get_attribute('class')

    def click_on_tool(self, name):
        tool = getattr(self, '_{tool}_tool'.format(tool=name))
        tool_icon = tool.find_element_by_css_selector('.oneicon')
        click_on_web_elem(self.driver, tool_icon,
                          lambda: 'cannot click on "{}" in '
                                  '{}'.format(name, self))

    def double_click(self):
        ActionChains(self.driver).double_click(self.web_elem).perform()
