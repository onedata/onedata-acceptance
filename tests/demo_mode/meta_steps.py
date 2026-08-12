"""Composite steps used by demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Final

import pytest

from tests.demo_mode.steps import (
    assert_persistent_provider_state,
    assert_rest_file_content,
    create_space_for_provider,
    get_comprehensive_example_file_name,
    get_demo_access_token,
    get_oneprovider_id,
    run_oneprovider,
    run_onezone,
    run_second_oneprovider,
    upload_rest_file,
)

COMPREHENSIVE_DEMO_SPACE_ID: Final = "cb274b2b8bb1750d9be37dd4a3eb7014chb175"
COMPREHENSIVE_FILE_CONTENT: Final = b"hello world\\n"
PERSISTENCE_SPACE_NAME: Final = "demo-mode-persistence-space"


def run_onezone_with_two_oneproviders(
    release: str,
    first_provider_container: str,
    second_provider_container: str,
    request: pytest.FixtureRequest,
) -> None:
    """Start Onezone and two Oneproviders and wait until they are ready."""
    onezone_process = run_onezone(release, request)
    run_oneprovider(
        release,
        onezone_process,
        first_provider_container,
        request,
    )
    run_second_oneprovider(
        release,
        onezone_process,
        second_provider_container,
        request,
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
        PERSISTENCE_SPACE_NAME,
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


def assert_comprehensive_example(
    release: str,
    command_output: str,
    provider_container: str,
) -> None:
    """Assert the file created by the comprehensive example."""
    file_name = get_comprehensive_example_file_name(command_output)
    access_token = get_demo_access_token(release)
    assert_rest_file_content(
        provider_container,
        access_token,
        COMPREHENSIVE_DEMO_SPACE_ID,
        file_name,
        COMPREHENSIVE_FILE_CONTENT,
    )
