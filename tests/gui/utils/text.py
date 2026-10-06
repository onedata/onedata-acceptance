"""Text normalization helpers for GUI tests."""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import re
from collections.abc import Callable
from datetime import datetime
from typing import cast, overload

from selenium.webdriver.remote.webdriver import WebDriver

# RE_URL regexp is matched as shown below:
#
# https://172.18.0.8/#/onedata/data/small_space/g2gDZAAEZ3VpZG0AAAAkZzJnQ
# \       \        /   \     / \  / \         /                        /
#  \        domain      \   /   tab  \___id__/                        /
#   \            /      access                                       /
#    \_base_url_/         \_________________method__________________/

RE_URL = re.compile(
    r"(?P<base_url>https?://(?P<domain>.*?)"
    r"(/(?P<where>[^/]*)/(?P<cluster>[^/]*))?)"
    r"(/i#)?(?P<method>/(?P<access>[^/]*)/(?P<tab>[^/]*)"
    r"(/(?P<id>[^/]*).*)?)"
)


def parse_url(url: str) -> re.Match[str]:
    match = RE_URL.match(url)
    if match is None:
        raise ValueError(f"Invalid URL: {url}")
    return match


def go_to_relative_url(selenium: WebDriver, relative_url: str) -> None:
    match = parse_url(selenium.current_url)
    new_url = match.group("base_url") + relative_url
    selenium.get(new_url)


@overload
def parse_seq(
    seq: str,
    pattern: str | None = None,
    separator: str | None = None,
) -> list[str]: ...


@overload
def parse_seq[T](
    seq: str,
    pattern: str | None = None,
    separator: str | None = None,
    *,
    default: Callable[[str], T],
) -> list[T]: ...


@overload
def parse_seq[T](
    seq: str,
    pattern: str | None,
    separator: str | None,
    default: Callable[[str], T],
) -> list[T]: ...


def parse_seq[T](
    seq: str,
    pattern: str | None = None,
    separator: str | None = None,
    default: Callable[[str], T] | None = None,
) -> list[T]:
    """Parses regex-matched or separator-delimited values into a list,
    e.g. '["1", "2"]', '"1"', '1,2', or '1'.
    """
    item_parser = cast(Callable[[str], T], str) if default is None else default
    if pattern is not None:
        return [item_parser(el.group()) for el in re.finditer(pattern, seq)]
    separator = "," if separator is None else separator
    return [
        item_parser(el.strip().strip('"')) for el in seq.strip("[]").split(separator) if el != ""
    ]


# An empty sequence, e.g. []
EMPTY_SEQUENCE = r"\[\]"

# A quoted element, including spaces and special characters, e.g. "dev-oneprovider-0"
QUOTED_ELEMENT = r'"[^"\n]+"'

# A single unquoted element without separators or whitespace, e.g. new_space1
UNQUOTED_ELEMENT = r'[^,\[\]"\s]+'

# An element inside a sequence can be quoted or contain unquoted whitespace,
# see BRACKETED_SEQUENCE
SEQUENCE_ELEMENT = rf'(?:{QUOTED_ELEMENT}|[^,\]"\n]+)'

# A comma-separated sequence of elements enclosed in square brackets.
# Examples:
#   [abc]                  -> element 1: abc
#   [abc, def]             -> element 1: abc       | element 2: def
#   [abc def, ghi]         -> element 1: abc def   | element 2: ghi
#   ["abc", "def ghi"]     -> element 1: abc       | element 2: def ghi
#   ["abc, def", ghi]      -> element 1: abc, def  | element 2: ghi
BRACKETED_SEQUENCE = rf"\[\s*{SEQUENCE_ELEMENT}" rf"(?:\s*,\s*{SEQUENCE_ELEMENT})*\s*\]"

# An element sequence can be:
#   abc                    -> element 1: abc
#   abc-def                -> element 1: abc-def
#   "abc def"              -> element 1: abc def
#   "abc, def"             -> element 1: abc, def
#   [abc]                  -> element 1: abc
#   [abc, def]             -> element 1: abc       | element 2: def
#   [abc def, ghi]         -> element 1: abc def   | element 2: ghi
#   ["abc", "def ghi"]     -> element 1: abc       | element 2: def ghi
#   ["abc, def", ghi]      -> element 1: abc, def  | element 2: ghi
ELEMENTS_SEQUENCE_PATTERN = (
    rf"(?:{QUOTED_ELEMENT}|{UNQUOTED_ELEMENT}|{BRACKETED_SEQUENCE}|{EMPTY_SEQUENCE})"
)


def parse_elements_sequence(value: str) -> list[str]:
    if re.fullmatch(ELEMENTS_SEQUENCE_PATTERN, value) is None:
        raise ValueError(f"Invalid elements sequence: {value!r}")
    return parse_seq(value)


def parse_time(value: str) -> datetime:
    date_match = re.match(
        r"\d{4}-\d{2}-\d{2} at \d{1,2}:\d{2} \(UTC[+-]\d{2}:\d{2}\)",
        value,
    )
    assert date_match, f'Invalid time format: "{value}"'

    return datetime.strptime(
        date_match.group(),
        "%Y-%m-%d at %H:%M (UTC%z)",
    )


def transform(val: str, strip_char: str | None = None) -> str:
    return val.strip(strip_char).lower().replace(" ", "_").replace("'", "")
