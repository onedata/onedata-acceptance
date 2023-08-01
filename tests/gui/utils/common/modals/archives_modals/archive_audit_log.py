"""Utils and fixtures to facilitate operations on archive audit log modal.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


import time
from tests.gui.utils.common.common import Toggle
from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import Input, Label, Button,\
    WebElementsSequence, WebItemsSequence, WebElement
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.oneprovider.browser_row import BrowserRow


class FilesLog(PageObject, BrowserRow):
    name = id = Label('.file-name')
    clickable_field = WebElement('.file-name')

    def click_and_enter(self):
        time.sleep(0.1)
        ActionChains(self.driver).click(self.clickable_field).perform()
        self.wait_for_selected()
        ActionChains(self.driver).key_down(Keys.ENTER).perform()

    def click(self):
        time.sleep(0.1)
        ActionChains(self.driver).click(self.clickable_field).perform()


class ArchiveAuditLog(Modal):
    file_creation_time = Label('.timestamp-cell')
    _data = WebElementsSequence('.table-entry.data-row')
    data = WebItemsSequence('.table-entry.data-row', cls=FilesLog)
    _bottom_of_visible_fragment = WebElement('.bottom-shadow-keeper')
    scroll_bar = WebElement('.table-scrollable-container .ps__rail-y')

    info_dict = {'creation_time': 0,
                 'name': 1,
                 'info_message': 2,
                 'creation_duration_time': 3}
    _elems_extra_info = {}

    time_taken = Label('.property-value.time-taken-text')

    def scroll_by_press_space(self):
        action = ActionChains(self.driver)
        action.key_down(Keys.SPACE).perform()

    def gather_extra_info(self, elems):
        for elem in elems:
            if not self._elems_extra_info[elem[self.info_dict['name']]]:
                self._elems_extra_info[elem[self.info_dict['name']]] = [elem]
            else:
                self._elems_extra_info[elem[self.info_dict['name']]].append(elem)

    def info_of_visible_elems(self, option):
# creation time | name | event message | creation duration time
        index = self.info_dict[option]
        files = self._data
        names = [f.text.split('\n') for f in files]
        print(names)
        elems_info = []
        for name in names:
            if len(name) > 3:
                if len(name) == 5:
                    name[1] += name[2]
                    name[2] = name[3]
                    name.pop()
                elems_info.append(name[index])
        return elems_info

    def __str__(self):
        return 'Archive audit log'
