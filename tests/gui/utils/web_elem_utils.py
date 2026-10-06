"""Utils for working with web elements in GUI tests."""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from collections.abc import Callable, Iterator
from contextlib import contextmanager
from functools import partial
from typing import Protocol

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement
from selenium.webdriver.support.expected_conditions import (
    visibility_of,
    visibility_of_element_located,
)
from selenium.webdriver.support.ui import WebDriverWait

from tests.gui.constants import WAIT_FRONTEND
from tests.gui.type_definitions import (
    VisibilityCondition,
    WebElementOrCssLocator,
    WebElementOrSelector,
    WebElemRoot,
)
from tests.gui.utils.core.exceptions import PageObjectNotFoundError
from tests.utils.utils import element_has_class, repeat_failed


class VisibleElement(Protocol):
    def is_displayed(self) -> bool: ...


def is_element_visible_on_page(
    driver: WebDriver,
    web_elem_or_selector: WebElementOrSelector,
) -> bool:
    try:
        condition = get_visibility_condition(get_web_elem_or_locator(web_elem_or_selector))
        return bool(condition(driver))
    except (NoSuchElementException, StaleElementReferenceException):
        return False


def get_web_elem_or_locator(
    web_elem_or_selector: WebElementOrSelector,
) -> WebElementOrCssLocator:
    match web_elem_or_selector:
        case SeleniumWebElement():
            return web_elem_or_selector
        case str():
            return By.CSS_SELECTOR, web_elem_or_selector
    raise TypeError(f"Unsupported element or selector: {web_elem_or_selector!r}")


def get_visibility_condition(
    web_elem_or_locator: WebElementOrCssLocator,
) -> VisibilityCondition:
    match web_elem_or_locator:
        case SeleniumWebElement() as element:
            return visibility_of(element)

        case (By.CSS_SELECTOR, str()) as locator:
            return visibility_of_element_located(locator)

        case unsupported:
            raise TypeError(f"Unsupported element or locator: {unsupported!r}")


def is_element_visible_using_getter[VisibleElementT: VisibleElement](
    driver: WebDriver,
    web_elem_getter: Callable[[WebDriver], VisibleElementT],
) -> VisibleElementT | None:
    try:
        web_elem = web_elem_getter(driver)
        return web_elem if web_elem.is_displayed() else None
    except (NoSuchElementException, StaleElementReferenceException, PageObjectNotFoundError):
        return None


def wait_for_visible_element_using_getter[VisibleElementT: VisibleElement](
    driver: WebDriver,
    web_elem_getter: Callable[[WebDriver], VisibleElementT],
    timeout: float = WAIT_FRONTEND,
) -> VisibleElementT:
    # Wait until the getter returns a visible element.

    return WebDriverWait(driver, timeout=timeout).until(
        partial(is_element_visible_using_getter, web_elem_getter=web_elem_getter)
    )


def wait_for_element_to_disappear_using_getter[VisibleElementT: VisibleElement](
    driver: WebDriver,
    web_elem_getter: Callable[[WebDriver], VisibleElementT],
    timeout: float = WAIT_FRONTEND,
) -> None:
    WebDriverWait(driver, timeout=timeout).until_not(
        partial(is_element_visible_using_getter, web_elem_getter=web_elem_getter)
    )


def get_element_css_classes_when_visible(
    driver: WebDriver,
    web_elem: SeleniumWebElement,
    timeout: float = WAIT_FRONTEND // 4,
) -> list[str]:
    def get_element_classes(driver: WebDriver) -> list[str] | None:
        return web_elem.get_attribute("class").split() if visibility_of(web_elem)(driver) else None

    return WebDriverWait(
        driver,
        timeout=timeout,
        poll_frequency=0.05,
        ignored_exceptions=[
            ElementNotInteractableException,
            StaleElementReferenceException,
        ],
    ).until(get_element_classes)


def find_web_elem(
    web_elem_root: WebElemRoot,
    css_selector: str,
    error_message: str | Callable[[], str],
    scroll: bool = True,
) -> SeleniumWebElement:
    try:
        if scroll:
            _scroll_to_css_selector(web_elem_root, css_selector)
        item = web_elem_root.find_element(By.CSS_SELECTOR, css_selector)
    except NoSuchElementException as exc:
        if callable(error_message):
            error_message = error_message()
        raise NoSuchElementException(error_message) from exc
    return item


def find_web_elem_with_text(
    web_elem_root: WebElemRoot,
    css_selector: str,
    text: str,
    error_message: str | Callable[[], str],
    scroll: bool = True,
) -> SeleniumWebElement:
    items = web_elem_root.find_elements(By.CSS_SELECTOR, css_selector)
    if scroll:
        _scroll_to_css_selector(web_elem_root, css_selector)
    for item in items:
        if item.text.lower() == text.lower():
            return item
    if callable(error_message):
        error_message = error_message()
    raise NoSuchElementException(f'Css element with "{text}" text not found. {error_message}')


@repeat_failed(
    timeout=1,
    interval=0.05,
    exceptions=(
        ElementNotInteractableException,
        ElementClickInterceptedException,
    ),
)
def click_on_web_elem(
    web_elem: SeleniumWebElement,
    error_message: str | Callable[[], str],
) -> None:
    if (
        not web_elem.is_enabled()
        or not web_elem.is_displayed()
        or element_has_class(web_elem, "disabled")
    ):
        message = error_message() if callable(error_message) else error_message
        raise ElementNotInteractableException(message)

    web_elem.click()


def _scroll_to_css_selector(web_elem_root: WebElemRoot, css_selector: str) -> None:
    driver = getattr(web_elem_root, "parent", web_elem_root)
    driver.execute_script(
        "var el = (typeof $ === 'function' ? "
        f"$('{css_selector}')[0] : "
        f"document.querySelector('{css_selector}')); "
        "el && el.scrollIntoView(true);"
    )


@contextmanager
def rm_css_cls(
    driver: WebDriver, web_elem: SeleniumWebElement, css_cls: str
) -> Iterator[SeleniumWebElement]:
    driver.execute_script(f"arguments[0].classList.remove('{css_cls}')", web_elem)
    yield web_elem
    driver.execute_script(f"arguments[0].classList.add('{css_cls}')", web_elem)
