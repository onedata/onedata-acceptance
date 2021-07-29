"""Utils and fixtures to facilitate operation on dataset row in archive file
browser in oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label
from selenium.webdriver import ActionChains


class DataRow(PageObject):
    name = id = Label('.file-name-inner')
    size = Label('.fb-table-col-size .file-item-text')

    def double_click(self):
        ActionChains(self.driver).double_click(self.web_elem).perform()
