"""Generic GUI testing utils - mainly helpers and extensions for Selenium."""

__author__ = "Jakub Liput, Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2016-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import json
import os
from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from contextlib import suppress as contextlib_suppress
from itertools import islice
from typing import TypeVar

from _pytest._py.path import LocalPath
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from tests import gui
from tests.gui.constants import WAIT_FRONTEND, WAIT_NORMAL_DOWNLOAD
from tests.gui.utils import text as text_utils
from tests.type_definitions import JsonValue
from tests.utils.utils import repeat_failed

T = TypeVar("T")
suppress = contextlib_suppress
transform = text_utils.transform


def upload_file_path(file_name: str) -> str:
    """Resolve an absolute path for file with name file_name stored
    in upload_files dir
    """
    return os.path.join(
        os.path.dirname(os.path.abspath(gui.__file__)),
        "upload_files",
        file_name,
    )


def upload_workflow_path(workflow_name: str | None = None) -> str:
    """Resolve an absolute path for workflow file with name workflow_name
    stored in automation-examples submodule
    """
    if workflow_name:
        return os.path.abspath(
            os.path.join(
                os.path.dirname(gui.__file__),
                "..",
                "..",
                "automation-examples",
                "workflows",
                workflow_name,
            )
        )
    return os.path.abspath(
        os.path.join(
            os.path.dirname(gui.__file__),
            "..",
            "..",
            "automation-examples",
            "workflows",
        )
    )


def upload_lambda_path(lambda_name: str | None) -> str:
    """Resolve an absolute path for lambda dump file with name lambda_name
    stored in automation-examples submodule
    """
    if lambda_name:
        return os.path.abspath(
            os.path.join(
                os.path.dirname(gui.__file__),
                "..",
                "..",
                "automation-examples",
                "lambdas",
                lambda_name,
            )
        )
    return os.path.abspath(
        os.path.join(
            os.path.dirname(gui.__file__),
            "..",
            "..",
            "automation-examples",
            "lambdas",
        )
    )


def strip_path(path_string: str, separator: str = "/") -> str:
    """Strips string from whitespaces inside file path. Useful for file
     paths rendered
    in DOM which contains `\\n` characters in `innerText`.
    """
    return separator.join([path_item.strip() for path_item in path_string.split(separator)])


@contextmanager
def implicit_wait(
    driver: WebDriver, timeout: int | float, prev_timeout: int | float
) -> Iterator[None]:
    driver.implicitly_wait(timeout)
    try:
        yield
    finally:
        driver.implicitly_wait(prev_timeout)


def iter_ahead[T](iterable: Iterable[T]) -> Iterator[tuple[T, T]]:
    read_ahead = iter(iterable)
    next(read_ahead, None)
    yield from zip(iterable, read_ahead, strict=False)


def perform_action[ActionResultT](
    action: Callable[[], ActionResultT],
    /,
    assertion: Callable[[], None] | None = None,
    timeout: float = WAIT_FRONTEND,
) -> ActionResultT:
    @repeat_failed(timeout=timeout)
    def attempt() -> ActionResultT:
        result = action()
        if assertion is not None:
            assertion()
        return result

    return attempt()


def wait_for_file_to_download(
    driver: WebDriver,
    downloaded_file: LocalPath,
    file_name: str,
    timeout: float = WAIT_NORMAL_DOWNLOAD,
) -> None:
    WebDriverWait(driver, timeout).until(
        lambda _: downloaded_file.isfile(),
        message=f"File {file_name} did not finish downloading",
    )


def nth[T](seq: Iterable[T], idx: int) -> T | None:
    return next(islice(seq, idx, None), None)


@contextmanager
def redirect_display(new_display: str) -> Iterator[None]:
    """Replace DISPLAY environment variable with new value"""
    old_display = os.environ.get("DISPLAY", "DUMMY_DISPLAY")
    os.environ["DISPLAY"] = new_display
    try:
        yield
    finally:
        if old_display is not None:
            os.environ["DISPLAY"] = old_display
        else:
            del os.environ["DISPLAY"]


def assert_each_event_is_gathered(
    events: list[str],
    gathered_events: list[str],
    option: str,
) -> None:
    for event in events:
        assert event in gathered_events, (
            f'No gathered event with {option} "{event}" was found. '
            f"Gathered {option}s: {gathered_events}"
        )


def are_events_gathered_together(
    first_event: str, second_event: str, gathered_events: list[str]
) -> bool:
    for gathered_event in gathered_events:
        if first_event in gathered_event and second_event in gathered_event:
            return True
    return False


def assert_events_are_gathered_with_event(
    events: list[str],
    other_event: str,
    gathered_events: list[str],
    option: str,
) -> None:
    for event in events:
        events_are_gathered_together = are_events_gathered_together(
            event, other_event, gathered_events
        )

        assert events_are_gathered_together, (
            f'No gathered event with {option} containing "{event}" '
            f'and event "{other_event}" was found. '
            f"Gathered {option}s: {gathered_events}"
        )


def sort_json_keys(obj: JsonValue) -> JsonValue:
    if isinstance(obj, dict):
        items = list(obj.items())
        items.sort(reverse=True)
        return {k: sort_json_keys(v) for k, v in items}

    if isinstance(obj, list):
        return [sort_json_keys(x) for x in obj]
    return obj  # number or string


def sort_json_from_string(value: str) -> JsonValue:
    parsed_value = json.loads(value)
    return sort_json_keys(parsed_value)
