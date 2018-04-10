"""Utils for data tab in Oneprovider GUI tests
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebElementsSequence, WebItem
from .file_uploader import FileUploader
from .sidebar import DataTabSidebar
from .toolbar import DataTopToolBar
from ..breadcrumbs import Breadcrumbs
from ..file_browser import FileBrowser


class DataTab(PageObject):
    toolbar = WebItem('header nav.navbar ul.data-files-list-toolbar',
                      cls=DataTopToolBar)
    breadcrumbs = Breadcrumbs('.secondary-top-bar .file-breadcrumbs-list')
    file_browser = FileBrowser('.lower-main-content .data-files-list')
    file_uploader = WebItem('#main-content + .file-upload .file-upload',
                            cls=FileUploader)
    _sidebar = WebElementsSequence('.lower-main-content nav.secondary-sidebar, '
                                   '#data-sidebar-resize-handler')

    @property
    def sidebar(self):
        sidebar_, resize_handler = self._sidebar
        return DataTabSidebar(self.web_elem, sidebar_, self,
                              resize_handler=resize_handler)
