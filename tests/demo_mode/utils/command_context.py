"""Context shared by commands executed within a demo-mode test."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os
import re
import signal
import subprocess
import time
from collections.abc import Generator, Iterator
from contextlib import contextmanager, suppress
from contextvars import ContextVar
from dataclasses import dataclass, field
from itertools import count
from pathlib import Path
from typing import Final

from tests.demo_mode.type_definitions import DemoImages
from tests.utils.path_utils import make_logdir

COMMAND_LOGS_ROOT: Final = Path(__file__).resolve().parents[1] / "logs"
COMMAND_LOGS_DIRECTORY: Final = Path(make_logdir(str(COMMAND_LOGS_ROOT), "report"))
_current_command_context: ContextVar["CommandContext"] = ContextVar("current_command_context")


def _safe_log_name(name: str) -> str:
    file_name = Path(name).name
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", file_name).strip("-.") or "unknown"


@dataclass
class CommandContext:
    """State and resources owned by a single demo-mode test."""

    images: DemoImages
    _logs_directory: Path
    _log_counter: Iterator[int] = field(default_factory=lambda: count(1))
    _processes: list[subprocess.Popen[str]] = field(default_factory=list)

    def next_command_log_path(self, command_name: str) -> Path:
        """Return a uniquely numbered log path for the next command."""
        command_number = next(self._log_counter)
        log_name = _safe_log_name(command_name).removesuffix(".sh")
        return self._logs_directory / f"command-{command_number:03d}-{log_name}.log"

    def register_process(self, process: subprocess.Popen[str]) -> None:
        """Register a process for cleanup at the end of the test."""
        self._processes.append(process)

    def reap_processes(self, timeout: float) -> None:
        """Reap processes, killing remaining process groups after the timeout."""
        deadline = time.monotonic() + timeout

        for process in self._processes:
            try:
                process.wait(timeout=max(0.0, deadline - time.monotonic()))
            except subprocess.TimeoutExpired:
                break

        running_processes = [process for process in self._processes if process.poll() is None]
        for process in running_processes:
            with suppress(ProcessLookupError):
                os.killpg(process.pid, signal.SIGKILL)
        for process in running_processes:
            process.wait()

        self._processes.clear()

    @property
    def logs_directory(self) -> Path:
        return self._logs_directory


def current_command_context() -> CommandContext:
    """Return the active context or fail when called outside a demo test."""
    try:
        return _current_command_context.get()
    except LookupError as error:
        raise RuntimeError(
            "No demo command context is active; commands must be used "
            "within the demo_test_context fixture"
        ) from error


@contextmanager
def command_context(
    test_name: str,
    images: DemoImages,
) -> Generator[CommandContext, None, None]:
    """Create and activate a command context for one demo-mode test."""
    logs_directory = COMMAND_LOGS_DIRECTORY / _safe_log_name(test_name.removeprefix("test_"))
    logs_directory.mkdir()
    context = CommandContext(images, logs_directory)
    token = _current_command_context.set(context)
    try:
        yield context
    finally:
        _current_command_context.reset(token)
