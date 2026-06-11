"""Shared types for dynamic GUI test helpers and fixtures."""

from collections import defaultdict
from collections.abc import Callable, Iterator, Mapping, MutableMapping
from typing import Optional, Protocol

from selenium.webdriver.remote.webdriver import WebDriver


class GuiObject(Protocol):
    """Structural type for dynamically composed page and plugin objects."""

    def __getattr__(self, name: str) -> "GuiObject": ...

    def __call__(self, *args: object, **kwargs: object) -> "GuiObject": ...

    def __getitem__(self, key: object) -> "GuiObject": ...

    def __setitem__(self, key: object, value: object) -> None: ...

    def __iter__(self) -> Iterator["GuiObject"]: ...

    def __len__(self) -> int: ...

    def __bool__(self) -> bool: ...

    def __contains__(self, item: object) -> bool: ...


type DisplayMap = dict[str, str]
type DriverMap = dict[str, WebDriver]
type Numerals = dict[str, int]
type TmpMemory = defaultdict[str, dict[str, GuiObject]]
type GuiMapping = MutableMapping[str, GuiObject]
type GuiConfig = Mapping[str, GuiObject]
type OptionalString = Optional[str]
type StringCallback = Callable[[str], object]


class Clipboard(Protocol):
    def copy(self, text: str, display: str) -> None: ...

    def paste(self, display: str) -> str: ...
