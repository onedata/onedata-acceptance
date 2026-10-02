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
from tests.demo_mode.utils.commands import CommandTemplate
from tests.demo_mode.utils.logging import log_step
from tests.demo_mode.utils.rest import get_provider_supported_space_ids


@log_step("Starting persistent Onezone")
def start_persistent_onezone(
    release: str,
    request: pytest.FixtureRequest,
) -> Onezone:
    """Start Onezone using the unmodified persistence command."""
    onezone = Onezone(
        container=ONEZONE_CONTAINER,
        process=CommandTemplate(
            "persistency/run_onezone.sh",
            release,
        ).start(),
    )
    request.addfinalizer(onezone.stop_process)
    return onezone


@log_step("Starting persistent Oneprovider")
def start_persistent_oneprovider(
    release: str,
    onezone: Onezone,
    request: pytest.FixtureRequest,
) -> Oneprovider:
    """Start Oneprovider using the unmodified persistence command."""
    if onezone.process is None or onezone.process.poll() is not None:
        raise AssertionError("Onezone stopped before Oneprovider could be started")

    oneprovider = Oneprovider(
        container=FIRST_ONEPROVIDER_CONTAINER,
        process=CommandTemplate(
            "persistency/run_oneprovider.sh",
            release,
        ).start(),
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


@log_step("Asserting demo access token persisted")
def assert_access_token_is_persistent(
    expected_access_token: str,
    actual_access_token: str,
) -> None:
    """Assert that the demo access token persisted across a restart."""
    assert actual_access_token == expected_access_token, (
        "Demo access token changed after restart: "
        f"expected {expected_access_token!r}, got {actual_access_token!r}"
    )


@log_step("Asserting provider ID persisted")
def assert_provider_id_is_persistent(
    expected_provider_id: str,
    actual_provider_id: str,
) -> None:
    """Assert that a provider ID persisted across a restart."""
    assert actual_provider_id == expected_provider_id, (
        f"Expected provider ID {expected_provider_id!r} after restart, got {actual_provider_id!r}"
    )


@log_step("Asserting provider space support persisted")
def assert_space_support_is_persistent(
    provider_container: str,
    space_id: str,
    access_token: str,
) -> None:
    """Assert that provider space support persisted across a restart."""
    supported_space_ids = get_provider_supported_space_ids(
        provider_container,
        access_token,
    )
    assert space_id in supported_space_ids, (
        f"Space {space_id} is no longer supported by {provider_container} after restart"
    )
