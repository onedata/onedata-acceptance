"""Steps for starting demo-mode environments."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess
from functools import partial

import pytest

from tests.demo_mode.utils.commands import (
    load_command,
    run_background_command,
    start_command,
    stop_command,
    wait_for_successful_command,
)
from tests.demo_mode.utils.logging import log_step


@log_step("Running Onezone")
def run_onezone(release: str, request: pytest.FixtureRequest) -> subprocess.Popen[str]:
    """Start Onezone and wait until it is ready."""
    command = load_command("run_in_foreground/run_onezone.sh", release)
    process = start_command(command)
    request.addfinalizer(partial(stop_command, process))

    await_command = load_command(
        "run_in_background/await_onezone.sh",
        release,
    )
    wait_for_successful_command(await_command)

    return process


@log_step("Running Oneprovider")
def run_oneprovider(
    release: str,
    onezone_process: subprocess.Popen[str],
    request: pytest.FixtureRequest,
) -> subprocess.Popen[str]:
    """Start the first Oneprovider and wait until it is ready."""
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

    return process


@log_step("Running second Oneprovider")
def run_second_oneprovider(
    release: str,
    onezone_process: subprocess.Popen[str],
    request: pytest.FixtureRequest,
) -> subprocess.Popen[str]:
    """Start the second Oneprovider and wait until it is ready."""
    if onezone_process.poll() is not None:
        raise AssertionError(
            "Onezone stopped before second Oneprovider could be started"
        )

    command = load_command(
        "distributed_environment/run_second_oneprovider.sh",
        release,
    )
    process = start_command(command)
    request.addfinalizer(partial(stop_command, process))
    await_command = load_command(
        "test_only/await_second_oneprovider.sh",
        release,
    )
    wait_for_successful_command(await_command)

    return process


@log_step("Running Onezone in background")
def run_onezone_in_background(release: str) -> None:
    """Start Onezone in detached mode and actively wait until it is ready."""
    command = load_command("run_in_background/run_onezone.sh", release)
    run_background_command(command)
    await_command = load_command("run_in_background/await_onezone.sh", release)
    wait_for_successful_command(await_command)


@log_step("Running Oneprovider in background")
def run_oneprovider_in_background(release: str) -> None:
    """Start Oneprovider in detached mode and actively wait until it is ready."""
    command = load_command("run_in_background/run_oneprovider.sh", release)
    run_background_command(command)
    await_command = load_command("run_in_background/await_oneprovider.sh", release)
    wait_for_successful_command(await_command)
