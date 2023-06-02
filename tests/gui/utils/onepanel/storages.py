"""Utils to facilitate storages control in panel GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import re

from selenium.webdriver import ActionChains

from tests.gui.utils.common.common import Toggle, DropdownSelector
from tests.gui.utils.core import scroll_to_css_selector
from tests.gui.utils.core.base import PageObject, ExpandableMixin
from tests.gui.utils.core.web_elements import (
    WebItemsSequence, Label, NamedButton, Input, WebItem, WebElement, Button,
    WebElementsSequence)
from tests.gui.utils.onezone.common import InputBox
from tests.utils.utils import repeat_failed


class POSIX(PageObject):
    storage_name = Input('input.field-generic-name')
    imported_storage = Toggle('.toggle-field-generic-importedStorage')
    mount_point = Input('input.field-posix-mountPoint')
    timeout = Input('input.field-posix-timeout')
    read_only = Toggle('.toggle-field-posix-readonly')


class EmbeddedCeph(PageObject):
    storage_name = Input('input.field-generic-name')
    imported_storage = Toggle('.toggle-field-generic-importedStorage')
    number_of_copies = Input('input.field-localceph-copiesNumber')
    timeout = Input('input.field-localceph-timeout')


class StorageAddForm(PageObject):
    storage_selector = DropdownSelector('.ember-basic-dropdown')
    skip_storage_detection = Toggle('.toggle-field-generic-skipStorageDetection')
    add = Button('.submit-group button')
    posix = WebItem('form', cls=POSIX)
    embedded_ceph = WebItem('form', cls=EmbeddedCeph)


class POSIXEditorKeyValue(PageObject):
    key = WebItem('.text-left', cls=InputBox)
    key_name = id = Label('.show-edit-icon .one-label')
    val = WebItem('.form-control-column', cls=InputBox)
    delete = Button('.remove-param')


class QOSParams(PageObject):
    key_values = WebItemsSequence('.text-input.group-with-tip',
                                  cls=POSIXEditorKeyValue)
    last_key = WebItem('.text-input.group-with-tip.last-record .text-left',
                       cls=InputBox)
    enabled_remove_icons = WebElementsSequence('.remove-param')

    def set_last_key(self, key):
        self.last_key.value = key

    def click_value_in_modified_record(self):
        size = len(self.key_values)
        self.key_values[size - 2].key.click()
        self.key_values[size - 2].val.click()

    def get_key_values_count(self):
        return len(self.key_values) - 1

    def delete_first_additional_param(self):
        if self.enabled_remove_icons:
            css_sel = '.remove-param'
            scroll_to_css_selector(self.driver, css_sel)
            self.enabled_remove_icons[0].click()


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

    @repeat_failed(timeout=15)
    def click_modify_button_of_storage(self, driver, storage_name):
        for index, record in enumerate(self.storages):
            if record.name == storage_name:
                driver.execute_script(f'$(".btn-default")[{index}].click();')
                err_msg = f'{record.name} is not expanded after being clicked'
                assert record.is_expanded(), err_msg
                break
        else:
            raise Exception(f'Cannot click on {storage_name} Modify button '
                            f'because storage is not visible on page.')

