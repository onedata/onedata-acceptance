"""Utils and fixtures to facilitate operation on public share view"""

__author__ = "Bartosz Walkowicz, Natalia Organek"
__copyright__ = "Copyright (C) 2017-2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import (Label, Button, Input, WebItem)
from .share import ShareView
from ..breadcrumbs import Breadcrumbs
from ..file_browser import FileBrowser
from ...core.base import PageObject


class URLTypeSelector(PageObject):
    public_share_link = Button('.option-share-link')
    public_rest_endpoint = Button('.option-rest-link')


class PublicShareView(ShareView):
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

    def __str__(self):
        return 'Public Share View'

