"""Utils to facilitate storages control in panel GUI."""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import re
from typing import Any

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

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
    WebElementWithText,
    WebItem,
    WebItemsSequence,
)
from tests.gui.utils.onezone.common import InputBox
from tests.utils.utils import repeat_failed


class StoragePathType(PageObject):
    flat = WebElementWithText(".radio-inline", text="flat")
    canonical = WebElementWithText(".radio-inline", text="canonical")


class StorageForm(PageObject):
    storage_name = Input(".name-field input")
    imported_storage = Toggle(".importedStorage-field .one-way-toggle")
    storage_path_type = WebItem(".storagePathType-field", cls=StoragePathType)


class POSIX(StorageForm):
    mount_point = Input(".mountPoint-field input")
    timeout = Input(".timeout-field input")
    read_only = Toggle(".readonly-field .one-way-toggle")


class S3(StorageForm):
    bucket_name = Input(".bucketName-field input")
    admin_access_key = Input(".accessKey-field input")
    admin_secret_key = Input(".secretKey-field input")
    endpoint_url = Input(".hostname-field input")


class Ceph(StorageForm):
    pool_name = Input(".poolName-field input")
    username = Input(".username-field input")
    key = Input(".key-field input")
    monitor_hostname = Input(".monitorHostname-field input")
    cluster_name = Input(".clusterName-field input")
    block_size = Input(".blockSize-field input")


class StorageAddForm(PageObject):
    storage_selector = DropdownSelector(".type-field .dropdown-field")
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
    key_values = WebItemsSequence(".text-input.group-with-tip", cls=POSIXEditorKeyValue)
    last_key = WebItem(
        ".text-input.group-with-tip.last-record .text-left", cls=InputBox
    )
    enabled_remove_icons = WebElementsSequence(".remove-param")

    def set_last_key(self, key: Any) -> Any:
        self.last_key.value = key

    def click_value_in_modified_record(self) -> Any:
        size = len(self.key_values)
        self.key_values[size - 2].key.click()
        self.key_values[size - 2].val.click()

    def get_key_values_count(self) -> Any:
        return len(self.key_values) - 1

    def delete_first_additional_param(self) -> Any:
        if self.enabled_remove_icons:
            css_sel = ".remove-param"
            scroll_to_css_selector(self.driver, css_sel)
            self.enabled_remove_icons[0].click()


class Editor(PageObject):
    storage_name = Input(".name-field input")
    params = WebItem(".qos-params-editor", cls=QOSParams)

    save_button = Button("button.btn-primary")
    cancel_button = NamedButton("button", text="Cancel")


class POSIXEditor(Editor):
    mount_point = WebElement(".mountPoint-field input")
    timeout = Input(".timeout-field input")
    read_only = Toggle(".readonly-field .one-way-toggle")

    def change_mount_point(self, val: Any) -> Any:
        input_box = self.mount_point
        self.driver.execute_script("arguments[0].scrollIntoView();", input_box)
        input_box.clear()

        if val != "":
            input_box.send_keys(val)
            assert input_box.get_attribute("value") == val, f'entering "{val}" failed'


class S3Editor(Editor):
    bucket_name = Input(".bucketName-field input")
    admin_secret_key = Input(".secretKey-field input")


class CephEditor(Editor):
    pool_name = WebElement(".poolName-field input")


class StorageEditForm(PageObject):
    posix_editor = WebItem("form", cls=POSIXEditor)
    s3_editor = WebItem("form", cls=S3Editor)
    ceph_editor = WebItem("form", cls=CephEditor)


class StorageRecord(PageObject, ExpandableMixin):
    modify = Button(".one-icon.oneicon.oneicon-browser-rename")
    support_space = Button(".one-icon.oneicon.oneicon-space")

    name = id = Label(".item-icon-container + .one-label")
    edit_form = WebItem(
        ".storage-info .cluster-storage-add-form",
        cls=StorageEditForm,
    )
    storage_type = Label(".item-table .type-field .text")
    mount_point = Label(".item-table .mountPoint-field .text-like-field")
    bucket_name = Label(".item-table .bucketName-field .text-like-field")
    pool_name = Label(".item-table .poolName-field .text-like-field")
    _toggle = WebElement(".one-collapsible-list-item-header")

    copy_id_button = Button(".copy-btn-icon")

    menu_button = Button(".collapsible-toolbar-toggle")

    def is_expanded(self) -> Any:
        return bool(
            re.match(r".*\b(?<!-)opened\b.*", self._toggle.get_attribute("class"))
        )

    def expand_menu(self) -> Any:
        self.menu_button.click()

    def click_toggle(self) -> Any:
        self._click_on_toggle()


class StorageContentPage(PageObject):
    form = WebItem(".cluster-storage-add-form", cls=StorageAddForm)
    storages = WebItemsSequence("ul li .storage-item", cls=StorageRecord)
    add_storage_backend = NamedButton("button", text="Add storage backend")
    cancel = NamedButton("button", text="Cancel")

    @repeat_failed(timeout=30)
    def click_modify_button_of_storage(self, driver: Any, storage_name: Any) -> Any:
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

    def scroll_by_press_space(self) -> Any:
        action = ActionChains(self.driver)
        action.key_down(Keys.SPACE).perform()
