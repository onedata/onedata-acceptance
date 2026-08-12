"""Composite steps for demo-mode REST assertions."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import cast

from tests.demo_mode.steps.rest import (
    assert_oneprovider_id,
    assert_oneprovider_ids_are_distinct,
    assert_oneprovider_version,
    assert_onezone_name,
    assert_onezone_version,
    assert_provider_does_not_support_space,
    get_oneprovider_rest_configuration,
    get_onezone_rest_configuration,
)


def assert_onezone_configuration(release: str, expected_name: str) -> None:
    """Assert that Onezone exposes the expected public REST configuration."""
    configuration = get_onezone_rest_configuration()
    assert_onezone_name(configuration.get("name"), expected_name)
    assert_onezone_version(configuration.get("version"), release)


def get_oneprovider_id(provider_container: str, release: str) -> str:
    """Return the validated ID exposed by a Oneprovider."""
    configuration = get_oneprovider_rest_configuration(provider_container)
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
    first_space_id: str,
    second_provider_container: str,
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
