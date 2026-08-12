"""Composite steps used by demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Final

import pytest

from tests.demo_mode.steps import (
    assert_file_contents_are_distinct,
    assert_oneproviders_are_distinct,
    assert_persistent_provider_state,
    assert_provider_rest_file_roundtrip,
    assert_rest_file_content,
    assert_space_support_is_isolated,
    create_space_for_provider,
    get_comprehensive_example_file_name,
    get_demo_access_token,
    get_oneprovider_id,
    upload_rest_file,
)

FIRST_DISTRIBUTED_SPACE_NAME: Final = "demo-mode-first-provider-space"
SECOND_DISTRIBUTED_SPACE_NAME: Final = "demo-mode-second-provider-space"
COMPREHENSIVE_DEMO_SPACE_ID: Final = "cb274b2b8bb1750d9be37dd4a3eb7014chb175"
COMPREHENSIVE_FILE_CONTENT: Final = b"hello world\\n"
PERSISTENCE_SPACE_NAME: Final = "demo-mode-persistence-space"


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


def assert_distributed_rest_file_roundtrips(
    release: str,
    first_file_content: bytes,
    second_file_content: bytes,
    first_provider_container: str,
    second_provider_container: str,
) -> None:
    """Assert isolated file access through two distinct Oneproviders."""
    assert_file_contents_are_distinct(first_file_content, second_file_content)
    assert_oneproviders_are_distinct(
        first_provider_container,
        second_provider_container,
        release,
    )

    access_token = get_demo_access_token(release)
    first_space_id = create_space_for_provider(
        first_provider_container,
        FIRST_DISTRIBUTED_SPACE_NAME,
        access_token,
    )
    second_space_id = create_space_for_provider(
        second_provider_container,
        SECOND_DISTRIBUTED_SPACE_NAME,
        access_token,
    )
    assert_space_support_is_isolated(
        first_provider_container,
        first_space_id,
        second_provider_container,
        second_space_id,
        access_token,
    )
    assert_provider_rest_file_roundtrip(
        first_provider_container,
        access_token,
        first_file_content,
        first_space_id,
    )
    assert_provider_rest_file_roundtrip(
        second_provider_container,
        access_token,
        second_file_content,
        second_space_id,
    )
