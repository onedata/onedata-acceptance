"""Shared, concrete types for performance benchmarks"""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from collections.abc import Mapping
from queue import Queue

type ParameterValue = int | float | str | bool
type PerformanceParams = Mapping[str, Mapping[str, ParameterValue]]
type ExceptionQueue = Queue[Exception]


def int_parameter(params: PerformanceParams, name: str) -> int:
    value = params[name]["value"]
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"Performance parameter {name} is not an integer")
    return value


def bool_parameter(params: PerformanceParams, name: str) -> bool:
    value = params[name]["value"]
    if not isinstance(value, bool):
        raise TypeError(f"Performance parameter {name} is not a boolean")
    return value


def str_parameter(params: PerformanceParams, name: str, field: str = "value") -> str:
    value = params[name][field]
    if not isinstance(value, str):
        raise TypeError(f"Performance parameter {name} is not a string")
    return value
