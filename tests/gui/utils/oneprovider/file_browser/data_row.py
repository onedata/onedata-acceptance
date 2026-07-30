"""Utils and fixtures to facilitate operation on file row in file browser
in oneprovider web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.utils.core.web_elements import Button, Label, WebElement
from tests.gui.utils.oneprovider.browser_row import BrowserRow


class DataRow(BrowserRow):
    size = Label(".fb-table-col-size .file-item-text")
    replication_rate = Label(".fb-table-col-replication .replication-rate-text")
    qos_status = WebElement(".status-icon .qos-status-icon")
    modified = Label(".fb-table-col-modification .file-item-text")
    changed = Label(".fb-table-col-ctime .file-item-text")

    shared_tag = WebElement(".file-status-shared")
    public_data_tag = WebElement(".file-public-data-icon")
    metadata_tag = WebElement(".file-status-metadata")
    qos_tag = WebElement(".file-status-qos")
    dataset_tag = WebElement(".file-status-dataset")
    inherited_tag = WebElement(".item-inheritance-icon")
    data_protected_tag = WebElement(".file-data-protected-icon")
    metadata_protected_tag = WebElement(".file-metadata-protected-icon")
    no_access_tag = WebElement(".file-status-forbidden")
    hardlink_tag = WebElement(".file-status-hardlinks")
    recalled_tag = WebElement(".file-status-recalled")
    recalling_tag = WebElement(".file-status-recalling")
    tag_label = Label(".file-status-tag")
    size_statistics_icon = WebElement(".dir-size-container .one-icon")

    xattr = Label(".table-cell-xattr-info")
    json = Label(".table-cell-json-info")
    copy_json_icon = Button(".oneicon-browser-copy")

    def __str__(self) -> str:
        return f"{self.name} in {self.parent}"

    def is_symbolic_link(self) -> bool:
        return "browser-file" in self._icon.get_attribute(
            "class"
        ) and "oneicon-shortcut" in self._icon_tag.get_attribute("class")

    def is_directory_symbolic_link(self) -> bool:
        return "browser-directory" in self._icon.get_attribute(
            "class"
        ) and "oneicon-shortcut" in self._icon_tag.get_attribute("class")

    def is_malformed_symbolic_link(self) -> bool:
        return "browser-file" in self._icon.get_attribute(
            "class"
        ) and "oneicon-x" in self._icon_tag.get_attribute("class")

    def is_malformed_directory_symbolic_link(self) -> bool:
        return "browser-directory" in self._icon.get_attribute(
            "class"
        ) and "oneicon-x" in self._icon_tag.get_attribute("class")
