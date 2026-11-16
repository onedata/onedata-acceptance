"""Utils to facilitate operations on pages in Onezone gui"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import math
from collections.abc import Collection, Iterable
from dataclasses import dataclass
from typing import ClassVar

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from tests.gui.constants import WAIT_FRONTEND
from tests.gui.type_definitions import ListItemMainField, PageName
from tests.gui.utils.core import scroll_to_css_selector
from tests.gui.utils.core.base import NamedElement, PageObject, PageObjectMeta
from tests.gui.utils.core.web_elements import Label, NamedButton
from tests.utils.utils import repeat_failed


@dataclass
class ScrollAnchors:
    initial_window: int
    next_windows: int


DEFAULT_SCROLLBAR_SELECTOR = ".perfect-scrollbar-element.ps--active-y"


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


class VirtualizedListPage[T: NamedElement](ListPage):
    """Base class for lists that render only a moving window of their items."""

    item_cls: type[T]
    item_selector_prefix: str
    scroll_shift: int
    initial_window_offset: int
    next_window_offset: int

    def scroll_to_top(
        self, timeout: float = WAIT_FRONTEND, selector: str = DEFAULT_SCROLLBAR_SELECTOR
    ) -> None:
        self.driver.execute_script(f"document.querySelector('{selector}').scrollTo(0, 0)")

        def is_top_window_loaded(_: WebDriver) -> bool:
            visible_items = self.get_visible_items()
            return bool(visible_items and visible_items[0].name)

        WebDriverWait(
            self.driver,
            timeout=timeout,
            ignored_exceptions=(StaleElementReferenceException,),
        ).until(is_top_window_loaded)

    def get_visible_items(self) -> list[T]:
        raise NotImplementedError

    def get_initial_and_next_scroll_anchors(self) -> ScrollAnchors:
        raise NotImplementedError

    def get_element_names(self) -> list[str]:
        return [item.name for item in self.get_visible_items()]

    def get_all_rendered_items(self) -> Collection[T]:
        """Return rendered items, including empty virtualized placeholders."""
        raise NotImplementedError

    def scroll_to_list_top(self) -> None:
        raise NotImplementedError

    def trigger_first_render_using_scroll(self) -> None:
        # Trigger rendering of the first full window before measuring it.
        initial_scroll_idx = self.get_initial_and_next_scroll_anchors().initial_window
        self.scroll_to_nth_type_selector(self.item_selector_prefix, initial_scroll_idx)
        self.scroll_to_list_top()
        self.scroll_to_nth_type_selector(self.item_selector_prefix, initial_scroll_idx)

    def get_some_first_visible_names_and_first_page_count(self) -> tuple[int, list[str]]:
        visible_names = self.get_element_names()
        first_page_count = len(visible_names)
        self.scroll_to_nth_type_selector(self.item_selector_prefix, first_page_count)

        new_visible_names = self.get_element_names()
        prev_last_name_idx = new_visible_names.index(visible_names[-1])

        visible_names.extend(new_visible_names[prev_last_name_idx + 1 :])
        self.scroll_to_list_top()
        return first_page_count, visible_names

    def get_initial_window_layout(self) -> list[dict[str, int]]:
        first_page_count, visible_names = self.get_some_first_visible_names_and_first_page_count()
        self.trigger_first_render_using_scroll()
        next_visible_items = self.get_visible_items()
        first_name_after_scroll = next_visible_items[0].name
        first_idx_after_scroll = visible_names.index(first_name_after_scroll)

        return [
            {"start": 0, "end": first_page_count - 1},
            {
                "start": first_idx_after_scroll,
                "end": first_idx_after_scroll + len(next_visible_items) - 1,
            },
        ]

    def get_item_name_at_slot(self, idx: int | None = None) -> str:
        scroll_anchor_index = self.get_initial_and_next_scroll_anchors().next_windows
        return self.get_item_row(
            self.item_cls,
            self.item_selector_prefix,
            scroll_anchor_index if idx is None else idx,
        ).name

    def scroll_and_wait_for_item_change(self, previous_name: str) -> str:
        scroll_anchor_index = self.get_initial_and_next_scroll_anchors().next_windows
        self.scroll_to_nth_type_selector(self.item_selector_prefix, scroll_anchor_index)
        return self.get_element_and_wait(
            previous_name,
            self.item_cls,
            self.item_selector_prefix,
            scroll_anchor_index,
            timeout=WAIT_FRONTEND // 2,
        ).name

    def get_item_by_index(self, index: int) -> T:
        self.scroll_to_list_top()
        loaded_items = self.get_visible_items()

        if index < len(loaded_items):
            return loaded_items[index]

        windows = self.get_initial_window_layout()
        if len(windows) == 1:
            raise IndexError(f"Index {index} is larger than number of elements")

        second_window = windows[1]
        additional_scrolls = (
            math.ceil((index - second_window["end"]) / self.scroll_shift)
            if index > second_window["end"]
            else 0
        )
        previous_name = self.get_item_name_at_slot()
        for _ in range(additional_scrolls):
            previous_name = self.scroll_and_wait_for_item_change(previous_name)

        window_start = second_window["start"] + additional_scrolls * self.scroll_shift
        return self.get_visible_items()[index - window_start]

    def count_items(self) -> int:
        self.scroll_to_list_top()
        scroll_anchor_index = self.get_initial_and_next_scroll_anchors().next_windows
        windows = self.get_initial_window_layout()

        if len(windows) == 1:
            return windows[0]["end"] + 1

        self.initial_window_offset = windows[1]["start"] - self.scroll_shift
        previous_name = self.get_element_and_wait(
            "",
            self.item_cls,
            self.item_selector_prefix,
            scroll_anchor_index,
        ).name
        expected_first_item_next_window = self.get_item_name_at_slot(
            scroll_anchor_index + (self.initial_window_offset - 12) + self.scroll_shift
        )

        additional_scrolls = 0
        partial_scroll = False

        while True:
            self.scroll_to_nth_type_selector(self.item_selector_prefix, scroll_anchor_index)
            try:
                new_name = self.get_element_and_wait(
                    previous_name,
                    self.item_cls,
                    self.item_selector_prefix,
                    scroll_anchor_index,
                ).name
            except TimeoutException:
                break

            first_item_this_window = self.get_item_name_at_slot(
                scroll_anchor_index + self.next_window_offset
            )
            if first_item_this_window != expected_first_item_next_window:
                partial_scroll = True
                break

            expected_first_item_next_window = self.get_item_name_at_slot(
                scroll_anchor_index + self.next_window_offset + self.scroll_shift
            )
            previous_name = new_name
            additional_scrolls += 1

        elements_count = windows[1]["start"] + additional_scrolls * self.scroll_shift
        item_names = self.get_element_names()

        if partial_scroll:
            elements_count += self.scroll_shift - item_names.index(expected_first_item_next_window)
        return elements_count + len(item_names)


class SidebarPanelPage(GenericPage, ListPage):
    panel_name: ClassVar[PageName]
