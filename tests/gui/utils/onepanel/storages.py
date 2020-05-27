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


class POSIX(PageObject):
    storage_name = Input('input.field-generic-name')
    imported_storage = Toggle('.toggle-field-generic-importedStorage')
    mount_point = Input('input.field-posix-mountPoint')
    timeout = Input('input.field-posix-timeout')
    read_only = Toggle('.toggle-field-posix-readonly')


class StorageAddForm(PageObject):
    storage_selector = DropdownSelector('.ember-basic-dropdown')
    add = Button('.submit-group button')
    posix = WebItem('form', cls=POSIX)


class POSIXEditor(PageObject):
    storage_name = Input('input.field-generic_editor-name')
    mount_point = Input('input.field-posix_editor-mountPoint')
    timeout = Input('input.field-posix_editor-timeout')
    read_only = Toggle('.toggle-field-posix_editor-readonly')

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
