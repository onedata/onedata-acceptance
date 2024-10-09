"""Utils for archive browser and it's components in Oneprovider GUI tests"""

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


class ArchiveColumnHeader(PageObject):
    name = id = Label(".column-name")


class _ArchiveBrowser(PageObject):
    data = WebItemsSequence(
        ".archive-browser-container .data-row.fb-table-row", cls=DataRow
    )
    breadcrumbs = Breadcrumbs(".archive-browser .fb-breadcrumbs")
    create_archive = Button(
        ".hidden-xs .toolbar-buttons .oneicon-browser-archive-add"
    )
    create_archive_elem = WebElement(
        ".hidden-xs .toolbar-buttons .oneicon-browser-archive-add"
    )
    create_a_new_archive = Button(".empty-archives-create-action")
    empty_dir_msg = Label(".empty-dir-text")
    error_msg = Label(".error-dir-text")
    header = WebElement(".file-browser-head-container")
    _bottom = WebElement(".table-bottom-spacing")

    configure_columns = Button(".archive-browser .columns-configuration-button")
    column_headers = WebItemsSequence(
        ".fb-table-thead .fb-table-secondary-col", cls=ArchiveColumnHeader
    )

    def __str__(self):
        return f"archive browser in {self.parent}"

    def scroll_to_bottom(self):
        self.driver.execute_script(
            "arguments[0].scrollTo(arguments[1]);", self.web_elem, self._bottom
        )

    def click_on_background(self):
        ActionChains(self.driver).move_to_element_with_offset(
            self.header, 0, 0
        ).click().perform()

    def move_to_elem(self, driver, elem):
        element = getattr(self, elem + "_elem")
        ActionChains(driver).move_to_element(element).perform()

    def scroll_to_top(self):
        try:
            self.driver.execute_script(
                "document.querySelector('.perfect-scrollbar-element."
                "ps--active-y').scrollTo(0, 0)"
            )
        except JavascriptException:
            pass


ArchiveBrowser = partial(WebItem, cls=_ArchiveBrowser)
