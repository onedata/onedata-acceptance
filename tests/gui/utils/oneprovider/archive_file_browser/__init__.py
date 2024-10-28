"""Utils for archive file browser and it's components in Oneprovider GUI tests"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from functools import partial

from selenium.common.exceptions import JavascriptException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    WebElement,
    WebElementsSequence,
    WebItem,
    WebItemsSequence,
)

from ...core import scroll_to_css_selector
from ..breadcrumbs import Breadcrumbs
from .data_row import DataRow


class _ArchiveFileBrowser(PageObject):
    data = WebItemsSequence(
        ".archive-browser-container .data-row.fb-table-row", cls=DataRow
    )
    breadcrumbs = Breadcrumbs(".archive-filesystem-browser .fb-breadcrumbs")
    _empty_dir_icon = WebElement(".empty-dir-image")
    _data = WebElementsSequence(".data-row.fb-table-row")
    _bottom = WebElement(".table-bottom-spacing")
    header = WebElement(".file-browser-head-container")

    def __str__(self):
        return f"archive file browser in {self.parent}"

    def is_empty(self):
        try:
            self._empty_dir_icon
        except RuntimeError:
            return False
        return True

    def names_of_visible_elems(self):
        files = self._data
        names = [f.text.split("\n")[0] for f in files]
        return names

    def scroll_to_bottom(self):
        self.driver.execute_script(
            "arguments[0].scrollTo(arguments[1]);", self.web_elem, self._bottom
        )

    def get_css_selector(self):
        css_selector = self.web_elem.get_attribute("class")
        css_selector = css_selector.replace(" ", ".")
        css_selector = "." + css_selector
        return css_selector

    def click_on_dip_aip_view_mode(self, driver, option):
        selector = f".archive-filesystem-table-head-row .select-archive-{option}-btn"
        driver.find_element(By.CSS_SELECTOR, selector).click()

    def scroll_to_number_file(self, driver, number, browser):
        selector = browser.get_css_selector() + " " + f".data-row:nth-of-type({number})"
        scroll_to_css_selector(driver, selector)

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


ArchiveFileBrowser = partial(WebItem, cls=_ArchiveFileBrowser)
