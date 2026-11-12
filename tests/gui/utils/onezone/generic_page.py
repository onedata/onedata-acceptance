"""Utils to facilitate operations on pages in Onezone gui"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from collections.abc import Iterable
from typing import ClassVar

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from tests.gui.constants import WAIT_FRONTEND
from tests.gui.type_definitions import ListItemMainField, PageName
from tests.gui.utils.core import scroll_to_css_selector
from tests.gui.utils.core.base import NamedElement, PageObject, PageObjectMeta
from tests.gui.utils.core.web_elements import Label, NamedButton
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_FRONTEND)
def get_visible_elements_list[T: NamedElement](
    elements_list: Iterable[T],
    main_field: ListItemMainField = "name",
) -> list[T]:
    return [element for element in elements_list if getattr(element, main_field)]


class GenericPage(PageObject, metaclass=PageObjectMeta):
    name = id = Label(".row-heading .col-title")
    get_started = NamedButton(".btn-default", text="Get started")


class ListPage(PageObject):
    """
    Base class for Onezone pages exposing one or more element lists.
    This class is basically needed for function get_visible_items_list and
    provides helpers for interacting with virtualized lists.
    """

    @staticmethod
    def create_nth_of_type_selector(prefix: str, selector_idx: int) -> str:
        return f"{prefix}({selector_idx})"

    def get_item_row[T: NamedElement](
        self,
        cls: type[T],
        selector_prefix: str,
        selector_idx: int,
    ) -> T:
        selector = self.create_nth_of_type_selector(selector_prefix, selector_idx)
        return cls(
            self.driver,
            self.web_elem.find_element(By.CSS_SELECTOR, selector),
        )

    def scroll_to_nth_type_selector(self, selector_prefix: str, selector_idx: int) -> None:
        selector = self.create_nth_of_type_selector(selector_prefix, selector_idx)
        scroll_to_css_selector(self.driver, selector)

    def get_element_and_wait[T: NamedElement](
        self,
        previous_name: str,
        cls: type[T],
        selector_prefix: str,
        selector_idx: int,
        timeout: int = WAIT_FRONTEND,
    ) -> T:
        def get_changed_element(_: WebDriver) -> T | bool:
            element = self.get_item_row(cls, selector_prefix, selector_idx)
            return element if element.name and element.name != previous_name else False

        return WebDriverWait(
            self.driver,
            timeout=timeout,
            ignored_exceptions=(StaleElementReferenceException,),
        ).until(get_changed_element)


class SidebarPanelPage(GenericPage, ListPage):
    panel_name: ClassVar[PageName]
