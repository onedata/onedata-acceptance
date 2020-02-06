"""Utils and fixtures for operations on edit permissions modal.
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.common.common import Toggle
from tests.gui.utils.common.modals import MenuModal
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import (Label, WebItemsSequence, Input,
                                               WebItem, Button, NamedButton, 
                                               WebElement)


class ACLPermissionType(PageObject):
    name = id = Label('.checkbox-label')
    checkbox = Button('.permission-checkbox')

    def is_checked(self):
        classes = self.checkbox.get_attribute('class')
        if 'checked' in classes:
            return True
        return False

    def __str__(self):
        return 'permission type option {} in {}'.format(self.name, self.parent)


class PosixPermissionList(PageObject):
    name = id = Label('.entity-name')
    permission_type = WebItemsSequence('li.permission', cls=ACLPermissionType)


class POSIX(PageObject):
    value = Input('input')
    description = WebElement('.permissions-string-container')
    entity_permission_list = WebItemsSequence('.row entity-permissions-row',
                                              cls=PosixPermissionList)

    def __str__(self):
        return 'POSIX permission in {}'.format(self.parent)


class AclPermission(PageObject):
    name = id = Label('label')
    toggle = Toggle('.one-way-toggle')


class AclPermissionGroup(PageObject):
    name = id = Label('.one-tree-item-content > label')
    toggle = Toggle('.one-tree-item-content .form-group .one-way-toggle')
    permissions = WebItemsSequence('.tree-expanded li', cls=AclPermission)

    def is_expanded(self):
        return 'subtree-expanded' in self.web_elem.get_attribute('class')

    def expand(self):
        if not self.is_expanded():
            self.click()


class MemberAclPermission(PageObject):
    name = id = Label('.subject-name')
    menu_button = Button('.btn-menu-toggle')
    menu = WebItem('.webui-popover-content '
                   '.one-webui-popover.one-collapsible-toolbar-popover',
                   cls=MenuModal)
    acl_permission_group = WebItemsSequence('.privileges-tree-editor '
                                            '.one-tree-item.has-subtree ',
                                            cls=AclPermissionGroup)

    allow_option = Button('.ace-type-allow')
    deny_option = Button('.ace-type-deny')

    def expand(self):
        self.click()


class ACL(PageObject):
    member_permission_list = WebItemsSequence('.acl-editor '
                                              '.ace.one-collapsible-list-item',
                                              cls=MemberAclPermission)
    _toggle = WebElement('.ember-basic-dropdown-trigger[role="button"]')

    def expand_dropdown(self):
        self._toggle.click()


class EditPermissionsModal(Modal):
    posix = WebItem('.modal-body', cls=POSIX)
    acl = WebItem('.modal-body', cls=ACL)

    posix_button = Button('.permissions-type-posix')
    acl_button = Button('.permissions-type-acl')

    cancel_button = NamedButton('button', text='Cancel')
    save_button = NamedButton('button', text='Save')

    permission_denied_alert = WebElement('.alert.error')

    def __str__(self):
        return 'Edit permission modal'

