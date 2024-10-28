"""Utils and fixtures to facilitate operations on Task time series modal."""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import Button, Label, WebElement


class TaskTimeSeries(Modal):
    chart = WebElement(".canvas-area")
    _canvas = WebElement("canvas")
    time_resolution = Button(".time-resolutions-trigger")
    no_data_message = Label(".no-data-message")
    x = Button(".close")

    def get_time_from_chart(self):
        chart = self.driver.execute_script(_canvas_fill, self._canvas)
        if chart is not False:
            time = [chunk[0] for chunk in chart["series"][0]["data"]]
            return time
        else:
            raise RuntimeError("Failed to get data from task time series canvas")

    def get_last_column_value(self):
        chart = self.driver.execute_script(_canvas_fill, self._canvas)
        if chart is not False:
            value1 = [chunk[1] for chunk in chart["series"][0]["data"]]
            value_type1 = chart["series"][0]["name"]
            value2 = [chunk[1] for chunk in chart["series"][1]["data"]]
            value_type2 = chart["series"][1]["name"]
            return [(value1[-1], value_type1), (value2[-1], value_type2)]
        else:
            raise RuntimeError("Failed to get data from task time series canvas")

    def __str__(self):
        return "Task time series modal"


_canvas_fill = """
function getCanvasData(canvas) {
  return canvas.__onedata__;
}
return getCanvasData(arguments[0]);
"""
