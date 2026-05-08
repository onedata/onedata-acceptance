"""Utils and fixtures to facilitate operations on Onedata documentation"""

__author__ = "Mateusz Zając"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.web_elements import WebElementsSequence
from tests.gui.utils.homepage.api import APIPage
from tests.gui.utils.homepage.documentation import DocsPage
from tests.gui.utils.homepage.how_it_works import HowItWorksPage
from tests.gui.utils.homepage.quick_start import QuickStartPage

panels_dict = {"how it works": 0, "quick start": 1, "docs": 2, "api": 3}


class Homepage:
    _panels = WebElementsSequence(".nav-list .nav-link")

    panels = {
        "how it works": HowItWorksPage,
        "quick start": QuickStartPage,
        "api": APIPage,
        "docs": DocsPage,
    }

    def __init__(self, driver):
        self.web_elem = driver

    def __str__(self):
        return "Onedata Docs page"

    def __getitem__(self, item):
        return get_page(self, item, False)

    def get_page_and_click(self, item):
        return get_page(self, item)

    def get_panels(self):
        return self._panels


def get_page(docs_page, item, click=True):
    item = item.lower()
    cls = docs_page.panels.get(item, None)
    if cls:
        panel = docs_page.get_panels()[panels_dict[item]]
        if click:
            panel.click()
        return cls(docs_page.web_elem, docs_page.web_elem, parent=docs_page)
    raise RuntimeError(f'no "{item}" on {docs_page} found')
