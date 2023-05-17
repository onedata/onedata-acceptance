"""Utils and fixtures to facilitate operations on spaces tags popup.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItemsSequence, Label, Button, \
    WebItem
from tests.gui.utils.onezone.common import InputBox


class TagsList(PageObject):
    name = id = Label('.tag-label')


class SpacesTags(PageObject):
    general_button = Button('.category-selector .btn-general')
    domains_button = Button('.category-selector .btn-domains')
    search_bar = WebItem('.filter-tags-input', cls=InputBox)

    tags_list = WebItemsSequence('.tags-container', cls=TagsList)

    def __str__(self):
        return 'Spaces tags'
