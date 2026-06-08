"""Utils for archive file browser and it's components in Oneprovider GUI tests"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from functools import partial
from typing import Any

from selenium.webdriver.common.by import By

from tests.gui.utils.core.web_elements import WebItem

from ..browser import Browser
from .data_row import DataRow


class _ArchiveFileBrowser(Browser):
    row_cls = DataRow

    def __str__(self) -> Any:
        return f"archive file browser in {self.parent}"

    def click_on_dip_aip_view_mode(self, driver: Any, option: Any) -> Any:
        selector = f".archive-filesystem-table-head-row .select-archive-{option}-btn"
        driver.find_element(By.CSS_SELECTOR, selector).click()


ArchiveFileBrowser = partial(WebItem, cls=_ArchiveFileBrowser)
