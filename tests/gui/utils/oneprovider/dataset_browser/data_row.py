"""Utils and fixtures to facilitate operation on dataset row in dataset browser
in oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.utils.core.web_elements import Label, WebElement
from tests.gui.utils.oneprovider.browser_row import BrowserRow


class DataRow(BrowserRow):
    number_of_archives = WebElement(".fb-table-col-archives .file-item-text")
    data_protected_tag = WebElement(".file-data-protected-icon")
    metadata_protected_tag = WebElement(".file-metadata-protected-icon")
    path_to_root_file = Label(".dataset-info-secondary-file-path-internal")
    deleted_root_file_icon = WebElement(".one-icon-tag-circle")

    def __str__(self) -> str:
        return f"{self.name} in {str(self.parent)}"
