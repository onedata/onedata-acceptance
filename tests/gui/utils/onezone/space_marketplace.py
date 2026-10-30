"""Utils and fixtures to facilitate operations on Space Marketplace in Onezone GUI"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Input,
    Label,
    NamedButton,
    WebElement,
    WebItem,
    WebItemsSequence,
)
from tests.gui.utils.onezone.generic_page import ListPage
from tests.gui.utils.onezone.space_configuration_subpage import SpaceTag


class SpaceSupportItem(PageObject):
    text = id = Label(".text")


class MarketplaceSpace(PageObject):
    name = id = Label(".space-name .item-name", scroll=False)
    tags_list = WebItemsSequence(".tags-input .tag-item", cls=SpaceTag)
    access_info = Label(".access-info-head-container")

    organization_name = Label(".organization-name")
    creation_time = Label(".creation-time .creation-time-text")
    providers_list = WebItemsSequence(
        ".space-item-support-list .support-item", cls=SpaceSupportItem
    )

    visit_space = Button(".visit-space-link")
    configure_space = Button(".configure-space-link")
    request_access = Button(".access-info-col .btn")

    show_description_button = Button(".expand-btn")
    description = Label(".marketplace-space-description")
    description_element = WebElement(".marketplace-space-description")


class SpaceTagsFilter(PageObject):
    tags = WebItemsSequence(".tag-item", cls=SpaceTag)
    add_tag = Button(".tag-creator-trigger")
    clear = Button(".input-clear-trigger")


class SpaceMarketplaceFilter(PageObject):
    search_input = Input(".input-group .search-bar")
    tags_input = WebItem(".tags-input", cls=SpaceTagsFilter)


class SpaceMarketplacePage(ListPage):
    advertise_space_button = NamedButton(".one-button", text="Advertise your space")
    refresh_button = Button(".refresh-advertised-spaces-list")
    filter_header = WebItem(".spaces-marketplace-filter-header", cls=SpaceMarketplaceFilter)
    spaces_marketplace_list = WebItemsSequence(
        ".spaces-marketplace-list .spaces-marketplace-item",
        cls=MarketplaceSpace,
    )
