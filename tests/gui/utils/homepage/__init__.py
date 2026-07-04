"""Utils and fixtures to facilitate operations on Onedata homepage"""

__author__ = "Mateusz Zając"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from typing import cast

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebElementsSequence
from tests.gui.utils.homepage.documentation import (
    APIPage,
    DocsPage,
    HowItWorksPage,
    QuickStartPage,
)


class Homepage:
    _panels = WebElementsSequence(".nav-list .nav-link")

    panels_classes: dict[str, type[PageObject]] = {
        "how_it_works": HowItWorksPage,
        "quick_start": QuickStartPage,
        "api": APIPage,
        "docs": DocsPage,
    }

    def __init__(self, driver: WebDriver) -> None:
        self.web_elem = driver

    def __str__(self) -> str:
        return "Onedata Docs page"

    def open_page_and_click(self, item: str) -> PageObject:
        return self.get_page(item, True)

    def get_panel_by_name(self, name: str) -> WebElement:
        return [p for p in self._panels if p.text.lower() == name.lower()][0]

    def get_page(self, item: str, click: bool = False) -> PageObject:
        item = item.lower()
        cls = self.panels_classes.get(item, None)
        if cls:
            panel = self.get_panel_by_name(item)
            if click:
                panel.click()
            return cls(self.web_elem, self.web_elem, parent=self)
        raise RuntimeError(f'no "{item}" on {self} found')

    @property
    def how_it_works(self) -> HowItWorksPage:
        return cast(HowItWorksPage, self.get_page("how_it_works"))

    @property
    def quick_start(self) -> QuickStartPage:
        return cast(QuickStartPage, self.get_page("quick_start"))

    @property
    def api(self) -> APIPage:
        return cast(APIPage, self.get_page("api"))

    @property
    def docs(self) -> DocsPage:
        return cast(DocsPage, self.get_page("docs"))
