"""Shared types for dynamic GUI test helpers and fixtures"""

__author__ = "Mateusz Zając"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from collections import defaultdict
from collections.abc import Iterator
from typing import Protocol

from selenium.webdriver.remote.webdriver import WebDriver


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

class Clipboard(Protocol):
    def copy(self, text: str, display: str) -> None: ...

    def paste(self, display: str) -> str: ...
