"""Utils to facilitate operations on manage account page in Onezone gui"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.web_elements import Button, Input, Label, WebItem
from tests.gui.utils.onezone.common import EditBox
from tests.gui.utils.onezone.generic_page import GenericPage


class ManageAccountPage(GenericPage):
    profile = Button(".user-account-button-main")
    full_name = Label(".full-name-editor")
    rename_full_name = Button(".full-name-editor .edit-icon")
    rename_username = Button(".username-editor .edit-icon")
    rename_password = Button(".password-editor-trigger .edit-icon")
    change_password = Button(".user-credentials-form .btn-primary")
    edit_box = WebItem(".editor", cls=EditBox)
    edit_user_name_box = WebItem(".username-editor", cls=EditBox)
    current_password_box = Input(".field-verify-currentPassword")
    type_new_password_box = Input(".field-change-newPassword")
    retype_new_password_box = Input(".field-change-newPasswordRetype")
    user_name = Label(".username-editor .one-label")
    show_user_account_menu_toolbar = Button(".btn-toolbar .collapsible-toolbar-toggle")
