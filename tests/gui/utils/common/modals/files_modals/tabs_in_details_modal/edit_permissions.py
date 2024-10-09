"""Utils and fixtures for operations on edit permissions modal."""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

from tests.gui.utils.common.common import Toggle
from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.common.popups import MenuPopupWithLabel
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


class ACLPermissionType(PageObject):
    name = id = Label(".checkbox-label")
    checkbox = Button(".permission-checkbox")

    def is_checked(self):
        classes = self.checkbox.get_attribute("class")
        if "checked" in classes:
            return True
        return False

    def __str__(self):
        return "permission type option {} in {}".format(self.name, self.parent)


class PosixPermissionList(PageObject):
    name = id = Label(".entity-name")
    permission_type = WebItemsSequence("li.permission", cls=ACLPermissionType)


class POSIX(PageObject):
    value = Input("input")
    description = WebElement(".permissions-string-container")
    entity_permission_list = WebItemsSequence(
        ".row entity-permissions-row", cls=PosixPermissionList
    )

    def __str__(self):
        return "POSIX permission in {}".format(self.parent)


class AclPermission(PageObject):
    name = id = Label("label")
    name_web_elem = WebElement(".node-text")
    toggle = Toggle(".one-way-toggle")


class AclPermissionGroup(PageObject):
    name = id = Label(".one-tree-item-content > label")
    toggle = Toggle(".one-tree-item-content .form-group .one-way-toggle")
    permissions = WebItemsSequence(".tree-expanded li", cls=AclPermission)

    def is_expanded(self):
        return "subtree-expanded" in self.web_elem.get_attribute("class")

    def expand(self):
        if not self.is_expanded():
            self.click()

    def get_elem_id(self):
        elem_id = self.web_elem.get_attribute("id")
        return elem_id


class MemberAclPermission(PageObject):
    name = id = Label(".subject-name")
    menu_button = Button(".btn-menu-toggle")
    menu = WebItem(
        ".webui-popover-content "
        ".one-webui-popover.one-collapsible-toolbar-popover",
        cls=MenuPopupWithLabel,
    )
    acl_permission_group = WebItemsSequence(
        ".privileges-tree-editor .one-tree-item.has-subtree ",
        cls=AclPermissionGroup,
    )

    allow_option = WebElement(".ace-type-allow")
    deny_option = WebElement(".ace-type-deny")
    _subject_type = WebElement(".item-icon .oneicon")
    header = WebElement(".one-collapsible-list-item-header")
    subject_id = Label(".subject-identifier")

    def expand(self):
        self.click()

    def subject_type(self):
        classes = self._subject_type.get_attribute("class")
        if "oneicon-user" in classes:
            return "user"
        elif "oneicon-group" in classes:
            return "group"
        else:
            return None

    def is_allow_option_checked(self):
        return "active" in self.allow_option.get_attribute("class")

    def scroll_to_elem_on_acl_permission_group(self, elem):
        css_sel = "#" + elem.get_elem_id()
        self.driver.execute_script(
            f"var el = (typeof $ === 'function' ? $('{css_sel}')[0] : "
            f"document.querySelector('{css_sel}')); "
            "el && el.scrollIntoView(true);"
        )


class ACL(PageObject):
    member_permission_list = WebItemsSequence(
        ".acl-editor .ace.one-collapsible-list-item", cls=MemberAclPermission
    )
    _toggle = WebElement('.ember-basic-dropdown-trigger[role="button"]')

    def expand_dropdown(self):
        toggle_class = self._toggle.get_attribute("class")
        if "ember-basic-dropdown-trigger--left" not in toggle_class:
            self._toggle.click()


class EditPermissionsTab(Modal):
    posix = Button(".modal-body", cls=POSIX)
    acl = Button(".modal-body", cls=ACL)

    posix_button = Button(".permissions-type-btn-posix ")
    acl_button = Button(".permissions-type-btn-acl")

    save = NamedButton(".btn-primary", text="Save")
    discard_changes = NamedButton(".btn-warning", text="Discard changes")

    permission_denied_alert = WebElement(".alert.alert-warning.forbidden")

    posix_permission_edition = WebElement(".posix-permissions-editor")

    close = Button(".close")

    def __str__(self):
        return "Edit permission tab"

    def is_hidden(self, element_name):
        element = getattr(self, element_name)
        return "hidden" in element.get_attribute("class")
