"""Steps for demo-mode REST operations and assertions."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from functools import partial

import pytest

from tests.demo_mode.utils.commands import get_access_token
from tests.demo_mode.utils.logging import log_step
from tests.demo_mode.utils.rest import (
    create_and_support_space,
    download_file,
    get_provider_supported_space_ids,
    get_space_id,
    remove_file,
    upload_file,
)


@log_step("Asserting Onezone name")
def assert_onezone_name(actual_name: object, expected_name: str) -> None:
    """Assert that Onezone exposes the expected name."""
    assert (
        actual_name == expected_name
    ), f"Expected Onezone name {expected_name!r}, got {actual_name!r}"


@log_step("Asserting Onezone version")
def assert_onezone_version(actual_version: object, expected_version: str) -> None:
    """Assert that Onezone exposes the expected version."""
    assert (
        actual_version == expected_version
    ), f"Expected Onezone version {expected_version!r}, got {actual_version!r}"


@log_step("Getting demo access token")
def get_demo_access_token(release: str) -> str:
    """Get the access token exposed by the demo environment."""
    return get_access_token(release)


@log_step("Downloading REST file")
def download_rest_file(
    provider_container: str,
    access_token: str,
    space_id: str,
    file_name: str,
) -> bytes:
    """Download an existing file through REST."""
    return download_file(
        provider_container,
        space_id,
        file_name,
        access_token,
    )


@log_step("Asserting file content")
def assert_file_content(
    provider_container: str,
    actual_content: bytes,
    expected_content: bytes,
) -> None:
    """Assert that a downloaded file has the expected content."""
    assert actual_content == expected_content, (
        f"{provider_container} returned {actual_content!r}, "
        f"expected {expected_content!r}"
    )


@log_step("Asserting Oneprovider ID")
def assert_oneprovider_id(provider_container: str, provider_id: object) -> None:
    """Assert that a Oneprovider exposes a valid ID."""
    assert isinstance(provider_id, str) and provider_id, (
        f"Expected {provider_container} to expose a non-empty provider ID, "
        f"got {provider_id!r}"
    )


@log_step("Asserting Oneprovider version")
def assert_oneprovider_version(
    provider_container: str,
    actual_version: object,
    expected_version: str,
) -> None:
    """Assert that a Oneprovider exposes the expected version."""
    assert actual_version == expected_version, (
        f"Expected {provider_container} version {expected_version!r}, got"
        f" {actual_version!r}"
    )


@log_step("Asserting Oneproviders are distinct")
def assert_oneprovider_ids_are_distinct(
    first_provider_id: str,
    second_provider_id: str,
) -> None:
    """Assert that two Oneprovider IDs are distinct."""
    assert (
        first_provider_id != second_provider_id
    ), f"Distributed Oneproviders expose the same ID: {first_provider_id}"


@log_step("Creating provider space")
def create_space_for_provider(
    provider_container: str,
    space_name: str,
    access_token: str,
) -> str:
    """Create a space supported by the selected Oneprovider."""
    return create_and_support_space(provider_container, space_name, access_token)


@log_step("Getting REST space ID")
def get_rest_space_id(
    provider_container: str,
    space_name: str,
    access_token: str,
) -> str:
    """Get the ID of an existing space accessible through REST."""
    return get_space_id(provider_container, space_name, access_token)


@log_step("Uploading REST file")
def upload_rest_file(
    provider_container: str,
    space_id: str,
    file_name: str,
    access_token: str,
    content: bytes,
    request: pytest.FixtureRequest,
) -> None:
    """Upload a REST file and schedule its removal after the test."""
    upload_file(provider_container, space_id, file_name, access_token, content)
    request.addfinalizer(
        partial(
            remove_file,
            provider_container,
            space_id,
            file_name,
            access_token,
        )
    )


@log_step("Asserting provider does not support space")
def assert_provider_does_not_support_space(
    provider_container: str,
    space_id: str,
    access_token: str,
) -> None:
    """Assert that a provider does not support a specific space."""
    supported_space_ids = get_provider_supported_space_ids(
        provider_container,
        access_token,
    )
    assert (
        space_id not in supported_space_ids
    ), f"{provider_container} unexpectedly supports space {space_id}"
