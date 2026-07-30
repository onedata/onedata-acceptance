"""Utils to facilitate operations on alert info popups."""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button, Label
from tests.gui.utils.generic import get_element_css_classes_when_visible

from .generic import AlertPopupCssClass


class AlertInfoPopup(PageObject):
    popup_css_class: AlertPopupCssClass

    def __init__(
        self,
        driver: WebDriver,
        web_elem: WebElement,
        parent: object | None = None,
    ) -> None:
        super().__init__(driver, web_elem, parent)
        self.popup_css_class = get_popup_css_class(self)

    message = id = Label(".message-body")
    close = Button(".close")

    def __str__(self) -> str:
        return "alert info popup"


def get_popup_css_class(alert_popup: AlertInfoPopup) -> AlertPopupCssClass:
    css_classes: list[str] = get_element_css_classes_when_visible(
        alert_popup.driver, alert_popup.web_elem
    )
    for popup_type in AlertPopupCssClass:
        if popup_type.value in css_classes:
            return popup_type

    raise RuntimeError(f"Unknown alert popup type in {alert_popup}")
