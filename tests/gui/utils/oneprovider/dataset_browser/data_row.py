"""Utils and fixtures to facilitate operation on dataset row in dataset browser
in oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from tests.gui.utils.core.web_elements import Button, Label, WebElement
from tests.gui.utils.generic import transform
from tests.gui.utils.oneprovider.browser_row import BrowserRow


class DataRow(BrowserRow):
    name = id = Label(".file-name-inner")
    number_of_archives = WebElement(".fb-table-col-archives .file-item-text")
    menu_button = Button(".fb-table-col-actions-menu .menu-toggle")
    data_protected_tag = WebElement(".file-data-protected-icon")
    metadata_protected_tag = WebElement(".file-metadata-protected-icon")
    _status_tag = WebElement(".file-status-tag")
    clickable_field = WebElement(".file-name")
    path_to_root_file = Label(".dataset-info-secondary-file-path-internal")
    deleted_root_file_icon = WebElement(".one-icon-tag-circle")

    def __str__(self):
        return f"{self.name} in {str(self.parent)}"

    def click(self):
        ActionChains(self.driver).click(self.clickable_field).perform()
        self.wait_for_selected()

    def click_and_enter(self):
        self.click()
        ActionChains(self.driver).key_down(Keys.ENTER).perform()

    def is_tag_visible(self, name):
        try:
            getattr(self, f"{transform(name)}_tag")
        except RuntimeError:
            return False
        return True
