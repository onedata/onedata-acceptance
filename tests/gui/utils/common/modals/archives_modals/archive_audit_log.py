"""Utils and fixtures to facilitate operations on archive audit log modal."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import time
from typing import Dict, List

from selenium.common.exceptions import JavascriptException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import (
    Button,
    Label,
    WebElement,
    WebItemsSequence,
)
from tests.gui.utils.oneprovider.browser_row import BrowserRow
from tests.utils.utils import repeat_failed


class FilesLog(BrowserRow):
    file = id = Label(".file-name", scroll=False)
    event = Label(".message-text", scroll=False)
    clickable_field = WebElement(".file-name", scroll=False)
    time = Label(".timestamp-cell", scroll=False)
    duplicated_name_hash = Label(".log-filename-duplicate-hash", scroll=False)
    time_taken = Label(".time-taken-text", scroll=False)

    def click(self):
        time.sleep(0.1)
        ActionChains(self.driver).click(self.clickable_field).perform()


class ArchiveAuditLog(Modal):
    archive_name = Label(".file-base-name")
    data_row = WebItemsSequence(".table-entry.data-row", cls=FilesLog)

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
    def get_rows_of_columns(self, options):
        params_dict: Dict[str, List[str]] = {}

        options_set = set(options)
        options_set.add("file")

        for row in self.data_row:
            params = [getattr(row, option) for option in options_set]
            if any(param == "" for param in params):
                continue
            try:
                name_hash = row.duplicated_name_hash
            except RuntimeError:
                name_hash = None

            if name_hash:
                params[options.index("name")] += name_hash

            for option, param in zip(options, params):
                params_dict[option] = params_dict.get(option, []) + [param]

        return params_dict

    def __str__(self):
        return "Archive audit log"
