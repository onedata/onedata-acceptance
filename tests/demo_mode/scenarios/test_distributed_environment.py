"""Tests for running a distributed demo-mode environment."""

__author__ = "Mateusz Zajac"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import pytest

from tests.demo_mode.meta_steps.environment import start_distributed_environment
from tests.demo_mode.meta_steps.rest import (
    assert_oneproviders_are_distinct,
    assert_onezone_configuration,
    assert_space_support_is_isolated,
    upload_and_verify_rest_file_content,
)
from tests.demo_mode.steps.rest import (
    create_space_for_provider,
    get_demo_access_token,
)


def test_distributed_environment(
    release: str,
    request: pytest.FixtureRequest,
) -> None:
    first_file_name = "first-provider-rest-test.txt"
    first_file_content = b"Data stored through the first Oneprovider\n"
    second_file_name = "second-provider-rest-test.txt"
    second_file_content = b"Data stored through the second Oneprovider\n"

    environment = start_distributed_environment(release, request)
    first_provider, second_provider = environment.oneproviders
    assert_onezone_configuration(release)

    assert_oneproviders_are_distinct(
        first_provider.container,
        second_provider.container,
        release,
    )

    access_token = get_demo_access_token()
    first_space_id = create_space_for_provider(
        first_provider.container,
        "demo-mode-first-provider-space",
        access_token,
    )
    second_space_id = create_space_for_provider(
        second_provider.container,
        "demo-mode-second-provider-space",
        access_token,
    )
    assert_space_support_is_isolated(
        first_provider.container,
        second_provider.container,
        first_space_id,
        second_space_id,
        access_token,
    )

    upload_and_verify_rest_file_content(
        first_space_id,
        first_file_name,
        access_token,
        first_file_content,
        request,
        provider_container=first_provider.container,
    )
    upload_and_verify_rest_file_content(
        second_space_id,
        second_file_name,
        access_token,
        second_file_content,
        request,
        provider_container=second_provider.container,
    )
