"""Utils and fixtures to facilitate operation on public share view"""

__author__ = "Bartosz Walkowicz, Natalia Organek"
__copyright__ = "Copyright (C) 2017-2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.web_elements import (
    Button,
    Input,
    Label,
    WebElement,
    WebElementsSequence,
    WebItem,
)

from ...core.base import PageObject
from ..breadcrumbs import Breadcrumbs
from ..file_browser import FileBrowser


class URLTypeSelector(PageObject):
    public_share_link = Button(".option-share-link")
    share_rest_endpoint = Button(".option-rest-link")


class PublicShareView:
    share_name = Label(".share-name")
    link_type_selector = Button(".url-type-selector-trigger")
    url_type_popup = WebItem(".compact-url-type-selector-actions", cls=URLTypeSelector)
    url = Input(".clipboard-input.form-control")
    copy_icon = Button(".oneicon-browser-copy")
    breadcrumbs = Breadcrumbs(".file-browser-head-container")
    shares_file_browser = FileBrowser(".content-file-browser")
    error_msg = Label(".error-details.active")

    description = Label(".markdown-view")
    no_files_message_header = Label(".content-info-content-container h1")
    share_not_found = Label(".text-center .col-xs-12")

    xml = Button(".btn-xml-editor")
    xml_data = Label(".public-data-xml-textarea")

    xml_data_openaire = WebElement(".ace_layer.ace_text-layer")
    xml_first_line = WebElement(".ace_line_group .ace_line")

    description_tab = Button(".nav-link-description")
    expose_as_public_data_tab = Button(".nav-link-publicdata")
    files_tab = Button(".nav-link-files")
    dublin_core_metadata_data = WebElementsSequence(".public-data-value")
    copy_link = Button(
        ".clipboard-btn-input[data-clipboard-target~="
        '".clipboard-line-public-url-input"]'
    )

    def __init__(self, driver):
        self.web_elem = self.driver = driver

    def __str__(self):
        return "Public share View"
