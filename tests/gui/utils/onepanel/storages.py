"""Utils to facilitate storages control in panel GUI."""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

import re

from selenium.webdriver import ActionChains
from tests.gui.utils.common.common import DropdownSelector, Toggle
from tests.gui.utils.core import scroll_to_css_selector
from tests.gui.utils.core.base import ExpandableMixin, PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Input,
    Label,
    NamedButton,
    WebElement,
    WebElementsSequence,
    WebItem,
    WebItemsSequence,
)
from tests.gui.utils.onezone.common import InputBox
from tests.utils.utils import repeat_failed


class StorageForm(PageObject):
    storage_name = Input("input.field-generic-name")
    imported_storage = Toggle(".toggle-field-generic-importedStorage")


class POSIX(StorageForm):
    mount_point = Input("input.field-posix-mountPoint")
    timeout = Input("input.field-posix-timeout")
    read_only = Toggle(".toggle-field-posix-readonly")


class S3(StorageForm):
    hostname = Input("input.field-s3-hostname")
    bucket_name = Input("input.field-s3-bucketName")
    admin_access_key = Input("input.field-s3-accessKey")
    admin_secret_key = Input("input.field-s3-secretKey")


class Ceph(StorageForm):
    pool_name = Input("input.field-cephrados-poolName")
    username = Input("input.field-cephrados-username")
    key = Input("input.field-cephrados-key")
    monitor_hostname = Input("input.field-cephrados-monitorHostname")
    cluster_name = Input("input.field-cephrados-clusterName")
    block_size = Input("input.field-cephrados-blockSize")


class StorageAddForm(PageObject):
    storage_selector = DropdownSelector(".ember-basic-dropdown")
    add = Button(".submit-group button")
    posix = WebItem("form", cls=POSIX)
    s3 = WebItem("form", cls=S3)
    ceph = WebItem("form", cls=Ceph)


class POSIXEditorKeyValue(PageObject):
    key = WebItem(".text-left", cls=InputBox)
    key_name = id = Label(".show-edit-icon .one-label")
    val = WebItem(".form-control-column", cls=InputBox)
    delete = Button(".remove-param")


class QOSParams(PageObject):
    key_values = WebItemsSequence(
        ".text-input.group-with-tip", cls=POSIXEditorKeyValue
    )
    last_key = WebItem(
        ".text-input.group-with-tip.last-record .text-left", cls=InputBox
    )
    enabled_remove_icons = WebElementsSequence(".remove-param")

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
            css_sel = ".remove-param"
            scroll_to_css_selector(self.driver, css_sel)
            self.enabled_remove_icons[0].click()


class Editor(PageObject):
    storage_name = Input("input.field-generic_editor-name")
    params = WebItem(".qos-params-editor", cls=QOSParams)

    save_button = Button("button.btn-primary")
    cancel_button = NamedButton("button", text="Cancel")


class POSIXEditor(Editor):
    mount_point = Input("input.field-posix_editor-mountPoint")
    timeout = Input("input.field-posix_editor-timeout")
    read_only = Toggle(".toggle-field-posix_editor-readonly")


class S3Editor(Editor):
    bucket_name = Input("input.field-s3_editor-bucketName")
    admin_secret_key = Input("input.field-s3_editor-secretKey")


class CephEditor(Editor):
    pool_name = Input("input.field-cephrados_editor-poolName")


class StorageEditForm(PageObject):
    posix_editor = WebItem("form", cls=POSIXEditor)
    s3_editor = WebItem("form", cls=S3Editor)
    ceph_editor = WebItem("form", cls=CephEditor)


class StorageRecord(PageObject, ExpandableMixin):
    modify = Button(".btn-default")
    name = id = Label(".item-icon-container + .one-label")
    edit_form = WebItem(
        ".storage-info .cluster-storage-add-form:not(.form-static)",
        cls=StorageEditForm,
    )
    storage_type = Label(".item-table .field-type_static-type")
    mount_point = Label(".item-table .field-posix_static-mountPoint")
    bucket_name = Label(".item-table .field-s3_static-bucketName")
    pool_name = Label(".item-table .field-cephrados_static-poolName")
    _toggle = WebElement(".one-collapsible-list-item-header")

    copy_id_button = Button(".copy-btn-icon")

    menu_button = Button(".collapsible-toolbar-toggle")
    _toolbar = WebElement(".one-collapsible-toolbar")

    def is_expanded(self):
        return bool(
            re.match(
                r".*\b(?<!-)opened\b.*", self._toggle.get_attribute("class")
            )
        )

    def expand_menu(self, driver):
        ActionChains(driver).move_to_element(self._toolbar).perform()
        self.menu_button.click()


class StorageContentPage(PageObject):
    form = WebItem(".cluster-storage-add-form", cls=StorageAddForm)
    storages = WebItemsSequence("ul li .storage-item", cls=StorageRecord)
    add_storage_backend = NamedButton("button", text="Add storage backend")
    cancel = NamedButton("button", text="Cancel")

    @repeat_failed(timeout=30)
    def click_modify_button_of_storage(self, driver, storage_name):
        for index, record in enumerate(self.storages):
            if record.name == storage_name:
                driver.execute_script(f'$(".btn-default")[{index}].click();')
                err_msg = f"{record.name} is not expanded after being clicked"
                assert record.is_expanded(), err_msg
                break
        else:
            raise RuntimeError(
                f"Cannot click on {storage_name} Modify button "
                "because storage is not visible on page."
            )
