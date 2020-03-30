"""Utils for Oneprovider GUI tests
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from .data_tab import DataTab
from .user_profile import UserProfile
from .shares import SharesContentPage
from .spaces import SpacesContentPage
from .transfers import TransfersTab
from .file_browser import FileBrowser


class OPLoggedIn(object):
    file_browser = FileBrowser('.content-file-browser')
    transfers = TransfersTab('.content-space-transfers')

    def __init__(self, driver):
        self.web_elem = self.driver = driver

    def __str__(self):
        return 'Oneprovider page'

    def __getattr__(self, item):
        return self.tabs[item](self.web_elem, self.web_elem, self)

