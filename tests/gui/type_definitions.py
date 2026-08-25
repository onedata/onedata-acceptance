"""Shared types for dynamic GUI test helpers and fixtures"""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from collections import defaultdict, namedtuple
from collections.abc import Callable
from os import PathLike
from typing import Any, Literal, Protocol, TypedDict

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class Checkable(Protocol):
    def is_checked(self) -> bool: ...


class Clickable(Protocol):
    def click(self) -> None: ...


type TmpMemory = defaultdict[str, dict[str, Any]]

type FilePath = str | bytes | PathLike[str] | PathLike[bytes]
type WebElemRoot = WebDriver | WebElement
type CssLocator = tuple[Literal["css selector"], str]
type WebElementOrCssLocator = WebElement | CssLocator
type WebElementOrSelector = WebElement | str
type VisibilityCondition = Callable[[WebElemRoot], WebElement | Literal[False]]

type LocalDirectoryContent = int | dict[str, "LocalDirectoryContent | dict[str, str]"]
type DataDirectoryContent = list[str | dict[str, "DataDirectoryContent"]]

type TarTree = list[str | dict[str, "TarTree | str | int"]]
type TreeConfig = list[str | dict[str, "TreeConfig | str | int"]]

type AuditLogValue = (
    str | int | float | bool | list["AuditLogValue"] | dict[str, "AuditLogValue"]
)
type AuditLogContent = dict[str, AuditLogValue]

type PrivilegeGranted = Literal[True, False, "Partially"]
PrivilegeGroupConfig = TypedDict(
    "PrivilegeGroupConfig",
    {
        "granted": PrivilegeGranted,
        "privilege subtypes": dict[str, bool],
    },
)
type PrivilegesConfig = dict[str, PrivilegeGroupConfig]


Clipboard = namedtuple("Clipboard", ["copy", "paste"])
