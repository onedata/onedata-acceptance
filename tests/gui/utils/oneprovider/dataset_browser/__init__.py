"""Utils for dataset browser and it's components in Oneprovider GUI tests"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

from functools import partial

from selenium.common.exceptions import JavascriptException
from selenium.webdriver import ActionChains
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Label,
    WebElement,
    WebItem,
    WebItemsSequence,
)

from ..breadcrumbs import Breadcrumbs
from .data_row import DataRow


class DatasetColumnHeader(PageObject):
    name = id = Label(".column-name")


class _DatasetBrowser(PageObject):
    breadcrumbs = Breadcrumbs(".fb-breadcrumbs")
    data = WebItemsSequence(".data-row.fb-table-row", cls=DataRow)
    _empty_dir_icon = WebElement(".empty-dir-image")
    error_msg = Label(".error-dir-text")
    header = WebElement(".file-browser-head-container")
    _bottom = WebElement(".table-bottom-spacing")

    configure_columns = Button(".dataset-browser .columns-configuration-button")
    column_headers = WebItemsSequence(
        ".fb-table-secondary-col", cls=DatasetColumnHeader
    )

    def __str__(self):
        return f"dataset browser in {self.parent}"

    def is_empty(self):
        try:
            self._empty_dir_icon
        except RuntimeError:
            return False
        return True

    def scroll_to_bottom(self):
        self.driver.execute_script(
            "arguments[0].scrollTo(arguments[1]);", self.web_elem, self._bottom
        )

    def click_on_background(self):
        ActionChains(self.driver).move_to_element_with_offset(
            self.header, 0, 0
        ).click().perform()

    def scroll_to_top(self):
        try:
            self.driver.execute_script(
                "document.querySelector('.perfect-scrollbar-element."
                "ps--active-y').scrollTo(0, 0)"
            )
        except JavascriptException:
            pass


DatasetBrowser = partial(WebItem, cls=_DatasetBrowser)
