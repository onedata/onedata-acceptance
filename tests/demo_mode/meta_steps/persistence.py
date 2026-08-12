"""Composite steps for persistent demo-mode state."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.steps.persistence import assert_persistent_provider_state
from tests.demo_mode.steps.rest import (
    create_space_for_provider,
    get_demo_access_token,
    get_oneprovider_id,
    upload_rest_file,
)


def create_persistence_state(
    release: str,
    file_content: bytes,
    provider_container: str,
    request: pytest.FixtureRequest,
) -> tuple[str, str, str, str]:
    """Create and return state that must survive a demo-mode restart."""
    access_token = get_demo_access_token(release)
    provider_id = get_oneprovider_id(provider_container, release)
    space_id = create_space_for_provider(
        provider_container,
        "demo-mode-persistence-space",
        access_token,
    )
    file_name = upload_rest_file(
        provider_container,
        space_id,
        access_token,
        file_content,
        request,
    )
    return access_token, provider_id, space_id, file_name


def assert_persistence_state(
    release: str,
    file_content: bytes,
    provider_container: str,
    access_token: str,
    provider_id: str,
    space_id: str,
    file_name: str,
) -> None:
    """Assert that demo credentials, configuration, and data survived restart."""
    restarted_access_token = get_demo_access_token(release)
    assert restarted_access_token == access_token, (
        "Demo access token changed after restart: "
        f"expected {access_token!r}, got {restarted_access_token!r}"
    )
    assert_persistent_provider_state(
        provider_container,
        release,
        provider_id,
        space_id,
        file_name,
        file_content,
        access_token,
    )
