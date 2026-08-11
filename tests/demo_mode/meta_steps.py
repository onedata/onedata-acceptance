"""Composite steps used by demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Final

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
from tests.demo_mode.utils.common import (
    FIRST_ONEPROVIDER_CONTAINER_NAME,
    SECOND_ONEPROVIDER_CONTAINER_NAME,
)

FIRST_DISTRIBUTED_SPACE_NAME: Final = "demo-mode-first-provider-space"
SECOND_DISTRIBUTED_SPACE_NAME: Final = "demo-mode-second-provider-space"
COMPREHENSIVE_DEMO_SPACE_ID: Final = "cb274b2b8bb1750d9be37dd4a3eb7014chb175"
COMPREHENSIVE_FILE_CONTENT: Final = b"hello world\\n"
PERSISTENCE_SPACE_NAME: Final = "demo-mode-persistence-space"


def create_persistence_state(
    release: str,
    file_content: bytes,
) -> tuple[str, str, str, str]:
    """Create and return state that must survive a demo-mode restart."""
    access_token = get_demo_access_token(release)
    provider_id = get_oneprovider_id(FIRST_ONEPROVIDER_CONTAINER_NAME, release)
    space_id = create_space_for_provider(
        FIRST_ONEPROVIDER_CONTAINER_NAME,
        PERSISTENCE_SPACE_NAME,
        access_token,
    )
    file_name = upload_rest_file(
        FIRST_ONEPROVIDER_CONTAINER_NAME,
        space_id,
        access_token,
        file_content,
    )
    return access_token, provider_id, space_id, file_name


def assert_persistence_state(
    release: str,
    file_content: bytes,
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
        FIRST_ONEPROVIDER_CONTAINER_NAME,
        release,
        provider_id,
        space_id,
        file_name,
        file_content,
        access_token,
    )


def assert_rest_file_roundtrip(release: str, file_content: bytes) -> None:
    """Assert a file upload and download through the default Oneprovider."""
    access_token = get_demo_access_token(release)
    assert_provider_rest_file_roundtrip(
        FIRST_ONEPROVIDER_CONTAINER_NAME,
        access_token,
        file_content,
    )


def assert_comprehensive_example(release: str, command_output: str) -> None:
    """Assert the file created by the comprehensive example."""
    file_name = get_comprehensive_example_file_name(command_output)
    access_token = get_demo_access_token(release)
    assert_rest_file_content(
        FIRST_ONEPROVIDER_CONTAINER_NAME,
        access_token,
        COMPREHENSIVE_DEMO_SPACE_ID,
        file_name,
        COMPREHENSIVE_FILE_CONTENT,
    )


def assert_distributed_rest_file_roundtrips(
    release: str,
    first_file_content: bytes,
    second_file_content: bytes,
) -> None:
    """Assert isolated file access through two distinct Oneproviders."""
    assert_file_contents_are_distinct(first_file_content, second_file_content)
    assert_oneproviders_are_distinct(
        FIRST_ONEPROVIDER_CONTAINER_NAME,
        SECOND_ONEPROVIDER_CONTAINER_NAME,
        release,
    )

    access_token = get_demo_access_token(release)
    first_space_id = create_space_for_provider(
        FIRST_ONEPROVIDER_CONTAINER_NAME,
        FIRST_DISTRIBUTED_SPACE_NAME,
        access_token,
    )
    second_space_id = create_space_for_provider(
        SECOND_ONEPROVIDER_CONTAINER_NAME,
        SECOND_DISTRIBUTED_SPACE_NAME,
        access_token,
    )
    assert_space_support_is_isolated(
        FIRST_ONEPROVIDER_CONTAINER_NAME,
        first_space_id,
        SECOND_ONEPROVIDER_CONTAINER_NAME,
        second_space_id,
        access_token,
    )
    assert_provider_rest_file_roundtrip(
        FIRST_ONEPROVIDER_CONTAINER_NAME,
        access_token,
        first_file_content,
        first_space_id,
    )
    assert_provider_rest_file_roundtrip(
        SECOND_ONEPROVIDER_CONTAINER_NAME,
        access_token,
        second_file_content,
        second_space_id,
    )
