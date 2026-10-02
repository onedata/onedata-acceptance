"""Structured execution of demo-mode commands and script templates."""

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
CONTAINER_NAME_PLACEHOLDER: Final = "xCONTAINERxNAMEx"
SHORT_COMMAND_TIMEOUT: Final = 60.0


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

    def _run_once(self, timeout: float) -> subprocess.CompletedProcess[str]:
        log_running_command(self.text)
        with open_command_log(self.text, self.name) as log_file:
            process = _start_subprocess(
                self.text,
                self.cwd,
                log_file,
                capture_output=True,
            )
            try:
                stdout, stderr = process.communicate(timeout=timeout)
            except subprocess.TimeoutExpired:
                stdout, stderr = _kill_process(process)
                log_file.write(stdout)
                log_file.write(stderr)
                raise

            log_file.write(stdout)
            log_file.write(stderr)
            assert process.returncode is not None
            return subprocess.CompletedProcess(
                process.args,
                process.returncode,
                stdout,
                stderr,
            )

    def run(self, *, timeout: float = SHORT_COMMAND_TIMEOUT) -> str:
        """Run once and return stdout, failing on timeout or a nonzero exit."""
        try:
            result = self._run_once(timeout)
        except subprocess.TimeoutExpired as error:
            raise AssertionError(
                f"Command {self.name!r} did not finish within {timeout}s"
            ) from error

        if result.returncode != 0:
            raise AssertionError(
                f"Command {self.name!r} failed with exit code "
                f"{result.returncode}:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )
        return result.stdout

    def run_until_success(self, *, timeout: float, interval: float = 1) -> str:
        """Retry until the command succeeds and return its stdout."""
        deadline = deadline_after(timeout)
        result: subprocess.CompletedProcess[str] | None = None

        while remaining_time(deadline) > 0:
            try:
                result = self._run_once(remaining_time(deadline))
            except subprocess.TimeoutExpired as error:
                raise AssertionError(
                    f"Command {self.name!r} did not finish within {timeout}s"
                ) from error

            if result.returncode == 0:
                return result.stdout
            sleep_before_retry(deadline, interval)

        if result is None:
            raise AssertionError(f"Command {self.name!r} was not run before its {timeout}s timeout")
        raise AssertionError(
            f"Command {self.name!r} did not succeed within {timeout}s "
            f"(exit code {result.returncode}):\n"
            f"{self.text}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    @staticmethod
    def stop_process(process: subprocess.Popen[str], timeout: float = 10) -> None:
        """Stop and reap a process together with its child processes."""
        if process.poll() is not None:
            return

        _send_signal_to_process_group(process, signal.SIGTERM)
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            _send_signal_to_process_group(process, signal.SIGKILL)
            process.wait()


@dataclass(frozen=True)
class CommandTemplate:
    """A command script whose release and container placeholders are rendered."""

    relative_path: str
    release: str | None = None

    @property
    def path(self) -> Path:
        """Return the validated path of this command script."""
        return command_path(self.relative_path)

    def render(self, container: str | None = None) -> str:
        """Load the command and substitute values required by its template."""
        command = self.path.read_text(encoding="utf-8")

        if RELEASE_PLACEHOLDER in command:
            if self.release is None:
                raise ValueError(f"Command {self.relative_path!r} requires a release")
            command = command.replace(RELEASE_PLACEHOLDER, self.release)

        if CONTAINER_NAME_PLACEHOLDER in command:
            if container is None:
                raise ValueError(f"Command {self.relative_path!r} requires a container name")
            command = command.replace(CONTAINER_NAME_PLACEHOLDER, container)

        return command

    def command(self, container: str | None = None) -> Command:
        """Render this template into an executable command."""
        return Command(self.render(container), self.relative_path)

    def run(
        self,
        container: str | None = None,
        *,
        timeout: float = SHORT_COMMAND_TIMEOUT,
    ) -> str:
        """Run the rendered command once and return its stdout."""
        return self.command(container).run(timeout=timeout)

    def start(self, container: str | None = None) -> subprocess.Popen[str]:
        """Start the rendered command and return its process without waiting."""
        return self.command(container).start()

    def run_until_success(
        self,
        container: str | None = None,
        *,
        timeout: float,
    ) -> str:
        """Retry the rendered command until it succeeds and return its stdout."""
        return self.command(container).run_until_success(timeout=timeout)
