"""Composite REST checks for demo-mode environments."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.constants import ONEZONE_NAME
from tests.demo_mode.steps.rest import download_rest_file, upload_rest_file
from tests.demo_mode.utils.rest import OneproviderRestClient, OnezoneRestClient


def assert_onezone_configuration(
    onezone: OnezoneRestClient,
    *,
    release: str,
) -> None:
    """Assert that Onezone exposes the expected public configuration."""
    configuration = onezone.configuration()
    assert configuration.get("name") == ONEZONE_NAME, (
        f"Expected Onezone name {ONEZONE_NAME!r}, got {configuration.get('name')!r}"
    )
    assert configuration.get("version") == release, (
        f"Expected Onezone version {release!r}, got {configuration.get('version')!r}"
    )


def get_oneprovider_id(
    provider: OneproviderRestClient,
    *,
    release: str,
) -> str:
    """Return the validated ID exposed by a Oneprovider."""
    configuration = provider.configuration()
    provider_id = configuration.get("providerId")
    assert isinstance(provider_id, str), (
        f"Expected {provider.container} to expose a string provider ID, got {provider_id!r}"
    )
    assert provider_id, f"Expected {provider.container} to expose a non-empty provider ID"
    assert configuration.get("version") == release, (
        f"Expected {provider.container} version {release!r}, got {configuration.get('version')!r}"
    )
    return provider_id


def assert_oneproviders_are_distinct(
    first_provider: OneproviderRestClient,
    second_provider: OneproviderRestClient,
    *,
    release: str,
) -> None:
    """Assert that two containers expose distinct Oneprovider services."""
    first_provider_id = get_oneprovider_id(first_provider, release=release)
    second_provider_id = get_oneprovider_id(second_provider, release=release)
    assert first_provider_id != second_provider_id, (
        f"Distributed Oneproviders expose the same ID: {first_provider_id}"
    )


def assert_space_support_is_isolated(
    first_provider: OneproviderRestClient,
    second_provider: OneproviderRestClient,
    *,
    first_space_id: str,
    second_space_id: str,
) -> None:
    """Assert that neither provider supports the other provider's space."""
    assert first_space_id not in second_provider.supported_space_ids(), (
        f"{second_provider.container} unexpectedly supports space {first_space_id}"
    )
    assert second_space_id not in first_provider.supported_space_ids(), (
        f"{first_provider.container} unexpectedly supports space {second_space_id}"
    )


def upload_and_verify_rest_file_content(
    provider: OneproviderRestClient,
    *,
    space_id: str,
    file_name: str,
    content: bytes,
    request: pytest.FixtureRequest,
) -> None:
    """Upload a REST file and verify that its content is unchanged."""
    upload_rest_file(
        provider,
        space_id=space_id,
        file_name=file_name,
        content=content,
        request=request,
    )
    downloaded_content = download_rest_file(
        provider,
        space_id=space_id,
        file_name=file_name,
    )
    assert downloaded_content == content, (
        f"{provider.container} returned {downloaded_content!r}, expected {content!r}"
    )
