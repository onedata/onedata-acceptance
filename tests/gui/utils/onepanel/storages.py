"""Utils to facilitate storages control in panel GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import re

from selenium.webdriver import ActionChains

from tests.gui.utils.common.common import Toggle, DropdownSelector
from tests.gui.utils.core.base import PageObject, ExpandableMixin
from tests.gui.utils.core.web_elements import (WebItemsSequence, Label,
                                               NamedButton, Input,
                                               WebItem, WebElement, Button)
from tests.gui.utils.onezone.common import InputBox


class POSIX(PageObject):
    storage_name = Input('input.field-generic-name')
    imported_storage = Toggle('.toggle-field-generic-importedStorage')
    mount_point = Input('input.field-posix-mountPoint')
    timeout = Input('input.field-posix-timeout')
    read_only = Toggle('.toggle-field-posix-readonly')


class StorageAddForm(PageObject):
    storage_selector = DropdownSelector('.ember-basic-dropdown')
    skip_storage_detection = Toggle('.toggle-field-generic-skipStorageDetection')
    add = Button('.submit-group button')
    posix = WebItem('form', cls=POSIX)


class POSIXEditorKeyValue(PageObject):
    key = WebItem('.form-group .text-left', cls=InputBox)
    key_name = Label('.show-edit-icon .one-label')
    val = WebItem('.form-group .form-control-column', cls=InputBox)
    delete = Button('.remove-param')


class QOSParams(PageObject):
    key_values = WebItemsSequence('.text-input.group-with-tip',
                                  cls=POSIXEditorKeyValue)

    def set_last_key(self, key):
        size = len(self.key_values)
        self.key_values[size - 1].key.value = key

    def click_last_but_one_value(self):
        size = len(self.key_values)
        self.key_values[size - 2].key.click()
        self.key_values[size - 2].val.click()

    def get_key_values_count(self):
        return len(self.key_values) - 1

    def delete_first_additional_param(self):
        for key_val in self.key_values:
            if key_val.key_name != 'storageId' and\
                    key_val.key_name != 'providerId':
                key_val.delete.click()
                break

    def delete_param(self, key):
        for key_val in self.key_values:
            if key_val.key_name == key:
                key_val.delete.click()
                break


class POSIXEditor(PageObject):
    storage_name = Input('input.field-generic_editor-name')
    mount_point = Input('input.field-posix_editor-mountPoint')
    timeout = Input('input.field-posix_editor-timeout')
    read_only = Toggle('.toggle-field-posix_editor-readonly')

    params = WebItem('.qos-params-editor', cls=QOSParams)

    save_button = Button('button.btn-primary')
    cancel_button = NamedButton('button', text='Cancel')


class StorageEditForm(PageObject):
    posix_editor = WebItem('form', cls=POSIXEditor)


class StorageRecord(PageObject, ExpandableMixin):
    name = id = Label('.item-icon-container + .one-label')
    edit_form = WebItem('.storage-info .cluster-storage-add-form'
                        ':not(.form-static)', cls=StorageEditForm)
    # TODO: add classes in GUI code or match by label text in tests
    storage_type = Label('.item-table .field-type_static-type')
    mount_point = Label('.item-table .field-posix_static-mountPoint')
    _toggle = WebElement('.one-collapsible-list-item-header')

    copy_id_button = Button('.copy-btn-icon')

    menu_button = Button('.collapsible-toolbar-toggle')
    _toolbar = WebElement('.one-collapsible-toolbar')

    def is_expanded(self):
        return bool(re.match(r'.*\b(?<!-)opened\b.*',
                             self._toggle.get_attribute('class')))

    def expand_menu(self, driver):
        ActionChains(driver).move_to_element(self._toolbar).perform()
        self.menu_button.click()


class StorageContentPage(PageObject):
    form = WebItem('.cluster-storage-add-form', cls=StorageAddForm)
    storages = WebItemsSequence('ul li .storage-item', cls=StorageRecord)
    add_storage = NamedButton('button', text='Add storage')
    cancel = NamedButton('button', text='Cancel')
