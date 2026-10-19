"""Utils and fixtures to facilitate operations on Space Marketplace in Onezone GUI"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Label,
    NamedButton,
    WebElement,
    WebItemsSequence,
)
from tests.gui.utils.onezone.generic_page import ListPage
from tests.gui.utils.onezone.space_configuration_subpage import SpaceTag


class SpaceSupportItem(PageObject):
    text = id = Label(".text")


class MarketplaceSpace(PageObject):
    name = id = Label(".space-name .item-name")
    tags_list = WebItemsSequence(".tags-input .tag-item", cls=SpaceTag)
    access_info = Label(".access-info-head-container")

    organization_name = Label(".organization-name")
    creation_time = Label(".creation-time .creation-time-text")
    providers_list = WebItemsSequence(
        ".space-item-support-list .support-item", cls=SpaceSupportItem
    )

    visit_space = Button(".visit-space-link")
    configure_space = Button(".configure-space-link")

    show_description_button = Button(".expand-btn")
    description = Label(".marketplace-space-description")
    description_element = WebElement(".marketplace-space-description")


class SpaceMarketplacePage(ListPage):
    advertise_space_button = NamedButton(".one-button", text="Advertise your space")
    spaces_marketplace_list = WebItemsSequence(
        ".spaces-marketplace-list .spaces-marketplace-item",
        cls=MarketplaceSpace,
    )
