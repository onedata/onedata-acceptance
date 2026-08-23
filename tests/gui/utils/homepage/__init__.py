"""Utils and fixtures to facilitate operations on Onedata homepage"""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from typing import Literal

from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebElementsSequence
from tests.gui.utils.homepage.documentation import (
    APIPage,
    DocsPage,
    HowItWorksPage,
    QuickStartPage,
)

PageName = Literal["how it works", "quick start", "api", "docs"]


class Homepage:
    _panels = WebElementsSequence(".nav-list .nav-link")

    def __init__(self, driver: WebDriver) -> None:
        self.web_elem = driver

    def __str__(self) -> str:
        return "Onedata Docs page"

    @property
    def how_it_works(self) -> HowItWorksPage:
        return HowItWorksPage(self.web_elem, self.web_elem, parent=self)

    @property
    def quick_start(self) -> QuickStartPage:
        return QuickStartPage(self.web_elem, self.web_elem, parent=self)

    @property
    def api(self) -> APIPage:
        return APIPage(self.web_elem, self.web_elem, parent=self)

    @property
    def docs(self) -> DocsPage:
        return DocsPage(self.web_elem, self.web_elem, parent=self)


class RestApiCommand(PageObject):
    command_title = Label(".api-command-title")
    command_type = Label(".api-command-type")
