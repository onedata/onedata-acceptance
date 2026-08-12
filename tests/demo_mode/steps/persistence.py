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
from tests.demo_mode.utils.logging import log_step_done, log_step_start
from tests.demo_mode.utils.rest import get_provider_supported_space_ids


def _run_persistent_service(
    description: str,
    command_path: str,
    await_command_path: str,
    release: str,
    container_name: str,
    request: pytest.FixtureRequest,
) -> PersistentService:
    log_step_start(description)

    command = load_command(command_path, release)
    process = start_command(command)
    request.addfinalizer(partial(stop_command, process))
    wait_for_successful_command(load_command(await_command_path, release))

    log_step_done(description)
    return PersistentService(container_name=container_name, process=process)


def run_persistent_onezone(
    release: str,
    container_name: str,
    request: pytest.FixtureRequest,
) -> PersistentService:
    """Start Onezone using the unmodified persistence command."""
    return _run_persistent_service(
        "Running persistent Onezone",
        "persistency/run_onezone.sh",
        "run_in_background/await_onezone.sh",
        release,
        container_name,
        request,
    )


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
        "Running persistent Oneprovider",
        "persistency/run_oneprovider.sh",
        "run_in_background/await_oneprovider.sh",
        release,
        container_name,
        request,
    )


def stop_persistent_environment(
    services: list[PersistentService],
    timeout: float = 60,
) -> None:
    """Gracefully stop and reap a persistent demo-mode environment."""
    description = "Stopping persistent demo-mode environment"
    log_step_start(description)

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

    log_step_done(description)


def assert_access_token_is_persistent(
    expected_access_token: str,
    actual_access_token: str,
) -> None:
    """Assert that the demo access token persisted across a restart."""
    description = "Asserting demo access token persisted"
    log_step_start(description)

    assert actual_access_token == expected_access_token, (
        "Demo access token changed after restart: "
        f"expected {expected_access_token!r}, got {actual_access_token!r}"
    )

    log_step_done(description)


def assert_provider_id_is_persistent(
    expected_provider_id: str,
    actual_provider_id: str,
) -> None:
    """Assert that a provider ID persisted across a restart."""
    description = "Asserting provider ID persisted"
    log_step_start(description)

    assert actual_provider_id == expected_provider_id, (
        f"Expected provider ID {expected_provider_id!r} after restart, "
        f"got {actual_provider_id!r}"
    )

    log_step_done(description)


def assert_space_support_is_persistent(
    provider_container: str,
    space_id: str,
    access_token: str,
) -> None:
    """Assert that provider space support persisted across a restart."""
    description = f"Asserting space support persisted through {provider_container}"
    log_step_start(description)

    supported_space_ids = get_provider_supported_space_ids(
        provider_container,
        access_token,
    )
    assert (
        space_id in supported_space_ids
    ), f"Space {space_id} is no longer supported by {provider_container} after restart"

    log_step_done(description)
