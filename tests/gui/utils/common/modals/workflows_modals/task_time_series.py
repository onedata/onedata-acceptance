"""Utils and fixtures to facilitate operations on Task time series modal."""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from typing import TypedDict, cast

from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.web_elements import Button, Label, WebElement


class ChartSeries(TypedDict):
    data: list[tuple[float, float]]
    name: str


class ChartData(TypedDict):
    series: list[ChartSeries]


class TaskTimeSeries(Modal):
    chart = WebElement(".canvas-area")
    _canvas = WebElement("canvas")
    time_resolution = Button(".time-resolutions-trigger")
    no_data_message = Label(".no-data-message")
    x = Button(".close")

    def get_time_from_chart(self) -> list[float]:
        chart = self.driver.execute_script(_canvas_fill, self._canvas)
        if chart is False:
            raise RuntimeError("Failed to get data from task time series canvas")
        chart_data = cast(ChartData, chart)
        return [chunk[0] for chunk in chart_data["series"][0]["data"]]

    def get_columns_values(self) -> list[tuple[list[float], str]]:
        chart = self.driver.execute_script(_canvas_fill, self._canvas)
        if chart is False:
            raise RuntimeError("Failed to get data from task time series canvas")
        chart_data = cast(ChartData, chart)
        values1 = [chunk[1] for chunk in chart_data["series"][0]["data"]]
        value_type1 = chart_data["series"][0]["name"]
        values2 = [chunk[1] for chunk in chart_data["series"][1]["data"]]
        value_type2 = chart_data["series"][1]["name"]
        return [(values1, value_type1), (values2, value_type2)]

    def get_last_column_value(self) -> list[tuple[float, str]]:
        values = self.get_columns_values()
        return [(values[0][0][-1], values[0][1]), (values[1][0][-1], values[1][1])]

    def get_max_value(self) -> list[tuple[float, str]]:
        values = self.get_columns_values()
        return [(max(values[0][0]), values[0][1]), (max(values[1][0]), values[1][1])]

    def __str__(self) -> str:
        return "Task time series modal"


_canvas_fill = """
function getCanvasData(canvas) {
  return canvas.__onedata__;
}
return getCanvasData(arguments[0]);
"""
