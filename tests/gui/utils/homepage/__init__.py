"""Utils and fixtures to facilitate operations on Onedata homepage"""

__author__ = "Mateusz Zając"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.web_elements import WebElementsSequence
from tests.gui.utils.homepage.documentation import APIPage, DocsPage
from tests.gui.utils.homepage.how_it_works import HowItWorksPage
from tests.gui.utils.homepage.quick_start import QuickStartPage


class Homepage:
    _panels = WebElementsSequence(".nav-list .nav-link")

    panels_classes = {
        "how_it_works": HowItWorksPage,
        "quick_start": QuickStartPage,
        "api": APIPage,
        "docs": DocsPage,
    }

    def __init__(self, driver):
        self.web_elem = driver

    def __str__(self):
        return "Onedata Docs page"

    def open_page_and_click(self, item):
        return self.open_page(item, True)

    def get_panel_by_name(self, name):
        return [p for p in self._panels if p.text.lower() == name.lower()][0]

    def open_page(self, item, click=False):
        item = item.lower()
        cls = self.panels_classes.get(item, None)
        if cls:
            panel = self.get_panel_by_name(item)
            if click:
                panel.click()
            return cls(self.web_elem, self.web_elem, parent=self)
        raise RuntimeError(f'no "{item}" on {self} found')

    @property
    def how_it_works(self):
        return self.open_page("how_it_works")

    @property
    def quick_start(self):
        return self.open_page("quick_start")

    @property
    def api(self):
        return self.open_page("api")

    @property
    def docs(self):
        return self.open_page("docs")
