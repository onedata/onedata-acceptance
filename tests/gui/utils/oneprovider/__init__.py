"""Utils for Oneprovider GUI tests
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from .data_tab import DataTab
from .provider_configuration import ProviderConfiguration
from .user_profile import UserProfile
from .shares import SharesContentPage
from .spaces import SpacesContentPage
from .transfers import TransfersTab
from .file_browser import FileBrowser
from ..core.web_elements import WebItem
from .dataset_browser import DatasetBrowser
from .archive_file_browser import ArchiveFileBrowser
from .archive_browser import ArchiveBrowser
from .archive_container import ArchiveContainer


class OPLoggedIn(object):
    file_browser = FileBrowser('.content-file-browser')
    shares_page = WebItem('.content-space-shares', cls=SharesContentPage)
    transfers = TransfersTab('.content-space-transfers')
    dataset_browser = DatasetBrowser('.dataset-browser')
    archive_file_browser = ArchiveFileBrowser('.content-space-datasets '
                                              '.dataset-archives-browser'
                                              ' .filesystem-browser')
    archive_browser = ArchiveBrowser('.content-space-datasets .archive-browser')
    archive_container = ArchiveContainer('.archive-browser-container')
    provider_configuration = ProviderConfiguration('.provider-config')

    def __init__(self, driver):
        self.web_elem = self.driver = driver

    def __str__(self):
        return 'Oneprovider page'

    def __getattr__(self, item):
        return self.tabs[item](self.web_elem, self.web_elem, self)

