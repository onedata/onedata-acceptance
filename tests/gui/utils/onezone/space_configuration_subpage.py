"""Utils and fixtures to facilitate operations on space configuration tab in Onezone GUI
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.common.common import Toggle
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import NamedButton, WebItem, Label, \
    WebItemsSequence, Button
from tests.gui.utils.onezone.common import EditBox


class SpaceTag(PageObject):
    name = id = Label('.tag-label')


class SpaceConfigurationPage(PageObject):
    space_name = WebItem('.space-name .one-label', cls=EditBox)
    organization_name = WebItem('.organization-name .one-label', cls=EditBox)
    tags = WebItemsSequence('.tag-item', cls=SpaceTag)

    preview_description_mode = Button('.btn-description-view')
    editor_description_mode = Button('.btn-description-edit')

    discard_button = Button('.btn-warning')
    save_button = Button('.btn-primary')

    advertise_toggle = Toggle('.one-way-toggle')
    contact_email = Label('.contact-email .one-label', cls=EditBox)
