"""Composite steps for starting demo-mode environments."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess

import pytest

from tests.demo_mode.constants import (
    FIRST_ONEPROVIDER_CONTAINER,
    ONEZONE_CONTAINER,
    SECOND_ONEPROVIDER_CONTAINER,
)
from tests.demo_mode.steps.environment import (
    await_running_container,
    start_environment_command,
)
from tests.demo_mode.utils.commands import wait_for_successful_process


def _start_oneprovider_command(
    release: str,
    command_path: str,
    onezone_process: subprocess.Popen[str],
    request: pytest.FixtureRequest,
) -> subprocess.Popen[str]:
    if onezone_process.poll() is not None:
        raise AssertionError("Onezone stopped before Oneprovider could be started")
    return start_environment_command(release, command_path, request)


def _await_background_command(
    release: str,
    container_name: str,
    start_command_path: str,
    await_command_path: str,
    process: subprocess.Popen[str],
) -> None:
    wait_for_successful_process(process, start_command_path)
    await_running_container(release, container_name, await_command_path)


def start_foreground_environment(
    release: str,
    request: pytest.FixtureRequest,
    start_second_oneprovider: bool = False,
) -> None:
    """Start all foreground commands before awaiting their services."""
    onezone_process = start_environment_command(
        release,
        "run_in_foreground/run_onezone.sh",
        request,
    )
    first_oneprovider_process = _start_oneprovider_command(
        release,
        "run_in_foreground/run_oneprovider.sh",
        onezone_process,
        request,
    )

    if start_second_oneprovider:
        second_oneprovider_process = _start_oneprovider_command(
            release,
            "distributed_environment/run_second_oneprovider.sh",
            onezone_process,
            request,
        )

    await_running_container(
        release,
        ONEZONE_CONTAINER,
        "run_in_background/await_onezone.sh",
        onezone_process,
    )
    await_running_container(
        release,
        FIRST_ONEPROVIDER_CONTAINER,
        "run_in_background/await_oneprovider.sh",
        first_oneprovider_process,
    )
    if start_second_oneprovider:
        await_running_container(
            release,
            SECOND_ONEPROVIDER_CONTAINER,
            "test_only/await_second_oneprovider.sh",
            second_oneprovider_process,
        )


def start_background_environment(
    release: str,
    request: pytest.FixtureRequest,
) -> None:
    """Start both detached commands before awaiting their services."""
    onezone_process = start_environment_command(
        release,
        "run_in_background/run_onezone.sh",
        request,
    )
    oneprovider_process = start_environment_command(
        release,
        "run_in_background/run_oneprovider.sh",
        request,
    )

    _await_background_command(
        release,
        ONEZONE_CONTAINER,
        "run_in_background/run_onezone.sh",
        "run_in_background/await_onezone.sh",
        onezone_process,
    )
    _await_background_command(
        release,
        FIRST_ONEPROVIDER_CONTAINER,
        "run_in_background/run_oneprovider.sh",
        "run_in_background/await_oneprovider.sh",
        oneprovider_process,
    )
