"""Utils and fixtures to facilitate operations on Onezone web GUI.
"""

__author__ = "Bartosz Walkowicz Michal Stanisz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from time import sleep

from selenium.webdriver.common.action_chains import ActionChains

from tests.gui.utils.core.web_elements import (WebElement, WebElementsSequence,
                                               Label)
from .common import OZPanel
from .data_page import DataPage
from .providers_page import ProvidersPage
from .groups.groups_page import GroupsPage
from .tokens_page import TokensPage
from .discovery_page import DiscoveryPage
from .clusters_page import ClustersPage
from .manage_account_page import ManageAccountPage
from .uploads_page import UploadsPage
from .automation_page import AutomationPage


class OZLoggedIn(object):
    _atlas = WebElement('.onezone-atlas')
    _panels = WebElementsSequence('.main-menu-content li.main-menu-item')
    _profile = WebElement('.app-layout')

    uploads = WebElement('.main-menu-column .main-menu-upload-item')

    provider_alert_message = Label('.content-info-content-container '
                                   '.text-center')

    profile_username = Label('.main-menu-column .user-account-button-username')

    panels = {
        'data': DataPage,
        'providers': ProvidersPage,
        'groups': GroupsPage,
        'tokens': TokensPage,
        'discovery': DiscoveryPage,
        'automation': AutomationPage,
        'clusters': ClustersPage
    }

    def __init__(self, driver):
        self.web_elem = driver

    def __str__(self):
        return 'Onezone page'

    def __getitem__(self, item):
        return get_page(self, item)

    def get_page_no_clicking(self, item):
        return get_page(self, item, False)


def get_page(oz_page, item, click=True):
    item = item.lower()
    # expand side panel
    ActionChains(oz_page.web_elem).move_to_element(oz_page._panels[0]).perform()
    # wait for side panel to expand so we can read panel name
    sleep(0.2)
    cls = oz_page.panels.get(item, None)
    if cls:
        item = item.replace('_', ' ').lower()
        for panel in oz_page._panels:
            if item == panel.text.lower():
                if click:
                    panel.click()
                # collapse side panel
                ActionChains(oz_page.web_elem).move_to_element(
                    oz_page.web_elem.find_element_by_css_selector(
                        '.row-heading .col-title')).perform()
                # wait for side panel to collapse
                sleep(0.2)
                return cls(oz_page.web_elem, oz_page.web_elem, parent=oz_page)
    elif item == 'profile':
        return ManageAccountPage(oz_page.web_elem, oz_page._profile, oz_page)
    elif item == 'uploads':
        return UploadsPage(oz_page.web_elem, oz_page.web_elem, oz_page)
    else:
        raise RuntimeError('no "{}" on {} found'.format(item, str(oz_page)))

