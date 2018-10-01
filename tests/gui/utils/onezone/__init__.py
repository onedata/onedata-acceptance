"""Utils and fixtures to facilitate operations on Onezone web GUI.
"""

__author__ = "Bartosz Walkowicz Michal Stanisz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.web_elements import WebElement, WebElementsSequence
from .common import OZPanel
from .spaces_page import SpacesPage
from .data_page import DataPage
from .groups.groups_page import GroupsPage
from .tokens_page import TokensPage
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


class OZLoggedIn(object):
    _atlas = WebElement('.onezone-atlas')
    _panels = WebElementsSequence('.main-menu-content li.main-menu-item')

    panels = {
        'data': DataPage,
        'tokens': TokensPage,
        'spaces': SpacesPage,
        'groups': GroupsPage,
    }

    def __init__(self, driver):
        self.web_elem = driver

    def __str__(self):
        return 'Onezone page'

    def __getitem__(self, item):
        item = item.lower()
        # expand side panel
        ActionChains(self.web_elem).move_to_element(self._panels[0]).perform()
        # wait for side panel to expand so we can read panel name
        sleep(0.2)
        cls = self.panels.get(item, None)
        if cls:
            item = item.replace('_', ' ').lower()
            for panel in self._panels:
                if item == panel.text.lower():
                    # open page
                    panel.click()
                    # collapse side panel
                    ActionChains(self.web_elem).move_to_element(
                        self.web_elem.find_element_by_css_selector(
                            '.row-heading .col-title')).perform()
                    # wait for side panel to collapse
                    sleep(0.2)
                    return cls(self.web_elem, self.web_elem, parent=self)
        else:
            raise RuntimeError('no "{}" on {} found'.format(item, str(self)))
