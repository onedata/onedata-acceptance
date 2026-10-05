"""Steps for persistent demo-mode environments."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess

import pytest
from environment import docker

from tests.demo_mode.constants import (
    FIRST_ONEPROVIDER_CONTAINER,
    ONEZONE_CONTAINER,
)
from tests.demo_mode.type_definitions import DemoEnvironment, Oneprovider, Onezone
from tests.demo_mode.utils.commands import DemoCommands
from tests.demo_mode.utils.logging import log_step


@log_step("Starting persistent Onezone")
def start_persistent_onezone(
    commands: DemoCommands,
    request: pytest.FixtureRequest,
) -> Onezone:
    """Start Onezone using the unmodified persistence command."""
    onezone = Onezone(
        container=ONEZONE_CONTAINER,
        process=commands.persistent_onezone().start(),
    )
    request.addfinalizer(onezone.stop_process)
    return onezone


@log_step("Starting persistent Oneprovider")
def start_persistent_oneprovider(
    commands: DemoCommands,
    onezone: Onezone,
    request: pytest.FixtureRequest,
) -> Oneprovider:
    """Start Oneprovider using the unmodified persistence command."""
    if onezone.process is None or onezone.process.poll() is not None:
        raise AssertionError("Onezone stopped before Oneprovider could be started")

    oneprovider = Oneprovider(
        container=FIRST_ONEPROVIDER_CONTAINER,
        process=commands.persistent_oneprovider().start(),
    )
    request.addfinalizer(oneprovider.stop_process)
    return oneprovider


@log_step("Stopping persistent demo-mode environment")
def stop_persistent_environment(
    environment: DemoEnvironment,
    timeout: float = 60,
) -> None:
    """Gracefully stop and reap a persistent demo-mode environment."""
    services = (*environment.oneproviders, environment.onezone)
    for service in services:
        docker.stop(
            service.container,
            command_timeout=timeout,
        )
        if service.process is None:
            raise AssertionError(f"Persistent service {service.container} has no launcher process")
        try:
            service.process.wait(timeout=timeout)
        except subprocess.TimeoutExpired as error:
            service.stop_process()
            raise AssertionError(
                f"The command running {service.container} did not exit after Docker stop"
            ) from error
