"""Utils and fixtures to facilitate operations on various web objects in web GUI."""

from abc import ABC, ABCMeta, abstractmethod
from typing import Optional, cast

from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement

from tests.gui.utils.generic import click_on_web_elem
from tests.webdriver import WebDriver

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


class AbstractWebElement(ABC):
    __metaclass__ = ABCMeta

    def __init__(self, css_sel: str, scroll: bool = True, name: str = "") -> None:
        self.css_sel = css_sel
        self.scroll = scroll
        self.name = name

    def __delete__(self, instance: object) -> None:
        raise AttributeError("can't delete attribute")

    def __set__(self, instance: object, value: object) -> None:
        raise AttributeError("can't set attribute")

    @abstractmethod
    def __get__(self, instance: object, owner: type[object]) -> object:
        pass


class AbstractWebItem(AbstractWebElement, ABC):
    __metaclass__ = ABCMeta

    def __init__(self, *args: object, **kwargs: object) -> None:
        item_cls = kwargs.pop("cls", None)
        if item_cls is None:
            raise ValueError("cls not specified")
        self.cls = cast(type["PageObject"], item_cls)
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]


class PageObjectMeta(ABCMeta):
    def __init__(
        cls,
        cls_name: str,
        bases: tuple[type[object], ...],
        cls_dict: dict[str, object],
    ) -> None:
        for key, val in cls_dict.items():
            if isinstance(val, AbstractWebElement) and val.name in ("id", ""):
                val.name = key
        super(PageObjectMeta, cls).__init__(cls_name, bases, cls_dict)


class AbstractPageObject:
    __metaclass__ = PageObjectMeta

    def __init__(
        self,
        driver: WebDriver,
        web_elem: SeleniumWebElement,
        parent: Optional[object] = None,
        name: str = "",
    ) -> None:
        self.driver = driver
        self.web_elem = web_elem
        self.parent = parent
        if name != "":
            self.name = name

    @abstractmethod
    def __str__(self) -> str:
        pass


class PageObject(AbstractPageObject):
    id: object

    def __init__(
        self,
        driver: WebDriver,
        web_elem: SeleniumWebElement,
        parent: Optional[object] = None,
        **kwargs: object,
    ) -> None:
        super().__init__(driver, web_elem, parent, **kwargs)  # type: ignore[arg-type]
        if not hasattr(self, "_click_area"):
            self._click_area = web_elem

    def __str__(self) -> str:
        name = self.__class__.__name__
        if self.parent:
            name += " in " + str(self.parent)
        return name

    def is_displayed(self) -> bool:
        return self.web_elem.is_displayed()

    def click(self) -> None:
        click_on_web_elem(
            self.driver,
            self._click_area,
            lambda: f"cannot click on {self}",
        )


class ExpandableMixin:
    __slots__ = ()
    _toggle: SeleniumWebElement
    driver: WebDriver

    def is_expanded(self) -> bool:
        aria_expanded = self._toggle.get_attribute("aria-expanded")
        return bool(aria_expanded and "true" == aria_expanded)

    def expand(self) -> None:
        if not self.is_expanded():
            self._click_on_toggle()

    def collapse(self) -> None:
        if self.is_expanded():
            self._click_on_toggle()

    def _click_on_toggle(self) -> None:
        click_on_web_elem(
            self.driver,
            self._toggle,
            lambda: f"cannot click on toggle for {self}",
        )
