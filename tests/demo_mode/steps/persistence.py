"""Steps for persistent demo-mode environments."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess
from functools import partial

import pytest

from tests.demo_mode.steps.rest import get_oneprovider_id
from tests.demo_mode.utils.commands import (
    load_command,
    start_command,
    stop_command,
    wait_for_successful_command,
)
from tests.demo_mode.utils.logging import log_step_done, log_step_start
from tests.demo_mode.utils.rest import download_file, get_provider_supported_space_ids


def _run_persistent_service(
    description: str,
    command_path: str,
    await_command_path: str,
    release: str,
    request: pytest.FixtureRequest,
) -> subprocess.Popen[str]:
    log_step_start(description)

    command = load_command(command_path, release)
    process = start_command(command)
    request.addfinalizer(partial(stop_command, process))
    wait_for_successful_command(load_command(await_command_path, release))

    log_step_done(description)
    return process


def run_persistent_onezone(
    release: str,
    request: pytest.FixtureRequest,
) -> subprocess.Popen[str]:
    """Start Onezone using the unmodified persistence command."""
    return _run_persistent_service(
        "Running persistent Onezone",
        "persistency/run_onezone.sh",
        "run_in_background/await_onezone.sh",
        release,
        request,
    )


def run_persistent_oneprovider(
    release: str,
    onezone_process: subprocess.Popen[str],
    request: pytest.FixtureRequest,
) -> subprocess.Popen[str]:
    """Start Oneprovider using the unmodified persistence command."""
    if onezone_process.poll() is not None:
        raise AssertionError("Onezone stopped before Oneprovider could be started")

    return _run_persistent_service(
        "Running persistent Oneprovider",
        "persistency/run_oneprovider.sh",
        "run_in_background/await_oneprovider.sh",
        release,
        request,
    )


def stop_persistent_environment(
    oneprovider_process: subprocess.Popen[str],
    onezone_process: subprocess.Popen[str],
    oneprovider_container: str,
    onezone_container: str,
    timeout: float = 60,
) -> None:
    """Gracefully stop and reap a persistent demo-mode environment."""
    description = "Stopping persistent demo-mode environment"
    log_step_start(description)

    for container_name, process in (
        (oneprovider_container, oneprovider_process),
        (onezone_container, onezone_process),
    ):
        result = subprocess.run(
            ["docker", "stop", container_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
            check=False,
        )
        if result.returncode != 0:
            raise AssertionError(
                f"Failed to stop {container_name} with exit code "
                f"{result.returncode}:\n{result.stdout}"
            )
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired as error:
            stop_command(process)
            raise AssertionError(
                f"The command running {container_name} did not exit after Docker stop"
            ) from error

    log_step_done(description)


def assert_persistent_provider_state(
    provider_container: str,
    release: str,
    expected_provider_id: str,
    space_id: str,
    file_name: str,
    expected_content: bytes,
    access_token: str,
) -> None:
    """Assert provider configuration, support, and file data after a restart."""
    description = f"Asserting persistent state through {provider_container}"
    log_step_start(description)

    provider_id = get_oneprovider_id(provider_container, release)
    assert provider_id == expected_provider_id, (
        f"Expected provider ID {expected_provider_id!r} after restart, "
        f"got {provider_id!r}"
    )
    supported_space_ids = get_provider_supported_space_ids(
        provider_container,
        access_token,
    )
    assert (
        space_id in supported_space_ids
    ), f"Space {space_id} is no longer supported by {provider_container} after restart"
    content = download_file(provider_container, space_id, file_name, access_token)
    assert content == expected_content, (
        f"{provider_container} returned {content!r} after restart, "
        f"expected {expected_content!r}"
    )

    log_step_done(description)
