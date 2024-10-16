"""Utils and fixtures to facilitate operation on file row in file, dataset
and archive browsers in oneprovider web GUI.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time

from tests.gui.utils.core.base import PageObject


class BrowserRow(PageObject):

    def is_selected(self):
        return "file-selected" in self.web_elem.get_attribute("class")

    def wait_for_selected(self):
        for _ in range(30):
            time.sleep(0.1)
            if self.is_selected():
                return

        raise RuntimeError("Waited too long for being selected")

    def is_file(self):
        return "fb-table-row-file" in self.web_elem.get_attribute("class")
