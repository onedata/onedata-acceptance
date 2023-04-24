"""Utils and fixtures to facilitate operations on spaces tags popup.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItemsSequence, Label, Button


class TagsList(PageObject):
    name = id = Label('.tag-label')


class SpacesTags(PageObject):
    general_button = Button('.category-selector .btn-general')
    domains_button = Button('.category-selector .btn-domains')

    tags_list = WebItemsSequence('.tags-container', cls=TagsList)

    def __str__(self):
        return 'Spaces tags'
