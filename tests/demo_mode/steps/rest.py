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


def assert_onezone_configuration(release: str, expected_name: str) -> None:
    """Assert that Onezone exposes the expected public REST configuration."""
    description = "Asserting Onezone configuration"
    log_step_start(description)

    configuration = get_onezone_configuration()
    onezone_name = configuration.get("name")
    onezone_version = configuration.get("version")
    assert (
        onezone_name == expected_name
    ), f"Expected Onezone name {expected_name!r}, got {onezone_name!r}"
    assert (
        onezone_version == release
    ), f"Expected Onezone version {release!r}, got {onezone_version!r}"

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


def get_oneprovider_id(provider_container: str, release: str) -> str:
    """Return the validated ID exposed by a Oneprovider."""
    configuration = get_oneprovider_configuration(provider_container)
    provider_id = configuration.get("providerId")
    provider_version = configuration.get("version")
    assert isinstance(provider_id, str) and provider_id, (
        f"Expected {provider_container} to expose a non-empty provider ID, "
        f"got {provider_id!r}"
    )
    assert (
        provider_version == release
    ), f"Expected {provider_container} version {release!r}, got {provider_version!r}"
    return provider_id


def assert_oneproviders_are_distinct(
    first_provider_container: str,
    second_provider_container: str,
    release: str,
) -> None:
    """Assert that two containers expose distinct Oneprovider services."""
    description = "Asserting Oneproviders are distinct"
    log_step_start(description)

    first_provider_id = get_oneprovider_id(first_provider_container, release)
    second_provider_id = get_oneprovider_id(second_provider_container, release)
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


def assert_space_support_is_isolated(
    first_provider_container: str,
    first_space_id: str,
    second_provider_container: str,
    second_space_id: str,
    access_token: str,
) -> None:
    """Assert that neither provider supports the other provider's space."""
    description = "Asserting provider space support is isolated"
    log_step_start(description)

    first_provider_spaces = get_provider_supported_space_ids(
        first_provider_container,
        access_token,
    )
    second_provider_spaces = get_provider_supported_space_ids(
        second_provider_container,
        access_token,
    )
    assert (
        first_space_id not in second_provider_spaces
    ), "Second Oneprovider unexpectedly supports the first provider's test space"
    assert (
        second_space_id not in first_provider_spaces
    ), "First Oneprovider unexpectedly supports the second provider's test space"
    log_step_done(description)
