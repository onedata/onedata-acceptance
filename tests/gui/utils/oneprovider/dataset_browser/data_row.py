"""Utils and fixtures to facilitate operation on dataset row in dataset browser
in oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from selenium.webdriver import ActionChains
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, Button, WebElement


class DataRow(PageObject):
    name = id = Label('.file-name-inner')
    archive = Label('.fb-table-col-archives .file-item-text')
    menu_button = Button('.fb-table-col-actions-menu .menu-toggle')
    number_of_archive = Button('.archives-count-link')

    def __str__(self):
        return f'{self.name} in {str(self.parent)}'

    def double_click(self):
        ActionChains(self.driver).double_click(self.web_elem).perform()
