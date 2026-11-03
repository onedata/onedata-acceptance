"""Run persistent demo-mode environments and verify retained state."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import subprocess
from dataclasses import dataclass

from environment import docker

from tests.demo_mode.constants import (
    ONEZONE_CONTAINER,
    SERVICE_READY_TIMEOUT,
    SHORT_COMMAND_TIMEOUT,
    oneprovider_container,
)
from tests.demo_mode.data import (
    assert_file_content,
    assert_space_support,
    create_space_for_provider,
    get_oneprovider_id,
    upload_file,
)
from tests.demo_mode.environment import (
    DemoEnvironment,
    DemoService,
    Oneprovider,
    Onezone,
    await_oneprovider,
    await_onezone,
    get_demo_access_token,
)
from tests.demo_mode.utils.commands import (
    RUN_ONEPROVIDER_PERSISTENT,
    RUN_ONEZONE_PERSISTENT,
)
from tests.demo_mode.utils.logging import log_step
from tests.utils.docker_utils import wait_for_running_container


@dataclass(frozen=True)
class PersistentState:
    """Demo-mode state expected to survive an environment restart."""

    access_token: str
    provider_id: str
    space_id: str
    file_name: str
    file_content: bytes


def start_persistent_environment() -> DemoEnvironment:
    """Start both persistent commands before awaiting their services."""
    onezone = _start_persistent_onezone()
    oneprovider = _start_persistent_oneprovider(
        oneprovider_container(1),
        onezone,
    )

    await_onezone(onezone)
    await_oneprovider(oneprovider)

    return DemoEnvironment(
        onezone=onezone,
        oneproviders=(oneprovider,),
    )


def save_persistent_state(
    environment: DemoEnvironment,
    *,
    space_name: str,
    file_name: str,
    file_content: bytes,
) -> PersistentState:
    """Create and return state that must survive a demo-mode restart."""
    onezone = environment.onezone
    (provider,) = environment.oneproviders
    access_token = get_demo_access_token(provider)
    provider_id = get_oneprovider_id(provider)
    space_id = create_space_for_provider(
        onezone,
        provider,
        space_name=space_name,
        access_token=access_token,
    )
    upload_file(
        provider,
        space_id=space_id,
        file_name=file_name,
        content=file_content,
        access_token=access_token,
    )
    return PersistentState(
        access_token=access_token,
        provider_id=provider_id,
        space_id=space_id,
        file_name=file_name,
        file_content=file_content,
    )


def assert_persistent_state(
    environment: DemoEnvironment,
    *,
    state: PersistentState,
) -> None:
    """Assert that demo credentials, configuration, and data survived restart."""
    (provider,) = environment.oneproviders
    restarted_access_token = get_demo_access_token(provider)
    assert restarted_access_token == state.access_token, (
        "Demo access token changed after restart: "
        f"expected {state.access_token!r}, got {restarted_access_token!r}"
    )

    restarted_provider_id = get_oneprovider_id(provider)
    assert restarted_provider_id == state.provider_id, (
        f"Expected provider ID {state.provider_id!r} after restart, got {restarted_provider_id!r}"
    )
    assert_space_support(
        provider,
        space_id=state.space_id,
        access_token=state.access_token,
    )
    assert_file_content(
        provider,
        space_id=state.space_id,
        file_name=state.file_name,
        expected_content=state.file_content,
        access_token=state.access_token,
    )


def stop_persistent_environment(
    environment: DemoEnvironment,
    timeout: float = SHORT_COMMAND_TIMEOUT,
) -> None:
    """Gracefully stop and reap a persistent demo-mode environment."""
    services = (*environment.oneproviders, environment.onezone)
    for service in services:
        _stop_persistent_service(service, timeout)


@log_step("Starting persistent Onezone")
def _start_persistent_onezone() -> Onezone:
    """Start Onezone using the unmodified persistence command."""
    onezone = Onezone(
        container=ONEZONE_CONTAINER,
        process=RUN_ONEZONE_PERSISTENT.start(),
    )
    wait_for_running_container(
        onezone.container,
        onezone.process,
        timeout=SERVICE_READY_TIMEOUT,
    )
    return onezone


@log_step("Starting persistent Oneprovider")
def _start_persistent_oneprovider(
    container: str,
    onezone: Onezone,
) -> Oneprovider:
    """Start Oneprovider using the unmodified persistence command."""
    if onezone.process is None or onezone.process.poll() is not None:
        raise AssertionError("Onezone stopped before Oneprovider could be started")

    return Oneprovider(
        container=container,
        process=RUN_ONEPROVIDER_PERSISTENT.start(container),
    )


@log_step("Stopping persistent demo-mode service")
def _stop_persistent_service(service: DemoService, timeout: float) -> None:
    docker.stop(
        service.container,
        command_timeout=timeout,
    )
    if service.process is None:
        raise AssertionError(f"Persistent service {service.container} has no launcher process")
    try:
        service.process.wait(timeout=timeout)
    except subprocess.TimeoutExpired as error:
        raise AssertionError(
            f"The command running {service.container} did not exit after Docker stop"
        ) from error
