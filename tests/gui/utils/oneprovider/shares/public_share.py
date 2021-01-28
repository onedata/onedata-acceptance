"""Utils and fixtures to facilitate operation on public share view"""

__author__ = "Bartosz Walkowicz, Natalia Organek"
__copyright__ = "Copyright (C) 2017-2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.web_elements import Label, Button, Input, WebElement
from ..breadcrumbs import Breadcrumbs
from ..file_browser import FileBrowser


class PublicShareView(object):
    name = Label('.fb-breadcrumbs-dir')
    url = Input('.clipboard-input.form-control')
    copy_icon = Button('.oneicon-browser-copy')
    breadcrumbs = Breadcrumbs('.file-browser-head-container')
    file_browser = FileBrowser('.content-file-browser')
    error_msg = Label('.error-details.active')
    description_tab = Button('.nav-link-description')
    description = Label('.markdown-view')
    no_files_message_header = Label('.content-info-content-container h1')

    def __init__(self, driver):
        self.web_elem = self.driver = driver

    def __str__(self):
        return 'Public Share View'

