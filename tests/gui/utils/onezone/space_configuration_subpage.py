"""Utils and fixtures to facilitate operations on space configuration tab
in Onezone GUI
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from selenium.webdriver import ActionChains
from tests.gui.utils.common.common import Toggle
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    AceEditor,
    Button,
    Label,
    WebElement,
    WebItem,
    WebItemsSequence,
)
from tests.gui.utils.onezone.common import EditBox


class SpaceTag(PageObject):
    name = id = Label(".tag-label")


class SpaceTagsEditor(PageObject):
    tags = WebItemsSequence(".tag-item", cls=SpaceTag)
    add_tag = Button(".tag-creator-trigger")
    save_button = Button(".save-icon")


class MarketplaceContactEmail(PageObject):
    name = Label(".one-label")

    save_icon = Button(".save-icon")
    edit_icon = Button(".edit-icon")
    cancel_icon = Button(".cancel-icon")


class SpaceConfigurationPage(PageObject):
    space_name = WebItem(".space-name", cls=EditBox)
    organization_name = WebItem(".organization-name", cls=EditBox)
    space_tags_editor = WebItem(".space-tags", cls=SpaceTagsEditor)

    preview_description_mode = Button(".btn-description-view")
    editor_description_mode = Button(".btn-description-edit")

    description_text_area = AceEditor(".ace_editor")

    discard_button = Button(".btn-warning")
    save_button = Button(".btn-primary")

    advertise_toggle = Toggle(".advertised-toggle")
    advertise_toggle_web = WebElement(".advertised-toggle")
    contact_email = WebItem(".contact-email", cls=MarketplaceContactEmail)
    marketplace_link = Button(".view-in-marketplace-link")

    header_label_warning = Label(".label.label-warning")

    def move_to_toggle(self, driver):
        ActionChains(driver).move_to_element(self.advertise_toggle_web).perform()
