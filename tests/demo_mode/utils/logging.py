"""Logging utilities for demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import re
from collections.abc import Callable, Generator
from contextlib import contextmanager
from contextvars import ContextVar
from functools import wraps
from itertools import count
from pathlib import Path
from typing import Final, ParamSpec, TextIO, TypeVar

from tests.utils.path_utils import make_logdir

ANSI_RESET: Final = "\033[0m"
ANSI_BOLD: Final = "\033[1m"
ANSI_GREEN: Final = "\033[32m"
ANSI_YELLOW: Final = "\033[33m"
ANSI_CYAN: Final = "\033[36m"
COMMAND_LOGS_ROOT: Final = Path(__file__).resolve().parents[1] / "logs"
COMMAND_LOGS_DIR: Final = Path(make_logdir(str(COMMAND_LOGS_ROOT), "report"))
_current_command_logs_dir: ContextVar[Path] = ContextVar(
    "current_command_logs_dir",
    default=COMMAND_LOGS_DIR,
)
_command_log_counter = ContextVar(
    "command_log_counter",
    default=count(1),
)
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


def _safe_log_name(name: str) -> str:
    file_name = Path(name).name
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", file_name).strip("-.") or "unknown"


def _next_command_log_number() -> int:
    return next(_command_log_counter.get())


@contextmanager
def command_logs_for_test(test_name: str) -> Generator[None, None, None]:
    test_logs_dir = COMMAND_LOGS_DIR / _safe_log_name(test_name)
    test_logs_dir.mkdir()
    directory_token = _current_command_logs_dir.set(test_logs_dir)
    counter_token = _command_log_counter.set(count(1))
    try:
        yield
    finally:
        _command_log_counter.reset(counter_token)
        _current_command_logs_dir.reset(directory_token)


@contextmanager
def open_command_log(
    command: str,
    command_name: str,
) -> Generator[TextIO, None, None]:
    command_number = _next_command_log_number()
    log_name = _safe_log_name(command_name)
    log_path = (
        _current_command_logs_dir.get() / f"command-{command_number:03d}-{log_name}.log"
    )
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
