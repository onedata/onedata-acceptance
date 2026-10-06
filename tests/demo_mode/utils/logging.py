"""Logging utilities for demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from collections.abc import Callable, Generator
from contextlib import contextmanager
from functools import wraps
from typing import ParamSpec, TextIO, TypeVar

from tests.demo_mode.utils.command_context import current_command_context

P = ParamSpec("P")
R = TypeVar("R")
Step = Callable[P, R]
StepDecorator = Callable[[Step[P, R]], Step[P, R]]


def _log_step_start(description: str) -> None:
    print(f"[demo-mode] START: {description}", flush=True)


def _log_step_done(description: str) -> None:
    print(f"[demo-mode] DONE: {description}", flush=True)


def log_running_command(command: str) -> None:
    print(f"[demo-mode] RUNNING COMMAND:\n{command}", flush=True)


@contextmanager
def open_command_log(
    command: str,
    command_name: str,
) -> Generator[TextIO, None, None]:
    log_path = current_command_context().next_command_log_path(command_name)
    with log_path.open("w", encoding="utf-8") as log_file:
        log_file.write(f"Command:\n{command}\n\nOutput:\n")
        log_file.flush()
        yield log_file


def log_step(description: str) -> StepDecorator:
    """Log start and completion of a step."""

    def decorator(function: Step[P, R]) -> Step[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            _log_step_start(description)
            result = function(*args, **kwargs)
            _log_step_done(description)
            return result

        return wrapper

    return decorator
