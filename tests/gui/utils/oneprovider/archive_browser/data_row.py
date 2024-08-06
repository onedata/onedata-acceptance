"""Utils and fixtures to facilitate operation on archive row in archive
browser in oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import time
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebElement, Button, WebItem
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from tests.gui.utils.generic import transform
from tests.gui.utils.oneprovider.browser_row import BrowserRow
import re


class ArchiveState(PageObject):
    state_type = Label('.archive-state-type')
    state_details = Label('.archive-state-details')

    def get_state_name(self):
        return self.state_type.lower()

    def get_files_count(self):
        return int(re.match(r'.*(\d+) file.*', self.state_details).group(1))

    def get_size(self):
        return self.state_details.split(',')[-1].strip()


class DataRow(PageObject, BrowserRow):
    name = id = Label('.file-name-inner')
    description = Label('.secondary-description')
    state = WebItem('.fb-table-col-state .file-item-text', cls=ArchiveState)
    bagit_tag = WebElement('.archive-bagit-tag')
    dip_tag = WebElement('.archive-dip-tag')
    base_archive = Label('.base-archive-name')
    base_archive_description = Label('.fb-table-col-incremental '
                                     '.secondary-description')
    creator = Label('.fb-table-col-creator .file-item-text .file-owner-line')
    menu_button = Button('.file-row-actions-trigger')
    clickable_field = WebElement('.file-name')
    size_statistics_icon = WebElement('.dir-size-container .one-icon')

    def click_and_enter(self):
        time.sleep(0.1)
        ActionChains(self.driver).click(self.clickable_field).perform()
        self.wait_for_selected()
        ActionChains(self.driver).key_down(Keys.ENTER).perform()

    def is_tag_visible(self, name):
        try:
            getattr(self, f'{transform(name)}_tag')
        except RuntimeError:
            return False
        else:
            return True
