"""Composite steps for demo-mode REST assertions."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import cast

import pytest

from tests.demo_mode.constants import ONEZONE_NAME
from tests.demo_mode.steps.rest import (
    assert_file_content,
    assert_oneprovider_id,
    assert_oneprovider_ids_are_distinct,
    assert_oneprovider_version,
    assert_onezone_name,
    assert_onezone_version,
    assert_provider_does_not_support_space,
    download_rest_file,
    upload_rest_file,
)
from tests.demo_mode.utils.rest import (
    get_oneprovider_configuration,
    get_onezone_configuration,
)


def assert_onezone_configuration(release: str) -> None:
    """Assert that Onezone exposes the expected public REST configuration."""
    configuration = get_onezone_configuration()
    assert_onezone_name(configuration.get("name"), ONEZONE_NAME)
    assert_onezone_version(configuration.get("version"), release)


def get_oneprovider_id(provider_container: str, release: str) -> str:
    """Return the validated ID exposed by a Oneprovider."""
    configuration = get_oneprovider_configuration(provider_container)
    provider_id = configuration.get("providerId")
    assert_oneprovider_id(provider_container, provider_id)
    assert_oneprovider_version(
        provider_container,
        configuration.get("version"),
        release,
    )
    return cast(str, provider_id)


def assert_oneproviders_are_distinct(
    first_provider_container: str,
    second_provider_container: str,
    release: str,
) -> None:
    """Assert that two containers expose distinct Oneprovider services."""
    first_provider_id = get_oneprovider_id(first_provider_container, release)
    second_provider_id = get_oneprovider_id(second_provider_container, release)
    assert_oneprovider_ids_are_distinct(first_provider_id, second_provider_id)


def assert_space_support_is_isolated(
    first_provider_container: str,
    second_provider_container: str,
    first_space_id: str,
    second_space_id: str,
    access_token: str,
) -> None:
    """Assert that neither provider supports the other provider's space."""
    assert_provider_does_not_support_space(
        second_provider_container,
        first_space_id,
        access_token,
    )
    assert_provider_does_not_support_space(
        first_provider_container,
        second_space_id,
        access_token,
    )


def upload_and_verify_rest_file_content(
    space_id: str,
    file_name: str,
    access_token: str,
    content: bytes,
    request: pytest.FixtureRequest,
    provider_container: str,
) -> None:
    """Upload a REST file, download it, and assert that its content is unchanged."""
    upload_rest_file(
        provider_container,
        space_id,
        file_name,
        access_token,
        content,
        request,
    )
    downloaded_content = download_rest_file(
        provider_container,
        access_token,
        space_id,
        file_name,
    )
    assert_file_content(provider_container, downloaded_content, content)
