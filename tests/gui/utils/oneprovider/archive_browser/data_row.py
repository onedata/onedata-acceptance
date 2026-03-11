"""Utils and fixtures to facilitate operation on archive row in archive
browser in oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import re

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebElement, WebItem
from tests.gui.utils.oneprovider.browser_row import BrowserRow


class ArchiveState(PageObject):
    state_type = Label(".archive-state-type")
    state_details = Label(".archive-state-details")

    def get_state_name(self):
        return self.state_type.lower()

    def get_files_count(self) -> int:
        match = re.match(r".*(\d+) file.*", self.state_details)
        if match is None:
            raise ValueError(f"Cannot parse file count from: {self.state_details}")
        return int(match.group(1))

    def get_size(self):
        return self.state_details.split(",")[-1].strip()


class DataRow(BrowserRow):
    state = WebItem(".fb-table-col-state .file-item-text", cls=ArchiveState)
    bagit_tag = WebElement(".archive-bagit-tag")
    dip_tag = WebElement(".archive-dip-tag")
    base_archive = Label(".base-archive-name")
    base_archive_description = Label(".fb-table-col-incremental .secondary-description")
    creator = Label(".fb-table-col-creator .file-item-text .file-owner-line")
    size_statistics_icon = WebElement(".dir-size-container .one-icon")
