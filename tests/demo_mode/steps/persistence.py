"""Steps for persistent demo-mode environments."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess

import pytest
from environment import docker  # pylint: disable=import-error

from tests.demo_mode.type_definitions import PersistentService
from tests.demo_mode.utils.commands import stop_command
from tests.demo_mode.utils.logging import log_step
from tests.demo_mode.utils.persistence import start_persistent_service
from tests.demo_mode.utils.rest import get_provider_supported_space_ids


@log_step("Starting persistent Onezone")
def start_persistent_onezone(
    release: str,
    container_name: str,
    request: pytest.FixtureRequest,
) -> PersistentService:
    """Start Onezone using the unmodified persistence command."""
    return start_persistent_service(
        "persistency/run_onezone.sh",
        release,
        container_name,
        request,
    )


@log_step("Starting persistent Oneprovider")
def start_persistent_oneprovider(
    release: str,
    onezone: PersistentService,
    container_name: str,
    request: pytest.FixtureRequest,
) -> PersistentService:
    """Start Oneprovider using the unmodified persistence command."""
    if onezone.process.poll() is not None:
        raise AssertionError("Onezone stopped before Oneprovider could be started")

    return start_persistent_service(
        "persistency/run_oneprovider.sh",
        release,
        container_name,
        request,
    )


@log_step("Stopping persistent demo-mode environment")
def stop_persistent_environment(
    services: list[PersistentService],
    timeout: float = 60,
) -> None:
    """Gracefully stop and reap a persistent demo-mode environment."""
    for service in services:
        docker.stop(
            service.container_name,
            command_timeout=timeout,
        )
        try:
            service.process.wait(timeout=timeout)
        except subprocess.TimeoutExpired as error:
            stop_command(service.process)
            raise AssertionError(
                "The command running "
                f"{service.container_name} did not exit after Docker stop"
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
        f"Expected provider ID {expected_provider_id!r} after restart, "
        f"got {actual_provider_id!r}"
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
    assert (
        space_id in supported_space_ids
    ), f"Space {space_id} is no longer supported by {provider_container} after restart"
