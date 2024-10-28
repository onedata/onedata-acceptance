"""Utils and fixtures to facilitate operations on Select files, directories
or symlinks modal.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Label,
    WebElement,
    WebItemsSequence,
)
from tests.gui.utils.oneprovider import FileBrowser
from tests.gui.utils.oneprovider.browser_row import BrowserRow


class Files(BrowserRow):
    name = id = Label(".file-name")
    clickable_field = WebElement(".file-base-name")

    def click_and_enter(self):
        time.sleep(0.1)
        ActionChains(self.driver).click(self.clickable_field).perform()
        self.wait_for_selected()
        ActionChains(self.driver).key_down(Keys.ENTER).perform()


class SelectFiles(Modal):
    file_browser = FileBrowser(".items-select-browser-part.upload-drop-zone-container")
    confirm_button = Button(".submit-selection-btn")
    files = WebItemsSequence(".fb-table-tbody .data-row", cls=Files)
    error_msg = Label(".selection-validation-error")

    def __str__(self):
        return "Select files, directories or symlinks modal"
