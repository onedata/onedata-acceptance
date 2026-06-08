"""Utils and fixtures to facilitate operations on recall archive information
modal.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

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


class ErrorLogRow(BrowserRow):
    source_file = Label(".cell-file", scroll=False)
    time = Label(".timestamp-cell", scroll=False)
    error_message = Label(".truncated-string", scroll=False)


class ArchiveRecallInformation(Modal):
    status = Label(".recall-info-row-process-status .property-value")
    dataset = Label(".recall-info-row-dataset .property-value")
    files_recalled = Label(".recall-info-row-files .property-value")
    data_recalled = Label(".recall-info-row-bytes .property-value")
    started_at = Label(".recall-info-row-started-at .property-value")
    cancelled_at = Label(".recall-info-row-cancelled-at .property-value")
    finished_at = Label(".recall-info-row-finished-at .property-value")
    items_failed = Label(".recall-info-row-files-failed .property-value")
    last_error = Label(".recall-info-row-last-error .property-value")
    cancel_recall = Button(".cancel-recall-btn")
    recalling_oneprovider = Label(".recall-info-row-recalling-provider .property-value")
    recall_destination = Label(".recall-info-row-target-path .property-value")
    error_log = Button(".logs-nav-link")
    error_file_rows = WebItemsSequence(".table-entry.data-row", cls=ErrorLogRow)
    error_log_table = WebElement(".infinite-scroll-table")

    @staticmethod
    def parse_progress(progress_text_content):
        """Parses recall progress values in format: <current_value>/<target_value>,
        eg. "1 B / 3 B" to tuple containing two strings: (current_value, target_value).
        """
        [progress_info, total_info] = progress_text_content.split("/")
        progress_info = progress_info.strip()
        total_info = total_info.strip()
        return (progress_info, total_info)

    def __str__(self):
        return "Archive recall information"

    def get_progress_info(self, type):
        """Returns a tuple with (currnet_value, total_value) for progress info.
        Return values are in string, because they can contain size with units, eg.
        ("3 B", "40 KiB").

        :param str type: one of values that are in "<current> / <total>" format,
                         eg. "files_recalled" or "data_recalled"
        """
        return ArchiveRecallInformation.parse_progress(getattr(self, type))

    def scroll_by_press_space(self):
        action = ActionChains(self.driver)
        action.key_down(Keys.SPACE).perform()

    def move_to_error_logs_table(self, driver):
        ActionChains(driver).move_to_element(self.error_log_table).perform()

    def scroll_to_top(self):
        try:
            self.driver.execute_script(
                "document.querySelector('.infinite-scroll-table "
                ".table-scrollable-container').scrollTo(0,0)"
            )
        except JavascriptException:
            pass

    @repeat_failed(timeout=WAIT_FRONTEND)
    def get_rows_of_columns(
        self, column_names: List[str] = None
    ) -> Dict[str, List[str]]:

        temp_columns = list(set(column_names or []) | {"source_file"})
        column_values = {column: [] for column in temp_columns}
        for row in self.error_file_rows:
            values_in_row = [getattr(row, column) for column in temp_columns]
            if any(value_in_row == "" for value_in_row in values_in_row):
                continue

            for column, value in zip(temp_columns, values_in_row):
                column_values[column].append(value)

        return column_values

    @repeat_failed(timeout=WAIT_FRONTEND)
    def get_param_of_visible_rows(self, param) -> List[str]:
        column_values = self.get_rows_of_columns([param])
        return column_values[param]
