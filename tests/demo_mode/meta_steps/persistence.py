"""Composite steps for persistent demo-mode state."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.meta_steps.rest import get_oneprovider_id
from tests.demo_mode.steps.environment import await_oneprovider, await_onezone
from tests.demo_mode.steps.persistence import (
    start_persistent_oneprovider,
    start_persistent_onezone,
)
from tests.demo_mode.steps.rest import (
    create_space_for_provider,
    download_rest_file,
    get_demo_access_token,
    upload_rest_file,
)
from tests.demo_mode.type_definitions import DemoEnvironment, PersistentState
from tests.demo_mode.utils.commands import DemoCommands
from tests.demo_mode.utils.rest import OneproviderRestClient, OnezoneRestClient


def start_persistent_environment(
    commands: DemoCommands,
    request: pytest.FixtureRequest,
) -> DemoEnvironment:
    """Start both persistent commands before awaiting their services."""
    onezone = start_persistent_onezone(commands, request)
    oneprovider = start_persistent_oneprovider(
        commands,
        onezone,
        request,
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
    release: str,
    file_content: bytes,
    request: pytest.FixtureRequest,
) -> PersistentState:
    """Create and return state that must survive a demo-mode restart."""
    file_name = "persistence-rest-test.txt"
    access_token = get_demo_access_token(commands)
    onezone = OnezoneRestClient(commands, access_token)
    provider = OneproviderRestClient(environment.oneproviders[0], access_token)
    provider_id = get_oneprovider_id(provider, release=release)
    space_id = create_space_for_provider(
        onezone,
        provider,
        space_name="demo-mode-persistence-space",
    )
    upload_rest_file(
        provider,
        space_id=space_id,
        file_name=file_name,
        content=file_content,
        request=request,
    )
    return PersistentState(
        access_token=access_token,
        provider_id=provider_id,
        space_id=space_id,
        file_name=file_name,
    )


def assert_persistence_state(
    environment: DemoEnvironment,
    commands: DemoCommands,
    *,
    release: str,
    file_content: bytes,
    state: PersistentState,
) -> None:
    """Assert that demo credentials, configuration, and data survived restart."""
    restarted_access_token = get_demo_access_token(commands)
    assert restarted_access_token == state.access_token, (
        "Demo access token changed after restart: "
        f"expected {state.access_token!r}, got {restarted_access_token!r}"
    )

    provider = OneproviderRestClient(environment.oneproviders[0], state.access_token)
    restarted_provider_id = get_oneprovider_id(provider, release=release)
    assert restarted_provider_id == state.provider_id, (
        f"Expected provider ID {state.provider_id!r} after restart, got {restarted_provider_id!r}"
    )
    assert state.space_id in provider.supported_space_ids(), (
        f"Space {state.space_id} is no longer supported by {provider.container} after restart"
    )
    downloaded_content = download_rest_file(
        provider,
        space_id=state.space_id,
        file_name=state.file_name,
    )
    assert downloaded_content == file_content, (
        f"{provider.container} returned {downloaded_content!r}, expected {file_content!r}"
    )
