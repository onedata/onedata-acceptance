"""Command helpers for demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os
import signal
import subprocess
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Final, TextIO

from tests.demo_mode.utils.logging import log_running_command, open_command_log
from tests.utils.time_utils import deadline_after, remaining_time, sleep_before_retry

DEMO_MODE_ROOT: Final = Path(__file__).resolve().parents[1]
COMMANDS_ROOT: Final = DEMO_MODE_ROOT / "commands"
RELEASE_PLACEHOLDER: Final = "xRELEASExVERSIONx"
ONEZONE_URL_PREFIX: Final = "URL: "


@dataclass(frozen=True)
class CommandOutput:
    stdout: str
    stderr: str


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


def load_command(relative_path: str, release: str) -> str:
    """Load a command verbatim, replacing only its release placeholder."""
    command = command_path(relative_path).read_text(encoding="utf-8")
    command = command.replace(RELEASE_PLACEHOLDER, release)
    return command


def _start_subprocess(  # pylint: disable=consider-using-with
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
        process = _start_subprocess(
            command,
            DEMO_MODE_ROOT,
            log_file,
        )
    return process


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


def run_command(
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


def wait_for_successful_process(
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


def wait_for_successful_command(
    command: str,
    command_name: str,
    timeout: float = 600,
    interval: float = 1,
) -> subprocess.CompletedProcess[str]:
    deadline = deadline_after(timeout)
    result: subprocess.CompletedProcess[str] | None = None

    while remaining_time(deadline) > 0:
        try:
            result = run_command(
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


def get_access_token(release: str) -> str:
    relative_command_path = "common/get_oneprovider_token.sh"
    command = load_command(relative_command_path, release)
    result = run_command(command, relative_command_path, capture_output=True)
    if result.returncode != 0:
        raise AssertionError(
            "The access-token command failed with exit code "
            f"{result.returncode}:\n{result.stderr}"
        )

    access_token = result.stdout.strip()
    if not access_token:
        raise AssertionError("The access-token command returned an empty result")
    return access_token


def get_onezone_url() -> str:
    """Run the common tutorial command and return its Onezone URL."""
    relative_command_path = "common/get_onezone_url.sh"
    command = command_path(relative_command_path).read_text(encoding="utf-8")
    result = run_command(command, relative_command_path, capture_output=True)
    if result.returncode != 0:
        raise AssertionError(
            "The Onezone URL command failed with exit code "
            f"{result.returncode}:\n{result.stderr}"
        )

    output_lines = result.stdout.splitlines()
    if len(output_lines) != 1 or not output_lines[0].startswith(ONEZONE_URL_PREFIX):
        raise AssertionError(
            f"The Onezone URL command returned unexpected output: {result.stdout!r}"
        )

    onezone_url = output_lines[0].removeprefix(ONEZONE_URL_PREFIX)
    if not onezone_url:
        raise AssertionError("The Onezone URL command returned an empty URL")
    return onezone_url
