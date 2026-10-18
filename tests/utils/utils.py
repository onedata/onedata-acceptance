"""This module contains utility functions to be used in acceptance tests."""

__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2016-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import logging
import re
import subprocess as sp
import traceback
from collections.abc import Callable, Sequence
from time import sleep, time
from types import ModuleType
from typing import Final, ParamSpec, TypeVar, cast

import pytest
from decorator import decorator
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement

from tests.oneclient.constants import ONECLIENT_REPEATS_INTERVAL

P = ParamSpec("P")
T = TypeVar("T")


def check_call_with_logging(cmd: str | Sequence[str]) -> None:
    try:
        sp.check_call(cmd)
    except sp.CalledProcessError as e:
        logging.error("%s\nCaptured output: %s", e, e.output)
        raise e


def log_exception() -> None:
    extracted_stack = traceback.format_exc(10)
    logging.error(extracted_stack)


GENERIC_MESSAGE: Final[str] = "Operation succeeded, expected it to fail"


def assert_with_expected_fail(
    condition: Callable[[], object],
    timeout: float,
    should_fail: bool = False,
    interval: float = ONECLIENT_REPEATS_INTERVAL,
    message: str = GENERIC_MESSAGE,
    exceptions: type[BaseException] | tuple[type[BaseException], ...] = (Exception,),
) -> None:
    try:
        perform_action_with_timeout(
            condition,
            timeout=timeout,
            interval=interval,
            ignored_exceptions=exceptions,
        )
    except exceptions:
        if should_fail:
            return
        raise

    if should_fail:
        raise AssertionError(message)


def get_fun_name(fun: str) -> str | None:
    if "method" in fun:
        return fun.split("method ")[1].split(" ", maxsplit=1)[0]
    if "function" in fun:
        return fun.split("function ")[1].split(".", maxsplit=1)[0]
    return None


def assert_expected_failure(fun: Callable[..., object], *args: object, **kwargs: object) -> None:
    # Filesystem operations can report different OSError subclasses and messages by platform.
    with pytest.raises(OSError):  # noqa: PT011
        fun(*args, **kwargs)


def repeat_failed(
    attempts: int = 10,
    timeout: float | None = None,
    interval: float = 0.1,
    exceptions: type[BaseException] | tuple[type[BaseException], ...] = (Exception,),
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Returns wrapper on function, which keeps calling it until timeout or
    for attempts times in case of failure (exception).

    :param attempts: maximum num of attempts, defaults to 10
    :type attempts: int
    :param interval: time between subsequent calls
    :type interval: float
    :param timeout: time limit of now when to stop repeating fun,
                    if set alongside attempts take precedence
    :type timeout: Optional[float]
    :param exceptions: in case of which consider failure of call
    :type exceptions: list[Exception]
    :return: wrapper decorator
    """

    @decorator
    def wrapper(fun: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T:
        now = time()
        limit, i = (now + timeout, now) if timeout is not None else (attempts, 0)

        while i < limit:
            try:
                result = fun(*args, **kwargs)
            except exceptions:
                sleep(interval)
                i = time() if timeout else i + 1
                continue
            else:
                return result
        return fun(*args, **kwargs)

    return cast(Callable[[Callable[P, T]], Callable[P, T]], wrapper)


def perform_action_with_timeout[ActionResultT](
    action: Callable[[], ActionResultT],
    /,
    timeout: float,
    ignored_exceptions: type[BaseException] | tuple[type[BaseException], ...] = (Exception,),
    interval: float = 0.1,
) -> ActionResultT:
    @repeat_failed(timeout=timeout, exceptions=ignored_exceptions, interval=interval)
    def attempt() -> ActionResultT:
        return action()

    return attempt()


def get_copyright(mod: ModuleType) -> str:
    return mod.__copyright__ if hasattr(mod, "__copyright__") else ""


def get_authors(mod: ModuleType) -> list[str]:
    author = mod.__author__ if hasattr(mod, "__author__") else ""
    return re.split(r"\s*,\s*", author)


def get_suite_description(mod: ModuleType) -> str | None:
    return mod.__doc__


def element_has_class(element: SeleniumWebElement, class_name: str) -> bool:
    return class_name in (element.get_attribute("class") or "").split()
