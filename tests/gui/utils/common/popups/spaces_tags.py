"""Utils and fixtures to facilitate operations on spaces tags popup."""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button, Input, Label, WebItemsSequence


class Tag(PageObject):
    name = id = Label(".tag-label")


class SpacesTags(PageObject):
    general = Button(".category-selector .btn-general")
    domains = Button(".category-selector .btn-domains")
    search_bar = Input(".filter-tags-input")

    tags_list = WebItemsSequence(".tags-container .selector-item", cls=Tag)

    def __str__(self):
        return "Spaces tags"
