"""Utils and fixtures to facilitate operations on various web elements in web GUI."""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from functools import partial
from typing import Any

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from tests.gui.utils.generic import find_web_elem, find_web_elem_with_text

from .base import AbstractWebElement, AbstractWebItem
from .web_objects import ButtonPageObject, ButtonWithTextPageObject, PageObjectsSequence


class WebElement(AbstractWebElement):
    """Locate a Selenium element within a page object's root element.

    ``WebElement`` is intended to be declared as a class attribute of a
    ``PageObject`` subclass.  Access through a page-object instance searches its
    ``web_elem`` using the descriptor's CSS selector and returns the matching
    Selenium ``WebElement``.  The lookup happens on every access, so the result is
    not cached.  Access through the class returns the descriptor itself.

    By default, the lookup scrolls to the matching element.  The ``scroll``
    constructor argument can disable that behavior.  The ``name`` and
    ``parent_name`` arguments customize the element and parent descriptions used
    in lookup errors.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.parent_name = kwargs.pop("parent_name", "")
        super().__init__(*args, **kwargs)

    def __get__(self, instance: Any, owner: object) -> Any:
        if instance is None:
            return self

        return find_web_elem(
            instance.web_elem,
            self.css_selector,
            lambda: self._format_msg("no {item} item found in {parent}", instance),
            scroll=self.scroll,
        )

    def _format_msg(self, error_message: str, parent: Any, **kwargs: Any) -> str:
        name = self.name.replace("_", " ").strip().upper()
        p_name = self.parent_name if self.parent_name != "" else str(parent)
        return error_message.format(item=name, parent=p_name, **kwargs)


class WebElementWithText(WebElement):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.text = kwargs.pop("text", None)
        if self.text is None:
            raise ValueError("text not specified")
        super().__init__(*args, **kwargs)

    def __get__(self, instance: Any, owner: object) -> Any:
        if instance is None:
            return self

        error_message = 'no {item} with "{text}" text found in {parent}'
        return find_web_elem_with_text(
            instance.web_elem,
            self.css_selector,
            self.text,
            lambda: self._format_msg(error_message, instance, text=self.text),
            scroll=self.scroll,
        )


class WebItem(AbstractWebItem, WebElement):
    def __get__(self, instance: Any, owner: object) -> Any:
        elem = super().__get__(instance, owner)
        return (
            elem
            if instance is None
            else self.cls(instance.driver, elem, parent=instance, name=self.name)
        )


class WebItemWithText(WebItem, WebElementWithText):
    pass


Button = partial(WebItem, cls=ButtonPageObject)
NamedButton = partial(WebItemWithText, cls=ButtonWithTextPageObject)


class Label(WebElement):
    item_not_found_msg = "{item} label not found in {parent}"

    def __get__(self, instance: Any, owner: object) -> Any:
        item = super().__get__(instance, owner)
        return item.text if instance else item


class Input(WebElement):
    def __get__(self, instance: Any, owner: object) -> Any:
        item = super().__get__(instance, owner)
        return item.get_attribute("value") if instance else item

    def __set__(self, instance: Any, val: Any) -> None:
        input_box = super().__get__(instance, type(instance))
        input_box.clear()
        if val != "":
            input_box.send_keys(val)
            assert (
                input_box.get_attribute("value") == val
            ), f'entering "{val}" to {self.name} in {instance} failed'


class AceEditor(WebElement):
    def __get__(self, instance: Any, owner: object) -> Any:
        selector = self.css_selector + " .ace_content"
        script = f"var textarea = document.querySelector('{selector}');return textarea"
        driver = instance.web_elem.parent
        if item := driver.execute_script(script):
            return item.text
        raise NoSuchElementException(
            self._format_msg("no {item} item found in {parent}", instance)
        )

    def __set__(self, instance: Any, val: Any) -> None:
        driver = instance.web_elem.parent
        selector = self.css_selector + " .ace_text-input"
        script = (
            f"var textarea = document.querySelector('{selector}');"
            f"textarea.value = '{val}';"
            "textarea.dispatchEvent(new Event('input', { bubbles: true}));"
            "return textarea.value"
        )
        inserted_val = driver.execute_script(script)
        msg = f"Inserted val is {inserted_val} instead of {val}"
        assert val == inserted_val, msg


class WebElementsSequence(AbstractWebElement):
    def __get__(self, instance: Any, owner: object) -> Any:
        if instance is None:
            return self

        return instance.web_elem.find_elements(By.CSS_SELECTOR, self.css_selector)


class WebItemsSequence(AbstractWebItem, WebElementsSequence):
    def __get__(self, instance: Any, owner: object) -> Any:
        seq = super().__get__(instance, owner)
        return (
            seq
            if instance is None
            else PageObjectsSequence(instance.driver, seq, self.cls, instance)
        )


class Icon(WebElement):
    item_not_found_msg = "{item} icon not found in {parent}"
