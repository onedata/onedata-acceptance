"""Text normalization helpers for GUI tests."""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


def transform(val: str, strip_char: str | None = None) -> str:
    return val.strip(strip_char).lower().replace(" ", "_").replace("'", "")