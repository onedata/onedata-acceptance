"""Utils to facilitate operations on alert info popups."""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import visibility_of
from selenium.webdriver.support.ui import WebDriverWait

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button, Label
from tests.gui.utils.generic import AlertPopupType
from tests.utils.utils import element_has_class


class AlertInfoPopup(PageObject):
    popup_type: AlertPopupType

    def _get_popup_type(self) -> AlertPopupType:
        WebDriverWait(self.driver, timeout=1, poll_frequency=0.05).until(
            visibility_of(self.web_elem)
        )
        print(self.web_elem.get_attribute("class").split())
        for popup_type in AlertPopupType:
            if element_has_class(self.web_elem, popup_type.value):
                return popup_type
        raise RuntimeError(f"Unknown alert popup type in {self}")

    def __init__(
        self,
        driver: WebDriver,
        web_elem: WebElement,
        parent: object | None = None,
    ) -> None:
        super().__init__(driver, web_elem, parent)
        self.popup_type = self._get_popup_type()

    message = id = Label(".message-body")
    close = Button(".close")

    def __str__(self) -> str:
        return "alert info popup"
