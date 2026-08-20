"""Composite steps for persistent demo-mode state."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.meta_steps.rest import get_oneprovider_id
from tests.demo_mode.steps.environment import await_running_container
from tests.demo_mode.steps.persistence import (
    assert_access_token_is_persistent,
    assert_provider_id_is_persistent,
    assert_space_support_is_persistent,
    start_persistent_oneprovider,
    start_persistent_onezone,
)
from tests.demo_mode.steps.rest import (
    assert_file_content,
    create_space_for_provider,
    download_rest_file,
    get_demo_access_token,
    upload_rest_file,
)
from tests.demo_mode.type_definitions import PersistentService, PersistentState


def start_persistent_environment(
    release: str,
    onezone_container: str,
    first_oneprovider_container: str,
    request: pytest.FixtureRequest,
) -> tuple[PersistentService, PersistentService]:
    """Start both persistent commands before awaiting their services."""
    onezone = start_persistent_onezone(release, onezone_container, request)
    oneprovider = start_persistent_oneprovider(
        release,
        onezone,
        first_oneprovider_container,
        request,
    )

    await_running_container(
        release,
        onezone.container_name,
        "run_in_background/await_onezone.sh",
        onezone.process,
    )
    await_running_container(
        release,
        oneprovider.container_name,
        "run_in_background/await_oneprovider.sh",
        oneprovider.process,
    )
    return onezone, oneprovider


def save_persistent_state(
    release: str,
    file_content: bytes,
    provider_container: str,
    request: pytest.FixtureRequest,
) -> PersistentState:
    """Create and return state that must survive a demo-mode restart."""
    file_name = "persistence-rest-test.txt"
    access_token = get_demo_access_token(release)
    provider_id = get_oneprovider_id(provider_container, release)
    space_id = create_space_for_provider(
        provider_container,
        "demo-mode-persistence-space",
        access_token,
    )
    upload_rest_file(
        provider_container,
        space_id,
        file_name,
        access_token,
        file_content,
        request,
    )
    return PersistentState(
        access_token=access_token,
        provider_id=provider_id,
        space_id=space_id,
        file_name=file_name,
    )


def assert_persistence_state(
    release: str,
    file_content: bytes,
    provider_container: str,
    state: PersistentState,
) -> None:
    """Assert that demo credentials, configuration, and data survived restart."""
    restarted_access_token = get_demo_access_token(release)
    assert_access_token_is_persistent(state.access_token, restarted_access_token)

    restarted_provider_id = get_oneprovider_id(provider_container, release)
    assert_provider_id_is_persistent(state.provider_id, restarted_provider_id)
    assert_space_support_is_persistent(
        provider_container,
        state.space_id,
        state.access_token,
    )
    downloaded_content = download_rest_file(
        provider_container,
        state.access_token,
        state.space_id,
        state.file_name,
    )
    assert_file_content(provider_container, downloaded_content, file_content)
