"""This module contains gherkin steps to run acceptance tests featuring
copy paste operations using local system clipboard.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.type_definitions import Clipboard, TmpMemory
from tests.gui.utils.generic import (
    ELEMENTS_SEQUENCE_PATTERN,
    parse_elements_sequence,
)
from tests.utils.bdd_utils import parsers, wt


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) sends copied (?P<item_type>.*?) "
        rf"to users? of (?P<browser_list>{ELEMENTS_SEQUENCE_PATTERN})"
    ),
    converters={
        "browser_list": parse_elements_sequence,
    },
)
def send_copied_item_to_other_users(
    browser_id: str,
    item_type: str,
    browser_list: list[str],
    tmp_memory: TmpMemory,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:
    item = clipboard.paste(display=displays[browser_id])
    for browser in browser_list:
        tmp_memory[browser]["mailbox"][item_type.lower()] = item


@wt(parsers.parse("user of {browser_id} sees that copied token matches displayed one"))
def assert_copied_token_match_displayed_one(
    browser_id: str,
    tmp_memory: TmpMemory,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:
    displayed_token = tmp_memory[browser_id]["token"]
    copied_token = clipboard.paste(display=displays[browser_id])
    error_message = (
        f"Displayed token: {displayed_token} does not match copied one: {copied_token}"
    )
    assert copied_token == displayed_token, error_message


@wt(
    parsers.parse(
        "user of {browser_id} sees that copied token does not match displayed one"
    )
)
def assert_copied_token_does_not_match_displayed_one(
    browser_id: str,
    tmp_memory: TmpMemory,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:
    displayed_token = tmp_memory[browser_id]["token"]
    copied_token = clipboard.paste(display=displays[browser_id])
    error_message = (
        f"Displayed token: {displayed_token} match copied one: {copied_token} "
        "while it should not be"
    )
    assert copied_token != displayed_token, error_message
