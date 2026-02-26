"""Utils and fixtures to facilitate operation on archive row in archive file
browser in oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.utils.core.web_elements import Label, WebElement
from tests.gui.utils.oneprovider.browser_row import BrowserRow


class DataRow(BrowserRow):
    size = Label(".fb-table-col-size .file-item-text")
    symlink_tag = WebElement(".fb-table-row-symlink .one-icon-tag-circle")
    hardlink_tag = WebElement(".file-status-hardlinks")
