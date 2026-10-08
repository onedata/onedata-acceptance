"""Executable demo-mode command abstraction."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import signal
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO

from tests.demo_mode.constants import PROCESS_EXIT_TIMEOUT, SHORT_COMMAND_TIMEOUT
from tests.demo_mode.utils.commands.helpers import (
    DEMO_MODE_ROOT,
    _kill_process,
    _send_signal_to_process_group,
    _start_subprocess,
)
from tests.demo_mode.utils.logging import log_running_command, open_command_log
from tests.utils.time_utils import deadline_after, remaining_time, sleep_before_retry


class _CommandTimeout(Exception):
    """Captured output and exit status of a command killed after a timeout."""

    def __init__(self, returncode: int, stdout: str, stderr: str) -> None:
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


@dataclass(frozen=True)
class Command:
    """A rendered shell command with logging and process lifecycle handling."""

    text: str
    name: str
    cwd: Path = DEMO_MODE_ROOT

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
            stdout, stderr = _kill_process(process)
            log_file.write(stdout)
            log_file.write(stderr)
            log_file.flush()
            assert process.returncode is not None
            raise _CommandTimeout(
                process.returncode,
                stdout,
                stderr,
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

    def run(self, *, timeout: float = SHORT_COMMAND_TIMEOUT) -> str:
        """Run once and return stdout, failing with captured output."""
        log_running_command(self.text)

        try:
            with open_command_log(self.text, self.name) as log_file:
                result = self._run_once(timeout, log_file)
        except _CommandTimeout as error:
            raise AssertionError(
                f"Command {self.name!r} did not finish within {timeout}s "
                f"(exit code {error.returncode}):\n"
                f"stdout:\n{error.stdout}\n"
                f"stderr:\n{error.stderr}"
            ) from error

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
        deadline = deadline_after(timeout)
        result: subprocess.CompletedProcess[str] | None = None
        attempt = 1

        log_running_command(self.text)

        with open_command_log(self.text, self.name) as log_file:
            while remaining_time(deadline) > 0:
                log_file.write(f"\n=== attempt {attempt} ===\n")
                log_file.flush()

                try:
                    result = self._run_once(
                        remaining_time(deadline),
                        log_file,
                    )
                except _CommandTimeout as error:
                    raise AssertionError(
                        f"Command {self.name!r} did not finish within {timeout}s "
                        f"(exit code {error.returncode}):\n"
                        f"stdout:\n{error.stdout}\n"
                        f"stderr:\n{error.stderr}"
                    ) from error

                if result.returncode == 0:
                    return result.stdout

                attempt += 1
                sleep_before_retry(deadline, interval)

        if result is None:
            raise AssertionError(f"Command {self.name!r} was not run before its {timeout}s timeout")

        raise AssertionError(
            f"Command {self.name!r} did not succeed within {timeout}s "
            f"(exit code {result.returncode}):\n"
            f"{self.text}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

    @staticmethod
    def stop_process(process: subprocess.Popen[str], timeout: float = PROCESS_EXIT_TIMEOUT) -> None:
        """Stop and reap a process together with its child processes."""
        if process.poll() is not None:
            return

        _send_signal_to_process_group(process, signal.SIGTERM)
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            _send_signal_to_process_group(process, signal.SIGKILL)
            process.wait()
