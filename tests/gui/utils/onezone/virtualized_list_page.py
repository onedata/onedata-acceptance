"""Utils for interacting with virtualized lists."""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import math
from collections.abc import Collection
from dataclasses import dataclass
from enum import Enum, auto
from typing import ClassVar

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from tests.gui.constants import WAIT_FRONTEND, ScreenSize, WindowSize
from tests.gui.utils.core import scroll_to_css_selector
from tests.gui.utils.core.base import NamedElement
from tests.gui.utils.onezone.generic_page import ListPage


@dataclass
class ScrollAnchors:
    initial_window: int
    next_windows: int


class ThirdWindowStatus(Enum):
    READY = auto()
    TIMEOUT = auto()
    UNEXPECTED_FIRST_ITEM = auto()


@dataclass(frozen=True)
class ThirdWindowResult:
    status: ThirdWindowStatus
    anchor_name: str | None = None
    expected_next_item: str | None = None


@dataclass(frozen=True)
class WindowMetrics:
    start: int
    capacity: int
    first_item_gui_idx: int


@dataclass
class WindowLayout:
    first: WindowMetrics
    second: WindowMetrics | None = None
    third: WindowMetrics | None = None
    look_back_idx: int | None = None


@dataclass(frozen=True)
class WindowLayoutCacheKey:
    page_type: type
    screen_size: WindowSize


DEFAULT_SCROLLBAR_SELECTOR = ".perfect-scrollbar-element.ps--active-y"
WINDOW_SIZE_TOLERANCE = 10


class VirtualizedListPage[T: NamedElement](ListPage):
    """Base class for lists that render only a moving window of their items."""

    item_cls: type[T]
    item_selector_prefix: str
    scroll_shift: int
    look_back_idx: int
    window_layout_cache: ClassVar[dict[WindowLayoutCacheKey, WindowLayout]] = {}

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

    @staticmethod
    def create_nth_of_type_selector(prefix: str, selector_idx: int) -> str:
        return f"{prefix}({selector_idx})"

    def get_item_row[ItemT: NamedElement](
        self,
        cls: type[ItemT],
        selector_prefix: str,
        selector_idx: int,
    ) -> ItemT:
        selector = self.create_nth_of_type_selector(selector_prefix, selector_idx)
        return cls(
            self.driver,
            self.web_elem.find_element(By.CSS_SELECTOR, selector),
        )

    def scroll_to_nth_type_selector(self, selector_prefix: str, selector_idx: int) -> None:
        selector = self.create_nth_of_type_selector(selector_prefix, selector_idx)
        scroll_to_css_selector(self.driver, selector)

    def get_element_and_wait[ItemT: NamedElement](
        self,
        previous_name: str,
        cls: type[ItemT],
        selector_prefix: str,
        selector_idx: int,
        timeout: int = WAIT_FRONTEND,
    ) -> ItemT:
        def get_changed_element(_: WebDriver) -> ItemT | None:
            element = self.get_item_row(cls, selector_prefix, selector_idx)
            return element if element.name and element.name != previous_name else None

        return WebDriverWait(
            self.driver,
            timeout=timeout,
            ignored_exceptions=(StaleElementReferenceException,),
        ).until(get_changed_element)

    def get_screen_size(self) -> WindowSize:
        size = self.driver.get_window_size()
        return WindowSize(
            width=size["width"],
            height=size["height"],
        )

    def _is_screen_size(self, screen_size: ScreenSize) -> bool:
        actual_size = self.get_screen_size()
        expected_size = screen_size.value
        return (
            abs(actual_size.width - expected_size.width) <= WINDOW_SIZE_TOLERANCE
            and abs(actual_size.height - expected_size.height) <= WINDOW_SIZE_TOLERANCE
        )

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

        self.scroll_to_nth_type_selector(self.item_selector_prefix, first_page_count - 1)

        new_visible_names = self.get_element_names()
        prev_last_name_idx = new_visible_names.index(visible_names[-1])

        visible_names.extend(new_visible_names[prev_last_name_idx + 1 :])
        self.scroll_to_list_top()
        return first_page_count, visible_names

    def get_initial_window_layout(self, use_cached: bool = False) -> WindowLayout:
        if use_cached:
            windows_cache = self.window_layout_cache[self.get_cache_key()]
            if windows_cache:
                self.trigger_first_render_using_scroll()
                if not windows_cache.second:
                    return WindowLayout(first=windows_cache.first)
                return WindowLayout(first=windows_cache.first, second=windows_cache.second)

        first_page_count, visible_names = self.get_some_first_visible_names_and_first_page_count()

        layout = WindowLayout(
            first=WindowMetrics(start=0, capacity=first_page_count, first_item_gui_idx=0)
        )

        if len(visible_names) == first_page_count:
            return layout

        self.trigger_first_render_using_scroll()

        scroll_anchor_index = self.get_initial_and_next_scroll_anchors().next_windows
        next_visible_names = self.get_element_names()

        first_name_after_scroll = next_visible_names[0]
        first_idx_after_scroll = visible_names.index(first_name_after_scroll)

        second_window_anchor_idx = next_visible_names.index(
            self.get_item_name_at_slot(scroll_anchor_index)
        )

        layout.second = WindowMetrics(
            start=first_idx_after_scroll,
            capacity=len(next_visible_names),
            first_item_gui_idx=scroll_anchor_index - second_window_anchor_idx,
        )
        return layout

    def get_item_name_at_slot(self, idx: int | None = None) -> str:
        scroll_anchor_index = self.get_initial_and_next_scroll_anchors().next_windows
        return self.get_element_and_wait(
            "",
            self.item_cls,
            self.item_selector_prefix,
            scroll_anchor_index if idx is None else idx,
            timeout=WAIT_FRONTEND // 2,
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

        windows: WindowLayout = self.get_initial_window_layout()
        if windows.second is None:
            raise IndexError(f"Index {index} is larger than number of elements")

        second_window: WindowMetrics = windows.second
        second_window_start, second_window_end = (
            second_window.start,
            second_window.start + second_window.capacity - 1,
        )

        expected_first_item_third_window = self.get_item_name_at_slot(
            second_window.first_item_gui_idx + self.scroll_shift
        )
        third_window: ThirdWindowResult = self._manage_third_window(
            previous_anchor_name=self.get_item_name_at_slot(),
            second_window=second_window,
            expected_first_item=expected_first_item_third_window,
        )

        if third_window.status is ThirdWindowStatus.READY:
            # that means third window is not last window
            additional_scrolls = (
                math.ceil((index - second_window_end - self.scroll_shift) / self.scroll_shift)
                if index > second_window_end
                else 0
            )
            previous_name = third_window.anchor_name
            if previous_name is None:
                raise RuntimeError(
                    "Previous name attribute for third window result should be given"
                )
            for _ in range(additional_scrolls):
                previous_name = self.scroll_and_wait_for_item_change(previous_name)

            window_start = second_window_start + (additional_scrolls + 1) * self.scroll_shift

        elif third_window.status is ThirdWindowStatus.UNEXPECTED_FIRST_ITEM:
            items_count, element_names = self._calculate_item_count(
                second_window_start, 0, True, expected_first_item_third_window
            )
            window_start = items_count - len(element_names)
        else:
            window_start = second_window_start

        return self.get_visible_items()[index - window_start]

    def _manage_third_window(
        self,
        previous_anchor_name: str,
        second_window: WindowMetrics,
        expected_first_item: str,
        use_cached: bool = False,
    ) -> ThirdWindowResult:
        scroll_anchor_index = self.get_initial_and_next_scroll_anchors().next_windows

        try:
            new_anchor_name = self.scroll_and_wait_for_item_change(previous_anchor_name)
        except TimeoutException:
            return ThirdWindowResult(ThirdWindowStatus.TIMEOUT)

        if use_cached:
            cached_windows = self.window_layout_cache[self.get_cache_key()]
            if cached_windows and cached_windows.third and cached_windows.look_back_idx:
                first_item_gui_idx = cached_windows.third.first_item_gui_idx
                expected_next_item = self.get_item_name_at_slot(
                    first_item_gui_idx + self.scroll_shift
                )
                self.look_back_idx = cached_windows.look_back_idx

                return ThirdWindowResult(
                    status=ThirdWindowStatus.READY,
                    anchor_name=new_anchor_name,
                    expected_next_item=expected_next_item,
                )

        second_window_first_item_gui_idx = second_window.first_item_gui_idx
        names = self.get_element_names()

        if names[0] != expected_first_item:
            return ThirdWindowResult(ThirdWindowStatus.UNEXPECTED_FIRST_ITEM)

        anchor_shift = names.index(new_anchor_name) - names.index(previous_anchor_name)
        expected_next_item = names[self.scroll_shift]

        cache_key = self.get_cache_key()
        layout = self.window_layout_cache[cache_key]
        layout.look_back_idx = self.look_back_idx = (
            second_window_first_item_gui_idx + self.scroll_shift - anchor_shift
        )

        layout.third = WindowMetrics(
            start=second_window.start + self.scroll_shift,
            capacity=len(names),
            first_item_gui_idx=scroll_anchor_index - names.index(new_anchor_name),
        )

        return ThirdWindowResult(
            status=ThirdWindowStatus.READY,
            anchor_name=new_anchor_name,
            expected_next_item=expected_next_item,
        )

    def get_cache_key(self) -> WindowLayoutCacheKey:
        return WindowLayoutCacheKey(type(self), self.get_screen_size())

    def _calculate_item_count(
        self,
        second_window_start: int,
        completed_scrolls: int,
        partial_scroll: bool,
        expected_first_item: str,
    ) -> tuple[int, list[str]]:
        item_names = self.get_element_names()
        item_count = second_window_start + completed_scrolls * self.scroll_shift

        if partial_scroll:
            item_count += self.scroll_shift - item_names.index(expected_first_item)

        return item_count + len(item_names), item_names

    def _count_from_second_window(
        self, second_window: WindowMetrics, use_cached: bool = False
    ) -> int:
        scroll_anchor_index = self.get_initial_and_next_scroll_anchors().next_windows

        expected_first_item_third_window = self.get_item_name_at_slot(
            second_window.first_item_gui_idx + self.scroll_shift
        )

        second_window_anchor_name = self.get_item_name_at_slot(scroll_anchor_index)

        result: ThirdWindowResult = self._manage_third_window(
            second_window_anchor_name,
            second_window,
            expected_first_item_third_window,
            use_cached=use_cached,
        )

        if result.status is not ThirdWindowStatus.READY:
            count, _ = self._calculate_item_count(
                second_window.start,
                completed_scrolls=0,
                partial_scroll=result.status is ThirdWindowStatus.UNEXPECTED_FIRST_ITEM,
                expected_first_item=expected_first_item_third_window,
            )
            return count

        if result.anchor_name is None or result.expected_next_item is None:
            raise RuntimeError("Ready third-window result is missing window data")

        previous_anchor_name = result.anchor_name
        expected_first_item_next_window = result.expected_next_item
        completed_scrolls = 1
        partial_scroll = False

        while True:
            try:
                new_anchor_name = self.scroll_and_wait_for_item_change(previous_anchor_name)
            except TimeoutException:
                break

            first_item_this_window = self.get_item_name_at_slot(self.look_back_idx)

            if first_item_this_window != expected_first_item_next_window:
                partial_scroll = True
                break

            expected_first_item_next_window = self.get_item_name_at_slot(
                self.look_back_idx + self.scroll_shift
            )

            previous_anchor_name = new_anchor_name
            completed_scrolls += 1

        count, _ = self._calculate_item_count(
            second_window.start,
            completed_scrolls=completed_scrolls,
            partial_scroll=partial_scroll,
            expected_first_item=expected_first_item_next_window,
        )
        return count

    def add_inital_window_layout_to_cache(self, windows: WindowLayout) -> None:
        cache_key = self.get_cache_key()
        if cache_key not in self.window_layout_cache:
            self.window_layout_cache[cache_key] = windows

    def count_items(self, use_cached: bool = False) -> int:
        # `use_cached` is set when we know the virtualized list's content has not changed since the previous call.
        self.scroll_to_list_top()
        windows: WindowLayout = self.get_initial_window_layout()

        if windows.second is None:
            return windows.first.start + windows.first.capacity

        if self.get_cache_key() not in self.window_layout_cache:
            self.add_inital_window_layout_to_cache(windows)

        return self._count_from_second_window(windows.second, use_cached=use_cached)
