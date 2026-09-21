"""Shared types for dynamic GUI test helpers and fixtures"""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from collections import defaultdict, namedtuple
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from os import PathLike
from typing import Any, Literal, Protocol, Self, TypedDict

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement


class Checkable(Protocol):
    def is_checked(self) -> bool: ...


class Clickable(Protocol):
    def click(self) -> None: ...


class WhichBrowser(Enum):
    ARCHIVE_BROWSER = "archive browser"
    ARCHIVE_FILE_BROWSER = "archive file browser"
    DATASET_BROWSER = "dataset browser"
    FILE_BROWSER = "file browser"
    SHARES_FILE_BROWSER = "share's file browser"
    DATASET_ARCHIVE_BROWSER = "dataset archive browser"
    ARCHIVE_RECALL_BROWSER = "archive recall browser"


type BrowserColumn = Literal[
    WhichBrowser.FILE_BROWSER,
    WhichBrowser.ARCHIVE_BROWSER,
    WhichBrowser.DATASET_BROWSER,
]

type ColumnTable = BrowserColumn | Literal["transfers"]


@dataclass(frozen=True)
class ColumnContext:
    browser_id: str
    column_view: ColumnTable

    @classmethod
    def transfers(cls, browser_id: str) -> Self:
        return cls(browser_id=browser_id, column_view="transfers")

    @classmethod
    def browser(cls, browser_id: str, which_browser: BrowserColumn) -> Self:
        return cls(browser_id=browser_id, column_view=which_browser)


type TmpMemory = defaultdict[str, dict[str, Any]]
type VisibleColumns = defaultdict[ColumnContext, set[str]]

type FilePath = str | bytes | PathLike[str] | PathLike[bytes]
type WebElemRoot = WebDriver | SeleniumWebElement
type CssLocator = tuple[Literal["css selector"], str]
type WebElementOrCssLocator = SeleniumWebElement | CssLocator
type WebElementOrSelector = SeleniumWebElement | str
type VisibilityCondition = Callable[[WebElemRoot], SeleniumWebElement | Literal[False]]

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
