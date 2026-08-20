"""Composite steps for starting demo-mode environments."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess

import pytest

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
    onezone_container: str,
    first_oneprovider_container: str,
    request: pytest.FixtureRequest,
    second_oneprovider_container: str | None = None,
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

    if second_oneprovider_container is not None:
        second_oneprovider_process = _start_oneprovider_command(
            release,
            "distributed_environment/run_second_oneprovider.sh",
            onezone_process,
            request,
        )

    await_running_container(
        release,
        onezone_container,
        "run_in_background/await_onezone.sh",
        onezone_process,
    )
    await_running_container(
        release,
        first_oneprovider_container,
        "run_in_background/await_oneprovider.sh",
        first_oneprovider_process,
    )
    if second_oneprovider_container is not None:
        await_running_container(
            release,
            second_oneprovider_container,
            "test_only/await_second_oneprovider.sh",
            second_oneprovider_process,
        )


def start_background_environment(
    release: str,
    onezone_container: str,
    first_oneprovider_container: str,
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
        onezone_container,
        "run_in_background/run_onezone.sh",
        "run_in_background/await_onezone.sh",
        onezone_process,
    )
    _await_background_command(
        release,
        first_oneprovider_container,
        "run_in_background/run_oneprovider.sh",
        "run_in_background/await_oneprovider.sh",
        oneprovider_process,
    )
