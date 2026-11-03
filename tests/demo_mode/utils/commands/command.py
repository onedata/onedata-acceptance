"""Executable demo-mode command abstraction."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Final, TextIO

from tests.demo_mode.constants import SHORT_COMMAND_TIMEOUT
from tests.demo_mode.utils.command_context import (
    current_command_context,
    kill_process_group,
)
from tests.demo_mode.utils.logging import log_running_command, open_command_log

_DEMO_MODE_ROOT: Final = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Command:
    """A rendered shell command with logging and process lifecycle handling."""

    text: str
    name: str
    cwd: Path = _DEMO_MODE_ROOT

    def start(self) -> subprocess.Popen[str]:
        """Start the command and return its process without waiting for it."""
        log_running_command(self.text)
        with open_command_log(self.text, self.name) as log_file:
            return _start_subprocess(
                self.text,
                self.cwd,
                log_file,
                capture_output=False,
            )

    def run(self, *, timeout: float = SHORT_COMMAND_TIMEOUT) -> str:
        """Run once and return stdout, failing with captured output."""
        _validate_timeout(timeout)
        log_running_command(self.text)

        with open_command_log(self.text, self.name) as log_file:
            result = self._run_once(timeout, log_file)

        if result.returncode != 0:
            raise AssertionError(
                f"Command {self.name!r} failed with exit code "
                f"{result.returncode}:\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            )

        return result.stdout

    def run_until_success(self, *, timeout: float, interval: float = 1) -> str:
        """Retry until success, writing every attempt to one command log."""
        _validate_timeout(timeout)
        deadline = _deadline_after(timeout)
        attempt = 1

        log_running_command(self.text)

        with open_command_log(self.text, self.name) as log_file:
            while True:
                log_file.write(f"\n=== attempt {attempt} ===\n")
                log_file.flush()

                result = self._run_once(
                    _remaining_time(deadline),
                    log_file,
                )

                if result.returncode == 0:
                    return result.stdout

                attempt += 1
                _sleep_before_retry(deadline, interval)
                if _remaining_time(deadline) <= 0:
                    break

        raise AssertionError(
            f"Command {self.name!r} did not succeed within {timeout}s "
            f"(exit code {result.returncode}):\n"
            f"{self.text}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

    def _run_once(
        self,
        timeout: float,
        log_file: TextIO,
    ) -> subprocess.CompletedProcess[str]:
        """Run one attempt using the supplied shared command log."""
        process = _start_subprocess(
            self.text,
            self.cwd,
            log_file,
            capture_output=True,
        )
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired as error:
            stdout, stderr = kill_process_group(process)
            log_file.write(stdout)
            log_file.write(stderr)
            log_file.flush()
            assert process.returncode is not None
            raise AssertionError(
                f"Command {self.name!r} did not finish within {timeout}s "
                f"(exit code {process.returncode}):\n"
                f"stdout:\n{stdout}\n"
                f"stderr:\n{stderr}"
            ) from error

        log_file.write(stdout)
        log_file.write(stderr)
        log_file.flush()

        assert process.returncode is not None
        return subprocess.CompletedProcess(
            process.args,
            process.returncode,
            stdout,
            stderr,
        )


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


def _validate_timeout(timeout: float) -> None:
    if timeout <= 0:
        raise ValueError(f"Command timeout must be positive, got {timeout}")


def _deadline_after(timeout: float) -> float:
    return time.monotonic() + timeout


def _remaining_time(deadline: float) -> float:
    return max(0, deadline - time.monotonic())


def _sleep_before_retry(deadline: float, interval: float) -> None:
    time.sleep(min(interval, _remaining_time(deadline)))
