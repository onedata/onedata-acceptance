"""Utils and fixtures for operations on edit permissions modal.
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject, ExpandableMixin
from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import (Label, WebItemsSequence, Input,
                                               WebItem, Button, NamedButton, 
                                               WebElement)


class PermissionType(PageObject):
    name = id = Label('.option-label')
    _options = WebElement('.one-icon')

    def is_checked(self):
        classes = self._options.get_attribute("class")
        if "oneicon-checkbox-option" in classes:
            return True
        if "oneicon-checkbox-filled" in classes:
            return True
        return False

    def click(self):
        self.web_elem.click()

    def __str__(self):
        return 'permission type option {} in {}'.format(self.name, self.parent)


class POSIX(PageObject):
    value = Input('input')

    def __str__(self):
        return 'POSIX permission in {}'.format(self.parent)


class ACLPermission(PageObject, ExpandableMixin):
    remove = Button('.oneicon-remove')
    move_up = Button('.oneicon-move-up')
    move_down = Button('.oneicon-move-down')
    _name_select = _toggle = WebElement('.col-permission-subject-select '
                                        '.select2-arrow')
    _type_select = WebElement('.col-permission-subject-type-select '
                              '.select2-arrow')
    _subject_type = WebElement('.col-permission-subject-type-select .oneicon')
    subject_name = Label('.col-permission-subject-select')
    options = WebItemsSequence('.one-option-button-container',
                               cls=PermissionType)


    def select_group(self):
        self._type_select.click()
        self.driver.find_element_by_css_selector('li.select2-result .oneicon-'
                                                 'group').click()
    
    def select_user(self):
        self._type_select.click()
        self.driver.find_element_by_css_selector('li.select2-result .oneicon-'
                                                 'user').click()

    def expand(self):
        super(ACLPermission, self).expand()
        self.subjects_list = (self.driver
                .find_elements_by_css_selector('.select2-result-label'))

    def subject_type(self):
        classes = self._subject_type.get_attribute("class")
        if 'oneicon-user' in classes:
            return 'user'
        elif 'oneicon-group' in classes:
            return 'group'
        else:
            return None


class ACL(PageObject):
    add = NamedButton('.add-ace', text='add')
    permissions = WebItemsSequence('.modal-row-main:not(:last-child)', 
                                   cls=ACLPermission)
    

class EditPermissionsModal(Modal):
    posix = WebItem('.modal-row-main.large-space', cls=POSIX)
    acl = WebItem('.ace-items', cls=ACL)
    options = WebItemsSequence('.one-option-button-container',
                               cls=PermissionType)

    def select(self, perm_type):
        for option in self.options:
            if option.name.lower() == perm_type.lower():
                option.click()
                break
        else:
            raise RuntimeError('{} permission option in {} not found'\
                               ''.format(perm_type, self))
    
    def __str__(self):
        return 'Edit permission modal'
