"""Steps for persistent demo-mode environments."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess
from functools import partial

import pytest

from tests.demo_mode.type_definitions import PersistentService
from tests.demo_mode.utils.commands import (
    load_command,
    start_command,
    stop_command,
    wait_for_successful_command,
)
from tests.demo_mode.utils.logging import log_step
from tests.demo_mode.utils.rest import get_provider_supported_space_ids


def _run_persistent_service(
    command_path: str,
    await_command_path: str,
    release: str,
    container_name: str,
    request: pytest.FixtureRequest,
) -> PersistentService:
    command = load_command(command_path, release)
    process = start_command(command)
    request.addfinalizer(partial(stop_command, process))
    wait_for_successful_command(load_command(await_command_path, release))

    return PersistentService(container_name=container_name, process=process)


@log_step("Running persistent Onezone")
def run_persistent_onezone(
    release: str,
    container_name: str,
    request: pytest.FixtureRequest,
) -> PersistentService:
    """Start Onezone using the unmodified persistence command."""
    return _run_persistent_service(
        "persistency/run_onezone.sh",
        "run_in_background/await_onezone.sh",
        release,
        container_name,
        request,
    )


@log_step("Running persistent Oneprovider")
def run_persistent_oneprovider(
    release: str,
    onezone: PersistentService,
    container_name: str,
    request: pytest.FixtureRequest,
) -> PersistentService:
    """Start Oneprovider using the unmodified persistence command."""
    if onezone.process.poll() is not None:
        raise AssertionError("Onezone stopped before Oneprovider could be started")

    return _run_persistent_service(
        "persistency/run_oneprovider.sh",
        "run_in_background/await_oneprovider.sh",
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
        result = subprocess.run(
            ["docker", "stop", service.container_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
            check=False,
        )
        if result.returncode != 0:
            raise AssertionError(
                f"Failed to stop {service.container_name} with exit code "
                f"{result.returncode}:\n{result.stdout}"
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
