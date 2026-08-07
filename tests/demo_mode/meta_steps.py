"""Composite steps used by demo-mode tests."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Final

from tests.demo_mode.steps import (
    assert_file_contents_are_distinct,
    assert_oneproviders_are_distinct,
    assert_provider_rest_file_roundtrip,
    assert_space_support_is_isolated,
    create_space_for_provider,
    get_demo_access_token,
)
from tests.demo_mode.utils.common import (
    FIRST_ONEPROVIDER_CONTAINER_NAME,
    SECOND_ONEPROVIDER_CONTAINER_NAME,
)

FIRST_DISTRIBUTED_SPACE_NAME: Final = "demo-mode-first-provider-space"
SECOND_DISTRIBUTED_SPACE_NAME: Final = "demo-mode-second-provider-space"


def assert_rest_file_roundtrip(release: str, file_content: bytes) -> None:
    """Assert a file upload and download through the default Oneprovider."""
    access_token = get_demo_access_token(release)
    assert_provider_rest_file_roundtrip(
        FIRST_ONEPROVIDER_CONTAINER_NAME,
        access_token,
        file_content,
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
