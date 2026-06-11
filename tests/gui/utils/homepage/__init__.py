"""Utils and fixtures to facilitate operations on Onedata homepage"""

__author__ = "Mateusz Zając"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Any
from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.utils.core.web_elements import WebElementsSequence
from tests.gui.utils.core.web_objects import PageObject
from tests.gui.utils.homepage.documentation import APIPage, DocsPage
from tests.gui.utils.homepage.how_it_works import HowItWorksPage
from tests.gui.utils.homepage.quick_start import QuickStartPage


class Homepage:
    _panels = WebElementsSequence(".nav-list .nav-link")

    panels_classes = {
        "how it works": HowItWorksPage,
        "quick Start": QuickStartPage,
        "api": APIPage,
        "docs": DocsPage,
    }

    def __init__(self, driver: WebDriver) -> None:
        self.web_elem = driver

    def __str__(self) -> str:
        return "Onedata Docs page"

    def __getitem__(self, item: str) -> Any:
        return get_page(self, item, False)

    def get_page_and_click(self, item: str) -> Any:
        return get_page(self, item)

    def get_panel_by_name(self, name: str) -> PageObject:
        return [p for p in self._panels if p.text.lower() == name.lower()][0]


def get_page(docs_page: 'Homepage', item: str, click: bool = True) -> Any:
    item = item.lower()
    cls = docs_page.panels_classes.get(item, None)
    if cls:
        panel = docs_page.get_panel_by_name(item)
        if click:
            panel.click()
        return cls(docs_page.web_elem, docs_page.web_elem, parent=docs_page)
    raise RuntimeError(f'no "{item}" on {docs_page} found')
