"""Utils and fixtures to facilitate operation on public share view"""

__author__ = "Bartosz Walkowicz, Natalia Organek"
__copyright__ = "Copyright (C) 2017-2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import (Label, Button, Input, WebItem,
                                               WebElementsSequence)
from ..breadcrumbs import Breadcrumbs
from ..file_browser import FileBrowser
from ...core.base import PageObject


class URLTypeSelector(PageObject):
    public_share_link = Button('.option-share-link')
    public_rest_endpoint = Button('.option-rest-link')


class PublicShareView(object):
    name = Label('.fb-breadcrumbs-dir')
    share_name = Label('.share-name')
    link_type_selector = Button('.url-type-selector-trigger')
    url_type_popup = WebItem('.compact-url-type-selector-actions',
                             cls=URLTypeSelector)
    url = Input('.clipboard-input.form-control')
    copy_icon = Button('.oneicon-browser-copy')
    breadcrumbs = Breadcrumbs('.file-browser-head-container')
    file_browser = FileBrowser('.content-file-browser')
    error_msg = Label('.error-details.active')

    description = Label('.markdown-view')
    no_files_message_header = Label('.content-info-content-container h1')
    share_not_found = Label('.text-center .col-xs-12')

    # used in both: private and public share
    dublin_core_metadata_data = WebElementsSequence('.open-data-value')
    copy_link = Button('.clipboard-btn-input[data-clipboard-target~='
                       '".clipboard-line-public-url-input"]')
    description_tab = Button('.nav-link-description')
    publish_as_open_data_tab = Button('.nav-link-opendata')
    files_tab = Button('.nav-link-files')
    xml = Button('.btn-xml-editor')
    xml_data = Label('.open-data-xml-textarea')

    def __init__(self, driver):
        self.web_elem = self.driver = driver

    def __str__(self):
        return 'Public Share View'

