"""Utils and fixtures to facilitate operations on Task time series modal.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import WebElement


class TaskTimeSeries(Modal):
    chart = WebElement('.canvas-area')

    def __str__(self):
        return 'Task time series modal'

