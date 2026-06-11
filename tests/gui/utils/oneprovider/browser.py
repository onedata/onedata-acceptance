"""The parent class responsible for handling browser operations
in oneprovider web GUI.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from abc import ABC
from typing import ClassVar, Optional

from selenium.common.exceptions import JavascriptException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.types import GuiObject
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Input,
    Label,
    WebElement,
    WebElementsSequence,
    WebItemsSequence,
)

from ..core import scroll_to_css_selector
from .breadcrumbs import Breadcrumbs
from .browser_row import BrowserRow


class Browser(ABC, PageObject):
    row_cls: ClassVar[Optional[type[BrowserRow]]] = None
    column_header_cls: ClassVar[Optional[type[PageObject]]] = None
    data: ClassVar[WebItemsSequence]
    column_headers: ClassVar[WebItemsSequence]

    header = WebElement(".file-browser-head-container")
    browser_msg_header = Label(".content-info-content-container h1")
    breadcrumbs = Breadcrumbs(".fb-breadcrumbs")
    refresh_button = Button(".toolbar-buttons .file-action-refresh")
    jump_input = Input(".jump-input")
    configure_columns = Button(".columns-configuration-button")
    empty_dir_msg = Label(".empty-dir-text")
    error_msg = Label(".error-dir-text")
    _empty_dir_icon = WebElement(".empty-dir-image")

    _data = WebElementsSequence(".data-row.fb-table-row")
    items_list_web_elems = WebElementsSequence(
        ".data-row.fb-table-row .fb-table-col-files"
    )

    _bottom = WebElement(".table-bottom-spacing")

    parent = ""

    def __init_subclass__(cls, **kwargs: GuiObject) -> None:
        super().__init_subclass__(**kwargs)
        if cls.row_cls is not None:
            cls.data = WebItemsSequence(".data-row.fb-table-row", cls=cls.row_cls)
        if cls.column_header_cls is not None:
            cls.column_headers = WebItemsSequence(
                ".fb-table-secondary-col", cls=cls.column_header_cls
            )

    # GETTING VISIBLE ITEMS FROM BROWSER FUNCTIONS

    def names_of_visible_elems(self) -> list[str]:
        files = self.items_list_web_elems
        names = [f.text.split("\n")[0] for f in files]
        return names

    def get_visible_items_list(self) -> list[object]:
        return [el for el in self.items_list_web_elems if el.text != ""]

    # CLICKING ON SPECIFIC OBJECTS FUNCTIONS

    def click_header(self) -> None:
        action = ActionChains(self.driver)
        action.click(self.header).perform()

    def click_on_background(self) -> None:
        ActionChains(self.driver).move_to_element_with_offset(
            self.header, 0, 0
        ).click().perform()

    # SCROLLING FUNCTIONS

    def scroll_one_file_down(self) -> None:
        action = ActionChains(self.driver)
        action.key_down(Keys.DOWN).key_down(Keys.DOWN).perform()

    def scroll_to_top(self) -> None:
        try:
            self.driver.execute_script(
                "document.querySelector('.perfect-scrollbar-element."
                "ps--active-y').scrollTo(0, 0)"
            )
        except JavascriptException:
            pass

    def scroll_to_bottom(self) -> None:
        self.driver.execute_script(
            "arguments[0].scrollTo(arguments[1]);", self.web_elem, self._bottom
        )

    def scroll_to_number_file(
        self, driver: WebDriver, number: int, browser: GuiObject
    ) -> None:
        selector = browser.get_css_selector() + " " + f".data-row:nth-of-type({number})"
        scroll_to_css_selector(driver, selector)

    def scroll_visible_fragment(self) -> None:
        self.driver.execute_script(
            "arguments[0].scrollTo(arguments[1]);",
            self.web_elem,
            self._bottom,
        )

    # OTHER UTILITIES FUNCTIONS

    def move_to_elem(self, driver: WebDriver, elem: GuiObject) -> None:
        element = getattr(self, elem + "_elem")
        ActionChains(driver).move_to_element(element).perform()

    def is_empty(self) -> bool:
        try:
            self._empty_dir_icon
        except RuntimeError:
            return False
        return True

    def get_css_selector(self) -> str:
        css_selector = self.web_elem.get_attribute("class")
        css_selector = css_selector.replace(" ", ".")
        css_selector = "." + css_selector
        return css_selector
