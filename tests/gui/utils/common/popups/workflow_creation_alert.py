"""Utils and fixtures to facilitate operations on workflow creation alert.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button


class WorkflowCreationAlert(PageObject):
    close = Button('.close')

    def __call__(self):
        self.click()
