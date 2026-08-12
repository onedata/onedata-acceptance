"""Lightweight progress logging for demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from collections.abc import Callable
from functools import wraps
from typing import Final, ParamSpec, TypeVar

ANSI_RESET: Final = "\033[0m"
ANSI_BOLD: Final = "\033[1m"
ANSI_GREEN: Final = "\033[32m"
ANSI_YELLOW: Final = "\033[33m"
ANSI_CYAN: Final = "\033[36m"
P = ParamSpec("P")
R = TypeVar("R")
Step = Callable[P, R]
StepDecorator = Callable[[Step[P, R]], Step[P, R]]


def _colored_label(label: str, color: str) -> str:
    return f"{ANSI_BOLD}{color}{label}{ANSI_RESET}"


def _log_step_start(description: str) -> None:
    label = _colored_label("START", ANSI_YELLOW)
    print(f"[demo-mode] {label}: {description}", flush=True)


def _log_step_done(description: str) -> None:
    label = _colored_label("DONE", ANSI_GREEN)
    print(f"[demo-mode] {label}: {description}", flush=True)


def log_running_command(command: str) -> None:
    label = _colored_label("RUNNING COMMAND", ANSI_CYAN)
    print(f"[demo-mode] {label}:\n{command}", flush=True)


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
