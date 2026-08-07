"""Logical steps used by demo-mode tests."""

__author__ = "Mateusz Zając"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess
from functools import partial

import pytest

from tests.demo_mode.utils.commands import (
    load_command,
    start_command,
    stop_command,
    wait_for_successful_command,
)
from tests.demo_mode.utils.logging import log_step_done, log_step_start
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


def assert_onezone_configuration(
    onezone_process: subprocess.Popen[str],
    oneprovider_process: subprocess.Popen[str],
) -> None:
    """Assert that both services run and Onezone exposes its REST configuration."""
    description = "Asserting Onezone configuration"
    log_step_start(description)

    if onezone_process.poll() is not None or oneprovider_process.poll() is not None:
        raise AssertionError("A demo-mode service stopped after reporting readiness")

    onezone_configuration = get_onezone_configuration()
    onezone_name = onezone_configuration.get("name")
    onezone_version = onezone_configuration.get("version")
    assert isinstance(onezone_name, str) and onezone_name
    assert isinstance(onezone_version, str) and onezone_version

    log_step_done(description)
