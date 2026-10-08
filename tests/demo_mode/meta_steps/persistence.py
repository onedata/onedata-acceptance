"""Composite steps for persistent demo-mode state."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.constants import SHORT_COMMAND_TIMEOUT, oneprovider_container
from tests.demo_mode.steps.environment import (
    await_oneprovider,
    await_onezone,
    get_demo_access_token,
)
from tests.demo_mode.steps.persistence import (
    start_persistent_oneprovider,
    start_persistent_onezone,
    stop_persistent_service,
)
from tests.demo_mode.steps.rest import (
    assert_file_content,
    assert_space_support,
    create_space_for_provider,
    get_oneprovider_id,
    upload_rest_file,
)
from tests.demo_mode.type_definitions import DemoEnvironment, PersistentState
from tests.demo_mode.utils.commands import DemoCommands


def start_persistent_environment(commands: DemoCommands) -> DemoEnvironment:
    """Start both persistent commands before awaiting their services."""
    onezone = start_persistent_onezone(commands)

    oneprovider = start_persistent_oneprovider(
        commands,
        oneprovider_container(1),
        onezone,
    )

    await_onezone(commands, onezone)
    await_oneprovider(commands, oneprovider)

    return DemoEnvironment(
        onezone=onezone,
        oneproviders=(oneprovider,),
    )


def save_persistent_state(
    environment: DemoEnvironment,
    commands: DemoCommands,
    *,
    space_name: str,
    file_name: str,
    file_content: bytes,
    request: pytest.FixtureRequest,
) -> PersistentState:
    """Create and return state that must survive a demo-mode restart."""
    onezone = environment.onezone
    (provider,) = environment.oneproviders
    access_token = get_demo_access_token(provider, commands)
    provider_id = get_oneprovider_id(
        provider,
        access_token=access_token,
    )
    space_id = create_space_for_provider(
        onezone,
        provider,
        space_name=space_name,
        access_token=access_token,
    )
    upload_rest_file(
        provider,
        space_id=space_id,
        file_name=file_name,
        content=file_content,
        access_token=access_token,
        request=request,
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
    commands: DemoCommands,
    *,
    state: PersistentState,
) -> None:
    """Assert that demo credentials, configuration, and data survived restart."""
    (provider,) = environment.oneproviders
    restarted_access_token = get_demo_access_token(provider, commands)
    assert restarted_access_token == state.access_token, (
        "Demo access token changed after restart: "
        f"expected {state.access_token!r}, got {restarted_access_token!r}"
    )

    restarted_provider_id = get_oneprovider_id(
        provider,
        access_token=state.access_token,
    )
    assert restarted_provider_id == state.provider_id, (
        f"Expected provider ID {state.provider_id!r} after restart, got {restarted_provider_id!r}"
    )
    assert_space_support(
        provider,
        space_id=state.space_id,
        expected=True,
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
        stop_persistent_service(service, timeout)
