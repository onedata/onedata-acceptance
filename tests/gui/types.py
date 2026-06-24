"""Shared types for dynamic GUI test helpers and fixtures"""

__author__ = "Mateusz Zając"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from collections import defaultdict
from collections.abc import Callable, Iterator
from os import PathLike
from typing import TYPE_CHECKING, Any, Literal, Protocol, TypedDict

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement

    from tests.gui.utils.common.popups import Popups
    from tests.types import JsonValue
else:
    WebDriver = Any
    WebElement = Any
    JsonValue = Any
    Popups = Any


class DynamicObject(Protocol):
    """Structural type for dynamically composed page and plugin objects."""

    def __getattr__(self, name: str) -> "DynamicObject": ...

    def __call__(self, *args: object, **kwargs: object) -> "DynamicObject": ...

    def __getitem__(self, key: object) -> "DynamicObject": ...

    def __setitem__(self, key: object, value: object) -> None: ...

    def __iter__(self) -> Iterator["DynamicObject"]: ...

    def __len__(self) -> int: ...

    def __bool__(self) -> bool: ...

    def __contains__(self, item: object) -> bool: ...

type TmpMemory = defaultdict[str, dict[str, DynamicObject]]

type BrowserTmpMemory = dict[str, dict[str, object]]
type FilePath = str | bytes | PathLike[str] | PathLike[bytes]
type WebElemRoot = WebDriver | WebElement

type LocalDirectoryContent = int | dict[
    str, "LocalDirectoryContent | dict[str, str]"
]
type DataDirectoryContent = list[str | dict[str, "DataDirectoryContent"]]

type TarTree = list[str | dict[str, "TarTree | str | int"]]
type TreeConfig = list[str | dict[str, "TreeConfig | str | int"]]

type ProviderResponse = dict[str, JsonValue]
type JsonObject = dict[str, JsonValue]

type AuditLogValue = (
    str | int | float | bool | list["AuditLogValue"] | dict[str, "AuditLogValue"]
)
type AuditLogContent = dict[str, AuditLogValue]

type PopupFactory = Callable[[WebDriver], Popups]

type PrivilegeGranted = Literal[True, False, "Partially"]
PrivilegeGroupConfig = TypedDict(
    "PrivilegeGroupConfig",
    {
        "granted": PrivilegeGranted,
        "privilege subtypes": dict[str, bool],
    },
)
type PrivilegesConfig = dict[str, PrivilegeGroupConfig]


class Clipboard(Protocol):
    def copy(self, text: str, display: str) -> None: ...

    def paste(self, display: str) -> str: ...
