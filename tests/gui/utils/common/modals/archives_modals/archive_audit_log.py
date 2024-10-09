"""Utils and fixtures to facilitate operations on archive audit log modal."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


import time

from selenium.common.exceptions import JavascriptException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Label,
    WebElement,
    WebElementsSequence,
    WebItemsSequence,
)
from tests.gui.utils.oneprovider.browser_row import BrowserRow


class FilesLog(PageObject, BrowserRow):
    name = id = Label(".file-name")
    event = Label(".message-text")
    clickable_field = WebElement(".file-name")

    def click(self):
        time.sleep(0.1)
        ActionChains(self.driver).click(self.clickable_field).perform()


class ArchiveAuditLog(Modal):
    _data_row = WebElementsSequence(".table-entry.data-row")
    data_row = WebItemsSequence(".table-entry.data-row", cls=FilesLog)
    info_dict = {"Time": 0, "File": 1, "Event": 2, "Time taken": 3}
    x = Button(".close")

    def scroll_by_press_space(self):
        action = ActionChains(self.driver)
        action.key_down(Keys.SPACE).perform()

    def scroll_to_top(self):
        try:
            self.driver.execute_script(
                "document.querySelector("
                "'.audit-log-browser "
                ".table-scrollable-container')"
                ".scrollTo(0, 0)"
            )
        except JavascriptException:
            pass

    def get_rows_of_column(self, option):
        # order in dict
        #  0   |  1   |   2   |     3
        # Time | File | Event | Time taken
        index = self.info_dict[option]
        rows_data = self._data_row
        all_rows = [f.text.split("\n") for f in rows_data]
        rows = []
        for row in all_rows:
            if len(row) > 3:
                # when file`s name repeats, annotation @... is added to
                # another column
                if len(row) == 5:
                    row[1] += row[2]
                    row.pop(2)
                rows.append(row[index])
        return rows

    def __str__(self):
        return "Archive audit log"
