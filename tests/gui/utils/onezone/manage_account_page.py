"""Utils to facilitate operations on manage account page in Onezone gui"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.onezone.common import EditBox
from tests.gui.utils.core.web_elements import Button, WebItem, Label
from tests.gui.utils.onezone.generic_page import GenericPage


class ManageAccountPage(GenericPage):
    profile = Button('.user-account-button-main')

    full_name = Label('.full-name-editor')
    rename_full_name = Button('.full-name-editor .edit-icon')
    edit_box = WebItem('.editor', cls=EditBox)

