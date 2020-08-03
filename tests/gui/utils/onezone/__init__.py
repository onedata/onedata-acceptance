"""Utils and fixtures to facilitate operations on Onezone web GUI.
"""

__author__ = "Bartosz Walkowicz Michal Stanisz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from time import sleep

from selenium.webdriver.common.action_chains import ActionChains

from tests.gui.utils.core.web_elements import (
    WebElement, WebElementsSequence, WebItem)
from .common import OZPanel
from .data_page import DataPage
from .providers_page import ProvidersPage
from .groups.groups_page import GroupsPage
from .tokens_page import TokensPage
from .discovery_page import DiscoveryPage
from .clusters_page import ClustersPage
from .manage_account_page import ManageAccountPage


class OZLoggedIn(object):
    _atlas = WebElement('.onezone-atlas')
    _panels = WebElementsSequence('.main-menu-content li.main-menu-item')
    _profile = WebElement('.app-layout')
    _data_discovery_page = WebElement('.ember-application')

    panels = {
        'data': DataPage,
        'providers': ProvidersPage,
        'groups': GroupsPage,
        'tokens': TokensPage,
        'discovery': DiscoveryPage,
        'clusters': ClustersPage
    }

    def __init__(self, driver):
        self.web_elem = driver

    def __str__(self):
        return 'Onezone page'

    def __getitem__(self, item):
        item = item.lower()
        if item == 'data discovery':
            return DataDiscoveryPage(self.web_elem, self._data_discovery_page, self)
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
        elif item == 'profile':
            return ManageAccountPage(self.web_elem, self._profile, self)
        else:
            raise RuntimeError('no "{}" on {} found'.format(item, str(self)))
