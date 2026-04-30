"""Utils and fixtures to facilitate operations on Onedata.org website"""

__author__ = "Mateusz Zając"
__copyright__ = "Copyright (C) 2026 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.web_elements import Label, WebItem
from tests.gui.utils.core.base import PageObject


class EndpointPage(PageObject):
    name = Label(".api-endpoint-title")
    
    def __getitem__(self, item):
        if hasattr(self, "elements_list"):
            return self.elements_list[item]
        raise ValueError("there is not elements_list member in class instance")


class APIReference:
    current_endpoint = WebItem(".docs-main-content", cls=EndpointPage)
    
    def __init__(self, driver):
        self.driver = driver
        self.web_elem = driver

    def __str__(self):
        return "API Reference page"
