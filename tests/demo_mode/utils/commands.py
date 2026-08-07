"""Command helpers for demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os
import signal
import subprocess
from pathlib import Path
from time import monotonic, sleep
from typing import Final

from tests.demo_mode.utils.logging import log_running_command
from tests.utils.docker_utils import remove_container

DEMO_MODE_ROOT: Final = Path(__file__).resolve().parents[1]
COMMANDS_ROOT: Final = DEMO_MODE_ROOT / "commands"
RELEASE_PLACEHOLDER: Final = "xRELEASExVERSIONx"
DEMO_CONTAINER_NAMES: Final = ("op_test1", "oz_test")


def command_path(relative_path: str) -> Path:
    """Return a validated path to an unmodified file in ``commands``."""
    path = (COMMANDS_ROOT / relative_path).resolve()
    try:
        path.relative_to(COMMANDS_ROOT)
    except ValueError as error:
        raise ValueError(
            f"Command path escapes {COMMANDS_ROOT}: {relative_path}"
        ) from error

    if not path.is_file():
        raise FileNotFoundError(path)
    return path


def load_command(relative_path: str, release: str) -> str:
    """Load a command verbatim, replacing only its release placeholder."""
    command = command_path(relative_path).read_text(encoding="utf-8")
    command = command.replace(RELEASE_PLACEHOLDER, release)
    return command


def start_command(command: str) -> subprocess.Popen[str]:
    log_running_command(command)
    process = subprocess.Popen(  # pylint: disable=consider-using-with
        command,
        cwd=DEMO_MODE_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        shell=True,
        start_new_session=True,
        text=True,
    )
    return process


def stop_command(process: subprocess.Popen[str], timeout: float = 10) -> None:
    """Stop and reap a command together with its child processes."""
    if process.poll() is not None:
        return

    try:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    except ProcessLookupError:
        pass

    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()


def remove_demo_containers() -> None:
    """Remove containers left by a current or interrupted demo-mode test."""
    for container_name in DEMO_CONTAINER_NAMES:
        remove_container(container_name)


def run_command(
    command: str,
    timeout: float | None = None,
    capture_output: bool = False,
    cwd: Path = DEMO_MODE_ROOT,
) -> subprocess.CompletedProcess[str]:
    output = subprocess.PIPE if capture_output else subprocess.DEVNULL
    return subprocess.run(
        command,
        cwd=cwd,
        stdout=output,
        stderr=output,
        shell=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def wait_for_successful_command(
    command: str,
    timeout: float = 480,
    interval: float = 1,
) -> subprocess.CompletedProcess[str]:
    deadline = monotonic() + timeout
    result: subprocess.CompletedProcess[str] | None = None

    while monotonic() < deadline:
        try:
            result = run_command(
                command,
                timeout=deadline - monotonic(),
                capture_output=True,
            )
        except subprocess.TimeoutExpired as error:
            raise AssertionError(
                f"Command did not finish within {timeout}s:\n{command}"
            ) from error

        if result.returncode == 0:
            return result

        sleep(min(interval, max(0, deadline - monotonic())))

    if result is None:
        raise AssertionError(f"Command was not run before its {timeout}s timeout")

    raise AssertionError(
        f"Command did not succeed within {timeout}s (exit code {result.returncode}):\n"
        f"{command}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )


def get_access_token(release: str) -> str:
    command = load_command("access_token/get_oneprovider_token.sh", release)
    result = run_command(command, capture_output=True)
    if result.returncode != 0:
        raise AssertionError(
            "The access-token command failed with exit code "
            f"{result.returncode}:\n{result.stderr}"
        )

    access_token = result.stdout.strip()
    if not access_token:
        raise AssertionError("The access-token command returned an empty result")
    return access_token
