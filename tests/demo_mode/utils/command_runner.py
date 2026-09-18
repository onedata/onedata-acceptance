"""Subprocess lifecycle helpers for demo-mode commands."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os
import signal
import subprocess
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

from tests.demo_mode.utils.command_templates import DEMO_MODE_ROOT
from tests.demo_mode.utils.logging import log_running_command, open_command_log
from tests.utils.time_utils import deadline_after, remaining_time, sleep_before_retry


@dataclass(frozen=True)
class CommandOutput:
    stdout: str
    stderr: str


def _start_subprocess(
    command: str,
    cwd: Path,
    log_file: TextIO,
    capture_output: bool = False,
) -> subprocess.Popen[str]:
    stdout: int | TextIO
    stderr: int | TextIO

    if capture_output:
        stdout = subprocess.PIPE
        stderr = subprocess.PIPE
    else:
        stdout = log_file
        # Merge stderr into stdout so both streams are written to the command log.
        stderr = subprocess.STDOUT

    return subprocess.Popen(
        command,
        cwd=cwd,
        stdout=stdout,
        stderr=stderr,
        executable="/bin/bash",
        shell=True,
        start_new_session=True,
        text=True,
    )


def start_command(command: str, command_name: str) -> subprocess.Popen[str]:
    log_running_command(command)
    with open_command_log(command, command_name) as log_file:
        return _start_subprocess(
            command,
            DEMO_MODE_ROOT,
            log_file,
        )


def _has_process_finished(process: subprocess.Popen[str]) -> bool:
    return process.poll() is not None


def _send_signal_to_process_group(
    process: subprocess.Popen[str], signal_number: signal.Signals
) -> None:
    with suppress(ProcessLookupError):
        os.killpg(process.pid, signal_number)


def _kill_subprocess(process: subprocess.Popen[str]) -> CommandOutput:
    _send_signal_to_process_group(process, signal.SIGKILL)
    stdout, stderr = process.communicate()
    return CommandOutput(stdout or "", stderr or "")


def stop_command(process: subprocess.Popen[str], timeout: float = 10) -> None:
    """Stop and reap a command together with its child processes."""
    if _has_process_finished(process):
        return

    _send_signal_to_process_group(process, signal.SIGTERM)

    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        _send_signal_to_process_group(process, signal.SIGKILL)
        process.wait()


def run_command_and_wait_to_finish(
    command: str,
    command_name: str,
    timeout: float | None = None,
    capture_output: bool = False,
    cwd: Path = DEMO_MODE_ROOT,
) -> subprocess.CompletedProcess[str]:
    with open_command_log(command, command_name) as log_file:
        process = _start_subprocess(command, cwd, log_file, capture_output)

        try:
            command_stdout, command_stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            command_output = _kill_subprocess(process)
            log_file.write(command_output.stdout)
            log_file.write(command_output.stderr)
            raise

        if capture_output:
            log_file.write(command_stdout)
            log_file.write(command_stderr)

        assert process.returncode is not None
        return subprocess.CompletedProcess(
            process.args,
            process.returncode,
            command_stdout,
            command_stderr,
        )


def assert_command_succeeded(
    result: subprocess.CompletedProcess[str],
    command_name: str,
) -> None:
    """Assert that a completed command exited successfully."""
    if result.returncode != 0:
        raise AssertionError(
            f"Command {command_name!r} failed with exit code "
            f"{result.returncode}:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


def wait_for_process_success(
    process: subprocess.Popen[str],
    command_name: str,
    timeout: float = 600,
) -> None:
    """Wait for an already started command and assert that it succeeds."""
    try:
        returncode = process.wait(timeout=timeout)
    except subprocess.TimeoutExpired as error:
        stop_command(process)
        raise AssertionError(
            f"Command {command_name} did not finish within {timeout}s"
        ) from error

    if returncode != 0:
        raise AssertionError(
            f"Command {command_name} failed with exit code {returncode}; "
            "see its command log for output"
        )


def retry_command_until_success(
    command: str,
    command_name: str,
    timeout: float = 600,
    interval: float = 1,
) -> subprocess.CompletedProcess[str]:
    deadline = deadline_after(timeout)
    result: subprocess.CompletedProcess[str] | None = None

    while remaining_time(deadline) > 0:
        try:
            result = run_command_and_wait_to_finish(
                command,
                command_name,
                timeout=remaining_time(deadline),
                capture_output=True,
            )
        except subprocess.TimeoutExpired as error:
            raise AssertionError(
                f"Command did not finish within {timeout}s:\n{command}"
            ) from error

        if result.returncode == 0:
            return result

        sleep_before_retry(deadline, interval)

    if result is None:
        raise AssertionError(f"Command was not run before its {timeout}s timeout")

    raise AssertionError(
        f"Command did not succeed within {timeout}s (exit code {result.returncode}):\n"
        f"{command}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
