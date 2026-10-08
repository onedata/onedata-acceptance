"""Low-level helpers for running demo-mode commands."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os
import re
import signal
import subprocess
from contextlib import suppress
from pathlib import Path
from typing import Final, TextIO

from tests.demo_mode.utils.command_context import current_command_context

DEMO_MODE_ROOT: Final = Path(__file__).resolve().parents[2]
COMMANDS_ROOT: Final = DEMO_MODE_ROOT / "commands"
RELEASE_PLACEHOLDER: Final = "xRELEASExVERSIONx"
CONTAINER_NAME_PLACEHOLDER: Final = "xCONTAINERxNAMEx"

PLACEHOLDER_PATTERN: Final = re.compile(r"x[A-Z][A-Z0-9]*(?:x[A-Z][A-Z0-9]*)*x")


def command_path(relative_path: str) -> Path:
    """Return a validated path to an unmodified file in ``commands``."""
    path = (COMMANDS_ROOT / relative_path).resolve()
    if not path.is_relative_to(COMMANDS_ROOT):
        raise ValueError(
            f"Command path must resolve within {COMMANDS_ROOT}, but "
            f"{relative_path!r} resolves to {path}"
        )

    if not path.is_file():
        raise FileNotFoundError(path)
    return path


def _start_subprocess(
    command: str,
    cwd: Path,
    log_file: TextIO,
    *,
    capture_output: bool,
) -> subprocess.Popen[str]:
    stdout: int | TextIO
    stderr: int | TextIO

    if capture_output:
        stdout = subprocess.PIPE
        stderr = subprocess.PIPE
    else:
        stdout = log_file
        stderr = subprocess.STDOUT

    process = subprocess.Popen(
        command,
        cwd=cwd,
        stdout=stdout,
        stderr=stderr,
        executable="/bin/bash",
        shell=True,
        start_new_session=True,
        text=True,
    )
    current_command_context().register_process(process)

    return process


def _send_signal_to_process_group(
    process: subprocess.Popen[str],
    signal_number: signal.Signals,
) -> None:
    with suppress(ProcessLookupError):
        os.killpg(process.pid, signal_number)


def _kill_process(process: subprocess.Popen[str]) -> tuple[str, str]:
    _send_signal_to_process_group(process, signal.SIGKILL)
    stdout, stderr = process.communicate()
    return stdout or "", stderr or ""
