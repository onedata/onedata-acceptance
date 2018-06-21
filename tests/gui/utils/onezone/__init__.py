"""Utils and fixtures to facilitate operations on Onezone web GUI.
"""

__author__ = "Bartosz Walkowicz Michal Stanisz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.web_elements import WebElement, WebElementsSequence
from .common import OZPanel
from .spaces_page import SpacesPage
from .providers_page import ProvidersPage
from .groups_page import GroupsPage
from .tokens_page import TokensPage
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep


class OZLoggedIn(object):
    _atlas = WebElement('.onezone-atlas')
    _panels = WebElementsSequence('.main-menu-content li.main-menu-item')

    panels = {
        'providers': ProvidersPage,
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
        # TODO change below sleep to wait for page to load in login step
        # wait for oz page to load
        sleep(1)
        # expand side panel
        ActionChains(self.web_elem).move_to_element(self._panels[0]).perform()
        # wait for side panel to expand so we can read panel name
        sleep(1)
        cls = self.panels.get(item, None)
        if cls:
            item = item.replace('_', ' ').lower()
            for panel in self._panels:
                if item == panel.text.lower():
                    # collapse side panel
                    ActionChains(self.web_elem).move_to_element(
                        self.web_elem.find_element_by_css_selector(
                            '.row-heading .col-title')).perform()
                    # wait for side panel to collapse
                    sleep(1)
                    return cls(self.web_elem, self.web_elem, parent=self)

        elif item == 'manage account':
            return ManageAccount(self.web_elem, self._manage_account, self)
        elif item == 'world map':
            return WorldMap(self.web_elem, self._atlas, self)
        else:
            raise RuntimeError('no "{}" on {} found'.format(item, str(self)))
