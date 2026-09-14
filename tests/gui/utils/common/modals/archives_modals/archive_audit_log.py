"""Utils and fixtures to facilitate operations on archive audit log modal."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import time
from typing import Optional, cast

from selenium.common.exceptions import JavascriptException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from tests.gui.constants import WAIT_FRONTEND
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

    def click(self) -> None:
        time.sleep(0.1)
        ActionChains(self.driver).click(self.clickable_field).perform()


class ArchiveAuditLog(Modal):
    archive_name = Label(".file-base-name")
    data_row = WebItemsSequence(".table-entry.data-row", cls=FilesLog)

    x = Button(".close")

    def scroll_by_press_space(self) -> None:
        action = ActionChains(self.driver)
        action.key_down(Keys.SPACE).perform()

    def scroll_to_top(self) -> None:
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
    def get_visible_rows_of_columns(
        self, column_names: Optional[list[str]] = None
    ) -> dict[str, list[str]]:

        temp_columns = list(set((column_names or []) + ["file"]))
        column_values: dict[str, list[str]] = {column: [] for column in temp_columns}

        for row in self.data_row:
            row = cast(FilesLog, row)
            values_in_row = [getattr(row, column) for column in temp_columns]
            if any(value_in_row == "" for value_in_row in values_in_row):
                continue

            for column, param in zip(temp_columns, values_in_row):
                column_values[column].append(param)

            try:
                name_hash = getattr(row, "duplicated_name_hash")
            except NoSuchElementException:
                name_hash = ""

            column_values["file"][-1] += name_hash
            # adding hash to last file name to make it unique in case of duplicated names

        return column_values

    @repeat_failed(timeout=WAIT_FRONTEND)
    def get_visible_rows_of_single_column(self, column_name: str) -> list[str]:
        column_values = self.get_visible_rows_of_columns([column_name])
        return column_values[column_name]

    def __str__(self) -> str:
        return "Archive audit log"
