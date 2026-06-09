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
from typing import Any

import pytest
from decorator import decorator  # pylint: disable=import-error


def check_call_with_logging(cmd: str | Sequence[str]) -> None:
    try:
        sp.check_call(cmd)
    except sp.CalledProcessError as e:
        logging.error("%s\nCaptured output: %s", e, e.output)
        raise e


def log_exception() -> None:
    extracted_stack = traceback.format_exc(10)
    logging.error(extracted_stack)


def assert_generic(
    expression: Callable[..., Any], should_fail: bool, *args: Any, **kwargs: Any
) -> None:
    if should_fail:
        assert_false(expression, *args, **kwargs)
    else:
        assert_(expression, *args, **kwargs)  # pylint: disable=deprecated-method


def assert_(expression: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
    assert_result = expression(*args, **kwargs)
    assert assert_result


def assert_false(expression: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
    assert_result = expression(*args, **kwargs)
    assert not assert_result


def get_fun_name(fun: str) -> str | None:
    if "method" in fun:
        return fun.split("method ")[1].split(" ")[0]
    if "function" in fun:
        return fun.split("function ")[1].split(".")[0]
    return None


def assert_expected_failure(fun: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
    with pytest.raises(OSError):
        fun(*args, **kwargs)


def repeat_failed(
    attempts: int = 10,
    timeout: float | None = None,
    interval: float = 0.1,
    exceptions: type[BaseException] | tuple[type[BaseException], ...] = (Exception,),
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Returns wrapper on function, which keeps calling it until timeout or
    for attempts times in case of failure (exception).

    :param attempts: maximum num of attempts, defaults to 10
    :type attempts: int
    :param interval: time between subsequent calls
    :type interval: float
    :param timeout: time limit of now when to stop repeating fun,
                    if set alongside attempts take precedence
    :type timeout: float | None
    :param exceptions: in case of which consider failure of call
    :type exceptions: list[Exception]
    :return: wrapper decorator
    """

    @decorator
    def wrapper(fun: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        now = time()
        limit, i = (now + timeout, now) if timeout else (attempts, 0)

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

    return wrapper


def get_copyright(mod: ModuleType) -> str:
    return mod.__copyright__ if hasattr(mod, "__copyright__") else ""


def get_authors(mod: ModuleType) -> list[str]:
    author = mod.__author__ if hasattr(mod, "__author__") else ""
    return re.split(r"\s*,\s*", author)


def get_suite_description(mod: ModuleType) -> str | None:
    return mod.__doc__
