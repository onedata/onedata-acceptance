"""Utils and fixtures to facilitate operation on shares in Oneprovider GUI"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Input,
    Label,
    WebElement,
    WebItemsSequence,
)

from ..breadcrumbs import Breadcrumbs
from ..file_browser import FileBrowser


class SharesOptions(PageObject):
    name = id = Label(".item-name")
    menu_button = Button(".menu-toggle-frame")
    icon = WebElement(".one-icon-tag-icon")

    def points_to_del_dir(self):
        return "oneicon-x" in self.icon.get_attribute("class")


class SharesContentPage(PageObject):
    no_shares_msg = Label(".content-info-content-container")
    name = Label(".file-browser .fb-breadcrumbs-dir > .truncate")
    shares_browser = WebItemsSequence(
        ".one-collapsible-list .list-header-row", cls=SharesOptions
    )
    path = Breadcrumbs(".share-header-path")
    url = Input(".clipboard-input.form-control")
    copy_icon = Button(".copy-btn-icon")
    breadcrumbs = Breadcrumbs(".file-browser-head-container")
    menu_button = Button(".menu-toggle-frame")
    file_browser = FileBrowser(".file-browser")

    description_tab = Button(".nav-link-description")
    create_description = Button(".btn-content-info")
    description_input = Input(".code-textarea")
    save_description = Button(".btn-primary")
    switch_editor_markdown = Button(".btn-switch-editor-mode")
    editor_mode = Label(".btn-switch-editor-mode .text")
    link_type_selector = Button(".share-link-type-selector-trigger")
