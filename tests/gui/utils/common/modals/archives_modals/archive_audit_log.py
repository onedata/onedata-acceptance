"""Utils and fixtures to facilitate operations on archive audit log modal."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import time

from selenium.common.exceptions import JavascriptException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import (
    Button,
    Label,
    WebElement,
    WebElementsSequence,
    WebItemsSequence,
)
from tests.gui.utils.oneprovider.browser_row import BrowserRow
from tests.utils.utils import repeat_failed


def trim_edges(lst):
    start = 0
    end = len(lst)

    while start < end and lst[start] == "":
        start += 1

    while end > start and lst[end - 1] == "":
        end -= 1

    return lst[start:end]


class FilesLog(BrowserRow):
    name = id = Label(".file-name", scroll=False)
    event = Label(".message-text", scroll=False)
    clickable_field = WebElement(".file-name", scroll=False)
    date = Label(".timestamp-cell", scroll=False)
    duplicated_name_hash = Label(".log-filename-duplicate-hash", scroll=False)
    time_taken = Label(".time-taken-text", scroll=False)

    def click(self):
        time.sleep(0.1)
        ActionChains(self.driver).click(self.clickable_field).perform()


class ArchiveAuditLog(Modal):
    archive_name = Label(".file-base-name")
    data_row = WebItemsSequence(".table-entry.data-row", cls=FilesLog)
    info_dict = {
        "Time": "date",
        "File": "name",
        "Event": "event",
        "Time taken": "time_taken",
    }

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

    @repeat_failed(timeout=WAIT_FRONTEND)
    def get_rows_of_column(self, option):
        params = []
        for row in self.data_row:                
            if getattr(row, "name") == "":
                continue
            name_hash = None
            try:
                name_hash = row.duplicated_name_hash
            except RuntimeError:
                pass
            param = getattr(row, self.info_dict[option])
            if option == "File" and name_hash:
                param += name_hash
            params.append(param)
        return trim_edges(params)

    def __str__(self):
        return "Archive audit log"
