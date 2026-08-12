"""Steps for demo-mode REST operations and assertions."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from functools import partial

import pytest

from tests.demo_mode.utils.commands import get_access_token
from tests.demo_mode.utils.logging import log_step_done, log_step_start
from tests.demo_mode.utils.rest import (
    create_and_support_space,
    download_file,
    get_oneprovider_configuration,
    get_onezone_configuration,
    get_provider_supported_space_ids,
    get_space_id,
    remove_file,
    upload_file,
)
from tests.type_definitions import JsonObject


def get_onezone_rest_configuration() -> JsonObject:
    """Get Onezone's public REST configuration."""
    return get_onezone_configuration()


def assert_onezone_name(actual_name: object, expected_name: str) -> None:
    """Assert that Onezone exposes the expected name."""
    description = "Asserting Onezone name"
    log_step_start(description)

    assert (
        actual_name == expected_name
    ), f"Expected Onezone name {expected_name!r}, got {actual_name!r}"

    log_step_done(description)


def assert_onezone_version(actual_version: object, expected_version: str) -> None:
    """Assert that Onezone exposes the expected version."""
    description = "Asserting Onezone version"
    log_step_start(description)

    assert (
        actual_version == expected_version
    ), f"Expected Onezone version {expected_version!r}, got {actual_version!r}"

    log_step_done(description)


def get_demo_access_token(release: str) -> str:
    """Get the access token exposed by the demo environment."""
    description = "Getting demo access token"
    log_step_start(description)

    access_token = get_access_token(release)
    log_step_done(description)
    return access_token


def assert_rest_file_content(
    provider_container: str,
    access_token: str,
    space_id: str,
    file_name: str,
    expected_content: bytes,
) -> None:
    """Download and verify an existing file through REST."""
    description = f"Checking {file_name} through {provider_container}"
    log_step_start(description)

    downloaded_content = download_file(
        provider_container,
        space_id,
        file_name,
        access_token,
    )
    assert downloaded_content == expected_content, (
        f"{provider_container} returned {downloaded_content!r}, "
        f"expected {expected_content!r}"
    )

    log_step_done(description)


def get_oneprovider_rest_configuration(provider_container: str) -> JsonObject:
    """Get a Oneprovider's public REST configuration."""
    return get_oneprovider_configuration(provider_container)


def assert_oneprovider_id(provider_container: str, provider_id: object) -> None:
    """Assert that a Oneprovider exposes a valid ID."""
    description = f"Asserting {provider_container} ID"
    log_step_start(description)

    assert isinstance(provider_id, str) and provider_id, (
        f"Expected {provider_container} to expose a non-empty provider ID, "
        f"got {provider_id!r}"
    )

    log_step_done(description)


def assert_oneprovider_version(
    provider_container: str,
    actual_version: object,
    expected_version: str,
) -> None:
    """Assert that a Oneprovider exposes the expected version."""
    description = f"Asserting {provider_container} version"
    log_step_start(description)

    assert actual_version == expected_version, (
        f"Expected {provider_container} version {expected_version!r}, got"
        f" {actual_version!r}"
    )

    log_step_done(description)


def assert_oneprovider_ids_are_distinct(
    first_provider_id: str,
    second_provider_id: str,
) -> None:
    """Assert that two Oneprovider IDs are distinct."""
    description = "Asserting Oneproviders are distinct"
    log_step_start(description)

    assert (
        first_provider_id != second_provider_id
    ), f"Distributed Oneproviders expose the same ID: {first_provider_id}"
    log_step_done(description)


def create_space_for_provider(
    provider_container: str,
    space_name: str,
    access_token: str,
) -> str:
    """Create a space supported by the selected Oneprovider."""
    description = f"Creating space for {provider_container}"
    log_step_start(description)

    space_id = create_and_support_space(provider_container, space_name, access_token)
    log_step_done(description)
    return space_id


def get_rest_space_id(
    provider_container: str,
    space_name: str,
    access_token: str,
) -> str:
    """Get the ID of an existing space accessible through REST."""
    description = f"Getting {space_name} ID through {provider_container}"
    log_step_start(description)

    space_id = get_space_id(provider_container, space_name, access_token)
    log_step_done(description)
    return space_id


def upload_rest_file(
    provider_container: str,
    space_id: str,
    file_name: str,
    access_token: str,
    content: bytes,
    request: pytest.FixtureRequest,
) -> None:
    """Upload a REST file and schedule its removal after the test."""
    description = f"Uploading file through {provider_container}"
    log_step_start(description)

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

    log_step_done(description)


def assert_provider_does_not_support_space(
    provider_container: str,
    space_id: str,
    access_token: str,
) -> None:
    """Assert that a provider does not support a specific space."""
    description = f"Asserting {provider_container} does not support {space_id}"
    log_step_start(description)

    supported_space_ids = get_provider_supported_space_ids(
        provider_container,
        access_token,
    )
    assert (
        space_id not in supported_space_ids
    ), f"{provider_container} unexpectedly supports space {space_id}"
    log_step_done(description)
