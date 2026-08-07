"""Logical steps used by demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess
from functools import partial

import pytest

from tests.demo_mode.utils.commands import (
    load_command,
    run_command,
    start_command,
    stop_command,
    wait_for_successful_command,
)
from tests.demo_mode.utils.logging import (
    log_running_command,
    log_step_done,
    log_step_start,
)
from tests.demo_mode.utils.rest import get_onezone_configuration


def run_onezone(release: str, request: pytest.FixtureRequest) -> subprocess.Popen[str]:
    """Start Onezone and wait until it is ready."""
    description = "Running Onezone"
    log_step_start(description)

    command = load_command("run_in_foreground/run_onezone.sh", release)
    process = start_command(command)
    request.addfinalizer(partial(stop_command, process))

    await_command = load_command(
        "run_in_background/await_onezone.sh",
        release,
    )
    wait_for_successful_command(await_command)

    log_step_done(description)
    return process


def run_oneprovider(
    release: str,
    onezone_process: subprocess.Popen[str],
    request: pytest.FixtureRequest,
) -> subprocess.Popen[str]:
    """Start Oneprovider and wait until it is ready."""
    description = "Running Oneprovider"
    log_step_start(description)

    if onezone_process.poll() is not None:
        raise AssertionError("Onezone stopped before Oneprovider could be started")

    command = load_command("run_in_foreground/run_oneprovider.sh", release)
    process = start_command(command)
    request.addfinalizer(partial(stop_command, process))

    await_command = load_command(
        "run_in_background/await_oneprovider.sh",
        release,
    )
    wait_for_successful_command(await_command)

    log_step_done(description)
    return process


def _run_background_command(command: str, timeout: float = 480) -> None:
    log_running_command(command)
    result = run_command(command, timeout=timeout, capture_output=True)
    if result.returncode != 0:
        raise AssertionError(
            f"Background command failed with exit code {result.returncode}:\n"
            f"{command}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


def run_onezone_in_background(release: str) -> None:
    """Start Onezone in detached mode and actively wait until it is ready."""
    description = "Running Onezone in background"
    log_step_start(description)

    command = load_command("run_in_background/run_onezone.sh", release)
    _run_background_command(command)

    await_command = load_command(
        "run_in_background/await_onezone.sh",
        release,
    )
    wait_for_successful_command(await_command)

    log_step_done(description)


def run_oneprovider_in_background(release: str) -> None:
    """Start Oneprovider in detached mode and actively wait until it is ready."""
    description = "Running Oneprovider in background"
    log_step_start(description)

    command = load_command("run_in_background/run_oneprovider.sh", release)
    _run_background_command(command)

    await_command = load_command(
        "run_in_background/await_oneprovider.sh",
        release,
    )
    wait_for_successful_command(await_command)

    log_step_done(description)


def assert_onezone_configuration() -> None:
    """Assert that Onezone exposes a valid public REST configuration."""
    description = "Asserting Onezone configuration"
    log_step_start(description)

    onezone_configuration = get_onezone_configuration()
    onezone_name = onezone_configuration.get("name")
    onezone_version = onezone_configuration.get("version")
    assert isinstance(onezone_name, str) and onezone_name
    assert isinstance(onezone_version, str) and onezone_version

    log_step_done(description)
